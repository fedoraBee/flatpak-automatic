import json
import logging
from datetime import datetime
from flatpak_automatic.logging_utils import JSONFormatter, ANSIFormatter


def test_json_formatter_basic() -> None:
    """Verify that JSONFormatter produces valid JSON with expected keys."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=None,
        exc_info=None,
    )

    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert data["message"] == "Test message"
    assert data["level"] == "INFO"
    assert data["logger"] == "test_logger"
    # Verify timestamp is ISO format
    assert datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))


def test_json_formatter_exception() -> None:
    """Verify that JSONFormatter includes exception info when available."""
    formatter = JSONFormatter()
    try:
        raise ValueError("Boom")
    except ValueError:
        import sys

        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="An error occurred",
            args=None,
            exc_info=sys.exc_info(),
        )

    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert "exception" in data
    assert "ValueError: Boom" in data["exception"]


def test_ansi_formatter_colors() -> None:
    """Verify that ANSIFormatter applies correct color codes based on level."""
    formatter = ANSIFormatter()

    # INFO -> Cyan (\033[36m)
    info_record = logging.LogRecord(
        "test", logging.INFO, "test.py", 1, "msg", None, None
    )
    assert "\033[36m" in formatter.format(info_record)

    # WARNING -> Yellow (\033[33m)
    warn_record = logging.LogRecord(
        "test", logging.WARNING, "test.py", 1, "msg", None, None
    )
    assert "\033[33m" in formatter.format(warn_record)

    # ERROR -> Red (\033[31m)
    err_record = logging.LogRecord(
        "test", logging.ERROR, "test.py", 1, "msg", None, None
    )
    assert "\033[31m" in formatter.format(err_record)

    # Reset code should be present
    assert "\033[0m" in formatter.format(info_record)
