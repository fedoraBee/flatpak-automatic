import unittest
import subprocess
import dbus
import dbusmock

import importlib.util

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "src/flatpak-automatic.py"
)
assert spec is not None
assert spec.loader is not None
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


class TestSnapperDBusIntegration(dbusmock.DBusTestCase):  # type: ignore[misc]
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
        # Corrected signature to sssa{ss} to match the dictionary payload
        self.dbusmock.AddMethod(
            "org.opensuse.Snapper", "CreateSingleSnapshot", "sssa{ss}", "i", "ret = 100"
        )

    def tearDown(self) -> None:
        # Terminate the mocked dbus server process after each test to free the bus name
        self.p_mock.terminate()
        self.p_mock.wait()

    def test_snapper_ipc_message_payload(self) -> None:
        manager = fa.SnapperManager()
        snapshot_id = manager.create_timeline_snapshot("Integration Test Description")
        self.assertEqual(snapshot_id, 100)

        calls = self.dbusmock.GetMethodCalls("CreateSingleSnapshot")
        self.assertEqual(len(calls), 1)

        # Safely extract payload (dbusmock returns tuples which may include timestamps depending on version)
        flat_args = []
        for item in calls[0]:
            if isinstance(item, (tuple, list, dbus.Array, dbus.Struct)):
                flat_args.extend(list(item))
            else:
                flat_args.append(item)

        self.assertIn("root", flat_args)
        self.assertIn("timeline", flat_args)
        self.assertIn("Integration Test Description", flat_args)

    def test_snapper_ipc_graceful_degradation(self) -> None:
        # Re-map the mock interface to force an exception
        self.dbusmock.AddMethod(
            "org.opensuse.Snapper",
            "CreateSingleSnapshot",
            "sssa{ss}",
            "i",
            "raise Exception('Mocked IPC Failure')",
        )
        manager = fa.SnapperManager()
        snapshot_id = manager.create_timeline_snapshot("Error Test Description")

        # The manager must trap the exception and safely return -1
        self.assertEqual(snapshot_id, -1)


if __name__ == "__main__":
    unittest.main()
