#!/usr/bin/env python3
"""Script to generate terminal status screenshot for README using rich, chrome/cairosvg."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from PIL import Image, ImageChops
from rich.console import Console
from rich.terminal_theme import TerminalTheme
from rich.text import Text


# Authentic terminal color palette matching standard terminal emulators (with rich purple HEADER)
VIBRANT_TERMINAL_THEME = TerminalTheme(
    background=(41, 41, 41),
    foreground=(248, 248, 242),
    normal=[
        (0, 0, 0),
        (255, 85, 85),
        (80, 250, 123),
        (241, 250, 140),
        (139, 233, 253),
        (189, 147, 249),  # Purple (#BD93F9)
        (0, 229, 255),
        (191, 191, 191),
    ],
    bright=[
        (98, 114, 164),
        (255, 110, 110),
        (105, 255, 148),
        (255, 255, 165),
        (120, 190, 255),
        (189, 147, 249),  # Bright Purple (#BD93F9)
        (0, 229, 255),
        (255, 255, 255),
    ],
)


def crop_margins(image_path: Path) -> None:
    """Crop white outer margins from generated screenshot."""
    im = Image.open(image_path)
    im_rgb = im.convert("RGB")
    bg = Image.new("RGB", im_rgb.size, (255, 255, 255))
    diff = ImageChops.difference(im_rgb, bg)
    bbox = diff.getbbox()
    if bbox:
        cropped = im.crop(bbox)
        cropped.save(image_path)


def convert_svg_to_png(svg_path: Path, output_png: Path) -> None:
    """Convert SVG to PNG using Google Chrome/Chromium if available, falling back to cairosvg."""
    chrome_bin = shutil.which("google-chrome") or shutil.which("chromium")

    if chrome_bin:
        temp_png = svg_path.parent / "temp_chrome.png"
        cmd = [
            chrome_bin,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--screenshot={temp_png}",
            "--window-size=1000,800",
            str(svg_path),
        ]
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if temp_png.exists():
            crop_margins(temp_png)
            shutil.move(temp_png, output_png)
        return

    # Fallback to cairosvg
    import cairosvg

    svg_data = svg_path.read_text(encoding="utf-8")
    svg_data = re.sub(
        r"font-family:\s*([^;]+);",
        r"font-family: \1, 'Noto Color Emoji', 'Noto Emoji', 'Segoe UI Emoji', 'Apple Color Emoji', 'Symbola', monospace;",
        svg_data,
    )
    cairosvg.svg2png(
        bytestring=svg_data.encode("utf-8"),
        write_to=str(output_png),
    )


def generate_screenshot() -> None:
    """Run status command as root (or fallback), capture terminal output with ASCII header banner, and export to PNG image."""
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent
    assets_dir = repo_root / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    output_png = assets_dir / "status-screenshot.png"
    temp_svg = assets_dir / "temp_status.svg"

    src_dir = str(repo_root / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    from flatpak_automatic.cli import banner

    cli_script = repo_root / "src" / "flatpak-automatic.py"

    output_text = None

    # Try non-interactive sudo first, then interactive sudo, then non-root execution
    attempts = [
        ["sudo", "-n", sys.executable, str(cli_script), "-s"],
        ["sudo", sys.executable, str(cli_script), "-s"],
        [sys.executable, str(cli_script), "-s"],
    ]

    if os.geteuid() == 0:
        attempts.insert(0, [sys.executable, str(cli_script), "-s"])

    for cmd in attempts:
        try:
            result = subprocess.run(
                cmd,
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            output_text = result.stdout.strip()
            if output_text:
                break
        except Exception:
            continue

    if not output_text:
        # Ultimate fallback
        result = subprocess.run(
            [sys.executable, str(cli_script), "-s"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        output_text = result.stdout.strip()

    banner_text = banner()
    full_output = f"{banner_text}\n{output_text}"

    console = Console(record=True, width=100)
    rich_text = Text.from_ansi(full_output)
    console.print(rich_text)

    svg_data = console.export_svg(
        title="sudo flatpak-automatic -s", theme=VIBRANT_TERMINAL_THEME
    )
    temp_svg.write_text(svg_data, encoding="utf-8")

    convert_svg_to_png(temp_svg, output_png)

    if temp_svg.exists():
        temp_svg.unlink()

    print(f"Successfully generated screenshot at: {output_png}")


if __name__ == "__main__":
    generate_screenshot()
