import os
from unittest.mock import MagicMock, patch
from flatpak_automatic.notifiers.desktop import DesktopNotifier
from flatpak_automatic.constants import ICON_PATH


class TestDesktopNotifier:
    @patch("flatpak_automatic.notifiers.desktop.ConfigManager.verify_policy")
    def test_disabled_policy(self, mock_verify: MagicMock) -> None:
        mock_verify.return_value = False
        notifier = DesktopNotifier()
        with patch("subprocess.run") as mock_run:
            notifier.send_notification("Title", "Body")
            mock_run.assert_not_called()

    @patch("flatpak_automatic.notifiers.desktop.ConfigManager.verify_policy")
    @patch("subprocess.run")
    @patch("os.getuid")
    @patch("os.path.exists")
    def test_send_notification_success(
        self,
        mock_exists: MagicMock,
        mock_getuid: MagicMock,
        mock_run: MagicMock,
        mock_verify: MagicMock,
    ) -> None:
        mock_verify.return_value = True
        mock_getuid.return_value = 0  # Running as root
        mock_exists.return_value = True

        # Mock loginctl list-sessions
        mock_loginctl = MagicMock()
        mock_loginctl.stdout = (
            "2 1000 alex seat0 4605 user tty2 no -\n3 1001 bob - 4658 manager - no -"
        )

        # Mock systemctl --user show-environment
        mock_env = MagicMock()
        mock_env.stdout = (
            "DISPLAY=:0\nWAYLAND_DISPLAY=wayland-0\nXDG_RUNTIME_DIR=/run/user/1000"
        )

        # Mock notify-send
        mock_notify = MagicMock()

        mock_run.side_effect = [mock_loginctl, mock_env, mock_notify]

        notifier = DesktopNotifier()
        notifier.send_notification("Test Title", "Test Body")

        # Check loginctl call
        mock_run.assert_any_call(
            ["loginctl", "list-sessions", "--no-legend"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Check environment call (for alex, since bob is manager/no-seat)
        mock_run.assert_any_call(
            ["sudo", "-u", "alex", "systemctl", "--user", "show-environment"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Check notify-send call
        expected_icon = f"file://{ICON_PATH}" if os.path.isabs(ICON_PATH) else ICON_PATH
        expected_hints = (
            ["-h", f"string:image-path:{ICON_PATH}"] if os.path.isabs(ICON_PATH) else []
        )

        mock_run.assert_any_call(
            [
                "sudo",
                "-u",
                "alex",
                "env",
                "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus",
                "XDG_RUNTIME_DIR=/run/user/1000",
                "notify-send",
                "-a",
                "Flatpak Automatic",
                "-i",
                expected_icon,
            ]
            + expected_hints
            + ["Test Title", "Test Body"],
            check=False,
        )

    @patch("flatpak_automatic.notifiers.desktop.ConfigManager.verify_policy")
    @patch("subprocess.run")
    @patch("os.getuid")
    def test_rootless_filtering(
        self, mock_getuid: MagicMock, mock_run: MagicMock, mock_verify: MagicMock
    ) -> None:
        mock_verify.return_value = True
        mock_getuid.return_value = 1000  # Running as alex

        # Mock loginctl list-sessions
        mock_loginctl = MagicMock()
        mock_loginctl.stdout = "2 1000 alex seat0 4605 user tty2 no -\n4 1001 bob seat0 4659 user tty3 no -"

        # Mock systemctl --user show-environment
        mock_env = MagicMock()
        mock_env.stdout = "DISPLAY=:0"

        mock_run.side_effect = [mock_loginctl, mock_env, MagicMock()]

        notifier = DesktopNotifier()
        notifier.send_notification("Title", "Body")

        # Should only call for alex (uid 1000), not bob (uid 1001)
        # First call: loginctl
        # Second call: systemctl (no sudo)
        # Third call: notify-send (no sudo)

        assert mock_run.call_count == 3
        mock_run.assert_any_call(
            ["systemctl", "--user", "show-environment"],
            capture_output=True,
            text=True,
            check=False,
        )
