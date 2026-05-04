import sys
import argparse
from typing import Any
from .constants import Colors


def banner() -> str:
    return (
        f"{Colors.BOLD}{Colors.OKCYAN}  ___ _       _               _    \n"
        f"{Colors.OKBLUE} | __| |__ _ | |_ _ __  __ _ | |__ \n"
        f"{Colors.HEADER} | _|| / _` || ._| '_ \\/ _` || / / \n"
        f"{Colors.OKPINK} |_| |_\\__,_|\\__|| .__/\\__,_||_\\_\\\n"
        f"    AUTOMATIC    |_| {Colors.ENDC}     {Colors.OKCYAN} v1.5.18{Colors.ENDC}\n"
    )


class BrandedArgumentParser(argparse.ArgumentParser):
    def print_help(self, file: Any = None) -> None:
        if file is None:
            file = sys.stdout
        file.write(banner() + "\n")
        super().print_help(file)
        file.write("\n")


def get_parser() -> BrandedArgumentParser:
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
    parser.add_argument(
        "--desktop-mode",
        action="store_true",
        help="Run in interactive desktop mode (keeps terminal open after completion).",
    )
    parser.add_argument(
        "-e",
        "--enable-timer",
        action="store_true",
        help="Enable and start the systemd timer (auto-scope).",
    )
    parser.add_argument(
        "-x",
        "--disable-timer",
        action="store_true",
        help="Disable and stop the systemd timer (auto-scope).",
    )
    return parser
