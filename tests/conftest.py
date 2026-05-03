import sys
from typing import Generator
from unittest.mock import MagicMock
import pytest

# Global mock for dbus to be used across all unit tests.
# This MUST happen at the top level of conftest.py to ensure that
# when pytest collects test modules, any 'import dbus' succeeds
# even if the physical library is missing.
mock_dbus = MagicMock()
mock_dbus_exceptions = MagicMock()

if "dbus" not in sys.modules:
    sys.modules["dbus"] = mock_dbus
    sys.modules["dbus.exceptions"] = mock_dbus_exceptions


@pytest.fixture(autouse=True, scope="session")  # type: ignore
def setup_dbus_mock() -> Generator[None, None, None]:
    # This fixture remains to provide a clean session-level hook if needed,
    # though the actual mocking is now done at module load time.
    yield
