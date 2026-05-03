import sys
import importlib.util
from typing import Generator
from unittest.mock import MagicMock
import pytest

# Global mock for dbus to be used across all unit tests.
# Only apply the mock if the real dbus library is NOT installed.
# This prevents shadowing the real library in integration tests.
if importlib.util.find_spec("dbus") is None:
    mock_dbus = MagicMock()
    # Setting __path__ makes Python treat this Mock as a package,
    # allowing sub-module imports like 'import dbus.exceptions'.
    mock_dbus.__path__ = []

    sys.modules["dbus"] = mock_dbus
    sys.modules["dbus.exceptions"] = MagicMock()
    sys.modules["dbus.service"] = MagicMock()
    sys.modules["dbus.mainloop"] = MagicMock()
    sys.modules["dbus.mainloop.glib"] = MagicMock()


@pytest.fixture(autouse=True, scope="session")  # type: ignore
def setup_dbus_mock() -> Generator[None, None, None]:
    """Session-level fixture for dbus mocking hooks."""
    yield
