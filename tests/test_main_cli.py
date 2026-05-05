import pytest
from unittest.mock import patch, MagicMock
from flatpak_automatic.__main__ import main


class TestMainCLI:
    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    def test_main_check_config(
        self,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock()
        args.check_config = True
        args.reload = False
        args.apply_schedule = False
        args.enable_timer = False
        args.disable_timer = False
        args.status = False
        args.history = False
        args.test_notify = False
        args.dry_run = False
        args.force = False
        args.desktop_mode = False
        mock_parser.return_value.parse_args.return_value = args

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        mock_engine.return_value.validate_config.assert_called_once()

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    @patch("subprocess.run")
    def test_main_status(
        self,
        mock_run: MagicMock,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=False,
            apply_schedule=False,
            enable_timer=False,
            disable_timer=False,
            status=True,
            history=False,
            test_notify=False,
        )
        mock_parser.return_value.parse_args.return_value = args

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        mock_engine.return_value.print_status_overview.assert_called_once()

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    @patch("subprocess.run")
    def test_main_enable_timer(
        self,
        mock_run: MagicMock,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=False,
            apply_schedule=False,
            enable_timer=True,
            disable_timer=False,
            status=False,
            history=False,
            test_notify=False,
        )
        mock_parser.return_value.parse_args.return_value = args

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        assert mock_run.called
        assert "enable" in mock_run.call_args[0][0]

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    @patch("subprocess.run")
    def test_main_disable_timer(
        self,
        mock_run: MagicMock,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=False,
            apply_schedule=False,
            enable_timer=False,
            disable_timer=True,
            status=False,
            history=False,
            test_notify=False,
        )
        mock_parser.return_value.parse_args.return_value = args

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        assert mock_run.called
        assert "disable" in mock_run.call_args[0][0]

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    @patch("subprocess.run")
    def test_main_reload(
        self,
        mock_run: MagicMock,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=True,
            apply_schedule=False,
            enable_timer=False,
            disable_timer=False,
            status=False,
            history=False,
            test_notify=False,
        )
        mock_parser.return_value.parse_args.return_value = args
        mock_run.return_value = MagicMock(returncode=0)

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        assert mock_run.called
        mock_engine.return_value.wipe_bytecode_cache.assert_called_once()

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    @patch("subprocess.run")
    def test_main_history(
        self,
        mock_run: MagicMock,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=False,
            apply_schedule=False,
            enable_timer=False,
            disable_timer=False,
            status=False,
            history=True,
            test_notify=False,
        )
        mock_parser.return_value.parse_args.return_value = args

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        assert mock_run.called
        assert "journalctl" in mock_run.call_args[0][0]

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    def test_main_test_notify(
        self,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=False,
            apply_schedule=False,
            enable_timer=False,
            disable_timer=False,
            status=False,
            history=False,
            test_notify=True,
        )
        mock_parser.return_value.parse_args.return_value = args

        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        mock_engine.return_value.dispatch_test_notifications.assert_called_once()

    @patch("flatpak_automatic.__main__.get_parser")
    @patch("flatpak_automatic.__main__.ConfigManager.load")
    @patch("flatpak_automatic.__main__.StateManager.load")
    @patch("flatpak_automatic.__main__.AutomationEngine")
    @patch("subprocess.run")
    @patch("os.makedirs")
    def test_main_apply_schedule(
        self,
        mock_makedirs: MagicMock,
        mock_run: MagicMock,
        mock_engine: MagicMock,
        mock_state: MagicMock,
        mock_config: MagicMock,
        mock_parser: MagicMock,
    ) -> None:
        args = MagicMock(
            check_config=False,
            reload=False,
            apply_schedule=True,
            enable_timer=False,
            disable_timer=False,
            status=False,
            history=False,
            test_notify=False,
        )
        mock_parser.return_value.parse_args.return_value = args
        mock_config.return_value = {"timer": {"schedule": "weekly", "delay": "2h"}}

        with patch("builtins.open", MagicMock()):
            with pytest.raises(SystemExit) as e:
                main()
        assert e.value.code == 0
        assert mock_makedirs.called
        assert mock_run.called
