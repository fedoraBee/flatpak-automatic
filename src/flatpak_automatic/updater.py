import subprocess
from typing import List, Optional


class FlatpakUpdater:
    def __init__(self, excludes: Optional[List[str]] = None) -> None:
        self.updates_available: bool = False
        self.update_log: str = ""
        self.update_count: int = 0
        self.excludes = excludes or []

    def check_updates(self) -> bool:
        cmd = [
            "flatpak",
            "remote-ls",
            "--updates",
            "--columns=application,branch,version",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout.strip() != "":
            lines = result.stdout.strip().split("\n")

            filtered_lines = []
            for line in lines:
                line = line.strip()
                if not line or "Application ID" in line:
                    continue

                # Basic validation: Flatpak App IDs usually have at least two dots
                # and don't contain spaces in the ID itself (the first column).
                parts = line.split()
                if not parts:
                    continue

                app_id = parts[0]
                # Filter out obvious non-AppID lines (like "Looking for updates...")
                if "." not in app_id or app_id.startswith(" "):
                    continue

                if app_id not in self.excludes:
                    filtered_lines.append(line)

            if filtered_lines:
                self.updates_available = True
                self.update_log = "\n".join(filtered_lines)
                self.update_count = len(filtered_lines)
        return self.updates_available

    def apply_updates(self) -> bool:
        cmd = ["flatpak", "update", "-y", "--noninteractive"]
        for exclude in self.excludes:
            cmd.extend(["--exclude", exclude])

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.update_log += (
            f"\n\n--- Flatpak Execution Log ---\n{result.stdout}\n{result.stderr}"
        )
        return result.returncode == 0
