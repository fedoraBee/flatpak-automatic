from pathlib import Path
from unittest.mock import patch, MagicMock
from flatpak_automatic.config import ConfigManager


class TestConfigManager:
    @patch("flatpak_automatic.config.ConfigManager._find_resource")
    @patch("flatpak_automatic.config.ConfigManager.get_user_config_path")
    @patch("flatpak_automatic.config.ConfigManager._generate_skeleton")
    @patch("yaml.safe_load")
    @patch("os.geteuid")
    def test_load_config_user_skeleton_source(
        self,
        mock_geteuid,
        mock_safe_load,
        mock_gen_skeleton,
        mock_get_user_path,
        mock_find_resource,
    ):
        # Simulate non-root user
        mock_geteuid.return_value = 1000

        # Setup paths
        user_config_path = MagicMock(spec=Path)
        user_config_path.exists.return_value = (
            False  # Simulate user config NOT existing
        )

        user_default_path = MagicMock(spec=Path)
        user_default_path.exists.return_value = True

        mock_get_user_path.return_value = user_config_path

        # Mock find_resource to return specific Path mocks
        def side_effect(filename, fallback):
            if filename == "config.user.default.yaml":
                return user_default_path
            return MagicMock(spec=Path)

        mock_find_resource.side_effect = side_effect

        # When calling load(), it should trigger _generate_skeleton
        # We want to verify that user_default_path is passed as source
        ConfigManager.load()

        mock_gen_skeleton.assert_called_once_with(user_config_path, user_default_path)

    @patch("pathlib.Path.mkdir")
    @patch("shutil.copy")
    def test_generate_skeleton_execution(self, mock_copy, mock_mkdir):
        target = MagicMock(spec=Path)
        source = MagicMock(spec=Path)
        source.exists.return_value = True

        ConfigManager._generate_skeleton(target, source)

        target.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_copy.assert_called_once_with(source, target)
