import sys
import importlib.util
from unittest.mock import MagicMock, patch, ANY
from typing import Any

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
    def test_dispatch_all_state_dependent_resolution(
        self, mock_webhook: Any, mock_mail: Any
    ) -> None:
        config = {
            "notification_groups": [
                {
                    "name": "StateDependentGroup",
                    "title": {"success": "Group Success", "failure": "Group Failure"},
                    "mail": {
                        "to": "admin@example.com",
                        "title": {"success": "Mail Success"},
                        "body_template": {
                            "success": "mail_success.md",
                            "failure": "mail_failure.md",
                        },
                    },
                    "webhooks": {
                        "urls": ["http://admin.local"],
                        "body_template": "flat_template.md",
                    },
                }
            ]
        }

        # Test 1: SUCCESS STATE
        with patch.object(fa, "TemplateRenderer") as mock_template:
            mock_template.render.return_value = "Rendered Body"
            router = fa.NotificationRouter(config)
            router.dispatch_all("Fallback Title", "Test Body", success=True)

            # Mail should grab target 'success' title and 'success' template
            mock_mail.return_value.send_mail.assert_called_with(
                "Mail Success", "Rendered Body"
            )
            mock_template.render.assert_any_call("mail_success.md", ANY)

            # Webhook should grab group 'success' title and its own flat template
            mock_webhook.assert_called_with(["http://admin.local"], "")
            mock_webhook.return_value.send_notification.assert_called_with(
                "Group Success", "Rendered Body"
            )
            mock_template.render.assert_any_call("flat_template.md", ANY)

        mock_mail.reset_mock()
        mock_webhook.reset_mock()

        # Test 2: FAILURE STATE
        with patch.object(fa, "TemplateRenderer") as mock_template:
            mock_template.render.return_value = "Rendered Error"
            router = fa.NotificationRouter(config)
            router.dispatch_all("Fallback Title", "Test Body", success=False)

            # Mail lacks failure title, falls back to group failure title, but has failure template
            mock_mail.return_value.send_mail.assert_called_with(
                "Group Failure", "Rendered Error"
            )
            mock_template.render.assert_any_call("mail_failure.md", ANY)
