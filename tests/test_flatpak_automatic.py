import pytest
import sys
import importlib.util
import logging
import json
from unittest.mock import MagicMock, patch, mock_open
from typing import Any

mock_dbus = MagicMock()
sys.modules["dbus"] = mock_dbus
sys.modules["dbus.exceptions"] = MagicMock()

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "scripts/flatpak-automatic.py"
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
        updater = fa.FlatpakUpdater()
        assert updater.check_updates() is True
        assert updater.updates_available is True

    @patch("subprocess.run")
    def test_check_updates_none(self, mock_run: Any) -> None:
        mock_run.return_value = MagicMock(
            stdout="Looking for updates...\nNothing to do.\n", returncode=0
        )
        updater = fa.FlatpakUpdater()
        assert updater.check_updates() is False
        assert updater.updates_available is False

    @patch("subprocess.run")
    def test_apply_updates_success(self, mock_run: Any) -> None:
        mock_run.return_value = MagicMock(stdout="Success", stderr="", returncode=0)
        updater = fa.FlatpakUpdater()
        assert updater.apply_updates() is True

    @patch("subprocess.run")
    def test_apply_updates_failure(self, mock_run: Any) -> None:
        mock_run.return_value = MagicMock(
            stdout="Update failed",
            stderr="Error: GPG verification failed",
            returncode=1,
        )
        updater = fa.FlatpakUpdater()
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


class TestLoadSysconfig:
    @patch("os.path.exists")
    def test_load_sysconfig_parsing(self, mock_exists: Any) -> None:
        mock_exists.side_effect = lambda path: path == "/etc/default/flatpak-automatic"
        mock_file_content = (
            'FLATPAK_AUTO_UPDATE="false"\nFLATPAK_CREATE_SNAPSHOT=true\n# Comment\n'
        )
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            config = fa.load_sysconfig()
            assert config.get("FLATPAK_AUTO_UPDATE") == "false"
            assert config.get("FLATPAK_CREATE_SNAPSHOT") == "true"


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
    @patch.object(fa, "load_sysconfig")
    @patch.object(fa, "FlatpakUpdater")
    @patch.object(fa, "SnapperManager")
    @patch.object(fa, "MailNotifier")
    def test_main_updates_found(self, mock_mail, mock_snapper, mock_updater, mock_load):
        mock_load.return_value = {
            "FLATPAK_AUTO_UPDATE": "true",
            "FLATPAK_CREATE_SNAPSHOT": "true",
            "FLATPAK_AUTO_NOTIFY": "none",
        }
        updater_instance = mock_updater.return_value
        updater_instance.check_updates.return_value = True
        updater_instance.apply_updates.return_value = True
        snapper_instance = mock_snapper.return_value

        with pytest.raises(SystemExit) as e:
            fa.main()

        assert e.value.code == 0
        snapper_instance.create_timeline_snapshot.assert_called_once_with(
            "Pre-Flatpak Update Automation"
        )
        updater_instance.apply_updates.assert_called_once()
