#!/usr/bin/env python3
# Version: 1.5.28
import sys
import os

# 1. Local Development Path (relative to script in src/)
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(script_dir, "flatpak_automatic")):
    sys.path.insert(0, script_dir)
# 2. System-wide Installation Path (RPM/DEB)
else:
    sys.path.insert(0, "/usr/share/flatpak-automatic")

from flatpak_automatic import (  # noqa: F401, E402
    AutomationEngine,
    ConfigManager,
    FlatpakUpdater,
    NotificationRouter,
    SnapperManager,
    StateManager,
    load_config,
    load_state,
    save_state,
    WebhookNotifier,
    MailNotifier,
    DesktopNotifier,
    TemplateRenderer,
    JSONFormatter,
    ANSIFormatter,
    setup_logging,
    Colors,
    ICON_PATH,
)
from flatpak_automatic.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
