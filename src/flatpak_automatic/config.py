import os
import json
import shutil
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, cast

# Import file path constants from sibling modules
from .logging_utils import STATE_FILE, USER_STATE_FILE
from .constants import CONFIG_FILE


class StateManager:
    """Handles persistence of the application's runtime state (last run times, etc.)."""

    @staticmethod
    def get_state_path(user_scope: bool = False) -> Path:
        """Get the path to the state file based on the execution scope."""
        path_str = USER_STATE_FILE if user_scope else STATE_FILE
        return Path(path_str)

    @staticmethod
    def load(user_scope: bool = False) -> Dict[str, Any]:
        """Load state from disk, falling back to defaults if missing or corrupted."""
        path = StateManager.get_state_path(user_scope)
        try:
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    return cast(Dict[str, Any], json.load(f))
        except (json.JSONDecodeError, PermissionError) as e:
            logging.warning(f"Could not load state from {path}: {e}")

        return {"last_try": "Never", "last_success": "Never"}

    @staticmethod
    def save(state: Dict[str, Any], user_scope: bool = False) -> None:
        """Persist state to disk, creating parent directories if necessary."""
        path = StateManager.get_state_path(user_scope)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                json.dump(state, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save state to {path}: {e}")


class ConfigManager:
    """Manages multi-layered configuration loading with XDG support and skeleton generation."""

    @staticmethod
    def get_user_config_path() -> Path:
        """Determine the XDG-compliant path for user configuration (~/.config/flatpak-automatic/config.yaml)."""
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            base = Path(xdg_config_home)
        else:
            base = Path.home() / ".config"
        return base / "flatpak-automatic" / "config.yaml"

    @staticmethod
    def _find_resource(filename: str, fallback_path: str) -> Path:
        """Locate a configuration resource in development or production environments."""
        # 1. Development: Check relative to package source (../../config/)
        dev_path = Path(__file__).resolve().parent.parent.parent / "config" / filename
        if dev_path.exists():
            return dev_path

        # 2. Production: Use the system-wide fallback path
        return Path(fallback_path)

    @staticmethod
    def load() -> Dict[str, Any]:
        """
        Load configuration using a Dual Default strategy.
        1. Load packaged system defaults (default for root, user for standard user).
        2. If root: Return defaults.
        3. If non-root: Auto-generate skeleton (if missing) and merge user overrides.
        """
        is_root = os.geteuid() == 0

        # Identify source paths for defaults and examples
        if is_root:
            default_filename = "config.default.yaml"
            default_fallback = CONFIG_FILE
        else:
            default_filename = "config.user.default.yaml"
            default_fallback = "/etc/flatpak-automatic/config.user.yaml"

        system_default_path = ConfigManager._find_resource(
            default_filename, default_fallback
        )

        # Layer 1: Base Defaults
        config: Dict[str, Any] = {}

        if system_default_path.exists():
            try:
                with system_default_path.open("r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}
            except (yaml.YAMLError, PermissionError) as e:
                logging.error(
                    f"Failed to load system defaults from {system_default_path}: {e}"
                )
        else:
            logging.debug(
                f"System default configuration not found at {system_default_path}"
            )

        # Root users use the system configuration exclusively
        if is_root:
            return config

        # Layer 2: User-specific Override (Non-root)
        user_config_path = ConfigManager.get_user_config_path()

        # Skeleton Mechanism: Create config from user defaults if it doesn't exist
        if not user_config_path.exists():
            ConfigManager._generate_skeleton(user_config_path, system_default_path)

        # Merge user override on top of system defaults
        if user_config_path.exists():
            try:
                logging.info(
                    f"Detected user-override configuration: {user_config_path}"
                )
                with user_config_path.open("r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}
                config = ConfigManager.deep_merge(config, user_config)
            except (yaml.YAMLError, PermissionError) as e:
                logging.error(
                    f"Failed to parse user configuration at {user_config_path}: {e}"
                )

        return config

    @staticmethod
    def _generate_skeleton(target_path: Path, source_path: Path) -> None:
        """Create directory structure and copy example config to user's XDG path."""
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if source_path.exists():
                shutil.copy(source_path, target_path)
                logging.info(f"Skeleton configuration auto-generated at {target_path}")
            else:
                logging.warning(
                    f"Skeleton source {source_path} not found. Skipping auto-generation."
                )
        except (PermissionError, OSError) as e:
            logging.warning(f"Could not create user configuration skeleton: {e}")

    @staticmethod
    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge dictionaries; override values take precedence over base."""
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                # Avoid recursion if they are the same object to prevent infinite loops
                if base[key] is not value:
                    ConfigManager.deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    @staticmethod
    def verify_policy(policy_key: str) -> bool:
        """Helper to check if a specific notification policy is enabled."""
        config = ConfigManager.load()
        return bool(config.get("notification_policy", {}).get(policy_key, False))
