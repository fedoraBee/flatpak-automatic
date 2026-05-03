import pytest  # type: ignore
import sys
import importlib.util
import logging
import json
from unittest.mock import MagicMock, patch, mock_open
from typing import Any
from pathlib import Path

mock_dbus = MagicMock()
sys.modules["dbus"] = mock_dbus
sys.modules["dbus.exceptions"] = MagicMock()

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "src/flatpak-automatic.py"
)
assert spec is not None
assert spec.loader is not None
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


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
            mock_dbus.Dictionary({}, signature="ss"),
        )

    def test_create_timeline_snapshot_no_interface(self) -> None:
        manager = fa.SnapperManager()
        manager.interface = None
        assert manager.create_timeline_snapshot() == -1


class TestLoadConfig:
    @patch("src.flatpak_automatic.config.ConfigManager._find_resource")
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
            fa.main()

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
