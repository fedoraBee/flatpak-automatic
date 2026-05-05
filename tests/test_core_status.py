from unittest.mock import patch, MagicMock
from flatpak_automatic.core import AutomationEngine


class TestAutomationEngineStatus:
    @patch("subprocess.run")
    @patch("flatpak_automatic.notifiers.MailNotifier.is_available")
    @patch("flatpak_automatic.notifiers.DesktopNotifier.is_available")
    @patch("flatpak_automatic.notifiers.WebhookNotifier.is_available")
    def test_print_status_overview(
        self,
        mock_wh: MagicMock,
        mock_dt: MagicMock,
        mock_mail: MagicMock,
        mock_run: MagicMock,
    ) -> None:
        # Mocking systemctl calls
        mock_run.side_effect = [
            MagicMock(returncode=0),  # is-enabled
            MagicMock(returncode=0),  # is-active
            MagicMock(
                stdout="Tue 2026-05-05 10:00:00 UTC", returncode=0
            ),  # show next run
            MagicMock(stdout="org.test.App 1.0\n", returncode=0),  # flatpak list
        ]
        mock_mail.return_value = True
        mock_dt.return_value = True
        mock_wh.return_value = True

        engine = AutomationEngine(
            {"exclusions": []}, {"last_try": "Never", "last_success": "Never"}
        )
        engine.user_scope = False

        # Capture stdout
        with patch("builtins.print") as mock_print:
            engine.print_status_overview()
            assert mock_print.called
            # Verify some key headers are printed
            printed_args = [
                call.args[0] if call.args else "" for call in mock_print.call_args_list
            ]
            assert any(
                "[ System Status & Monitoring Overview ]" in arg for arg in printed_args
            )
            assert any("📊 Execution State:" in arg for arg in printed_args)
            assert any("⏰ Automation Timer:" in arg for arg in printed_args)
            assert any(
                "🔔 Notification & Delivery Services:" in arg for arg in printed_args
            )

    @patch("subprocess.run")
    def test_print_status_timer_disabled(self, mock_run: MagicMock) -> None:
        mock_run.side_effect = [
            MagicMock(returncode=1),  # is-enabled
            MagicMock(returncode=1),  # is-active
            MagicMock(stdout="", returncode=0),  # flatpak list
        ]

        engine = AutomationEngine({"exclusions": []}, {})
        with patch("builtins.print") as mock_print:
            engine.print_status_overview()
            printed_args = [
                call.args[0] if call.args else "" for call in mock_print.call_args_list
            ]
            assert any("Disabled / Inactive" in arg for arg in printed_args)
