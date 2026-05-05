import pytest
import sys
import logging
import json
from unittest.mock import MagicMock, patch, mock_open
from typing import Any
from pathlib import Path

# Import from the package
import dbus
import flatpak_automatic as fa
from flatpak_automatic.__main__ import main as fa_main


class TestFlatpakUpdater:
    @patch("subprocess.run")
    def test_check_updates_found(self, mock_run: Any) -> None:
        mock_run.return_value = MagicMock(
            stdout="org.test.App\tmaster\t1.0", returncode=0
        )
        updater = fa.FlatpakUpdater(excludes=[])
        assert updater.check_updates() is True
        assert updater.updates_available is True

    @patch("subprocess.run")
    def test_check_updates_none(self, mock_run: Any) -> None:
        # Test with the typical "no updates" output or header-only output
        mock_run.return_value = MagicMock(
            stdout="Application ID\tBranch\tVersion\n", returncode=0
        )
        updater = fa.FlatpakUpdater(excludes=[])
        assert updater.check_updates() is False
        assert updater.updates_available is False

    @patch("subprocess.run")
    def test_check_updates_info_messages(self, mock_run: Any) -> None:
        # Test that informational messages without valid App IDs are ignored
        mock_run.return_value = MagicMock(
            stdout="Looking for updates...\nNothing to do.\n", returncode=0
        )
        updater = fa.FlatpakUpdater(excludes=[])
        assert updater.check_updates() is False
        assert updater.updates_available is False

    @patch("subprocess.run")
    def test_apply_updates_success(self, mock_run: Any) -> None:
        mock_run.return_value = MagicMock(stdout="Success", stderr="", returncode=0)
        updater = fa.FlatpakUpdater(excludes=[])
        assert updater.apply_updates() is True

    @patch("subprocess.run")
    def test_apply_updates_failure(self, mock_run: Any) -> None:
        mock_run.return_value = MagicMock(
            stdout="Update failed",
            stderr="Error: GPG verification failed",
            returncode=1,
        )
        updater = fa.FlatpakUpdater(excludes=[])
        assert updater.apply_updates() is False
        assert "Error: GPG verification failed" in updater.update_log


class TestSnapperManager:
    def test_create_timeline_snapshot_success(self) -> None:
        manager = fa.SnapperManager()
        manager.interface = MagicMock()
        manager.interface.CreateSingleSnapshot.return_value = 100

        snap_id = manager.create_timeline_snapshot("Test Description")
        assert snap_id == 100
        manager.interface.CreateSingleSnapshot.assert_called_once_with(
            "root",
            "timeline",
            "Test Description",
            dbus.Dictionary({}, signature="ss"),
        )

    def test_create_timeline_snapshot_no_interface(self) -> None:
        manager = fa.SnapperManager()
        manager.interface = None
        assert manager.create_timeline_snapshot() == -1


class TestAutomationEngine:
    @patch("os.walk")
    @patch("shutil.rmtree")
    @patch("os.path.exists")
    def test_wipe_bytecode_cache(
        self, mock_exists: Any, mock_rmtree: Any, mock_walk: Any
    ) -> None:
        mock_exists.return_value = True
        mock_walk.return_value = [
            ("/usr/share/flatpak-automatic", ["flatpak_automatic", "__pycache__"], []),
            ("/usr/share/flatpak-automatic/flatpak_automatic", ["__pycache__"], []),
        ]

        engine = fa.AutomationEngine({}, {})
        engine.user_scope = False
        engine.wipe_bytecode_cache()

        assert mock_rmtree.call_count == 2
        mock_rmtree.assert_any_call("/usr/share/flatpak-automatic/__pycache__")
        mock_rmtree.assert_any_call(
            "/usr/share/flatpak-automatic/flatpak_automatic/__pycache__"
        )


class TestAutomationEngineRun:
    @patch("flatpak_automatic.core.FlatpakUpdater")
    @patch("flatpak_automatic.config.StateManager.save")
    def test_run_no_updates(
        self, mock_save: MagicMock, mock_updater: MagicMock
    ) -> None:
        engine = fa.AutomationEngine({"auto_update": True}, {})
        mock_updater.return_value.check_updates.return_value = False

        assert engine.run() is True
        assert mock_updater.return_value.check_updates.called

    @patch("flatpak_automatic.core.FlatpakUpdater")
    @patch("flatpak_automatic.config.StateManager.save")
    def test_run_dry_run(self, mock_save: MagicMock, mock_updater: MagicMock) -> None:
        engine = fa.AutomationEngine({"auto_update": True}, {})
        mock_updater.return_value.check_updates.return_value = True
        mock_updater.return_value.update_log = "Some updates"

        assert engine.run(dry_run=True) is True
        assert not mock_updater.return_value.apply_updates.called

    @patch("flatpak_automatic.core.FlatpakUpdater")
    @patch("flatpak_automatic.core.NotificationRouter")
    @patch("flatpak_automatic.config.StateManager.save")
    def test_run_force(
        self, mock_save: MagicMock, mock_router: MagicMock, mock_updater: MagicMock
    ) -> None:
        # Even if auto_update is false, force=True should proceed
        engine = fa.AutomationEngine({"auto_update": False}, {})
        mock_updater.return_value.check_updates.return_value = True
        mock_updater.return_value.apply_updates.return_value = True

        assert engine.run(force=True) is True
        assert mock_updater.return_value.apply_updates.called


