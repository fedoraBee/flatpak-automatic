#!/usr/bin/env python3
import os
import datetime
from jinja2 import Environment, FileSystemLoader


def main():
    output_file = "public/index.html"
    repo_root = "public"

    def get_packages(repo_type, extension):
        repo_dir = os.path.join(repo_root, repo_type)
        versions = []
        if os.path.isdir(repo_dir):
            version_dirs = sorted(
                [d for d in os.listdir(repo_dir) if d.startswith("v")], reverse=True
            )
            for v_dir in version_dirs:
                v_path = os.path.join(repo_dir, v_dir)
                if not os.path.isdir(v_path):
                    continue

                channels = []
                for c_dir in sorted(os.listdir(v_path)):
                    c_path = os.path.join(v_path, c_dir)
                    if not os.path.isdir(c_path):
                        continue

                    packages = sorted(
                        [f for f in os.listdir(c_path) if f.endswith(extension)],
                        reverse=True,
                    )
                    channels.append({"name": c_dir, "packages": packages})

                versions.append({"name": v_dir, "channels": channels})
        return versions

    rpm_versions_raw = get_packages("rpms", ".rpm")
    deb_versions_raw = get_packages("debs", ".deb")

    # Merge versions by name
    all_version_names = sorted(
        list(set([v["name"] for v in rpm_versions_raw + deb_versions_raw])),
        reverse=True,
    )

    versions = []
    is_first_version = True
    for v_name in all_version_names:
        rpm_v = next((v for v in rpm_versions_raw if v["name"] == v_name), None)
        deb_v = next((v for v in deb_versions_raw if v["name"] == v_name), None)

        v_data = {
            "name": v_name,
            "is_first": is_first_version,
            "rpm_channels": rpm_v["channels"] if rpm_v else [],
            "deb_channels": deb_v["channels"] if deb_v else [],
        }
        versions.append(v_data)
        is_first_version = False

    env = Environment(loader=FileSystemLoader(".github/templates"))
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
