import logging
import os
import socket
import subprocess
import yaml
from datetime import datetime
from typing import Dict, Any

from .config import StateManager
from .updater import FlatpakUpdater
from .snapper import SnapperManager
from .notifiers import NotificationRouter
from .constants import Colors


class AutomationEngine:
    def __init__(self, config: Dict[str, Any], state: Dict[str, Any]) -> None:
        self.config = config
        self.state = state
        self.user_scope = os.geteuid() != 0
        self.flatpak_scope = ["--user"] if self.user_scope else ["--system"]

    def validate_config(self) -> None:
        print(
            f"{Colors.BOLD}{Colors.OKCYAN}⚙️  Validating Configuration...{Colors.ENDC}"
        )
        if self.config:
            print(f"{Colors.OKGREEN}✅ Configuration is valid.{Colors.ENDC}")
            dump = yaml.dump(self.config, default_flow_style=False, sort_keys=False)
            indented_dump = dump.replace("\n", "\n   ")
            print(f"   {indented_dump}")
        else:
            print(f"{Colors.WARNING}⚠️ Configuration is empty or invalid.{Colors.ENDC}")

    def dispatch_test_notifications(self) -> None:
        logging.info("Executing Test Notification dispatch...")
        router = NotificationRouter(self.config)
        test_body = (
            "org.mozilla.firefox 125.0.1\n"
            "org.gnome.Calculator 46.0\n"
            "org.freedesktop.Platform 23.08"
        )
        router.dispatch_all(
            "[TEST] Flatpak Automatic",
            test_body,
            True,
            update_count=3,
        )

    def print_status_overview(self) -> None:
        from .notifiers import APPRISE_AVAILABLE, MailNotifier

        print(
            f"{Colors.HEADER}{Colors.BOLD}[ System Status & Monitoring Overview ]{Colors.ENDC}"
        )
        print(f"\n{Colors.OKCYAN}📊 Execution State:{Colors.ENDC}")
        print(f"   Last Update Try: {self.state.get('last_try', 'Never')}")
        print(f"   Last Success:    {self.state.get('last_success', 'Never')}")

        # Timer Status Check
        print(f"\n{Colors.OKCYAN}⏰ Automation Timer:{Colors.ENDC}")
        try:
            # Check both 'is-enabled' and 'is-active' for a complete picture
            is_enabled = (
                subprocess.run(
                    ["systemctl", "is-enabled", "flatpak-automatic.timer"]
                    + self.flatpak_scope,
                    capture_output=True,
                    text=True,
                ).returncode
                == 0
            )
            is_active = (
                subprocess.run(
                    ["systemctl", "is-active", "flatpak-automatic.timer"]
                    + self.flatpak_scope,
                    capture_output=True,
                    text=True,
                ).returncode
                == 0
            )

            if is_active:
                status_str = f"{Colors.OKGREEN}Active & Running{Colors.ENDC}"
                icon = "🟢"
            elif is_enabled:
                status_str = f"{Colors.OKCYAN}Enabled but Idle{Colors.ENDC}"
                icon = "🟡"
            else:
                status_str = f"{Colors.WARNING}Disabled / Inactive{Colors.ENDC}"
                icon = "⚪"

            print(f"   Status: {icon} {status_str}")

            if is_active:
                # Show next run time if active
                next_run = subprocess.run(
                    [
                        "systemctl",
                        "show",
                        "flatpak-automatic.timer",
                        "--property=NextElapseUSecRealtime",
                        "--value",
                    ]
                    + self.flatpak_scope,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                if next_run and next_run != "0":
                    print(f"   Next Run: {next_run}")

        except Exception:
            print(
                f"   Status: {Colors.WARNING}❓ Unknown (Service not found){Colors.ENDC}"
            )

        # Notification Availability
        print(f"\n{Colors.OKCYAN}🔔 Notification Services:{Colors.ENDC}")
        apprise_status = (
            f"{Colors.OKGREEN}Available{Colors.ENDC}"
            if APPRISE_AVAILABLE
            else f"{Colors.WARNING}Not installed{Colors.ENDC}"
        )
        apprise_icon = "🟢" if APPRISE_AVAILABLE else "⚪"
        print(f"   Apprise Availability: {apprise_icon} {apprise_status}")

        mail_avail = MailNotifier.is_available()
        mail_status = (
            f"{Colors.OKGREEN}Available{Colors.ENDC}"
            if mail_avail
            else f"{Colors.WARNING}Client missing{Colors.ENDC}"
        )
        mail_icon = "🟢" if mail_avail else "⚪"
        print(f"   Mail Availability:    {mail_icon} {mail_status}")

        print(f"\n{Colors.OKCYAN}📦 Installed Flatpaks:{Colors.ENDC}")
        result = subprocess.run(
            ["flatpak", "list", "--app", "--columns=application,version"],
            capture_output=True,
            text=True,
        )
        for line in result.stdout.strip().split("\n"):
            if line:
                print(f"   {line}")
        print()  # Trailing empty line

    def run(
        self, dry_run: bool = False, force: bool = False, desktop_mode: bool = False
    ) -> bool:
        auto_update = self.config.get("auto_update", True)
        if not auto_update and not force:
            logging.info("Automatic updates are disabled via configuration.")
            return True

        self.state["last_try"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        StateManager.save(self.state, self.user_scope)

        updater = FlatpakUpdater(excludes=self.config.get("exclusions", []))
        if not updater.check_updates():
            logging.info("No Flatpak updates available.")
            return True

        logging.info("Updates found. Interfacing with System Services...")

        if dry_run:
            logging.info(
                "[DRY-RUN] Updates found, but dry-run is active. Skipping snapshots and applying updates."
            )
            logging.info(f"[DRY-RUN] Would have updated:\n{updater.update_log}")
            return True

        snap_cfg = self.config.get("snapshots", {})
        if snap_cfg.get("enabled", True):
            snapper = SnapperManager(config=snap_cfg.get("snapper_config", "root"))
            desc_cfg = snap_cfg.get("snapper_descriptions", {})
            snapper.create_timeline_snapshot(
                desc_cfg.get("pre", "flatpak-automatic-pre")
            )

        logging.info("Applying Flatpak updates...")
        success: bool = updater.apply_updates()

        if success:
            self.state["last_success"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            StateManager.save(self.state, self.user_scope)
            if snap_cfg.get("enabled", True):
                if "snapper" in locals():
                    desc_cfg = snap_cfg.get("snapper_descriptions", {})
                    snapper.create_timeline_snapshot(
                        desc_cfg.get("post", "flatpak-automatic-post")
                    )

        notify_type = self.config.get("auto_notify", "always").lower()
        trigger_notify = False

        if notify_type in ("always", "on-change"):
            trigger_notify = True
        elif notify_type == "on-failure" and not success:
            trigger_notify = True

        if trigger_notify:
            subject_prefix = "[SUCCESS]" if success else "[FAILED]"
            title = f"{subject_prefix} Flatpak Updates - {socket.gethostname()}"
            router = NotificationRouter(self.config)
            router.dispatch_all(
                title, updater.update_log, success, updater.update_count
            )

        return success
