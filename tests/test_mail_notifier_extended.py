from unittest.mock import patch, MagicMock
from flatpak_automatic.notifiers.mail import MailNotifier


class TestMailNotifierExtended:
    @patch("shutil.which")
    @patch("flatpak_automatic.config.ConfigManager.verify_policy", return_value=True)
    def test_send_mail_s_nail(
        self, mock_policy: MagicMock, mock_which: MagicMock
    ) -> None:
        mock_which.side_effect = lambda x: "/usr/bin/s-nail" if x == "s-nail" else None
        notifier = MailNotifier("to@example.com", "from@example.com")
        assert notifier.mail_cmd == "s-nail"

        with patch("subprocess.run") as mock_run:
            # Include s-nail in help output
            mock_run.return_value = MagicMock(
                stdout="s-nail v14.9.15. -a attach, -r address, -M mimetype", stderr=""
            )
            with patch("subprocess.Popen") as mock_popen:
                mock_popen.return_value.communicate.return_value = (b"", b"")
                notifier.send_mail("Subject", "<html>Body</html>")

                args, _ = mock_popen.call_args
                cmd = args[0]
                assert "text/html" in str(cmd)
                assert "-r" in cmd
                assert "-M" in cmd
                assert "-a" not in cmd  # Should NOT use -a for headers in s-nail

    @patch("shutil.which")
    @patch("flatpak_automatic.config.ConfigManager.verify_policy", return_value=True)
    def test_send_mail_bsd_style(
        self, mock_policy: MagicMock, mock_which: MagicMock
    ) -> None:
        # Only return /usr/bin/mail for 'mail'
        mock_which.side_effect = lambda x: "/usr/bin/mail" if x == "mail" else None
        notifier = MailNotifier("to@example.com", "from@example.com")
        assert notifier.mail_cmd == "mail"

        with patch("subprocess.run") as mock_run:
            # Only include -a header in help output
            mock_run.return_value = MagicMock(
                stdout="standard mail help: -a header", stderr=""
            )
            with patch("subprocess.Popen") as mock_popen:
                mock_popen.return_value.communicate.return_value = (b"", b"")
                notifier.send_mail("Subject", "Plain body")

                args, _ = mock_popen.call_args
                cmd = args[0]
                assert "mail" in cmd
                # Should fallback to -a From: if -r is not in help
                assert "From: from@example.com" in str(cmd)
                assert "-a" in cmd
                assert "Content-Type: text/plain; charset=UTF-8" in cmd

    @patch("shutil.which", return_value=None)
    @patch("flatpak_automatic.config.ConfigManager.verify_policy", return_value=True)
    def test_send_mail_no_client(
        self, mock_policy: MagicMock, mock_which: MagicMock
    ) -> None:
        notifier = MailNotifier("to@example.com", "from@example.com")
        assert notifier.mail_cmd is None
        notifier.send_mail("Sub", "Body")  # Should just return
