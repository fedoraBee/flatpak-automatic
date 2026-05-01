#!/usr/bin/env python3
import sys
import re
import os
from datetime import datetime, timezone
import subprocess
import argparse
from typing import Optional, Tuple, List


def get_git_info() -> str:
    """Fetches author info from git, falling back to a default."""
    try:
        name = subprocess.check_output(["git", "config", "user.name"]).decode().strip()
        email = (
            subprocess.check_output(["git", "config", "user.email"]).decode().strip()
        )
        return f"{name} <{email}>"
    except Exception:
        return "fedoraBee <9395414+fedoraBee@users.noreply.github.com>"


def format_date(date_str: str) -> str:
    """Converts YYYY-MM-DD from Markdown to RPM Day Mon DD YYYY."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%a %b %d %Y")


def get_version_from_makefile(makefile: str = "Makefile") -> Optional[str]:
    """Extracts the VERSION variable from a Makefile as a fallback."""
    try:
        with open(makefile, "r") as f:
            for line in f:
                match = re.match(r"^VERSION\s*:=\s*(\d+\.\d+\.\d+)", line)
                if match:
                    return match.group(1)
    except FileNotFoundError:
        pass
    return None


def update_changelog_file(version: str, changelog_file: str) -> None:
    """Runs git-cliff and safely injects the new entries below the static header."""
    print(f"🔄 Running git-cliff to generate changelog for version {version}...")
    try:
        # 1. Capture the new markdown from git-cliff instead of modifying the file directly
        result = subprocess.run(
            ["git-cliff", "--unreleased", "--tag", version],
            check=True,
            capture_output=True,
            text=True,
        )
        new_changelog_block = result.stdout.strip()

        # 2. Strip out the default git-cliff header so we don't duplicate your static text
        new_changelog_block = re.sub(
            r"^# Changelog\n+All notable changes to this project will be documented in this file\.\n+",
            "",
            new_changelog_block,
        )

        # 3. Read your current CHANGELOG.md
        with open(changelog_file, "r") as f:
            content = f.read()

        # 4. Find your static header's end point
        injection_marker = (
            "adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)."
        )

        if injection_marker in content:
            # Split the file exactly at the marker and sandwich the new block in between
            parts = content.split(injection_marker)
            updated_content = (
                parts[0]
                + injection_marker
                + "\n\n"
                + new_changelog_block
                + "\n"
                + parts[1]
            )

            with open(changelog_file, "w") as f:
                f.write(updated_content)
            print("✅ Safely injected new changelog below the static header.")
        else:
            print("⚠️ Warning: Injection marker not found. Appending to top instead.")
            with open(changelog_file, "w") as f:
                f.write(new_changelog_block + "\n\n" + content)

    except FileNotFoundError:
        print("❌ Error: 'git-cliff' is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(
            f"❌ Error: git-cliff failed with exit code {e.returncode}\n{e.stderr}",
            file=sys.stderr,
        )
        sys.exit(1)


def generate_rpm_changelog(
    changelog_in: str, current_epoch: str, current_version: str, current_rel: str
) -> Tuple[str, List[str]]:
    """Parses CHANGELOG.md, formats it for RPM, and extracts the latest entries for Debian."""
    try:
        with open(changelog_in, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(
            f"Warning: Changelog {changelog_in} not found. Skipping changelog generation."
        )
        return "", []

    # Matches headers like: ## [1.1.0] - 2026-04-22 OR ## [v1.1.0] - 2026-04-22
    version_pattern = re.compile(r"## \[v?([\w\.\-]+)\] - (\d{4}-\d{2}-\d{2})")
    author = get_git_info()
    sections = version_pattern.split(content)

    rpm_changelog = []
    latest_entries = []

    for i in range(1, len(sections), 3):
        md_version = sections[i]
        date_str = sections[i + 1]
        text = sections[i + 2].strip()

        rpm_date = format_date(date_str)

        lines = text.split("\n")
        entries = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("###"):
                continue
            if line.startswith("- "):
                entries.append(line)
            elif entries:
                entries[-1] += " " + line

        # Format markdown links and codeblocks to plain text for RPM
        formatted_entries = []
        for entry in entries:
            entry = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", entry)
            entry = entry.replace("`", "")
            formatted_entries.append(entry)

        # Ensure the current build version gets the full Epoch:Version-Release tuple
        if md_version == current_version:
            latest_entries = formatted_entries
            rpm_changelog.append(
                f"* {rpm_date} {author} {current_epoch}:{md_version}-{current_rel}"
            )
        else:
            rpm_changelog.append(f"* {rpm_date} {author} {md_version}")

        for entry in formatted_entries:
            rpm_changelog.append(entry)
        rpm_changelog.append("")

    return "\n".join(rpm_changelog), latest_entries


def build_spec_file(
    spec_in: str,
    spec_out: str,
    epoch: str,
    version: str,
    rel_num: str,
    changelog_content: str,
) -> None:
    """Injects EVR variables into the spec template and appends the changelog."""
    try:
        with open(spec_in, "r") as f:
            spec_text = f.read()
    except FileNotFoundError:
        print(f"Error: Spec template {spec_in} not found.", file=sys.stderr)
        sys.exit(1)

    # Replace the Makefile-injected placeholders
    spec_text = spec_text.replace("@@EPOCH@@", str(epoch))
    spec_text = spec_text.replace("@@VERSION@@", str(version))
    spec_text = spec_text.replace("@@REL_NUM@@", str(rel_num))

    # Append the Changelog section
    if changelog_content:
        spec_text += "\n%changelog\n"
        spec_text += changelog_content

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(spec_out)), exist_ok=True)

    with open(spec_out, "w") as f:
        f.write(spec_text)

    print(f"✅ Successfully generated complete spec at: {spec_out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile package metadata, inject EVR variables, and format changelogs."
    )

    # Define arguments with sensible RPM defaults
    parser.add_argument("--epoch", default="0", help="RPM Epoch (Default: 0)")
    parser.add_argument(
        "--version", help="RPM Version (Fallback: extracted from Makefile)"
    )
    parser.add_argument(
        "--rel-num", default="1", help="RPM Release Number (Default: 1)"
    )
    parser.add_argument(
        "--spec-in",
        default="rpm/flatpak-automatic.spec.in",
        help="Path to template .spec.in file",
    )
    parser.add_argument(
        "--spec-out",
        default=".rpmbuild/SPECS/flatpak-automatic.spec",
        help="Path to save the ready .spec file",
    )
    parser.add_argument(
        "--changelog-in",
        default="CHANGELOG.md",
        help="Path to source markdown changelog",
    )
    parser.add_argument(
        "--makefile",
        default="Makefile",
        help="Path to Makefile for fallback extraction",
    )
    parser.add_argument(
        "--date",
        help="Current build date (used for debian changelog timestamp if provided)",
    )
    parser.add_argument(
        "--generate-changelog",
        action="store_true",
        help="Run git-cliff to auto-generate changelog before parsing",
    )

    args = parser.parse_args()

    # Fallback to Makefile if version is missing
    version = args.version
    if not version:
        version = get_version_from_makefile(args.makefile)
        if not version:
            print(
                "Error: Could not find VERSION in Makefile and --version was not passed.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Standardize RPM version format (RPM doesn't like hyphens in the version string)
    version = version.replace("-", "~")

    # ==========================================
    # MODE 1: Release Prep (Triggered by tbump)
    # ==========================================
    if args.generate_changelog:
        update_changelog_file(version, args.changelog_in)
        # Exit immediately so we don't generate build artifacts during the git commit phase
        sys.exit(0)

    # ==========================================
    # MODE 2: Build Prep (Triggered by Makefile)
    # ==========================================

    # 1. Generate the RPM Changelog string and extract latest entries for Debian
    rpm_changelog_content, latest_entries = generate_rpm_changelog(
        args.changelog_in, args.epoch, version, args.rel_num
    )

    # 2. Compile the final Spec file
    build_spec_file(
        args.spec_in,
        args.spec_out,
        args.epoch,
        version,
        args.rel_num,
        rpm_changelog_content,
    )

    # 3. Generate Debian Changelog
    os.makedirs("debian", exist_ok=True)
    deb_changelog_path = "debian/changelog"

    # Check if a custom date was provided via arguments (useful for reproducible builds in Makefiles)
    if args.date:
        try:
            # Attempt to parse a standard ISO date if passed, otherwise use current time
            dt = datetime.fromisoformat(args.date.replace("Z", "+00:00"))
            date_str = dt.strftime("%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            date_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
    else:
        date_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")

    author = get_git_info()
    existing_deb = ""

    if os.path.exists(deb_changelog_path):
        with open(deb_changelog_path, "r") as f:
            existing_deb = f.read()

    with open(deb_changelog_path, "w") as f:
        f.write(
            f"flatpak-automatic ({version}-{args.rel_num}) unstable; urgency=medium\n\n"
        )

        if latest_entries:
            for entry in latest_entries:
                clean_entry = entry.lstrip("- ")
                f.write(f"  * {clean_entry}\n")
        else:
            f.write(f"  * Sync with CHANGELOG.md release {version}\n")

        f.write(f"\n -- {author}  {date_str}\n\n")
        f.write(existing_deb)

    print(f"✅ Successfully updated Debian changelog at: {deb_changelog_path}")


if __name__ == "__main__":
    main()
