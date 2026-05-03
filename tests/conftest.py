import sys
from typing import Generator
from unittest.mock import MagicMock
import pytest

# Global mock for dbus to be used across all unit tests
# This ensures that any import of flatpak_automatic (which might happen
# before a specific test file runs) will see the mock.
mock_dbus = MagicMock()
mock_dbus_exceptions = MagicMock()


@pytest.fixture(autouse=True, scope="session")  # type: ignore
def setup_dbus_mock() -> Generator[None, None, None]:
    # Only mock if not already present (prevents breaking integration tests if run together)
    if "dbus" not in sys.modules:
        sys.modules["dbus"] = mock_dbus
        sys.modules["dbus.exceptions"] = mock_dbus_exceptions
    yield
