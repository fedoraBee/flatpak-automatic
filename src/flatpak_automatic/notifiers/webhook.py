import json
import logging
from typing import List
from ..config import ConfigManager


class WebhookNotifier:
    def __init__(self, urls: List[str], secret: str = "") -> None:
        self.enabled = ConfigManager.verify_policy("webhooks")
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
