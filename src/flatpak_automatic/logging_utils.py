import os
import sys
import logging
import json
from datetime import datetime, timezone

STATE_FILE = "/var/cache/flatpak-automatic/state.json"
USER_STATE_FILE = os.path.expanduser("~/.cache/flatpak-automatic/state.json")


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


class ANSIFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        colors = {"INFO": "\033[36m", "WARNING": "\033[33m", "ERROR": "\033[31m"}
        color = colors.get(record.levelname, "")
        reset = "\033[0m"
        return f"{color}[{record.levelname}]{reset} {record.getMessage()}"


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    if not sys.stdout.isatty():
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(ANSIFormatter())
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
