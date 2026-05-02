#!/usr/bin/env python3
# Version: 1.5.14-rc3
import os
import sys
import signal
import json
import subprocess
import socket
import logging
import argparse
import yaml
from string import Template
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List


# Brand Asset Discovery
def _find_brand_icon() -> str:
    """Locate the best available icon for notifications."""
    # Preferred filenames
    icon_names = ["logo.svg", "icon.svg", "flatpak-automatic.svg"]

    # 1. Local Development Path (relative to script in src/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_assets = os.path.join(os.path.dirname(script_dir), "assets")
    if os.path.exists(local_assets):
        for name in icon_names:
            path = os.path.join(local_assets, name)
            if os.path.exists(path):
                return path

    # 2. System-wide Installation Path (RPM/DEB)
    # The spec file installs assets/logo.svg as flatpak-automatic.svg
    sys_path = "/usr/share/icons/hicolor/scalable/apps/flatpak-automatic.svg"
    if os.path.exists(sys_path):
        return sys_path

    # 3. Fallback to standard system icon name
    return "software-update-available"


ICON_PATH = _find_brand_icon()


def _resolve_active_dbus_sessions() -> dict:
    """
    Dynamically resolve active DBUS_SESSION_BUS_ADDRESS for local users.
    Bypasses strict $DISPLAY/$WAYLAND_DISPLAY requirements for background systemd timers.
    """
    sessions = {}
    base_dir = "/run/user"
    if os.path.exists(base_dir):
        for uid in os.listdir(base_dir):
            if uid.isdigit() and int(uid) >= 1000:
                bus_path = os.path.join(base_dir, uid, "bus")
                if os.path.exists(bus_path):
                    sessions[uid] = f"unix:path={bus_path}"
    return sessions


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    OKPINK = "\033[38;5;125m"
    DEEPPINK = "\033[38;5;125m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


STATE_FILE = "/var/cache/flatpak-automatic/state.json"
USER_STATE_FILE = os.path.expanduser("~/.cache/flatpak-automatic/state.json")
CONFIG_FILE = "/etc/flatpak-automatic/config.yaml"
TEMPLATE_DIR = "/etc/flatpak-automatic/templates"


def get_state_path(user_scope: bool = False) -> str:
    return user_scope and USER_STATE_FILE or STATE_FILE


