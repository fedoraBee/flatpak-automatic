import os
import logging
import subprocess
import shutil
from ..config import ConfigManager
from ..constants import ICON_PATH


class DesktopNotifier:
    @classmethod
    def is_available(cls) -> bool:
        return shutil.which("notify-send") is not None

    def __init__(self) -> None:
        self.enabled = ConfigManager.verify_policy("desktop")

    def send_notification(self, title: str, body: str) -> None:
        if not self.enabled:
            logging.info("Desktop notifications disabled by global policy. Skipping.")
            return

        current_uid = os.getuid()

        try:
            # We use list-sessions to find active graphical sessions with a seat attached.
            # This avoids sending notifications to background or service sessions.
            sessions_out = subprocess.run(
                ["loginctl", "list-sessions", "--no-legend"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout

            for line in sessions_out.strip().split("\n"):
                if not line:
                    continue
                parts = line.split()
                # loginctl list-sessions columns:
                # 0:SESSION, 1:UID, 2:USER, 3:SEAT, 4:LEADER, 5:CLASS, 6:TTY, ...
                if len(parts) < 6:
                    continue

                uid_str, user, seat, user_class = parts[1], parts[2], parts[3], parts[5]

                try:
                    uid = int(uid_str)
                except ValueError:
                    continue

                # Filter: must be a real user session and must have a seat attached (local display)
                if user_class != "user" or seat == "-":
                    continue

                # If running rootless, only notify the current user
                if current_uid != 0 and uid != current_uid:
                    continue

                # Prefix commands with sudo if running as root to execute as the target user
                cmd_prefix = ["sudo", "-u", user] if current_uid == 0 else []

                env_out = subprocess.run(
                    cmd_prefix + ["systemctl", "--user", "show-environment"],
                    capture_output=True,
                    text=True,
                    check=False,
                ).stdout

                env_dict = {}
                for el in env_out.splitlines():
                    if "=" in el:
                        k, v = el.split("=", 1)
                        env_dict[k] = v

                bus_path = f"/run/user/{uid}/bus"
                if (
                    "WAYLAND_DISPLAY" not in env_dict
                    and "DISPLAY" not in env_dict
                    and not os.path.exists(bus_path)
                ):
                    logging.info(
                        f"Skipping desktop notification for {user}: Headless session detected (No active display or D-Bus session)."
                    )
                    continue

                bus_address = env_dict.get(
                    "DBUS_SESSION_BUS_ADDRESS", f"unix:path=/run/user/{uid}/bus"
                )
                runtime_dir = env_dict.get("XDG_RUNTIME_DIR", f"/run/user/{uid}")

                # Use file:// URI for absolute paths to ensure compatibility with all notification daemons
                icon_param = ICON_PATH
                hints = []
                if os.path.isabs(ICON_PATH):
                    icon_param = f"file://{ICON_PATH}"
                    hints = ["-h", f"string:image-path:{ICON_PATH}"]

                subprocess.run(
                    cmd_prefix
                    + [
                        "env",
                        f"DBUS_SESSION_BUS_ADDRESS={bus_address}",
                        f"XDG_RUNTIME_DIR={runtime_dir}",
                        "notify-send",
                        "-a",
                        "Flatpak Automatic",
                        "-i",
                        icon_param,
                    ]
                    + hints
                    + [title, body],
                    check=False,
                )
            logging.info("Desktop UI notification dispatched to active sessions.")
        except Exception as e:
            logging.error(f"Failed to dispatch desktop UI notification: {e}")
