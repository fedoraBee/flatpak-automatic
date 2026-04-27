#!/usr/bin/env python3
# Version: 1.5.0
import os
import sys
import subprocess
import socket
import logging
import json
import shlex
import argparse
from datetime import datetime, timezone
from typing import Optional, Dict


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


# Configure native Systemd logging (syslog/journald ready)
class ANSIFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        colors = {"INFO": "\033[36m", "WARNING": "\033[33m", "ERROR": "\033[31m"}
        color = colors.get(record.levelname, "")
        reset = "\033[0m"
        return f"{color}[{record.levelname}]{reset} {record.getMessage()}"


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

try:
    import dbus  # type: ignore

    DBUS_AVAILABLE = True
except ImportError:
    DBUS_AVAILABLE = False
    logging.warning(
        "python3-dbus is not installed. Snapper snapshots will be bypassed."
    )

try:
    import apprise  # type: ignore

    APPRISE_AVAILABLE = True
except ImportError:
    APPRISE_AVAILABLE = False
    logging.warning(
        "apprise is not installed. Universal notifications will be bypassed."
    )


class SnapperManager:
    def __init__(self, config: str = "root") -> None:
        self.config: str = config
        self.interface: Optional[dbus.Interface] = None
        if DBUS_AVAILABLE:
            try:
                self.bus: dbus.SystemBus = dbus.SystemBus()
                self.proxy: dbus.proxies.ProxyObject = self.bus.get_object(
                    "org.opensuse.Snapper", "/org/opensuse/Snapper"
                )
                self.interface = dbus.Interface(self.proxy, "org.opensuse.Snapper")
            except Exception as e:
                # Graceful degradation for systems lacking Snapper
                logging.info(
                    f"Notice: Snapper DBus unavailable. Bypassing snapshots gracefully. ({type(e).__name__})"
                )
                self.interface = None

    def create_timeline_snapshot(
        self, description: str = "Pre-Flatpak Update Automation"
    ) -> int:
        if not self.interface:
            return -1
        try:
            empty_dict: dbus.Dictionary = dbus.Dictionary({}, signature="ss")
            snapshot_id: int = int(
                self.interface.CreateSingleSnapshot(
                    self.config, "timeline", description, empty_dict
                )
            )
            logging.info(f"Created Snapper timeline snapshot: #{snapshot_id}")
            return snapshot_id
        except Exception as e:
            logging.error(f"Snapper DBus execution error: {e}")
            return -1


