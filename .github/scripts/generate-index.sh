#!/bin/bash
OUTPUT_FILE="public/index.html"
RPM_DIR="public/rpms"

VERSIONS_HTML=""
if [ -d "$RPM_DIR" ]; then
    # Sort versions descending (-r) so newest is on top
    IS_FIRST_VERSION=true
    for version_path in $(ls -d "$RPM_DIR"/v* 2>/dev/null | sort -rV); do
        version=$(basename "$version_path")
        
        if [ "$IS_FIRST_VERSION" = true ]; then
            VERSIONS_HTML+="<h3>$version <span class=\"badge-latest\">LATEST</span></h3><ul>"
        else
            VERSIONS_HTML+="<h3>$version</h3><ul>"
        fi
        
        for channel_path in $(ls -d "$version_path"/* 2>/dev/null); do
            channel=$(basename "$channel_path")
            VERSIONS_HTML+="<details><summary>Channel: $channel</summary><ul class=\"rpm-list\">"
            
            rpm_files=($(ls "$channel_path"/*.rpm 2>/dev/null | sort -rV))
            if [ ${#rpm_files[@]} -gt 0 ]; then
                IS_FIRST_RPM=true
                for rpm_file in "${rpm_files[@]}"; do
                    rpm_name=$(basename "$rpm_file")
                    if [ "$IS_FIRST_VERSION" = true ] && [ "$IS_FIRST_RPM" = true ]; then
                        VERSIONS_HTML+="<li><a href=\"rpms/$version/$channel/$rpm_name\">$rpm_name</a> <span class=\"badge-latest-sm\">latest patch</span></li>"
                        IS_FIRST_RPM=false
                    else
                        VERSIONS_HTML+="<li><a href=\"rpms/$version/$channel/$rpm_name\">$rpm_name</a></li>"
                    fi
                done
            else
                VERSIONS_HTML+="<li><em>No RPMs available in this channel.</em></li>"
            fi
            VERSIONS_HTML+="</ul></details>"
        done
        VERSIONS_HTML+="</ul>"
        IS_FIRST_VERSION=false
    done
else
    VERSIONS_HTML="<p>No versions found.</p>"
fi

cat <<EOF_HTML > "$OUTPUT_FILE"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flatpak Automatic Repository</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 2rem; background: #f4f6f8; }
        .container { background: white; padding: 2.5rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 0.5rem; margin-top: 0; }
        h2 { color: #34495e; margin-top: 1.5rem; }
        h3 { color: #2980b9; margin-top: 1.0rem; margin-bottom: 0.2rem; }
        a { color: #3498db; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; color: #2980b9; }
        .code-block { background: #282c34; color: #abb2bf; padding: 1.2rem; border-radius: 6px; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9em; }
        .card { border: 1px solid #eaeaea; padding: 1.5rem; margin-top: 1.5rem; border-radius: 8px; background: #fafafa; }
        ul { padding-left: 1.5rem; }
        li { margin-bottom: 0.5rem; }
    
        details { background: #f9f9f9; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 0.5rem; padding: 0.5rem; }
        .rpm-list { max-height: 280px; overflow-y: auto; margin-top: 0.5rem; padding-right: 0.5rem; }
        summary { font-weight: 500; cursor: pointer; color: #2980b9; user-select: none; outline: none; }
        .badge-latest { background: #27ae60; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.6em; vertical-align: middle; margin-left: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
        .badge-latest-sm { background: #3498db; color: white; padding: 1px 5px; border-radius: 3px; font-size: 0.7em; margin-left: 6px; font-weight: bold; text-transform: uppercase; }
        @media (prefers-color-scheme: dark) {
            body { background: #121212; color: #e0e0e0; }
            .container { background: #1e1e1e; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            h1 { color: #ffffff; border-bottom-color: #333; }
            h2 { color: #eeeeee; }
            h3 { color: #64b5f6; }
            a { color: #64b5f6; }
            a:hover { color: #90caf9; }
            .card { background: #252525; border-color: #333; }
            .code-block { background: #111; border: 1px solid #333; }
            details { background: #2a2a2a; border-color: #444; }
            summary { color: #90caf9; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Flatpak Automatic</h1>
        <p>Welcome to the official DNF repository for <strong>Flatpak Automatic</strong>. This project provides a secure, configurable, and systemd-native automation wrapper for Flatpak updates with Snapper snapshot integration.</p>
        
        <div class="card">
            <h2>📦 Installation</h2>
            <p>Run the following commands to add the repository and install the package on Fedora or compatible RPM-based systems:</p>
            <div class="code-block">sudo tee /etc/yum.repos.d/flatpak-automatic.repo &lt;&lt;'EOF'
[flatpak-automatic]
name=Flatpak Automatic - Stable
baseurl=https://fedorabee.github.io/flatpak-automatic/rpms/latest/stable/
enabled=1
gpgcheck=1
gpgkey=https://fedorabee.github.io/flatpak-automatic/rpms/gpg.key

[flatpak-automatic-testing]
name=Flatpak Automatic - Testing
baseurl=https://fedorabee.github.io/flatpak-automatic/rpms/latest/testing/
enabled=0
gpgcheck=1
gpgkey=https://fedorabee.github.io/flatpak-automatic/rpms/gpg.key
EOF

sudo dnf makecache
sudo dnf install flatpak-automatic</div>
        </div>

        <div class="card">
            <h2>🗂️ Available Versions & Channels</h2>
            ${VERSIONS_HTML}
            
        </div>

        <div class="card">
            <h2>🔗 Resources</h2>
            <ul>
                <li><a href="rpms/gpg.key">Download Repository GPG Key</a></li>
                <li><a href="https://github.com/fedoraBee/flatpak-automatic">GitHub Source Code &amp; Documentation</a></li>
                <li><a href="https://github.com/fedoraBee/flatpak-automatic/issues">Report an Issue</a></li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF_HTML

echo "Generated styled index.html at $OUTPUT_FILE"
