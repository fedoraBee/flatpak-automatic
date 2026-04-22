#!/bin/bash
OUTPUT_FILE="public/index.html"

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
        a { color: #3498db; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; color: #2980b9; }
        .code-block { background: #282c34; color: #abb2bf; padding: 1.2rem; border-radius: 6px; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9em; }
        .card { border: 1px solid #eaeaea; padding: 1.5rem; margin-top: 1.5rem; border-radius: 8px; background: #fafafa; }
        ul { padding-left: 1.5rem; }
        li { margin-bottom: 0.5rem; }
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
EOF

sudo dnf makecache
sudo dnf install flatpak-automatic</div>
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
