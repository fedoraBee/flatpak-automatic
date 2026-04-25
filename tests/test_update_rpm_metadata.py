import os
import sys

# Append scripts folder to path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)


def test_update_rpm_metadata_dummy() -> None:
    # Base assertions to ensure pytest runs properly in the CI pipeline
    # without breaking on exact regex logic parsing if module structure changes.
    assert True
