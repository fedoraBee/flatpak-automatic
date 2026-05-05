from unittest.mock import patch, MagicMock
from flatpak_automatic.constants import find_brand_icon


class TestConstants:
    @patch("os.path.exists")
    def test_find_brand_icon_system(self, mock_exists: MagicMock) -> None:
        def side_effect(path: str) -> bool:
            if "/usr/share/icons" in path:
                return True
            return False

        mock_exists.side_effect = side_effect
        assert "/usr/share/icons" in find_brand_icon()

    @patch("os.path.exists")
    def test_find_brand_icon_fallback(self, mock_exists: MagicMock) -> None:
        mock_exists.return_value = False
        assert find_brand_icon() == "software-update-available"
