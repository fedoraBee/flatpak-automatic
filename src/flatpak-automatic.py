#!/usr/bin/env python3
import sys
import os

# Ensure the package is in the path when running from the source tree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flatpak_automatic import (  # noqa: F401
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
from flatpak_automatic.__main__ import main

if __name__ == "__main__":
    main()
