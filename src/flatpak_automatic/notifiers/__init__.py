import logging
import socket
from datetime import datetime
from typing import Dict, Any
from .templates import TemplateRenderer
from .desktop import DesktopNotifier
from .mail import MailNotifier
from .webhook import WebhookNotifier
from ..config import ConfigManager

try:
    import apprise

    APPRISE_AVAILABLE = True
except ImportError:
    APPRISE_AVAILABLE = False
    logging.warning(
        "apprise is not installed. Universal notifications will be bypassed."
    )

__all__ = [
    "NotificationRouter",
    "TemplateRenderer",
    "DesktopNotifier",
    "MailNotifier",
    "WebhookNotifier",
]


class NotificationRouter:
    def __init__(self, config: Dict[str, Any]) -> None:
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

    def dispatch_all(
        self, title: str, body: str, success: bool, update_count: int = 0
    ) -> None:
        if not self.groups:
            return

        context = {
            "TITLE": title,
            "BODY": body,
            "STATUS": "SUCCESS" if success else "FAILED",
            "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "HOSTNAME": socket.gethostname(),
            "UPDATE_COUNT": str(update_count),
            "UPDATE_LIST": body if success else "",
            "LOG_OUTPUT": body if not success else "",
        }

        def _resolve(
            group_cfg: Dict[str, Any],
            target_cfg: Dict[str, Any],
            field_name: str,
            default_val: Any,
        ) -> Any:
            target_val = (
                target_cfg.get(field_name)
                if target_cfg and field_name in target_cfg
                else None
            )
            group_val = group_cfg.get(field_name)
            state_key = "success" if success else "failure"

            def get_state_val(v: Any) -> Any:
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
            # 1. Apprise
            apprise_cfg = group.get("apprise", {})
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
                if not ConfigManager.verify_policy("apprise"):
                    logging.info(
                        "Apprise notifications disabled by global policy. Skipping."
                    )
                else:
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

            # 4. Native Desktop Notifications
            desktop_cfg = group.get("desktop", {})
            if desktop_cfg.get("enabled", True):
                dt_title = _resolve(group, desktop_cfg, "title", title)
                dt_title = dt_title.replace("$UPDATE_COUNT", str(update_count)).replace(
                    "$(hostname)", socket.gethostname()
                )
                dt_tpl = _resolve(group, desktop_cfg, "body_template", "")
                dt_body = TemplateRenderer.render(dt_tpl, context) if dt_tpl else body
                desktop = DesktopNotifier()
                desktop.send_notification(dt_title, dt_body)
