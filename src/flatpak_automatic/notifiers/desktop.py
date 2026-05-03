import os
import logging
import subprocess
from ..config import ConfigManager
from ..constants import ICON_PATH, BANNER_PATH


class DesktopNotifier:
    def __init__(self) -> None:
        self.enabled = ConfigManager.verify_policy("desktop")

    def send_notification(self, title: str, body: str) -> None:
        if not self.enabled:
            logging.info("Desktop notifications disabled by global policy. Skipping.")
            return
        try:
            users_out = subprocess.run(
                ["loginctl", "list-users", "--no-legend"],
                capture_output=True,
                text=True,
            ).stdout
            for line in users_out.strip().split("\n"):
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    uid, user = parts[0], parts[1]
                    env_out = subprocess.run(
                        ["sudo", "-u", user, "systemctl", "--user", "show-environment"],
                        capture_output=True,
                        text=True,
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

                    bus_address = f"unix:path=/run/user/{uid}/bus"
                    runtime_dir = env_dict.get("XDG_RUNTIME_DIR", f"/run/user/{uid}")

                    # Use file:// URI for absolute paths to ensure compatibility with all notification daemons
                    icon_param = ICON_PATH
                    if os.path.isabs(icon_param):
                        icon_param = f"file://{icon_param}"

                    # Use the high-resolution banner for the notification body image (hints)
                    hints = []
                    if os.path.isabs(BANNER_PATH):
                        hints = ["-h", f"string:image-path:{BANNER_PATH}"]

                    subprocess.run(
                        [
                            "sudo",
                            "-u",
                            user,
                            "env",
                            f"DBUS_SESSION_BUS_ADDRESS={bus_address}",
                            f"XDG_RUNTIME_DIR={runtime_dir}",
                            "notify-send",
                            "-a",
                            "Flatpak Automatic",
                            "-n",
                            icon_param,
                        ]
                        + hints
                        + [title, body],
                        check=False,
                    )
            logging.info("Desktop UI notification dispatched to active sessions.")
        except Exception as e:
            logging.error(f"Failed to dispatch desktop UI notification: {e}")
