import logging
import subprocess
from typing import Optional
from ..config import ConfigManager


class MailNotifier:
    def __init__(self, to_address: str, from_address: str) -> None:
        self.enabled = ConfigManager.verify_policy("mails")
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