class TestLoadConfig:
    @patch("flatpak_automatic.config.ConfigManager._find_resource")
    @patch(
        "pathlib.Path.open", new_callable=mock_open, read_data="auto_update: false\n"
    )
    def test_load_config_parsing(
        self, mock_path_open: Any, mock_find_resource: Any
    ) -> None:
        # Mock find_resource to return a Path object that "exists"
        mock_find_resource.return_value = MagicMock(spec=Path)
        mock_find_resource.return_value.exists.return_value = True
        mock_find_resource.return_value.open = mock_path_open

        # We need to bypass geteuid to simulate root for this specific test
        with patch("os.geteuid", return_value=0):
            config = fa.load_config()
            assert config.get("auto_update") is False


class TestJSONFormatter:
    def test_format_standard_log(self) -> None:
        formatter = fa.JSONFormatter()
        record = logging.LogRecord(
            name="flatpak_automatic",
            level=logging.INFO,
            pathname="flatpak-automatic.py",
            lineno=100,
            msg="Successfully applied flatpak updates.",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        data = json.loads(output)

        assert "timestamp" in data
        assert data["level"] == "INFO"
        assert data["message"] == "Successfully applied flatpak updates."
        assert data["logger"] == "flatpak_automatic"
        assert "exception" not in data

    def test_format_exception_log(self) -> None:
        formatter = fa.JSONFormatter()
        try:
            raise ValueError("Simulated system bus failure")
        except ValueError:
            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="flatpak_automatic",
            level=logging.ERROR,
            pathname="flatpak-automatic.py",
            lineno=105,
            msg="Failed to connect to Snapper DBus",
            args=(),
            exc_info=exc_info,
        )
        output = formatter.format(record)
        data = json.loads(output)

        assert "timestamp" in data
        assert data["level"] == "ERROR"
        assert data["message"] == "Failed to connect to Snapper DBus"
        assert "exception" in data
        assert "ValueError: Simulated system bus failure" in data["exception"]


class TestMainIntegration:
    @patch("sys.argv", ["flatpak-automatic"])
    @patch("os.geteuid", return_value=0)
    @patch("flatpak_automatic.config.ConfigManager.load")
    @patch("flatpak_automatic.core.FlatpakUpdater")
    @patch("flatpak_automatic.core.SnapperManager")
    @patch("flatpak_automatic.core.NotificationRouter")
    @patch("flatpak_automatic.config.StateManager.load")
    @patch("flatpak_automatic.config.StateManager.save")
    def test_main_updates_found(
        self,
        mock_save_state: Any,
        mock_load_state: Any,
        mock_router: Any,
        mock_snapper: Any,
        mock_updater: Any,
        mock_load: Any,
        mock_geteuid: Any,
    ) -> None:
        mock_load.return_value = {
            "auto_update": True,
            "auto_notify": "none",
            "snapshots": {
                "enabled": True,
                "snapper_config": "root",
                "snapper_descriptions": {
                    "pre": "flatpak-automatic-pre",
                    "post": "flatpak-automatic-post",
                },
            },
        }
        mock_load_state.return_value = {"last_try": "Never", "last_success": "Never"}

        updater_instance = mock_updater.return_value
        updater_instance.check_updates.return_value = True
        updater_instance.apply_updates.return_value = True
        snapper_instance = mock_snapper.return_value

        with pytest.raises(SystemExit) as e:
            fa_main()

        assert e.value.code == 0
        assert snapper_instance.create_timeline_snapshot.call_count == 2
        snapper_instance.create_timeline_snapshot.assert_any_call(
            "flatpak-automatic-pre"
        )
        snapper_instance.create_timeline_snapshot.assert_any_call(
            "flatpak-automatic-post"
        )
        updater_instance.apply_updates.assert_called_once()
        mock_save_state.assert_called()
