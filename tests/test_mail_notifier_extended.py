from unittest.mock import patch, MagicMock
from flatpak_automatic.notifiers.mail import MailNotifier


class TestMailNotifierExtended:
    @patch("shutil.which", return_value="/usr/bin/s-nail")
    @patch("flatpak_automatic.config.ConfigManager.verify_policy", return_value=True)
    def test_send_mail_html(
        self, mock_policy: MagicMock, mock_which: MagicMock
    ) -> None:
        notifier = MailNotifier("to@example.com", "from@example.com")

        with patch("subprocess.run") as mock_run:
            # Include -a and -r in help output
            mock_run.return_value = MagicMock(
                stdout="s-nail help: -a header, -r address", stderr=""
            )
            with patch("subprocess.Popen") as mock_popen:
                mock_popen.return_value.communicate.return_value = (b"", b"")
                notifier.send_mail("Subject", "<html>Body</html>")

                args, _ = mock_popen.call_args
                cmd = args[0]
                assert "text/html" in str(cmd)
                assert "-r" in cmd
                assert "-a" in cmd

    @patch("shutil.which", return_value="/usr/bin/mail")
    @patch("flatpak_automatic.config.ConfigManager.verify_policy", return_value=True)
    def test_send_mail_bsd_style(
        self, mock_policy: MagicMock, mock_which: MagicMock
    ) -> None:
        notifier = MailNotifier("to@example.com", "from@example.com")

        with patch("subprocess.run") as mock_run:
            # Only include -a in help output
            mock_run.return_value = MagicMock(
                stdout="standard mail help: -a header", stderr=""
            )
            with patch("subprocess.Popen") as mock_popen:
                mock_popen.return_value.communicate.return_value = (b"", b"")
                notifier.send_mail("Subject", "Plain body")

                args, _ = mock_popen.call_args
                cmd = args[0]
                # Should fallback to -a From: if -r is not in help
                assert "From: from@example.com" in str(cmd)

    @patch("shutil.which", return_value=None)
    @patch("flatpak_automatic.config.ConfigManager.verify_policy", return_value=True)
    def test_send_mail_no_client(
        self, mock_policy: MagicMock, mock_which: MagicMock
    ) -> None:
        notifier = MailNotifier("to@example.com", "from@example.com")
        assert notifier.mail_cmd is None
        notifier.send_mail("Sub", "Body")  # Should just return
