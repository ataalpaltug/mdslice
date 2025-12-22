from __future__ import annotations

from pathlib import Path

from mdslice import MarkdownDocument
from mdslice.parser import parse_lines


def parse_markdown_file(file_path: Path) -> MarkdownDocument:
    # todo: add file path check
    with open(file_path, "r", encoding="utf-8") as fid:
        sections = parse_lines(fid)
    return MarkdownDocument(sections=sections, path=file_path)


def from_text(text: str) -> "MarkdownDocument":
    lines = text.splitlines(keepends=True)
    sections = parse_lines(lines)
    return MarkdownDocument(sections=sections)
