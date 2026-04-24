import sys
import os
import pytest
from unittest.mock import MagicMock, patch, mock_open

# Globally mock DBus to ensure tests pass on CI environments lacking native dbus bindings
mock_dbus = MagicMock()
sys.modules['dbus'] = mock_dbus
sys.modules['dbus.exceptions'] = MagicMock()

import importlib.util
spec = importlib.util.spec_from_file_location("flatpak_automatic", "scripts/flatpak-automatic.py")
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)

class TestFlatpakUpdater:
    @patch('subprocess.run')
    def test_check_updates_found(self, mock_run):
        mock_run.return_value = MagicMock(stdout="org.test.App\tmaster\t1.0", returncode=0)
        updater = fa.FlatpakUpdater()
        assert updater.check_updates() is True
        assert updater.updates_available is True

    @patch('subprocess.run')
    def test_check_updates_none(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Looking for updates...\nNothing to do.\n", returncode=0)
        updater = fa.FlatpakUpdater()
        assert updater.check_updates() is False
        assert updater.updates_available is False

    @patch('subprocess.run')
    def test_apply_updates_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Success", stderr="", returncode=0)
        updater = fa.FlatpakUpdater()
        assert updater.apply_updates() is True

class TestSnapperManager:
    def test_create_timeline_snapshot_success(self):
        manager = fa.SnapperManager()
        manager.interface = MagicMock()
        manager.interface.CreateSingleSnapshot.return_value = 100
        
        snap_id = manager.create_timeline_snapshot("Test Description")
        assert snap_id == 100
        manager.interface.CreateSingleSnapshot.assert_called_once_with(
            "root", "timeline", "Test Description", mock_dbus.Dictionary({}, signature="ss")
        )

    def test_create_timeline_snapshot_no_interface(self):
        manager = fa.SnapperManager()
        manager.interface = None
        assert manager.create_timeline_snapshot() == -1

class TestLoadSysconfig:
    @patch('os.path.exists')
    def test_load_sysconfig_parsing(self, mock_exists):
        mock_exists.side_effect = lambda path: path == '/etc/default/flatpak-automatic'
        mock_file_content = 'FLATPAK_AUTO_UPDATE="false"\nFLATPAK_CREATE_SNAPSHOT=true\n# Comment\n'
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            config = fa.load_sysconfig()
            assert config.get('FLATPAK_AUTO_UPDATE') == 'false'
            assert config.get('FLATPAK_CREATE_SNAPSHOT') == 'true'
