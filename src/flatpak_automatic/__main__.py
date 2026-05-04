import os
import sys
import logging
import signal
import subprocess
from typing import Any
from .cli import get_parser, banner
from .config import ConfigManager, StateManager
from .core import AutomationEngine
from .logging_utils import setup_logging
from .constants import Colors


def main() -> None:
    # 1. Initialize Parser & Logging
    parser = get_parser()
    args = parser.parse_args()
    setup_logging()

    # Dynamic Flatpak Scope for non-root execution
    user_scope = os.geteuid() != 0
    flatpak_scope = ["--user"] if user_scope else ["--system"]

    if sys.stdout.isatty():
        print(banner())

    # 2. Load Configuration & State
    config = ConfigManager.load()

    def sighup_handler(signum: int, frame: Any) -> None:
        logging.info("SIGHUP received. Hot-reloading configuration...")
        nonlocal config
        config = ConfigManager.load()

    try:
        signal.signal(signal.SIGHUP, sighup_handler)
    except AttributeError:
        pass  # Handle OS environments that do not support SIGHUP safely

    state = StateManager.load(user_scope)

    # 3. Initialize the Automation Engine
    engine = AutomationEngine(config, state)

    try:
        # 4. Handle specialized CLI commands
        if args.check_config:
            engine.validate_config()
            print()
            sys.exit(0)

        if args.reload:
            print(
                f"{Colors.BOLD}{Colors.OKCYAN}🔄 Sending SIGHUP to flatpak-automatic.service...{Colors.ENDC}"
            )
            try:
                # Check if the service is active/running first
                check_active = subprocess.run(
                    ["systemctl", "is-active", "flatpak-automatic.service"]
                    + flatpak_scope,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if check_active.returncode != 0:
                    print(
                        f"{Colors.WARNING}⚠️  Reload skipped: flatpak-automatic.service is not currently running.{Colors.ENDC}"
                    )
                    print(
                        "   Note: Since this is a oneshot service, it only needs a reload if it's currently executing."
                    )
                    print()
                    sys.exit(0)

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
            print()
            sys.exit(0)

        if args.apply_schedule:
            timer_cfg = config.get("timer", {})
            schedule = timer_cfg.get("schedule", "daily")
            delay = timer_cfg.get("delay", "1h")
            override_dir = "/etc/systemd/system/flatpak-automatic.timer.d"
            override_file = os.path.join(override_dir, "override.conf")

            try:
                print(
                    f"{Colors.BOLD}⚙️  Applying Systemd Timer Override...{Colors.ENDC}"
                )
                os.makedirs(override_dir, exist_ok=True)
                with open(override_file, "w") as f:
                    f.write(
                        f"[Timer]\nOnCalendar=\nOnCalendar={schedule}\nRandomizedDelaySec={delay}\n"
                    )
                print(f"  Wrote configuration to: {override_file}")
                subprocess.run(
                    ["systemctl", "daemon-reload"] + flatpak_scope, check=True
                )
                subprocess.run(
                    ["systemctl", "restart", "flatpak-automatic.timer"] + flatpak_scope,
                    check=True,
                )
                print(
                    f"{Colors.OKGREEN}✅ Successfully applied schedule: '{schedule}' with a '{delay}' randomization delay.{Colors.ENDC}"
                )
            except Exception as e:
                print(
                    f"{Colors.FAIL}❌ Failed to apply systemd schedule: {e}{Colors.ENDC}"
                )
            print()
            sys.exit(0)

        if args.enable_timer:
            print(
                f"{Colors.BOLD}{Colors.OKCYAN}🚀 Enabling and starting Flatpak Automatic Timer...{Colors.ENDC}"
            )
            try:
                subprocess.run(
                    ["systemctl", "enable", "--now", "flatpak-automatic.timer"]
                    + flatpak_scope,
                    check=True,
                )
                scope_str = "User" if user_scope else "System"
                print(
                    f"{Colors.OKGREEN}✅ {scope_str} timer enabled and started successfully.{Colors.ENDC}"
                )
            except Exception as e:
                print(f"{Colors.FAIL}❌ Failed to enable/start timer: {e}{Colors.ENDC}")
            print()
            sys.exit(0)

        if args.disable_timer:
            print(
                f"{Colors.BOLD}{Colors.OKCYAN}🛑 Disabling and stopping Flatpak Automatic Timer...{Colors.ENDC}"
            )
            try:
                subprocess.run(
                    ["systemctl", "disable", "--now", "flatpak-automatic.timer"]
                    + flatpak_scope,
                    check=True,
                )
                scope_str = "User" if user_scope else "System"
                print(
                    f"{Colors.OKGREEN}✅ {scope_str} timer disabled and stopped successfully.{Colors.ENDC}"
                )
            except Exception as e:
                print(f"{Colors.FAIL}❌ Failed to disable/stop timer: {e}{Colors.ENDC}")
            print()
            sys.exit(0)

        if args.status:
            engine.print_status_overview()
            sys.exit(0)

        if args.history:
            print(
                f"{Colors.HEADER}{Colors.BOLD}[ Recent Flatpak Automatic Execution History ]{Colors.ENDC}"
            )
            subprocess.run(
                [
                    "journalctl",
                    "-u",
                    "flatpak-automatic.service",
                    "-n",
                    "20",
                    "--no-pager",
                ]
            )
            print()
            sys.exit(0)

        if args.test_notify:
            engine.dispatch_test_notifications()
            print()
            sys.exit(0)

        # 5. Execute Primary Automation Loop
        success = engine.run(
            dry_run=args.dry_run, force=args.force, desktop_mode=args.desktop_mode
        )

        if args.desktop_mode:
            print("\n" + Colors.BOLD + "Execution finished." + Colors.ENDC)
            input("Press Enter to close this window...")

        print()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️ Execution interrupted by user.{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        logging.exception(f"Critical failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
