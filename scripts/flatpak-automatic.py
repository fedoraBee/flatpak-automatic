#!/usr/bin/env python3
# Version: 1.4.12
import os
import sys
import subprocess
import socket
import logging
import json
import shlex
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
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
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
    def __init__(self) -> None:
        self.updates_available: bool = False
        self.update_log: str = ""

    def check_updates(self) -> bool:
        cmd = ["flatpak", "update", "--dry-run", "--columns=application,branch,version"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if "Nothing to do" not in result.stdout and result.stdout.strip() != "":
            self.updates_available = True
            self.update_log = result.stdout
        return self.updates_available

    def apply_updates(self) -> bool:
        cmd = ["flatpak", "update", "-y", "--noninteractive"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.update_log += (
            f"\n\n--- Flatpak Execution Log ---\n{result.stdout}\n{result.stderr}"
        )
        return result.returncode == 0


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


def main() -> None:
    if sys.stdout.isatty():
        # Gradient banner: Cyan -> Deep Blue -> Magenta
        print(
            "\033[38;2;0;255;255m  ___ _       _               _    \n"
            "\033[38;2;85;170;255m | __| |__ _ | |_ _ __  __ _ | |__ \n"
            "\033[38;2;170;85;255m | _|| / _` ||  _| '_ \\/ _` || / / \n"
            "\033[38;2;255;0;255m |_| |_\\__,_|\\__| .__/\\__,_||_\\_\\\n"
            "                |_|\033[0m AUTOMATIC\n"
        )

    config: Dict[str, str] = load_sysconfig()

    if config.get("FLATPAK_AUTO_UPDATE", "true").lower() != "true":
        logging.info("Automatic updates are disabled via configuration.")
        sys.exit(0)

    updater = FlatpakUpdater()
    if not updater.check_updates():
        logging.info("No Flatpak updates available.")
        sys.exit(0)

    logging.info("Updates found. Interfacing with System Services...")

    if config.get("FLATPAK_CREATE_SNAPSHOT", "true").lower() == "true":
        snapper = SnapperManager()
        snapper.create_timeline_snapshot("Pre-Flatpak Update Automation")

    logging.info("Applying Flatpak updates...")
    success: bool = updater.apply_updates()

    notify_type: str = config.get("FLATPAK_AUTO_NOTIFY", "none").lower()
    trigger_notify: bool = False

    if notify_type in ("always", "on-update"):
        trigger_notify = True
    elif notify_type == "on-error" and not success:
        trigger_notify = True

    if trigger_notify:
        subject_prefix: str = "[SUCCESS]" if success else "[FAILED]"
        mailer = MailNotifier(
            config.get("FLATPAK_MAIL_TO", ""),
            config.get(
                "FLATPAK_MAIL_FROM", f"flatpak-automatic@{socket.gethostname()}"
            ),
        )
        mailer.send_mail(
            f"{subject_prefix} Flatpak Automatic Updates - {socket.gethostname()}",
            updater.update_log,
        )

        apprise_urls = config.get("FLATPAK_APPRISE_URLS", "")
        if apprise_urls:
            apprise_notifier = AppriseNotifier(apprise_urls)
            apprise_notifier.send_notification(
                f"{subject_prefix} Flatpak Automatic Updates - {socket.gethostname()}",
                updater.update_log,
            )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
