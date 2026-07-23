import os
import sys
from pathlib import Path

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/maintainer"))
)

import prepare_docs


def test_prepare_docs_copies_all_image_assets_and_transforms_paths(
    tmp_path: Path,
) -> None:
    # 1. Setup mock source structure
    src_dir = tmp_path / "src"
    docs_output_dir = tmp_path / "build_docs"

    src_dir.mkdir()
    assets_dir = src_dir / "assets"
    assets_dir.mkdir()
    docs_dir = src_dir / "docs"
    docs_dir.mkdir()
    github_dir = src_dir / ".github"
    github_dir.mkdir()

    # Create dummy asset files of various image formats
    (assets_dir / "banner.svg").write_text("<svg>banner</svg>")
    (assets_dir / "status-screenshot.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (assets_dir / "logo.jpg").write_bytes(b"\xff\xd8\xff")

    # Create dummy Markdown files
    readme_content = (
        '<img src="assets/banner.svg">\n'
        '<img src="assets/status-screenshot.png">\n'
        "![Logo](assets/logo.jpg)\n"
        "[AGENTS.md](AGENTS.md)\n"
    )
    (src_dir / "README.md").write_text(readme_content)
    (src_dir / "AGENTS.md").write_text('<img src="assets/banner.svg">')
    (src_dir / "LICENSE").write_text("MIT License")
    (docs_dir / "development.md").write_text('<img src="../assets/banner.svg">')
    (github_dir / "CONTRIBUTING.md").write_text('<img src="../assets/banner.svg">')

    # 2. Run prepare_docs
    prepare_docs.prepare_docs(str(src_dir), str(docs_output_dir))

    # 3. Assert asset files were copied
    out_assets = docs_output_dir / "assets"
    assert (out_assets / "banner.svg").exists()
    assert (out_assets / "status-screenshot.png").exists()
    assert (out_assets / "logo.jpg").exists()

    # 4. Assert content transformations
    index_md = (docs_output_dir / "index.md").read_text()
    assert 'src="assets/banner.svg"' in index_md
    assert 'src="assets/status-screenshot.png"' in index_md
    assert "![Logo](assets/logo.jpg)" in index_md
    assert "(agents.md)" in index_md

    agents_md = (docs_output_dir / "agents.md").read_text()
    assert 'src="../assets/banner.svg"' in agents_md

    dev_md = (docs_output_dir / "development.md").read_text()
    assert 'src="../assets/banner.svg"' in dev_md

    contrib_md = (docs_output_dir / "about" / "contributing.md").read_text()
    assert 'src="../../assets/banner.svg"' in contrib_md
