from .updater import FlatpakUpdater

__version__ = "1.5.23"

from .snapper import SnapperManager
from .config import ConfigManager, StateManager
from .logging_utils import JSONFormatter, ANSIFormatter, setup_logging
from .notifiers import (
    NotificationRouter,
    DesktopNotifier,
    MailNotifier,
    WebhookNotifier,
    TemplateRenderer,
)
from .core import AutomationEngine
from .constants import Colors, ICON_PATH

# Aliases for backward compatibility (especially for tests)
load_config = ConfigManager.load
save_state = StateManager.save
load_state = StateManager.load

__all__ = [
    "FlatpakUpdater",
    "SnapperManager",
    "ConfigManager",
    "StateManager",
    "JSONFormatter",
    "ANSIFormatter",
    "setup_logging",
    "NotificationRouter",
    "DesktopNotifier",
    "MailNotifier",
    "WebhookNotifier",
    "TemplateRenderer",
    "AutomationEngine",
    "Colors",
    "ICON_PATH",
    "load_config",
    "save_state",
    "load_state",
]
