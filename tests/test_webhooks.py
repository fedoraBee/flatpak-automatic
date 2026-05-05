from unittest.mock import patch, MagicMock
from flatpak_automatic.notifiers.webhook import WebhookNotifier


class TestWebhookNotifier:
    def test_webhook_initialization(self) -> None:
        urls = ["http://test.local"]
        secret = "supersecret"
        notifier = WebhookNotifier(urls, secret)
        assert notifier.urls == urls
        assert notifier.secret == secret

    @patch("socket.create_connection")
    def test_is_available_online(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value = MagicMock()
        assert WebhookNotifier.is_available() is True

    @patch("socket.create_connection")
    def test_is_available_offline(self, mock_conn: MagicMock) -> None:
        mock_conn.side_effect = OSError("Offline")
        assert WebhookNotifier.is_available() is False

    @patch("urllib.request.urlopen")
    @patch("urllib.request.Request")
    @patch("flatpak_automatic.config.ConfigManager.verify_policy")
    def test_send_notification_success(
        self, mock_verify: MagicMock, mock_request: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        mock_verify.return_value = True
        notifier = WebhookNotifier(["http://webhook.url"], "secret")

        # Mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        notifier.send_notification("Title", "Body")

        assert mock_request.called
        assert mock_urlopen.called

    @patch("urllib.request.urlopen")
    @patch("flatpak_automatic.config.ConfigManager.verify_policy")
    def test_send_notification_disabled(
        self, mock_verify: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        mock_verify.return_value = False
        notifier = WebhookNotifier(["http://webhook.url"])
        notifier.send_notification("Title", "Body")
        assert not mock_urlopen.called
