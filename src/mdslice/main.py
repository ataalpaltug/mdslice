from __future__ import annotations

from pathlib import Path
from typing import Union

from .models import MarkdownDocument
from .parser import parse_lines


def parse_markdown_file(file_path: Path) -> MarkdownDocument:
    file_path = check_path(file_path)
    with open(file_path, "r", encoding="utf-8") as fid:
        md = parse_lines(fid)
    md.add_path(file_path)
    return md


def from_text(text: str) -> MarkdownDocument:
    lines = text.splitlines(keepends=True)
    return parse_lines(lines)


def check_path(file_path: Union[Path, str]) -> Path:
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    return file_path
