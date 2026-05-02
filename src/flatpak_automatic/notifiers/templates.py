import os
from string import Template
from typing import Dict
from ..constants import TEMPLATE_DIR


class TemplateRenderer:
    @staticmethod
    def render(template_name: str, context: Dict[str, str]) -> str:
        path = os.path.join(TEMPLATE_DIR, f"{template_name}")
        if not os.path.exists(path):
            return context.get("BODY", "")
        with open(path, "r") as f:
            tpl = Template(f.read())
            return tpl.safe_substitute(context)
