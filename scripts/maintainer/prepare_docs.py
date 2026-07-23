#!/usr/bin/env python3
import os
import shutil
import sys
import re


def safe_copy(src: str, dst: str) -> None:
    """Copy file only if source and destination are different."""
    if os.path.exists(dst) and os.path.samefile(src, dst):
        return
    shutil.copy2(src, dst)


def prepare_docs(src_dir: str, docs_dir: str) -> None:
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
            safe_copy(src_path, os.path.join(docs_dir, dest_name))

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
            safe_copy(src_path, os.path.join(about_dir, f_name.lower()))

    # 4. Copy files already in docs/ to root of docs_dir
    src_docs_dir = os.path.join(src_dir, "docs")
    if os.path.isdir(src_docs_dir):
        for item in os.listdir(src_docs_dir):
            if item.endswith((".md", ".css", ".js")):
                safe_copy(
                    os.path.join(src_docs_dir, item), os.path.join(docs_dir, item)
                )

    # 5. Ensure assets are available
    assets_dest = os.path.join(docs_dir, "assets")
    if not os.path.exists(assets_dest):
        os.makedirs(assets_dest)

    src_assets_dir = os.path.join(src_dir, "assets")
    if os.path.isdir(src_assets_dir):
        valid_extensions = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp")
        for item in os.listdir(src_assets_dir):
            if item.lower().endswith(valid_extensions):
                safe_copy(
                    os.path.join(src_assets_dir, item), os.path.join(assets_dest, item)
                )

    # 6. Transform content
    # Fix banner paths and translate internal links
    transform_files(docs_dir)

    print(f"Documentation files prepared in {docs_dir}/")


def transform_files(docs_dir: str) -> None:
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

            # Determine relative asset path prefix based on MkDocs page depth.
            # In MkDocs:
            # - index.md is at site root -> 'assets/'
            # - Root md files (e.g. agents.md) become site/agents/index.html -> '../assets/'
            # - Nested md files (e.g. about/contributing.md) become site/about/contributing/index.html -> '../../assets/'
            if rel_path == "index.md":
                asset_prefix = "assets/"
            else:
                parts = rel_path.split(os.sep)
                depth = len(parts)
                asset_prefix = "../" * depth + "assets/"

            # HTML img tag src attribute replacement for assets/
            content = re.sub(
                r'src="(?:\.\./)*assets/([^"]+)"',
                f'src="{asset_prefix}\\1"',
                content,
            )

            # Markdown image syntax replacement for assets/
            content = re.sub(
                r"!\[([^\]]*)\]\((?:\.\./)*assets/([^)]+)\)",
                f"![\\1]({asset_prefix}\\2)",
                content,
            )

            # Link translations for index.md
            if rel_path == "index.md":
                content = content.replace("(AGENTS.md)", "(agents.md)")
                content = content.replace("(docs/development.md)", "(development.md)")
                content = content.replace("(docs/testing.md)", "(testing.md)")
                content = content.replace(
                    "(.github/CONTRIBUTING.md)", "(about/contributing.md)"
                )
                content = content.replace("(CHANGELOG.md)", "(changelog.md)")
                content = content.replace("(MAINTAINERS.md)", "(maintainers.md)")
                content = content.replace(
                    "(.github/SECURITY.md)", "(about/security.md)"
                )
                content = content.replace(
                    "- 📝 [Project Documentation](https://fedorabee.github.io/flatpak-automatic/)",
                    "- 📝 [GitHub Source Code](https://github.com/fedoraBee/flatpak-automatic/)",
                )
                content = content.replace(
                    "- 🌐 [Repository](https://fedorabee.github.io/flatpak-automatic/repository/)",
                    "- 🌐 [Repository](repository.md)",
                )

            # Link translations for agents.md
            elif rel_path == "agents.md":
                content = content.replace("(README.md)", "(index.md)")
                content = content.replace("(docs/development.md)", "(development.md)")
                content = content.replace("(docs/testing.md)", "(testing.md)")
                content = content.replace(
                    "(.github/CONTRIBUTING.md)", "(about/contributing.md)"
                )
                content = content.replace("(CHANGELOG.md)", "(changelog.md)")
                content = content.replace("(MAINTAINERS.md)", "(maintainers.md)")
                content = content.replace("(LICENSE)", "(license.md)")

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
    dest = "build_docs"
    prepare_docs(src, dest)
