import unittest
import subprocess
import dbus  # type: ignore
import dbusmock  # type: ignore

import importlib.util

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "scripts/flatpak-automatic.py"
)
assert spec is not None
assert spec.loader is not None
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


class TestSnapperDBusIntegration(dbusmock.DBusTestCase):  # type: ignore
    @classmethod
    def setUpClass(cls) -> None:
        # Start the local CI system bus
        cls.start_system_bus()

    def setUp(self) -> None:
        # Spawn a generic D-Bus server explicitly on the SYSTEM bus
        self.p_mock = self.spawn_server(
            "org.opensuse.Snapper",
            "/org/opensuse/Snapper",
            "org.opensuse.Snapper",
            system_bus=True,
            stdout=subprocess.PIPE,
        )

        # Fetch the newly spawned generic object from the system bus
        bus = self.get_dbus(True)
        self.obj_snapper = bus.get_object(
            "org.opensuse.Snapper", "/org/opensuse/Snapper"
        )

        # Bind the dbusmock control interface to our generic object
        self.dbusmock = dbus.Interface(self.obj_snapper, dbusmock.MOCK_IFACE)
        self.dbusmock.AddMethod(
            "org.opensuse.Snapper", "CreateSingleSnapshot", "ssss", "i", "ret = 100"
        )

    def test_snapper_ipc_message_payload(self) -> None:
        manager = fa.SnapperManager()
        snapshot_id = manager.create_timeline_snapshot("Integration Test Description")
        self.assertEqual(snapshot_id, 100)

        calls = self.dbusmock.GetMethodCalls("CreateSingleSnapshot")
        self.assertEqual(len(calls), 1)

        args = calls[0][0]
        self.assertEqual(args[0], "root")
        self.assertEqual(args[1], "timeline")
        self.assertEqual(args[2], "Integration Test Description")


if __name__ == "__main__":
    unittest.main()
