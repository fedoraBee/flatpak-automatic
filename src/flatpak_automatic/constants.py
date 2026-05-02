import os


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


def find_brand_icon() -> str:
    """Locate the best available icon for notifications."""
    icon_names = ["flatpak-automatic.svg", "logo.svg"]

    # 1. System-wide Installation Path (RPM/DEB)
    sys_path = "/usr/share/icons/hicolor/scalable/apps/flatpak-automatic.svg"
    if os.path.exists(sys_path):
        return sys_path

    # 2. Local Development Path (relative to script in src/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_assets = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "assets")
    if os.path.exists(local_assets):
        for name in icon_names:
            path = os.path.join(local_assets, name)
            if os.path.exists(path):
                return path

    # 3. Fallback to standard system icon name
    return "software-update-available"


ICON_PATH = find_brand_icon()
TEMPLATE_DIR = "/etc/flatpak-automatic/templates"
CONFIG_FILE = "/etc/flatpak-automatic/config.yaml"
