#!/usr/bin/env python3
import os
import datetime
import re
from jinja2 import Environment, FileSystemLoader


def get_version_info(filename):
    """Extract full version string from RPM or DEB filename."""
    # RPM: flatpak-automatic-1.4.9-1.noarch.rpm -> 1.4.9
    # DEB: flatpak-automatic_1.4.9_all.deb -> 1.4.9
    m = re.search(r"[-_](\d+\.\d+\.\d+)", filename)
    return m.group(1) if m else None


def main():
    output_file = "public/index.html"
    repo_root = "public"

    # 1. Collect all RPM versions and channels
    rpm_dir = os.path.join(repo_root, "rpms")
    major_minor_versions = []
    if os.path.isdir(rpm_dir):
        major_minor_versions = sorted(
            [d for d in os.listdir(rpm_dir) if d.startswith("v") and d != "latest"],
            reverse=True,
        )

    # 2. Collect all DEB packages from the pool
    pool_dir = os.path.join(repo_root, "debs", "pool", "main", "f", "flatpak-automatic")
    deb_pkgs = []
    if os.path.isdir(pool_dir):
        deb_pkgs = sorted(
            [f for f in os.listdir(pool_dir) if f.endswith(".deb")], reverse=True
        )

    # Map DEBs to MAJOR.MINOR
    deb_by_major_minor = {}
    for pkg in deb_pkgs:
        v = get_version_info(pkg)
        if v:
            mm = "v" + ".".join(v.split(".")[:2])
            if mm not in deb_by_major_minor:
                deb_by_major_minor[mm] = []
            deb_by_major_minor[mm].append(pkg)

    # Unified list of MAJOR.MINOR versions
    all_mm = sorted(
        list(set(major_minor_versions + list(deb_by_major_minor.keys()))), reverse=True
    )

    versions = []
    for mm in all_mm:
        v_data = {"name": mm, "channels": [], "is_first": False}

        # Check channels for this MM version in RPMs
        mm_path = os.path.join(rpm_dir, mm)
        channels_found = []
        if os.path.isdir(mm_path):
            channels_found = sorted(os.listdir(mm_path))  # stable, testing

        # If no channels found in RPMs but we have DEBs, default to stable
        if not channels_found and mm in deb_by_major_minor:
            channels_found = ["stable"]

        for channel in channels_found:
            c_path = os.path.join(mm_path, channel)
            rpms = []
            if os.path.isdir(c_path):
                rpms = sorted(
                    [f for f in os.listdir(c_path) if f.endswith(".rpm")], reverse=True
                )

            # Assign DEBs to this channel
            debs_in_channel = []
            if mm in deb_by_major_minor:
                if len(channels_found) == 1:
                    # If only one channel, all DEBs for this MM go here
                    debs_in_channel = deb_by_major_minor[mm]
                else:
                    # Try to match by full version string found in RPMs
                    rpm_full_versions = set([get_version_info(r) for r in rpms])
                    debs_in_channel = [
                        d
                        for d in deb_by_major_minor[mm]
                        if get_version_info(d) in rpm_full_versions
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

    env = Environment(loader=FileSystemLoader("docs/templates"))
    template = env.get_template("index.html.j2")
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
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"Generated styled index.html at {output_file}")


if __name__ == "__main__":
    main()
