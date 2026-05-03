#!/usr/bin/env python3
import os
import datetime
import re
import shutil
from typing import Optional, List, Dict, Any, Set
from jinja2 import Environment, FileSystemLoader, select_autoescape


def version_sort_key(ver_str: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", str(ver_str))]


def get_version_info(filename: str) -> Optional[str]:
    """Extract full version string from RPM or DEB filename."""
    # RPM: flatpak-automatic-1.4.9-1.noarch.rpm -> 1.4.9
    # DEB: flatpak-automatic_1.4.9_all.deb -> 1.4.9
    # Support pre-release suffixes like ~rc1 or -rc1
    m = re.search(r"[-_](\d+\.\d+\.\d+[^-_]*)", filename)
    if m:
        return m.group(1).replace("~", "-")
    return None


def main() -> None:
    repo_root = os.environ.get("REPO_ROOT", "public")
    output_file = os.environ.get("OUTPUT_FILE", os.path.join(repo_root, "index.html"))
    output_format = os.environ.get("OUTPUT_FORMAT", "html")
    template_dir = os.environ.get("TEMPLATE_DIR", "docs/templates")
    assets_src_dir = os.environ.get("ASSETS_SRC_DIR", "assets")

    if output_format == "markdown":
        template_name = "repository.md.j2"
    else:
        template_name = "index.html.j2"

    print(
        f"DEBUG: Using repo_root={repo_root}, output_file={output_file}, format={output_format}, template={template_name}"
    )
    # 1. Collect all RPM versions and channels
    rpm_dir = os.path.join(repo_root, "rpms")
    major_minor_versions: List[str] = []
    if os.path.isdir(rpm_dir):
        all_dirs = os.listdir(rpm_dir)
        print(f"DEBUG: All entries in {rpm_dir}: {all_dirs}")
        major_minor_versions = sorted(
            [d for d in all_dirs if d.startswith("v") and d != "latest"],
            key=version_sort_key,
            reverse=True,
        )
    else:
        print(f"DEBUG: RPM directory {rpm_dir} NOT FOUND")
    print(f"DEBUG: Found RPM MAJOR.MINOR versions: {major_minor_versions}")

    # 2. Collect all DEB packages from the pool
    pool_dir = os.path.join(repo_root, "debs", "pool", "main", "f", "flatpak-automatic")
    deb_pkgs: List[str] = []
    if os.path.isdir(pool_dir):
        all_files = os.listdir(pool_dir)
        print(f"DEBUG: All files in {pool_dir}: {all_files}")
        deb_pkgs = sorted(
            [f for f in all_files if f.endswith(".deb")],
            key=lambda x: version_sort_key(get_version_info(x) or "0"),
            reverse=True,
        )
    else:
        print(f"DEBUG: DEB pool directory {pool_dir} NOT FOUND")
    print(f"DEBUG: Found {len(deb_pkgs)} DEB packages in pool")

    # Map DEBs to MAJOR.MINOR
    deb_by_major_minor: Dict[str, List[str]] = {}
    for pkg in deb_pkgs:
        v = get_version_info(pkg)
        if v:
            mm = "v" + ".".join(v.split(".")[:2])
            if mm not in deb_by_major_minor:
                deb_by_major_minor[mm] = []
            deb_by_major_minor[mm].append(pkg)

    # Unified list of MAJOR.MINOR versions
    all_mm = sorted(
        list(set(major_minor_versions + list(deb_by_major_minor.keys()))),
        key=version_sort_key,
        reverse=True,
    )

    versions: List[Dict[str, Any]] = []
    for mm in all_mm:
        v_data: Dict[str, Any] = {"name": mm, "channels": [], "is_first": False}

        # Check channels for this MM version
        channels_set: Set[str] = set()

        # 1. From RPM directories
        mm_path = os.path.join(rpm_dir, mm)
        if os.path.isdir(mm_path):
            for d in os.listdir(mm_path):
                if os.path.isdir(os.path.join(mm_path, d)) and d != "repodata":
                    channels_set.add(d)

        # 2. From DEBs (ensure we check stable/testing if we have DEBs for this version)
        if mm in deb_by_major_minor:
            channels_set.add("stable")
            # Check if any DEB looks like a testing version
            has_testing_debs = any(
                any(pre in d.lower() for pre in ["rc", "beta", "alpha", "test"])
                for d in deb_by_major_minor[mm]
            )
            if has_testing_debs:
                channels_set.add("testing")

        channels_found = sorted(list(channels_set))
        print(f"DEBUG: Found channels for {mm}: {channels_found}")

        for channel in channels_found:
            c_path = os.path.join(mm_path, channel)
            rpms: List[str] = []
            if os.path.isdir(c_path):
                rpms = sorted(
                    [f for f in os.listdir(c_path) if f.endswith(".rpm")], reverse=True
                )

            # Assign DEBs to this channel
            debs_in_channel: List[str] = []
            if mm in deb_by_major_minor:
                if len(channels_found) == 1:
                    # If only one channel, all DEBs for this MM go here
                    debs_in_channel = deb_by_major_minor[mm]
                else:
                    # Try to match by base version string (ignoring debian release number like -1)
                    rpm_base_versions: Set[str] = set(
                        [
                            (get_version_info(r) or "").rsplit("-", 1)[0]
                            if "-" in (get_version_info(r) or "")
                            else (get_version_info(r) or "")
                            for r in rpms
                        ]
                    )
                    debs_in_channel = [
                        d
                        for d in deb_by_major_minor[mm]
                        if (get_version_info(d) or "").rsplit("-", 1)[0]
                        in rpm_base_versions
                    ]

                    # Fallback for testing/stable distinction if no exact match (e.g. only one format exists)
                    if not debs_in_channel:
                        if channel == "testing":
                            debs_in_channel = [
                                d
                                for d in deb_by_major_minor[mm]
                                if "rc" in d or "beta" in d or "alpha" in d
                            ]
                        elif channel == "stable":
                            debs_in_channel = [
                                d
                                for d in deb_by_major_minor[mm]
                                if not ("rc" in d or "beta" in d or "alpha" in d)
                            ]

            v_data["channels"].append(
                {"name": channel, "rpms": rpms, "debs": debs_in_channel}
            )

        versions.append(v_data)

    if versions:
        versions[0]["is_first"] = True

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "htm", "xml"]),
    )
    template = env.get_template(template_name)
    github_repo = os.environ.get("GITHUB_REPOSITORY", "fedoraBee/flatpak-automatic")
    build_sha = os.environ.get("GITHUB_SHA", "unknown")
    build_run_id = os.environ.get("GITHUB_RUN_ID", "unknown")
    build_date = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    html_out = template.render(
        versions=versions,
        github_repo=github_repo,
        build_sha=build_sha,
        build_run_id=build_run_id,
        build_date=build_date,
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Copy assets
    assets_dest = os.path.join(repo_root, "assets")
    os.makedirs(assets_dest, exist_ok=True)
    for asset in ["banner.svg", "logo.svg"]:
        src = os.path.join(assets_src_dir, asset)
        dst = os.path.join(assets_dest, asset)
        if os.path.exists(src):
            if not os.path.exists(dst) or os.path.abspath(src) != os.path.abspath(dst):
                print(f"DEBUG: Copying {src} to {dst}")
                shutil.copy2(src, dst)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"Generated styled index.html at {output_file}")


if __name__ == "__main__":
    main()
