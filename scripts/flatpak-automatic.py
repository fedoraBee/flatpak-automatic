#!/usr/bin/env python3
# Version: 1.4.6
import os
import sys
import subprocess
import socket

try:
    import dbus

    DBUS_AVAILABLE = True
except ImportError:
    DBUS_AVAILABLE = False
    print(
        "Warning: python3-dbus is not installed. Snapper snapshots will be bypassed.",
        file=sys.stderr,
    )


class SnapperManager:
    def __init__(self, config="root"):
        self.config = config
        self.interface = None
        if DBUS_AVAILABLE:
            try:
                self.bus = dbus.SystemBus()
                self.proxy = self.bus.get_object(
                    "org.opensuse.Snapper", "/org/opensuse/Snapper"
                )
                self.interface = dbus.Interface(self.proxy, "org.opensuse.Snapper")
            except Exception as e:
                # Graceful degradation for systems lacking Snapper (e.g., standard Ubuntu)
                print(
                    f"Notice: Snapper DBus unavailable. Bypassing snapshots gracefully. ({type(e).__name__})",
                    file=sys.stderr,
                )
                self.interface = None

    def create_timeline_snapshot(self, description="Pre-Flatpak Update"):
        if not self.interface:
            return -1
        try:
            empty_dict = dbus.Dictionary({}, signature="ss")
            snapshot_id = self.interface.CreateSingleSnapshot(
                self.config, "timeline", description, empty_dict
            )
            print(f"Created Snapper timeline snapshot: #{snapshot_id}")
            return snapshot_id
        except Exception as e:
            print(f"Snapper DBus execution error: {e}", file=sys.stderr)
            return -1


class FlatpakUpdater:
    def __init__(self):
        self.updates_available = False
        self.update_log = ""

    def check_updates(self):
        cmd = ["flatpak", "update", "--dry-run", "--columns=application,branch,version"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if "Nothing to do" not in result.stdout and result.stdout.strip() != "":
            self.updates_available = True
            self.update_log = result.stdout
        return self.updates_available

    def apply_updates(self):
        cmd = ["flatpak", "update", "-y", "--noninteractive"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.update_log += (
            f"\n\n--- Flatpak Execution Log ---\n{result.stdout}\n{result.stderr}"
        )
        return result.returncode == 0


class MailNotifier:
    def __init__(self, to_address, from_address):
        self.to_address = to_address
        self.from_address = from_address
        self.mail_cmd = self._find_mail_cmd()

    def _find_mail_cmd(self):
        for cmd in ["s-nail", "mailx", "mailutils", "mail"]:
            if (
                subprocess.run(["command", "-v", cmd], capture_output=True).returncode
                == 0
            ):
                return cmd
        return None

    def send_mail(self, subject, body):
        if not self.mail_cmd or not self.to_address:
            print("Skipping mail notification: Mail client or recipient missing.")
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
            print(f"Notification dispatched to {self.to_address} via {self.mail_cmd}.")
        except Exception as e:
            print(f"Failed to dispatch mail: {e}", file=sys.stderr)


def load_sysconfig():
    config = {}
    paths = ["/etc/sysconfig/flatpak-automatic", "/etc/default/flatpak-automatic"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if line.strip() and not line.startswith("#") and "=" in line:
                        k, v = line.strip().split("=", 1)
                        config[k] = v.strip("\"'")
            break
    return config


def main():
    config = load_sysconfig()

    if config.get("FLATPAK_AUTO_UPDATE", "true").lower() != "true":
        print("Automatic updates are disabled via configuration.")
        sys.exit(0)

    updater = FlatpakUpdater()
    if not updater.check_updates():
        print("No Flatpak updates available.")
        sys.exit(0)

    print("Updates found. Interfacing with System Services...")

    if config.get("FLATPAK_CREATE_SNAPSHOT", "true").lower() == "true":
        snapper = SnapperManager()
        snapper.create_timeline_snapshot("Pre-Flatpak Update Automation")

    print("Applying Flatpak updates...")
    success = updater.apply_updates()

    notify_type = config.get("FLATPAK_AUTO_NOTIFY", "none").lower()
    trigger_notify = False

    if notify_type in ("always", "on-update"):
        trigger_notify = True
    elif notify_type == "on-error" and not success:
        trigger_notify = True

    if trigger_notify:
        subject_prefix = "[SUCCESS]" if success else "[FAILED]"
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

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
