from unittest.mock import patch, mock_open, MagicMock
from flatpak_automatic.notifiers.templates import TemplateRenderer


class TestTemplateRenderer:
    @patch("os.path.exists")
    def test_render_missing_template(self, mock_exists: MagicMock) -> None:
        mock_exists.return_value = False
        context = {"BODY": "Fallback Body"}
        result = TemplateRenderer.render("missing.md", context)
        assert result == "Fallback Body"

    @patch("os.path.exists")
    def test_render_success(self, mock_exists: MagicMock) -> None:
        mock_exists.return_value = True
        template_content = "Hello ${NAME}!"
        context = {"NAME": "World"}

        with patch("builtins.open", mock_open(read_data=template_content)):
            result = TemplateRenderer.render("hello.md", context)
            assert result == "Hello World!"

    @patch("os.path.exists")
    def test_render_safe_substitute(self, mock_exists: MagicMock) -> None:
        mock_exists.return_value = True
        template_content = "Hello ${NAME} and ${MISSING}!"
        context = {"NAME": "World"}

        with patch("builtins.open", mock_open(read_data=template_content)):
            result = TemplateRenderer.render("hello.md", context)
            assert result == "Hello World and ${MISSING}!"
