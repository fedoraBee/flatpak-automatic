from unittest.mock import patch, MagicMock
import sys
import os

# Mock dbus before importing anything that might use it
sys.modules["dbus"] = MagicMock()
sys.modules["dbus.exceptions"] = MagicMock()

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from flatpak_automatic.notifiers.mail import MailNotifier  # noqa: E402


@patch("shutil.which")
@patch("flatpak_automatic.config.ConfigManager.verify_policy")
def test_mail_notifier_cmd_construction(mock_verify, mock_which):
    mock_verify.return_value = True
    # Only return a path for 'mailx', not for 's-nail' or others
    mock_which.side_effect = lambda x: "/usr/bin/mailx" if x == "mailx" else None

    notifier = MailNotifier("to@example.com", "from@example.com")
    assert notifier.mail_cmd == "mailx"

    with patch("subprocess.run") as mock_run, patch("subprocess.Popen") as mock_popen:
        # Mock help output showing -r and -a support
        mock_run.return_value = MagicMock(
            stdout="-r sender -a header", stderr="", returncode=0
        )
        mock_popen.return_value.communicate.return_value = (b"", b"")

        # 1. HTML body
        notifier.send_mail("Subject", "<html><body>Test</body></html>")

        # Verify cmd
        args, _ = mock_popen.call_args
        cmd = args[0]
        assert "mailx" in cmd
        assert "-s" in cmd
        assert "Subject" in cmd
        assert "-a" in cmd
        assert "Content-Type: text/html; charset=UTF-8" in cmd
        assert "-r" in cmd
        assert "from@example.com" in cmd
        assert "to@example.com" == cmd[-1]

        # 2. Plain text body
        notifier.send_mail("Subject", "Plain text")
        args, _ = mock_popen.call_args
        cmd = args[0]
        assert "Content-Type: text/plain; charset=UTF-8" in cmd

        # 3. Test fallback to -a for From header if -r is not in help
        mock_run.return_value = MagicMock(
            stdout="-a header (no r)", stderr="", returncode=0
        )
        notifier.send_mail("Subject", "Plain text")
        args, _ = mock_popen.call_args
        cmd = args[0]
        assert "-r" not in cmd
        assert "-a" in cmd
        assert "From: from@example.com" in cmd
