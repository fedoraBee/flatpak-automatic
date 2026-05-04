import logging
import subprocess
import shutil
from typing import Optional
from ..config import ConfigManager


class MailNotifier:
    def __init__(self, to_address: str, from_address: str) -> None:
        self.enabled = ConfigManager.verify_policy("mails")
        self.to_address: str = to_address
        self.from_address: str = from_address
        self.mail_cmd: Optional[str] = self._find_mail_cmd()

    @classmethod
    def is_available(cls) -> bool:
        for cmd in ["s-nail", "mailx", "mailutils", "mail"]:
            if shutil.which(cmd):
                return True
        return False

    def _find_mail_cmd(self) -> Optional[str]:
        for cmd in ["s-nail", "mailx", "mailutils", "mail"]:
            if shutil.which(cmd):
                return cmd
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
            # Determine content type (HTML vs Plain Text)
            is_html = "<html>" in body.lower() or "<!doctype html>" in body.lower()
            content_type = "text/html" if is_html else "text/plain"

            # Command-line arguments vary significantly between mail clients:
            # - s-nail / heirloom-mailx: Uses -r for sender, -a for headers
            # - mailutils: Uses -a "From: ..." or --return-address
            # - bsd-mailx: Uses -a for headers, often lacks -r
            cmd = [self.mail_cmd, "-s", subject]

            # Detect specific client capabilities to set the sender and headers correctly
            help_out = ""
            try:
                # Some clients use --help, others use -h, others just fail on unknown args
                res = subprocess.run(
                    [self.mail_cmd, "--help"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                help_out = (res.stdout or "") + (res.stderr or "")
                if not help_out:
                    res = subprocess.run(
                        [self.mail_cmd, "-h"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    help_out = (res.stdout or "") + (res.stderr or "")
            except Exception as e:
                logging.debug(f"Could not determine mail client capabilities: {e}")

            # Add Content-Type header via -a if supported (common for mailx/s-nail/mailutils)
            if "-a" in help_out or not help_out:
                cmd += ["-a", f"Content-Type: {content_type}; charset=UTF-8"]

            # Check if -r (sender/return-address) is supported
            # Known to work with: s-nail, heirloom-mailx, GNU Mailutils, and modern bsd-mailx
            if (
                "-r" in help_out
                or "s-nail" in help_out
                or "Heirloom" in help_out
                or "GNU Mailutils" in help_out
            ):
                if self.from_address:
                    cmd += ["-r", self.from_address]
            elif "-a" in help_out and self.from_address:
                # Fallback for clients where -r is missing but -a (append header) works
                cmd += ["-a", f"From: {self.from_address}"]
            else:
                # Default behavior (sender override may not be supported)
                logging.debug(
                    f"Using default mail dispatch for {self.mail_cmd} (sender override may not be supported)."
                )

            cmd.append(self.to_address)

            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
            )
            process.communicate(input=body.encode("utf-8"))
            logging.info(
                f"Notification dispatched to {self.to_address} via {self.mail_cmd} ({content_type})."
            )
        except Exception as e:
            logging.error(f"Failed to dispatch mail: {e}")
