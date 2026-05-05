from unittest.mock import patch, MagicMock
from flatpak_automatic.snapper import SnapperManager


class TestSnapperManagerExtended:
    @patch("dbus.SystemBus")
    @patch("dbus.Interface")
    def test_init_with_bus_error(
        self, mock_interface: MagicMock, mock_bus: MagicMock
    ) -> None:
        """Test SnapperManager initialization when DBus fails."""
        mock_bus.side_effect = Exception("Bus error")
        # Ensure dbus is seen as available at module level
        with patch("flatpak_automatic.snapper.DBUS_AVAILABLE", True):
            # Patch dbus.Interface to return None or similar if needed,
            # but the logic should handle SystemBus failing.
            manager = SnapperManager()
            assert manager.interface is None

    @patch("dbus.SystemBus")
    @patch("dbus.Interface")
    @patch("flatpak_automatic.snapper.dbus")
    def test_create_snapshot_interface_error(
        self, mock_dbus: MagicMock, mock_interface: MagicMock, mock_bus: MagicMock
    ) -> None:
        """Test snapshot creation when the interface method fails."""
        # Ensure dbus is seen as available
        with patch("flatpak_automatic.snapper.DBUS_AVAILABLE", True):
            manager = SnapperManager()
            manager.interface = MagicMock()
            manager.interface.CreateSingleSnapshot.side_effect = Exception(
                "DBus Method Error"
            )

            # This should handle the exception and not crash
            manager.create_timeline_snapshot("test")
            manager.interface.CreateSingleSnapshot.assert_called_once()

    def test_create_snapshot_no_interface(self) -> None:
        """Test snapshot creation when interface was never initialized."""
        manager = SnapperManager()
        manager.interface = None
        manager.create_timeline_snapshot("test")  # Should just return
