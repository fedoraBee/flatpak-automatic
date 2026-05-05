import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from typing import Any

# Ensure src is in the path for tests and linting
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from flatpak_automatic.config import ConfigManager


class TestConfigManager:
    @patch("flatpak_automatic.config.ConfigManager._find_resource")
    @patch("flatpak_automatic.config.ConfigManager.get_user_config_path")
    @patch("flatpak_automatic.config.ConfigManager._generate_skeleton")
    @patch("yaml.safe_load")
    @patch("os.geteuid")
    def test_load_config_user_skeleton_source(
        self,
        mock_geteuid: MagicMock,
        mock_safe_load: MagicMock,
        mock_gen_skeleton: MagicMock,
        mock_get_user_path: MagicMock,
        mock_find_resource: MagicMock,
    ) -> None:
        """Verify that user config is scaffolded from the correct user default source."""
        # Simulate non-root user
        mock_geteuid.return_value = 1000
        # Return a real dict to avoid MagicMock issues in deep_merge
        mock_safe_load.return_value = {"default": True}

        # Setup paths
        user_config_path = MagicMock(spec=Path)
        user_config_path.exists.return_value = False

        user_default_path = MagicMock(spec=Path)
        user_default_path.exists.return_value = True
        # Ensure open returns something that doesn't cause yaml to hang
        user_default_path.open.return_value.__enter__.return_value = MagicMock()
        user_default_path.open.return_value.__enter__.return_value.read.return_value = (
            ""
        )

        mock_get_user_path.return_value = user_config_path

        # Mock find_resource to return specific Path mocks
        def side_effect(filename: str, fallback: str) -> Any:
            if filename == "config.user.default.yaml":
                return user_default_path
            return MagicMock(spec=Path)

        mock_find_resource.side_effect = side_effect

        ConfigManager.load()

        mock_gen_skeleton.assert_called_once_with(user_config_path, user_default_path)

    @patch("pathlib.Path.mkdir")
    @patch("shutil.copy")
    def test_generate_skeleton_execution(
        self, mock_copy: MagicMock, mock_mkdir: MagicMock
    ) -> None:
        """Test the low-level _generate_skeleton file operations."""
        target = MagicMock(spec=Path)
        source = MagicMock(spec=Path)
        source.exists.return_value = True

        ConfigManager._generate_skeleton(target, source)

        target.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_copy.assert_called_once_with(source, target)

    @patch("flatpak_automatic.config.ConfigManager._find_resource")
    def test_load_system_config(self, mock_find: MagicMock) -> None:
        """Verify that system config is loaded correctly for root."""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        # Correctly mock the context manager and read() to return a string
        m_open = mock_open(read_data="auto_update: true\n")
        mock_path.open = m_open
        mock_find.return_value = mock_path

        with patch("os.geteuid", return_value=0):
            config = ConfigManager.load()
            assert config.get("auto_update") is True

    @patch("flatpak_automatic.config.ConfigManager._find_resource")
    def test_load_empty_config(self, mock_find: MagicMock) -> None:
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_find.return_value = mock_path
        with patch("os.geteuid", return_value=0):
            config = ConfigManager.load()
            assert config == {}

    def test_deep_merge_basic(self) -> None:
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = ConfigManager.deep_merge(base, override)
        assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}

    def test_deep_merge_circular_protection(self) -> None:
        """Verify that deep_merge handles trivial circularities safely."""
        inner = {"x": 1}
        base = {"a": inner}
        # In the original code, if override["a"] was 'inner', it would recurse.
        # Now it should skip recursion if they are the same object.
        result = ConfigManager.deep_merge(base, {"a": inner})
        assert result["a"] is inner
