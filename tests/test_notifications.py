import sys
import importlib.util
import socket
from unittest.mock import MagicMock, patch
from typing import Any

# Mock dbus before importing fa
mock_dbus = MagicMock()
sys.modules["dbus"] = mock_dbus
sys.modules["dbus.exceptions"] = MagicMock()

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "src/flatpak-automatic.py"
)
assert spec is not None
assert spec.loader is not None
fa: Any = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


class TestNotificationRouter:
    @patch.object(fa, "MailNotifier")
    @patch.object(fa, "WebhookNotifier")
    @patch.object(fa, "TemplateRenderer")
    def test_dispatch_all_legacy_global(
        self, mock_template: Any, mock_webhook: Any, mock_mail: Any
    ) -> None:
        config = {
            "mail": {"enabled": True, "to": "admin@example.com"},
            "webhooks": {"enabled": True, "urls": ["http://webhook.local"]},
        }
        router = fa.NotificationRouter(config)
        router.dispatch_all("Test Title", "Test Body", True)
        mock_mail.assert_called_once_with(
            "admin@example.com", f"bot@{socket.gethostname()}"
        )
        mock_mail.return_value.send_mail.assert_called_once_with(
            "Test Title", "Test Body"
        )
        mock_webhook.assert_called_once_with(["http://webhook.local"], "")
        mock_webhook.return_value.send_notification.assert_called_once_with(
            "Test Title", "Test Body"
        )

    @patch.object(fa, "MailNotifier")
    @patch.object(fa, "WebhookNotifier")
    def test_dispatch_all_hierarchical_resolution(
        self, mock_webhook: Any, mock_mail: Any
    ) -> None:
        config = {
            "notification_groups": [
                {
                    "name": "CascadeGroup",
                    "title": {"success": "Group Success"},
                    "mail": {
                        "to": "admin@example.com",
                        "title": {"success": "Mail Success"},
                    },
                    "webhooks": {"urls": ["http://admin.local"]},
                }
            ]
        }
        router = fa.NotificationRouter(config)
        router.dispatch_all("Test Title", "Test Body", True)

        # Mail uses specific title override
        mock_mail.return_value.send_mail.assert_called_once_with(
            "Mail Success", "Test Body"
        )

        # Webhook falls back to group title
        mock_webhook.assert_called_once_with(["http://admin.local"], "")
        mock_webhook.return_value.send_notification.assert_called_once_with(
            "Group Success", "Test Body"
        )

    def test_apprise_dispatch(self) -> None:
        fa.APPRISE_AVAILABLE = True
        config = {
            "notification_groups": [
                {
                    "name": "AppriseGroup",
                    "apprise": {"urls": ["mailto://user@example.com"]},
                }
            ]
        }
        if not hasattr(fa, "apprise"):
            fa.apprise = MagicMock()

        with patch.object(fa.apprise, "Apprise") as mock_ap_class:
            router = fa.NotificationRouter(config)
            router.dispatch_all("Title", "Body", True)
            mock_ap_class.return_value.add.assert_called_once_with(
                "mailto://user@example.com"
            )
            mock_ap_class.return_value.notify.assert_called_once()