class FlatpakUpdater:
    def __init__(self, excludes: str = "") -> None:
        self.updates_available: bool = False
        self.update_log: str = ""
        self.excludes = [x.strip() for x in excludes.split(",") if x.strip()]

    def check_updates(self) -> bool:
        cmd = ["flatpak", "update", "--dry-run", "--columns=application,branch,version"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if "Nothing to do" not in result.stdout and result.stdout.strip() != "":
            lines = result.stdout.strip().split("\n")
            filtered_lines = []
            for line in lines:
                app_id = line.split("\t")[0] if "\t" in line else line.split()[0]
                if app_id not in self.excludes and line.strip() != "":
                    filtered_lines.append(line)

            if filtered_lines:
                self.updates_available = True
                self.update_log = "\n".join(filtered_lines)
        return self.updates_available

    def apply_updates(self) -> bool:
        cmd = ["flatpak", "update", "-y", "--noninteractive"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.update_log += (
            f"\n\n--- Flatpak Execution Log ---\n{result.stdout}\n{result.stderr}"
        )
        return result.returncode == 0


class DesktopNotifier:
    def __init__(self, enabled: str = "no") -> None:
        self.enabled = enabled.lower() in ("yes", "true", "1")

    def send_notification(
        self, title: str, body: str, icon: str = "software-update-available"
    ) -> None:
        if not self.enabled:
            return
        try:
            # Safely traverse session boundary to find active graphical user
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

                    # Fetch user's systemd environment to accurately detect graphical sessions
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

                    if "WAYLAND_DISPLAY" not in env_dict and "DISPLAY" not in env_dict:
                        logging.info(
                            f"Skipping desktop notification for {user}: Headless session detected (No WAYLAND_DISPLAY/DISPLAY)."
                        )
                        continue

                    bus_address = f"unix:path=/run/user/{uid}/bus"
                    env = os.environ.copy()
                    env["DBUS_SESSION_BUS_ADDRESS"] = bus_address
                    if "WAYLAND_DISPLAY" in env_dict:
                        env["WAYLAND_DISPLAY"] = env_dict["WAYLAND_DISPLAY"]
                    if "DISPLAY" in env_dict:
                        env["DISPLAY"] = env_dict["DISPLAY"]
                    if "XDG_RUNTIME_DIR" in env_dict:
                        env["XDG_RUNTIME_DIR"] = env_dict["XDG_RUNTIME_DIR"]

                    subprocess.run(
                        [
                            "sudo",
                            "-u",
                            user,
                            "DBUS_SESSION_BUS_ADDRESS=" + bus_address,
                            "notify-send",
                            "-a",
                            "Flatpak Automatic",
                            "-i",
                            icon,
                            title,
                            body,
                        ],
                        env=env,
                        check=False,
                    )
            logging.info("Desktop UI notification dispatched to active sessions.")
        except Exception as e:
            logging.error(f"Failed to dispatch desktop UI notification: {e}")


class AppriseNotifier:
    def __init__(self, urls: str) -> None:
        self.urls = [url.strip() for url in urls.split(",") if url.strip()]

    def send_notification(self, title: str, body: str) -> None:
        if not APPRISE_AVAILABLE or not self.urls:
            logging.warning(
                "Skipping Apprise notification: Apprise not available or no URLs configured."
            )
            return
        try:
            apobj = apprise.Apprise()
            for url in self.urls:
                apobj.add(url)
            apobj.notify(body=body, title=title)
            logging.info(
                f"Apprise notification dispatched to {len(self.urls)} endpoints."
            )
        except Exception as e:
            logging.error(f"Failed to dispatch Apprise notification: {e}")


class WebhookNotifier:
    def __init__(self, urls: str, secret: str = "") -> None:
        self.urls = [url.strip() for url in urls.split(",") if url.strip()]
        self.secret = secret.strip()

    def send_notification(self, title: str, body: str) -> None:
        if not self.urls:
            return
        import urllib.request
        import urllib.error
        import json
        import hmac
        import hashlib

        payload = json.dumps({"title": title, "body": body}).encode("utf-8")

        for url in self.urls:
            try:
                req = urllib.request.Request(url, data=payload, method="POST")
                req.add_header("Content-Type", "application/json")

                if self.secret:
                    signature = hmac.new(
                        self.secret.encode("utf-8"), payload, hashlib.sha256
                    ).hexdigest()
                    req.add_header("X-Hub-Signature-256", f"sha256={signature}")

                with urllib.request.urlopen(req, timeout=10) as response:
                    logging.info(
                        f"Webhook dispatched to {url} (Status: {response.status})"
                    )
            except Exception as e:
                logging.error(f"Failed to dispatch webhook to {url}: {e}")


class MailNotifier:
    def __init__(self, to_address: str, from_address: str) -> None:
        self.to_address: str = to_address
        self.from_address: str = from_address
        self.mail_cmd: Optional[str] = self._find_mail_cmd()

    def _find_mail_cmd(self) -> Optional[str]:
        for cmd in ["s-nail", "mailx", "mailutils", "mail"]:
            if (
                subprocess.run(["command", "-v", cmd], capture_output=True).returncode
                == 0
            ):
                return cmd
        return None

    def send_mail(self, subject: str, body: str) -> None:
        if not self.mail_cmd or not self.to_address:
            logging.warning(
                "Skipping mail notification: Mail client or recipient missing."
            )
            return
        try:
            process = subprocess.Popen(
                [
                    self.mail_cmd,
                    "-s",
                    subject,
                    "-r",
                    self.from_address,
                    self.to_address,
                ],
                stdin=subprocess.PIPE,
            )
            process.communicate(input=body.encode("utf-8"))
            logging.info(
                f"Notification dispatched to {self.to_address} via {self.mail_cmd}."
            )
        except Exception as e:
            logging.error(f"Failed to dispatch mail: {e}")


def load_sysconfig() -> Dict[str, str]:
    config: Dict[str, str] = {}
    paths = ["/etc/sysconfig/flatpak-automatic", "/etc/default/flatpak-automatic"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.replace("export ", "").strip()
                        v = v.strip()
                        try:
                            parsed = shlex.split(v)
                            config[k] = parsed[0] if parsed else ""
                        except ValueError:
                            config[k] = v.strip("\"'")
            break
    return config


class BrandedArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        banner = (
            "\033[1m\033[38;2;0;155;155m  ___ _       _               _    \n"
            "\033[38;2;42;123;202m | __| |__ _ | |_ _ __  __ _ | |__ \n"
            "\033[38;2;138;58;185m | _|| / _` || ._| '_ \\/ _` || / / \n"
            "\033[38;2;193;14;140m |_| |_\\__,_|\\__|| .__/\\__,_||_\\_\\\n"
            "                 |_| AUTOMATIC\033[0m\n"
        )
        if file is None:
            import sys

            file = sys.stdout
        file.write(banner + "\n")
        super().print_help(file)


def main() -> None:

    parser = BrandedArgumentParser(
        description="Flatpak Automatic - Enterprise Update Automation"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Simulate the update process without applying changes.",
    )
    parser.add_argument(
        "-t",
        "--test-notify",
        action="store_true",
        help="Send a test notification to configured endpoints and exit.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force the update process, ignoring safeguards.",
    )
    parser.add_argument(
        "-s",
        "--status",
        action="store_true",
        help="Display system monitoring overview and exit.",
    )
    parser.add_argument(
        "-l",
        "--history",
        action="store_true",
        help="Display recent update history from journalctl and exit.",
    )
    parser.add_argument(
        "-a",
        "--apply-schedule",
        action="store_true",
        help="Apply systemd timer overrides based on config settings.",
    )

    parser.add_argument(
        "-u",
        "--setup",
        action="store_true",
        help="Launch the interactive configuration wizard to generate sysconfig.",
    )
    args = parser.parse_args()

    if sys.stdout.isatty():
        print(
            "\033[1m\033[38;2;0;155;155m  ___ _       _               _    \n"
            "\033[38;2;42;123;202m | __| |__ _ | |_ _ __  __ _ | |__ \n"
            "\033[38;2;138;58;185m | _|| / _` || ._| '_ \\/ _` || / / \n"
            "\033[38;2;193;14;140m |_| |_\\__,_|\\__|| .__/\\__,_||_\\_\\\n"
            "                 |_| AUTOMATIC\033[0m\n"
        )

    config: Dict[str, str] = load_sysconfig()

    if os.geteuid() != 0:
        print(
            "\033[31m❌ Error: This script requires root privileges. Please run with sudo.\033[0m"
        )
        sys.exit(1)

    if args.setup:
        print("\033[1m\033[36m--- Flatpak Automatic Configuration Wizard ---\033[0m")
        print(
            "This interactive wizard will generate /etc/sysconfig/flatpak-automatic\n"
        )

        def ask(prompt_text: str, default_val: str = "") -> str:
            ans = input(
                f"\033[33m? \033[0m{prompt_text} \033[90m[{default_val}]\033[0m: "
            ).strip()
            return ans if ans else default_val

        config_lines = ["# Generated by flatpak-automatic --setup"]

        config_lines.append(
            f'FLATPAK_AUTO_UPDATE="{ask("Enable automatic updates? (yes/no)", "yes")}"'
        )
        config_lines.append(
            f'ENABLE_SNAPSHOTS="{ask("Enable Snapper snapshots? (yes/no)", "yes")}"'
        )
        config_lines.append(
            f'MINIMUM_DELAY_HOURS="{ask("Minimum delay between updates in hours (0 to disable)", "0")}"'
        )
        config_lines.append(
            f'ENABLE_DESKTOP_NOTIFY="{ask("Enable desktop UI notifications? (yes/no)", "yes")}"'
        )

        email_notify = ask("Enable email notifications? (yes/no)", "no")
        config_lines.append(f'ENABLE_EMAIL="{email_notify}"')
        if email_notify.lower() in ("yes", "y", "true", "1"):
            config_lines.append(
                f'EMAIL_TO="{ask("Email Recipient (TO)", "root@localhost")}"'
            )
            config_lines.append(
                f'EMAIL_FROM="{ask("Email Sender (FROM)", "flatpak-automatic@localhost")}"'
            )

        webhooks = ask("Webhook URLs (comma-separated, leave blank to disable)", "")
        if webhooks:
            config_lines.append(f'WEBHOOK_URLS="{webhooks}"')
            secret = ask(
                "Webhook Secret (for HMAC-SHA256 signature, leave blank to skip)", ""
            )
            if secret:
                config_lines.append(f'WEBHOOK_SECRET="{secret}"')

        apprise = ask("Apprise URLs (comma-separated, leave blank to disable)", "")
        if apprise:
            config_lines.append(f'FLATPAK_APPRISE_URLS="{apprise}"')

        sysconfig_dir = "/etc/sysconfig"
        sysconfig_path = os.path.join(sysconfig_dir, "flatpak-automatic")
        try:
            os.makedirs(sysconfig_dir, exist_ok=True)
            with open(sysconfig_path, "w") as sysconf_file:
                sysconf_file.write("\n".join(config_lines) + "\n")
            print(
                f"\n\033[32m✅ Successfully wrote configuration to {sysconfig_path}\033[0m"
            )
        except Exception as e:
            print(f"\n\033[31m❌ Failed to write configuration: {e}\033[0m")

        sys.exit(0)

    if args.apply_schedule:
        schedule = config.get("TIMER_SCHEDULE", "daily")
        delay = config.get("TIMER_DELAY", "1h")
        override_dir = "/etc/systemd/system/flatpak-automatic.timer.d"
        override_file = os.path.join(override_dir, "override.conf")

        try:
            print("\033[1m⚙️  Applying Systemd Timer Override...\033[0m")
            os.makedirs(override_dir, exist_ok=True)
            with open(override_file, "w") as f:
                f.write(
                    f"[Timer]\nOnCalendar=\nOnCalendar={schedule}\nRandomizedDelaySec={delay}\n"
                )
            print(f"  Wrote configuration to: {override_file}")

            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(
                ["systemctl", "restart", "flatpak-automatic.timer"], check=True
            )
            print(
                f"\033[32m✅ Successfully applied schedule: '{schedule}' with a '{delay}' randomization delay.\033[0m"
            )
        except Exception as e:
            print(f"\033[31m❌ Failed to apply systemd schedule: {e}\033[0m")
        sys.exit(0)

    if args.status:
        print("\033[1m[ System Status & Monitoring Overview ]\033[0m")
        print("\n\033[1m⚙️  Configuration (/etc/sysconfig/flatpak-automatic):\033[0m")
        for k, v in config.items():
            print(f"  {k}: {v}")
        print("\n\033[1m📦 Flatpak Status:\033[0m")
        subprocess.run(["flatpak", "list", "--app", "--columns=application,version"])
        sys.exit(0)

    if args.history:
        print("\033[1m[ Recent flatpak-automatic Execution History ]\033[0m")
        subprocess.run(
            ["journalctl", "-u", "flatpak-automatic.service", "-n", "20", "--no-pager"]
        )
        sys.exit(0)

    if args.test_notify:
        logging.info("Executing Test Notification dispatch...")
        mailer = MailNotifier(
            config.get("FLATPAK_MAIL_TO", config.get("EMAIL_TO", "")),
            config.get(
                "FLATPAK_MAIL_FROM",
                config.get("EMAIL_FROM", f"flatpak-automatic@{socket.gethostname()}"),
            ),
        )
        mailer.send_mail(
            "[TEST] Flatpak Automatic",
            "This is a test notification from flatpak-automatic.",
        )
        apprise_urls = config.get("FLATPAK_APPRISE_URLS", "")
        if apprise_urls:
            apprise_notifier = AppriseNotifier(apprise_urls)
            apprise_notifier.send_notification(
                "[TEST] Flatpak Automatic",
                "This is a test notification from flatpak-automatic.",
            )

        webhook_urls = config.get("WEBHOOK_URLS", "")
        if webhook_urls:
            webhook_notifier = WebhookNotifier(
                webhook_urls, config.get("WEBHOOK_SECRET", "")
            )
            webhook_notifier.send_notification(
                "[TEST] Flatpak Automatic",
                "This is a test notification from flatpak-automatic.",
            )
        desktop = DesktopNotifier(
            config.get("ENABLE_DESKTOP_NOTIFY", "yes")
        )  # Force test to yes
        desktop.send_notification(
            "Test Notification", "This is a test notification from flatpak-automatic."
        )
        sys.exit(0)

    auto_update = config.get("FLATPAK_AUTO_UPDATE", "true").lower() == "true"
    if not auto_update and not args.force:
        logging.info("Automatic updates are disabled via configuration.")
        sys.exit(0)

    # Minimum delay check
    delay_hours_str = config.get("MINIMUM_DELAY_HOURS", "0")
    try:
        delay_hours = float(delay_hours_str)
    except ValueError:
        delay_hours = 0.0

    state_dir = "/var/lib/flatpak-automatic"
    state_file = os.path.join(state_dir, ".last_run")

    if (
        delay_hours > 0
        and not args.force
        and not getattr(args, "dry_run", False)
        and not getattr(args, "test_notify", False)
        and not getattr(args, "status", False)
        and not getattr(args, "history", False)
        and not getattr(args, "apply_schedule", False)
    ):
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f:
                    last_run = float(f.read().strip())
                if (datetime.now(timezone.utc).timestamp() - last_run) < (
                    delay_hours * 3600
                ):
                    logging.info(
                        f"Minimum delay of {delay_hours}h has not elapsed. Skipping update. Use --force to override."
                    )
                    sys.exit(0)
            except Exception as e:
                logging.warning(f"Failed to read state file: {e}")

    updater = FlatpakUpdater(excludes=config.get("FLATPAK_EXCLUDES", ""))
    if not updater.check_updates():
        logging.info("No Flatpak updates available.")
        sys.exit(0)

    logging.info("Updates found. Interfacing with System Services...")

    if args.dry_run:
        logging.info(
            "[DRY-RUN] Updates found, but dry-run is active. Skipping snapshots and applying updates."
        )
        logging.info(f"[DRY-RUN] Would have updated:\n{updater.update_log}")
        sys.exit(0)

    if config.get(
        "ENABLE_SNAPSHOTS", config.get("FLATPAK_CREATE_SNAPSHOT", "true")
    ).lower() in ("yes", "true", "1"):
        snapper = SnapperManager(config=config.get("SNAPPER_CONFIG", "root"))
        snapper.create_timeline_snapshot(
            config.get("SNAPPER_DESC_PRE", "flatpak-automatic-pre")
        )

    logging.info("Applying Flatpak updates...")
    success: bool = updater.apply_updates()

    if success and config.get("ENABLE_SNAPSHOTS", "true").lower() in (
        "yes",
        "true",
        "1",
    ):
        if "snapper" in locals():
            snapper.create_timeline_snapshot(
                config.get("SNAPPER_DESC_POST", "flatpak-automatic-post")
            )

    notify_type: str = config.get(
        "FLATPAK_AUTO_NOTIFY", config.get("ENABLE_EMAIL", "yes")
    ).lower()
    trigger_notify: bool = False

    if notify_type in ("always", "on-update", "yes", "true", "1"):
        trigger_notify = True
    elif notify_type == "on-error" and not success:
        trigger_notify = True

    if trigger_notify:
        subject_prefix: str = "[SUCCESS]" if success else "[FAILED]"
        title = f"{subject_prefix} Flatpak Updates - {socket.gethostname()}"
        mailer = MailNotifier(
            config.get("FLATPAK_MAIL_TO", config.get("EMAIL_TO", "")),
            config.get(
                "FLATPAK_MAIL_FROM",
                config.get("EMAIL_FROM", f"flatpak-automatic@{socket.gethostname()}"),
            ),
        )
        mailer.send_mail(title, updater.update_log)

        apprise_urls = config.get("FLATPAK_APPRISE_URLS", "")
        if apprise_urls:
            apprise_notifier = AppriseNotifier(apprise_urls)
            apprise_notifier.send_notification(title, updater.update_log)

        webhook_urls = config.get("WEBHOOK_URLS", "")
        if webhook_urls:
            webhook_notifier = WebhookNotifier(
                webhook_urls, config.get("WEBHOOK_SECRET", "")
            )
            webhook_notifier.send_notification(title, updater.update_log)

        desktop = DesktopNotifier(config.get("ENABLE_DESKTOP_NOTIFY", "no"))
        desktop.send_notification(title, updater.update_log)

    if (
        not getattr(args, "dry_run", False)
        and not getattr(args, "test_notify", False)
        and not getattr(args, "status", False)
        and not getattr(args, "history", False)
        and not getattr(args, "apply_schedule", False)
    ):
        try:
            os.makedirs(state_dir, exist_ok=True)
            with open(state_file, "w") as f:
                f.write(str(datetime.now(timezone.utc).timestamp()))
        except Exception as e:
            logging.warning(f"Failed to write state file: {e}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
