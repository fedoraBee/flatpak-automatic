import unittest
import subprocess
import dbus
import dbusmock

# Import the daemon dynamically to avoid running main()
import importlib.util

spec = importlib.util.spec_from_file_location(
    "flatpak_automatic", "scripts/flatpak-automatic.py"
)
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


class TestSnapperDBusIntegration(dbusmock.DBusTestCase):
    @classmethod
    def setUpClass(cls):
        # Starts a genuine local dbus-daemon session isolated for this test
        cls.start_system_bus()

    def setUp(self):
        # Mock the Snapper service on the system bus
        self.p_mock = self.spawn_server_template(
            "org.opensuse.Snapper", {}, stdout=subprocess.PIPE
        )

        # Add the specific interface and method we want to trace
        self.dbusmock = dbus.Interface(
            self.get_dbus(True).get_object(
                "org.opensuse.Snapper", "/org/opensuse/Snapper"
            ),
            dbusmock.MOCK_IFACE,
        )
        self.dbusmock.AddMethod(
            "org.opensuse.Snapper", "CreateSingleSnapshot", "ssss", "i", "ret = 100"
        )

    def test_snapper_ipc_message_payload(self):
        # Instantiate our manager which will connect to the dbusmock bus
        manager = fa.SnapperManager()

        # Execute the method
        snapshot_id = manager.create_timeline_snapshot("Integration Test Description")

        # 1. Assert the Python daemon correctly interpreted the mock DBus return signature (100)
        self.assertEqual(snapshot_id, 100)

        # 2. Assert the payload was transmitted accurately across the bus
        calls = self.dbusmock.GetMethodCalls("CreateSingleSnapshot")
        self.assertEqual(len(calls), 1)

        # calls[0] structure is (args_tuple, signature)
        args = calls[0][0]
        self.assertEqual(args[0], "root")  # config
        self.assertEqual(args[1], "timeline")  # cleanup algorithm
        self.assertEqual(args[2], "Integration Test Description")


if __name__ == "__main__":
    unittest.main()
