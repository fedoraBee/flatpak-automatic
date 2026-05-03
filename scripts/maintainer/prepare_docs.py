#!/usr/bin/env python3
import os
import shutil
import sys
import re


def prepare_docs(src_dir: str, docs_dir: str):
    print(f"Preparing documentation in {docs_dir} using sources from {src_dir}...")

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # 1. Map and copy root markdown files
    root_files = {
        "README.md": "index.md",
        "CHANGELOG.md": "changelog.md",
        "MAINTAINERS.md": "maintainers.md",
        "AGENTS.md": "agents.md",
    }

    for src_name, dest_name in root_files.items():
        src_path = os.path.join(src_dir, src_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(docs_dir, dest_name))

    # 2. Handle LICENSE
    license_src = os.path.join(src_dir, "LICENSE")
    if os.path.exists(license_src):
        with open(license_src, "r") as f:
            content = f.read()
        with open(os.path.join(docs_dir, "license.md"), "w") as f:
            f.write("# License\n\n```text\n")
            f.write(content)
            f.write("\n```\n")

    # 3. Handle files from .github/
    about_dir = os.path.join(docs_dir, "about")
    if not os.path.exists(about_dir):
        os.makedirs(about_dir)

    github_files = ["CONTRIBUTING.md", "SECURITY.md"]
    for f_name in github_files:
        src_path = os.path.join(src_dir, ".github", f_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(about_dir, f_name.lower()))

    # 4. Copy files already in docs/ to root of docs_dir
    src_docs_dir = os.path.join(src_dir, "docs")
    if os.path.isdir(src_docs_dir):
        for item in os.listdir(src_docs_dir):
            if item.endswith((".md", ".css", ".js")):
                shutil.copy2(os.path.join(src_docs_dir, item), docs_dir)

    # 5. Ensure assets are available
    assets_dest = os.path.join(docs_dir, "assets")
    if not os.path.exists(assets_dest):
        os.makedirs(assets_dest)

    src_assets_dir = os.path.join(src_dir, "assets")
    if os.path.isdir(src_assets_dir):
        for item in os.listdir(src_assets_dir):
            if item.endswith(".svg"):
                shutil.copy2(os.path.join(src_assets_dir, item), assets_dest)

    # 6. Transform content
    # Fix banner paths and translate internal links
    transform_files(docs_dir)

    print(f"Documentation files prepared in {docs_dir}/")


def transform_files(docs_dir: str):
    # Banner path replacements based on directory depth
    replacements = [
        # (pattern, replacement, file_glob)
        (r'src="assets/banner.svg"', r'src="assets/banner.svg"', r"^index\.md$"),
        (
            r'src="assets/banner.svg"',
            r'src="../assets/banner.svg"',
            r"^(agents|changelog|maintainers|development)\.md$",
        ),
        (
            r'src="\.\./assets/banner.svg"',
            r'src="../../assets/banner.svg"',
            r"^about/.*\.md$",
        ),
    ]

    # Link translations for index.md
    index_path = os.path.join(docs_dir, "index.md")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            content = f.read()

        # Translate internal links
        content = content.replace("(AGENTS.md)", "(agents.md)")
        content = content.replace("(docs/development.md)", "(development.md)")
        content = content.replace(
            "(.github/CONTRIBUTING.md)", "(about/contributing.md)"
        )
        content = content.replace("(CHANGELOG.md)", "(changelog.md)")
        content = content.replace("(MAINTAINERS.md)", "(maintainers.md)")

        # Actually, let's just do what they asked: translate the paths.
        # If they want it simplified, they can ask, but "translate paths" implies keeping them.
        with open(index_path, "w") as f:
            f.write(content)

    # Walk through docs and apply replacements
    for root, _, files in os.walk(docs_dir):
        for f_name in files:
            if not f_name.endswith(".md"):
                continue

            rel_path = os.path.relpath(os.path.join(root, f_name), docs_dir)
            file_path = os.path.join(root, f_name)

            with open(file_path, "r") as f:
                content = f.read()

            orig_content = content
            for pattern, repl, file_re in replacements:
                if re.search(file_re, rel_path):
                    content = re.sub(pattern, repl, content)

            # Specific fixes for about/ files
            if rel_path.startswith("about/"):
                content = content.replace("../LICENSE", "../license.md")
                content = content.replace(
                    "ISSUE_TEMPLATE/",
                    "https://github.com/fedoraBee/flatpak-automatic/tree/main/.github/ISSUE_TEMPLATE/",
                )

            if content != orig_content:
                with open(file_path, "w") as f:
                    f.write(content)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    dest = "docs"
    prepare_docs(src, dest)
