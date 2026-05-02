import os
import json
import logging
import yaml
from typing import Dict, Any
from .logging_utils import STATE_FILE, USER_STATE_FILE
from .constants import CONFIG_FILE


class StateManager:
    @staticmethod
    def get_state_path(user_scope: bool = False) -> str:
        return user_scope and USER_STATE_FILE or STATE_FILE

    @staticmethod
    def load(user_scope: bool = False) -> Dict[str, Any]:
        try:
            with open(StateManager.get_state_path(user_scope), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"last_try": "Never", "last_success": "Never"}

    @staticmethod
    def save(state: Dict[str, Any], user_scope: bool = False) -> None:
        try:
            path = StateManager.get_state_path(user_scope)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(state, f)
        except Exception as e:
            logging.warning(f"Failed to save state: {e}")


class ConfigManager:
    @staticmethod
    def load() -> Dict[str, Any]:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logging.error(f"Failed to parse YAML config: {e}")
        return {}

    @staticmethod
    def verify_policy(policy_key: str) -> bool:
        config = ConfigManager.load()
        return bool(config.get("notification_policy", {}).get(policy_key, False))
