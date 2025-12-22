from __future__ import annotations

from pathlib import Path

from .models import MarkdownDocument
from .parser import parse_lines


def parse_markdown_file(file_path: Path) -> MarkdownDocument:
    # todo: add file path check
    with open(file_path, "r", encoding="utf-8") as fid:
        md = parse_lines(fid)
    md.add_path(file_path)
    return md


def from_text(text: str) -> "MarkdownDocument":
    lines = text.splitlines(keepends=True)
    return parse_lines(lines)
