import sys
import importlib.util
from unittest.mock import MagicMock, patch

# Mock dbus before importing fa
mock_dbus = MagicMock()
sys.modules["dbus"] = mock_dbus
sys.modules["dbus.exceptions"] = MagicMock()

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "src/flatpak-automatic.py"
)
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


class TestNotificationRouter:
    @patch.object(fa, "MailNotifier")
    @patch.object(fa, "WebhookNotifier")
    @patch.object(fa, "TemplateRenderer")
    def test_dispatch_all_legacy_global(self, mock_template, mock_webhook, mock_mail):
        config = {
            "mail": {"enabled": True, "to": "admin@example.com"},
            "webhooks": {"enabled": True, "urls": ["http://webhook.local"]},
        }
        router = fa.NotificationRouter(config)

        router.dispatch_all("Test Title", "Test Body", True)

        mock_mail.assert_called_once_with(
            "admin@example.com", f"bot@{fa.socket.gethostname()}"
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
    def test_dispatch_all_group_specific(self, mock_webhook, mock_mail):
        config = {
            "notification_groups": [
                {
                    "name": "Admin",
                    "mail": {"to": "admin@example.com"},
                    "webhooks": {"urls": ["http://admin.local"]},
                }
            ]
        }
        router = fa.NotificationRouter(config)

        router.dispatch_all("Test Title", "Test Body", True)

        mock_mail.assert_called_once_with(
            "admin@example.com", f"bot@{fa.socket.gethostname()}"
        )
        mock_webhook.assert_called_once_with(["http://admin.local"], "")

    def test_apprise_dispatch(self):
        fa.APPRISE_AVAILABLE = True
        config = {
            "notification_groups": [
                {"name": "AppriseGroup", "urls": ["mailto://user@example.com"]}
            ]
        }

        # Manually inject a mock apprise module if it doesn't exist
        if not hasattr(fa, "apprise"):
            fa.apprise = MagicMock()

        with patch.object(fa.apprise, "Apprise") as mock_ap_class:
            router = fa.NotificationRouter(config)
            router.dispatch_all("Title", "Body", True)

            mock_ap_class.return_value.add.assert_called_once_with(
                "mailto://user@example.com"
            )
            mock_ap_class.return_value.notify.assert_called_once()
