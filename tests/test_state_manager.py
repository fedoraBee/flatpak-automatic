from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from flatpak_automatic.config import StateManager


class TestStateManager:
    @patch("flatpak_automatic.config.STATE_FILE", "/tmp/system_state.json")  # nosec
    @patch("flatpak_automatic.config.USER_STATE_FILE", "/tmp/user_state.json")  # nosec
    def test_get_state_path(self) -> None:
        assert StateManager.get_state_path(user_scope=False) == Path(
            "/tmp/system_state.json"  # nosec
        )
        assert StateManager.get_state_path(user_scope=True) == Path(
            "/tmp/user_state.json"  # nosec
        )

    @patch("pathlib.Path.exists", return_value=True)
    @patch(
        "pathlib.Path.open",
        new_callable=mock_open,
        read_data='{"last_try": "2023-01-01"}',
    )
    def test_load_success(self, mock_file: MagicMock, mock_exists: MagicMock) -> None:
        state = StateManager.load()
        assert state["last_try"] == "2023-01-01"

    @patch("pathlib.Path.exists", return_value=True)
    def test_load_corrupted(self, mock_exists: MagicMock) -> None:
        with patch("pathlib.Path.open", mock_open(read_data="invalid json")):
            state = StateManager.load()
            assert state["last_try"] == "Never"

    @patch("pathlib.Path.exists", return_value=True)
    def test_load_permission_error(self, mock_exists: MagicMock) -> None:
        m = mock_open()
        m.side_effect = PermissionError("Denied")
        with patch("pathlib.Path.open", m):
            state = StateManager.load()
            assert state["last_try"] == "Never"

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.open", new_callable=mock_open)
    def test_save_success(self, mock_file: MagicMock, mock_mkdir: MagicMock) -> None:
        state = {"last_try": "now"}
        StateManager.save(state)
        mock_mkdir.assert_called_once()
        mock_file().write.assert_called()

    @patch("pathlib.Path.mkdir")
    def test_save_error(self, mock_mkdir: MagicMock) -> None:
        mock_mkdir.side_effect = Exception("Write error")
        # Should not raise but log error
        StateManager.save({"a": 1})
