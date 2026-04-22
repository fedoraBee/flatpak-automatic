#!/usr/bin/env python3
import sys
import re
import os
from datetime import datetime
import subprocess
import argparse

def get_git_info():
    """Fetches author info from git, falling back to a default."""
    try:
        name = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
        email = subprocess.check_output(['git', 'config', 'user.email']).decode().strip()
        return f"{name} <{email}>"
    except Exception:
        return "fedoraBee <9395414+fedoraBee@users.noreply.github.com>"

def format_date(date_str):
    """Converts YYYY-MM-DD from Markdown to RPM Day Mon DD YYYY."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%a %b %d %Y')

def get_version_from_makefile(makefile='Makefile'):
    """Extracts the VERSION variable from a Makefile as a fallback."""
    try:
        with open(makefile, 'r') as f:
            for line in f:
                match = re.match(r'^VERSION\s*:=\s*(\d+\.\d+\.\d+)', line)
                if match:
                    return match.group(1)
    except FileNotFoundError:
        pass
    return None

def generate_rpm_changelog(changelog_in, current_epoch, current_version, current_rel):
    """Parses CHANGELOG.md and formats it for RPM."""
    try:
        with open(changelog_in, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Warning: Changelog {changelog_in} not found. Skipping changelog generation.")
        return ""

    # Matches headers like: ## [1.1.0] - 2026-04-22
    version_pattern = re.compile(r'## \[([\w\.\-]+)\] - (\d{4}-\d{2}-\d{2})')
    author = get_git_info()
    sections = version_pattern.split(content)
    
    rpm_changelog = []
    
    for i in range(1, len(sections), 3):
        md_version = sections[i]
        date_str = sections[i+1]
        text = sections[i+2].strip()
        
        rpm_date = format_date(date_str)
        
        lines = text.split('\n')
        entries = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('###'):
                continue
            if line.startswith('- '):
                entries.append(line)
            elif entries:
                entries[-1] += ' ' + line

        # Format markdown links and codeblocks to plain text for RPM
        formatted_entries = []
        for entry in entries:
            entry = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', entry)
            entry = entry.replace('`', '')
            formatted_entries.append(entry)

        # Ensure the current build version gets the full Epoch:Version-Release tuple
        if md_version == current_version:
            rpm_changelog.append(f"* {rpm_date} {author} {current_epoch}:{md_version}-{current_rel}")
        else:
            rpm_changelog.append(f"* {rpm_date} {author} {md_version}")
            
        for entry in formatted_entries:
            rpm_changelog.append(entry)
        rpm_changelog.append("")
    
    return '\n'.join(rpm_changelog)

def build_spec_file(spec_in, spec_out, epoch, version, rel_num, changelog_content):
    """Injects EVR variables into the spec template and appends the changelog."""
    try:
        with open(spec_in, 'r') as f:
            spec_text = f.read()
    except FileNotFoundError:
        print(f"Error: Spec template {spec_in} not found.", file=sys.stderr)
        sys.exit(1)

    # Replace the Makefile-injected placeholders
    spec_text = spec_text.replace('@@EPOCH@@', str(epoch))
    spec_text = spec_text.replace('@@VERSION@@', str(version))
    spec_text = spec_text.replace('@@REL_NUM@@', str(rel_num))

    # Append the Changelog section
    if changelog_content:
        spec_text += "\n%changelog\n"
        spec_text += changelog_content

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(spec_out)), exist_ok=True)

    with open(spec_out, 'w') as f:
        f.write(spec_text)
    
    print(f"Successfully generated complete spec at: {spec_out}")

def main():
    parser = argparse.ArgumentParser(description='Compile an RPM .spec file with EVR injection and Markdown changelog parsing.')
    
    # Define arguments with sensible RPM defaults
    parser.add_argument('--epoch', default='0', help='RPM Epoch (Default: 0)')
    parser.add_argument('--version', help='RPM Version (Fallback: extracted from Makefile)')
    parser.add_argument('--rel-num', default='1', help='RPM Release Number (Default: 1)')
    parser.add_argument('--spec-in', default='rpm/flatpak-automatic.spec.in', help='Path to template .spec.in file')
    parser.add_argument('--spec-out', default='.rpmbuild/SPECS/flatpak-automatic.spec', help='Path to save the ready .spec file')
    parser.add_argument('--changelog-in', default='CHANGELOG.md', help='Path to source markdown changelog')
    parser.add_argument('--makefile', default='Makefile', help='Path to Makefile for fallback version extraction')
    parser.add_argument('--date', help='Current build date (used for changelog headers if needed)')

    args = parser.parse_args()

    # Fallback to Makefile if version is missing
    version = args.version
    if not version:
        version = get_version_from_makefile(args.makefile)
        if not version:
            print("Error: Could not find VERSION in Makefile and --version was not passed.", file=sys.stderr)
            sys.exit(1)
            
    # Standardize RPM version format (RPM doesn't like hyphens in the version string)
    version = version.replace("-", "~")

    # 1. Generate the Changelog string
    rpm_changelog_content = generate_rpm_changelog(
        args.changelog_in, 
        args.epoch, 
        version, 
        args.rel_num
    )

    # 2. Compile the final Spec file
    build_spec_file(
        args.spec_in, 
        args.spec_out, 
        args.epoch, 
        version, 
        args.rel_num, 
        rpm_changelog_content
    )

if __name__ == '__main__':
    main()