def load_state(user_scope: bool = False) -> Dict[str, Any]:
    try:
        with open(get_state_path(user_scope), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_try": "Never", "last_success": "Never"}


def save_state(state: Dict[str, Any], user_scope: bool = False) -> None:
    try:
        os.makedirs(os.path.dirname(get_state_path(user_scope)), exist_ok=True)
        with open(get_state_path(user_scope), "w") as f:
            json.dump(state, f)
    except Exception as e:
        logging.warning(f"Failed to save state: {e}")


def exit_clean(code: int = 0):
    print("")
    sys.exit(code)


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
    def __init__(self, excludes: List[str] = None) -> None:
        self.updates_available: bool = False
        self.update_log: str = ""
        self.update_count: int = 0
        self.excludes = excludes or []

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
                self.update_count = len(filtered_lines)
        return self.updates_available

    def apply_updates(self) -> bool:
        cmd = ["flatpak", "update", "-y", "--noninteractive"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.update_log += (
            f"\n\n--- Flatpak Execution Log ---\n{result.stdout}\n{result.stderr}"
        )
        return result.returncode == 0


class DesktopNotifier:
    def __init__(self) -> None:
        self.enabled = verify_policy("desktop")

    def send_notification(
        self, title: str, body: str, icon: str = "software-update-available"
    ) -> None:

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
                    icon_param = icon
                    hints = []
                    if os.path.isabs(icon):
                        icon_param = f"file://{icon}"
                        hints = ["-h", f"string:image-path:{icon_param}"]

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
                            "-i",
                            icon_param,
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


class WebhookNotifier:
    def __init__(self, urls: List[str], secret: str = "") -> None:
        self.enabled = verify_policy("webhooks")
        self.urls = urls
        self.secret = secret.strip()

    def send_notification(self, title: str, body: str) -> None:

        if not self.enabled:
            logging.info("Webhook notifications disabled by global policy. Skipping.")
            return

        if not self.urls:
            return
        import urllib.request
        import urllib.error
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
        self.enabled = verify_policy("mails")
        self.to_address: str = to_address
        self.from_address: str = from_address
        self.mail_cmd: Optional[str] = self._find_mail_cmd()

    def _find_mail_cmd(self) -> Optional[str]:
        for cmd in ["s-nail", "mailx", "mailutils", "mail"]:
            try:
                if (
                    subprocess.run(
                        ["command", "-v", cmd], capture_output=True, shell=True
                    ).returncode
                    == 0
                ):
                    return cmd
            except Exception:
                continue
        return None

    def send_mail(self, subject: str, body: str) -> None:
        if not self.enabled:
            logging.info("Mail notifications disabled by global policy. Skipping.")
            return

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


class TemplateRenderer:
    @staticmethod
    def render(template_name: str, context: Dict[str, str]) -> str:
        path = os.path.join(TEMPLATE_DIR, f"{template_name}")
        if not os.path.exists(path):
            return context.get("BODY", "")
        with open(path, "r") as f:
            tpl = Template(f.read())
            return tpl.safe_substitute(context)


class NotificationRouter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.groups = config.get("notification_groups", [])

        # Support top-level legacy config by injecting it into a virtual group
        legacy_mail = config.get("mail")
        legacy_webhook = config.get("webhook")
        if legacy_mail or legacy_webhook:
            self.groups.append(
                {
                    "name": "Legacy Global Group",
                    "mails": legacy_mail if legacy_mail else {},
                    "webhooks": legacy_webhook if legacy_webhook else {},
                }
            )

    def dispatch_all(self, title: str, body: str, success: bool, update_count: int = 0):
        if not self.groups:
            return

        context = {
            "TITLE": title,
            "BODY": body,
            "STATUS": "SUCCESS" if success else "FAILED",
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "HOSTNAME": socket.gethostname(),
            "UPDATE_COUNT": str(update_count),
        }

        def _resolve(group_cfg, target_cfg, field_name, default_val):

            target_val = (
                target_cfg.get(field_name)
                if target_cfg and field_name in target_cfg
                else None
            )
            group_val = group_cfg.get(field_name)
            state_key = "success" if success else "failure"

            def get_state_val(v):
                if isinstance(v, dict):
                    return v.get(state_key)
                return v

            res = None
            if target_val is not None:
                res = get_state_val(target_val)

            if res is None and group_val is not None:
                res = get_state_val(group_val)

            if res is None:
                res = default_val

            return res

        for group in self.groups:
            # 1. Apprise (Universal)
            apprise_cfg = group.get("apprise", {})
            # if not apprise_cfg and group.get("urls"):
            #     apprise_cfg = {"urls": group.get("urls", [])}

            if (
                APPRISE_AVAILABLE
                and apprise_cfg.get("enabled", True)
                and apprise_cfg.get("urls")
            ):
                app_urls = apprise_cfg.get("urls", [])
                app_title = _resolve(group, apprise_cfg, "title", title)
                app_title = app_title.replace(
                    "$UPDATE_COUNT", str(update_count)
                ).replace("$(hostname)", socket.gethostname())
                app_tpl = _resolve(group, apprise_cfg, "body_template", "")
                app_body = (
                    TemplateRenderer.render(app_tpl, context) if app_tpl else body
                )
                if not verify_policy("apprise"):
                    logging.info(
                        "Apprise notifications disabled by global policy. Skipping."
                    )
                    return
                try:
                    apobj = apprise.Apprise()
                    for url in app_urls:
                        apobj.add(url)
                    apobj.notify(body=app_body, title=app_title)
                    logging.info(
                        f"Notification group '{group.get('name', 'unnamed')}' dispatched to {len(app_urls)} endpoints via Apprise."
                    )
                except Exception as e:
                    logging.error(f"Failed to dispatch Apprise notification: {e}")

            # 2. Direct Mails
            mails_cfg = group.get("mails", group.get("mail", {}))
            if (
                mails_cfg.get("enabled", True)
                and "to" in mails_cfg
                and "from" in mails_cfg
            ):
                to_addrs = mails_cfg.get("to", [])
                if isinstance(to_addrs, str):
                    to_addrs = [to_addrs]
                from_addr = mails_cfg.get("from", f"bot@{socket.gethostname()}")
                m_title = _resolve(group, mails_cfg, "title", title)
                m_title = m_title.replace("$UPDATE_COUNT", str(update_count)).replace(
                    "$(hostname)", socket.gethostname()
                )
                m_tpl = _resolve(group, mails_cfg, "body_template", "")
                m_body = TemplateRenderer.render(m_tpl, context) if m_tpl else body

                for to_addr in to_addrs:
                    mailer = MailNotifier(to_addr, from_addr)
                    mailer.send_mail(m_title, m_body)

            # 3. Direct Webhooks
            webhook_cfg = group.get("webhooks", group.get("webhook", {}))
            wh_urls = webhook_cfg.get("urls", [])
            if wh_urls and webhook_cfg.get("enabled", True):
                secret = webhook_cfg.get("secret", "")
                wh_title = _resolve(group, webhook_cfg, "title", title)
                wh_title = wh_title.replace("$UPDATE_COUNT", str(update_count)).replace(
                    "$(hostname)", socket.gethostname()
                )
                wh_tpl = _resolve(group, webhook_cfg, "body_template", "")
                wh_body = TemplateRenderer.render(wh_tpl, context) if wh_tpl else body

                wh = WebhookNotifier(wh_urls, secret)
                wh.send_notification(wh_title, wh_body)

            # 4. Native Desktop Notifications (Per-Group)
            desktop_cfg = group.get("desktop", {})
            if desktop_cfg.get("enabled", True):
                dt_title = _resolve(group, desktop_cfg, "title", title)
                dt_title = dt_title.replace("$UPDATE_COUNT", str(update_count)).replace(
                    "$(hostname)", socket.gethostname()
                )
                dt_tpl = _resolve(group, desktop_cfg, "body_template", "")
                dt_body = TemplateRenderer.render(dt_tpl, context) if dt_tpl else body
                desktop = DesktopNotifier()
                desktop.send_notification(dt_title, dt_body, ICON_PATH)


def load_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logging.error(f"Failed to parse YAML config: {e}")
    return {}


def verify_policy(policy_key: str) -> bool:
    return bool(load_config().get("notification_policy", {}).get(policy_key, False))


def banner() -> str:

    return (
        f"{Colors.BOLD}{Colors.OKCYAN}  ___ _       _               _    \n"
        f"{Colors.OKBLUE} | __| |__ _ | |_ _ __  __ _ | |__ \n"
        f"{Colors.HEADER} | _|| / _` || ._| '_ \\/ _` || / / \n"
        f"{Colors.OKPINK} |_| |_\\__,_|\\__|| .__/\\__,_||_\\_\\\n"
        f"    AUTOMATIC    |_| {Colors.ENDC}     {Colors.OKCYAN} v1.5.14-rc3{Colors.ENDC}\n"
    )


class BrandedArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        file.write(banner() + "\n")
        super().print_help(file)
        file.write("\n")


def main() -> None:
    parser = BrandedArgumentParser(
        description="Flatpak Automatic - Advanced Update Automation"
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
        "-c",
        "--check-config",
        action="store_true",
        help="Validate and print the current configuration, then exit.",
    )
    parser.add_argument(
        "-r",
        "--reload",
        action="store_true",
        help="Send SIGHUP to a running instance to reload its config.",
    )
    args = parser.parse_args()

    # Dynamic Flatpak Scope for non-root execution
    user_scope = os.geteuid() != 0
    flatpak_scope = ["--user"] if user_scope else ["--system"]

    if sys.stdout.isatty():
        print(banner())

    config: Dict[str, Any] = load_config()

    def sighup_handler(signum, frame):
        logging.info("SIGHUP received. Hot-reloading configuration...")
        nonlocal config
        config = load_config()

    try:
        signal.signal(signal.SIGHUP, sighup_handler)
    except AttributeError:
        pass  # Handle OS environments that do not support SIGHUP safely
    state = load_state(user_scope)

    if args.check_config:
        print(
            f"{Colors.BOLD}{Colors.OKCYAN}⚙️  Validating Configuration...{Colors.ENDC}"
        )
        chk_config = load_config()
        if chk_config:
            print(f"{Colors.OKGREEN}✅ Configuration is valid.{Colors.ENDC}")
            print(
                f"   {yaml.dump(chk_config, default_flow_style=False, sort_keys=False).replace('\n', '\n   ')}",
                end="",
            )
        else:
            print(f"{Colors.WARNING}⚠️ Configuration is empty or invalid.{Colors.ENDC}")
        exit_clean(0)

    if args.reload:
        print(
            f"{Colors.BOLD}{Colors.OKCYAN}🔄 Sending SIGHUP to flatpak-automatic.service...{Colors.ENDC}"
        )
        try:
            subprocess.run(
                ["systemctl", "kill", "-s", "HUP", "flatpak-automatic.service"]
                + flatpak_scope,
                check=True,
            )
            print(
                f"{Colors.OKGREEN}✅ Reload signal (SIGHUP) sent successfully.{Colors.ENDC}"
            )
        except Exception as e:
            print(f"{Colors.FAIL}❌ Failed to send reload signal: {e}{Colors.ENDC}")
        exit_clean(0)

    if args.apply_schedule:
        timer_cfg = config.get("timer", {})
        schedule = timer_cfg.get("schedule", "daily")
        delay = timer_cfg.get("delay", "1h")
        override_dir = "/etc/systemd/system/flatpak-automatic.timer.d"
        override_file = os.path.join(override_dir, "override.conf")

        try:
            print(f"{Colors.BOLD}⚙️  Applying Systemd Timer Override...{Colors.ENDC}")
            os.makedirs(override_dir, exist_ok=True)
            with open(override_file, "w") as f:
                f.write(
                    f"[Timer]\nOnCalendar=\nOnCalendar={schedule}\nRandomizedDelaySec={delay}\n"
                )
            print(f"  Wrote configuration to: {override_file}")

            subprocess.run(["systemctl", "daemon-reload"] + flatpak_scope, check=True)
            subprocess.run(
                ["systemctl", "restart", "flatpak-automatic.timer"] + flatpak_scope,
                check=True,
            )
            print(
                f"{Colors.OKGREEN}✅ Successfully applied schedule: '{schedule}' with a '{delay}' randomization delay.{Colors.ENDC}"
            )
        except Exception as e:
            print(f"{Colors.FAIL}❌ Failed to apply systemd schedule: {e}{Colors.ENDC}")
        exit_clean(0)

    if args.status:
        print(
            f"{Colors.HEADER}{Colors.BOLD}[ System Status & Monitoring Overview ]{Colors.ENDC}"
        )

        print(f"\n{Colors.OKCYAN}📊 Execution State:{Colors.ENDC}")
        print(f"   Last Update Try: {state.get('last_try', 'Never')}")
        print(f"   Last Success:    {state.get('last_success', 'Never')}")

        # print(f"\n{Colors.OKCYAN}⚙️  Configuration ({CONFIG_FILE}):{Colors.ENDC}")
        # print(
        #     f"   {yaml.dump(config, default_flow_style=False, sort_keys=False).replace('\n', '\n   ')}"
        # )

        print(f"\n{Colors.OKCYAN}📦 Installed Flatpaks:{Colors.ENDC}")
        result = subprocess.run(
            ["flatpak", "list", "--app", "--columns=application,version"],
            capture_output=True,
            text=True,
        )
        for line in result.stdout.strip().split("\n"):
            print(f"   {line}")
        exit_clean(0)

    if args.history:
        print(
            f"{Colors.HEADER}{Colors.BOLD}[ Recent flatpak-automatic Execution History ]{Colors.ENDC}"
        )
        subprocess.run(
            ["journalctl", "-u", "flatpak-automatic.service", "-n", "20", "--no-pager"]
        )
        exit_clean(0)

    if args.test_notify:
        logging.info("Executing Test Notification dispatch...")
        router = NotificationRouter(config)
        router.dispatch_all(
            "[TEST] Flatpak Automatic",
            "This is a test notification from flatpak-automatic.",
            True,
        )
        desktop = DesktopNotifier()

        desktop.send_notification(
            "Test Notification", "This is a test notification from flatpak-automatic."
        )
        exit_clean(0)

    auto_update = config.get("auto_update", True)
    if not auto_update and not args.force:
        logging.info("Automatic updates are disabled via configuration.")
        exit_clean(0)

    state["last_try"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(state, user_scope)

    updater = FlatpakUpdater(excludes=config.get("excludes", []))
    if not updater.check_updates():
        logging.info("No Flatpak updates available.")
        exit_clean(0)

    logging.info("Updates found. Interfacing with System Services...")

    if args.dry_run:
        logging.info(
            "[DRY-RUN] Updates found, but dry-run is active. Skipping snapshots and applying updates."
        )
        logging.info(f"[DRY-RUN] Would have updated:\n{updater.update_log}")
        exit_clean(0)

    snap_cfg = config.get("snapshots", {})
    if snap_cfg.get("enabled", True):
        snapper = SnapperManager(config=snap_cfg.get("snapper_config", "root"))
        desc_cfg = snap_cfg.get("snapper_descriptions", {})
        snapper.create_timeline_snapshot(desc_cfg.get("pre", "flatpak-automatic-pre"))

    logging.info("Applying Flatpak updates...")
    success: bool = updater.apply_updates()

    if success:
        state["last_success"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_state(state, user_scope)
        snap_cfg = config.get("snapshots", {})
        if snap_cfg.get("enabled", True):
            if "snapper" in locals():
                desc_cfg = snap_cfg.get("snapper_descriptions", {})
                snapper.create_timeline_snapshot(
                    desc_cfg.get("post", "flatpak-automatic-post")
                )

    notify_type = config.get("auto_notify", "always").lower()
    trigger_notify = False

    if notify_type in ("always", "on-update"):
        trigger_notify = True
    elif notify_type == "on-error" and not success:
        trigger_notify = True

    if trigger_notify:
        subject_prefix = "[SUCCESS]" if success else "[FAILED]"
        title = f"{subject_prefix} Flatpak Updates - {socket.gethostname()}"

        router = NotificationRouter(config)
        router.dispatch_all(title, updater.update_log, success, updater.update_count)

    exit_clean(0 if success else 1)


if __name__ == "__main__":
    main()
