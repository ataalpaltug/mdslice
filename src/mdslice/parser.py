from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Iterable, Any

from .constants import (
    _HEADER_RE,
    _FENCE_OPEN_RE,
    _FENCE_CLOSE_RE,
    _TABLE_RE,
    _IMAGE_RE,
    _QUOTE_RE,
    _LIST_RE,
)
from .models import ParsedSection, SectionType, MarkdownDocument


def _flush(
    buffer: List[str],
    sections: List[ParsedSection],
    sec_type: SectionType,
    header_depth: int = 0,
    meta: Optional[dict[str, Any]] = None,
) -> None:
    if not buffer:
        return
    content = "".join(buffer).rstrip("\n")
    sections.append(
        ParsedSection(
            type=sec_type, content=content, header_depth=header_depth, meta=meta
        )
    )
    buffer.clear()


def parse_markdown_file(file_path: Path) -> MarkdownDocument:
    with open(file_path, "r", encoding="utf-8") as fid:
        sections = parse_lines(fid)
    return MarkdownDocument(sections=sections, path=file_path)


def from_text(text: str, path: Optional[Path] = None) -> "MarkdownDocument":
    lines = text.splitlines(keepends=True)
    sections = parse_lines(lines)
    return MarkdownDocument(sections=sections, path=path)


def parse_lines(lines: Iterable[str]) -> List[ParsedSection]:
    """Parse an iterable of lines into a list of ParsedSection.

    This is a lightweight, line-oriented parser intended for simple extraction
    of major block-level elements, not a full CommonMark implementation.
    """
    # todo: Sections.LINK to extract links from md files
    sections: List[ParsedSection] = []
    current_buffer: List[str] = []
    current_type: SectionType = SectionType.NONE
    current_header_depth = 0

    in_code_block = False
    fence_char: str = ""
    fence_len: int = 0
    code_lang: Optional[str] = None

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if in_code_block:
            current_buffer.append(raw_line)
            m_close = _FENCE_CLOSE_RE.match(stripped)
            if (
                m_close
                and fence_char
                and m_close.group(1)[0] == fence_char
                and len(m_close.group(1)) >= fence_len
            ):
                # end of code block
                _flush(
                    current_buffer,
                    sections,
                    SectionType.CODE,
                    meta={"lang": code_lang} if code_lang else None,
                )
                in_code_block = False
                current_type = SectionType.NONE
                fence_char = ""
                fence_len = 0
                code_lang = None
            continue

        # Blank line flushes paragraph/list/table/quote buffers
        if stripped == "" or stripped == "&nbsp" or stripped == "&nbsp;":
            if current_type != SectionType.NONE:
                _flush(current_buffer, sections, current_type, current_header_depth)
                current_type = SectionType.NONE
                current_header_depth = 0
            continue

        # Fenced code block start
        m_open = _FENCE_OPEN_RE.match(stripped)
        if m_open:
            if current_type != SectionType.NONE:
                _flush(current_buffer, sections, current_type, current_header_depth)
            fence = m_open.group(1)
            rest = (m_open.group(2) or "").strip()
            # Determine language hint as first token in rest if present
            code_lang = rest.split()[0] if rest else None
            in_code_block = True
            current_type = SectionType.CODE
            current_header_depth = 0
            fence_char = fence[0]
            fence_len = len(fence)
            current_buffer.append(raw_line)
            continue

        # Header
        m = _HEADER_RE.match(stripped)
        # todo: Support for Setext headers:
        # todo: Supporting === and --- underlines for H1 and H2
        if m:
            # Flush previous buffer as paragraph/list/table
            if current_type != SectionType.NONE:
                _flush(current_buffer, sections, current_type, current_header_depth)
            hashes, content = m.groups()
            depth = len(hashes)
            sections.append(
                ParsedSection(SectionType.HEADER, content.strip(), header_depth=depth)
            )
            current_type = SectionType.NONE
            current_header_depth = 0
            continue

        # Table rows (simple heuristic)
        if _TABLE_RE.match(stripped):
            if current_type not in (SectionType.NONE, SectionType.TABLE):
                _flush(current_buffer, sections, current_type, current_header_depth)
            current_type = SectionType.TABLE
            current_header_depth = 0
            current_buffer.append(raw_line)
            continue

        # Image
        if _IMAGE_RE.match(stripped):
            if current_type != SectionType.NONE:
                _flush(current_buffer, sections, current_type, current_header_depth)
            sections.append(ParsedSection(SectionType.IMAGE, stripped))
            current_type = SectionType.NONE
            continue

        # Block quote
        if _QUOTE_RE.match(stripped):
            if current_type not in (SectionType.NONE, SectionType.QUOTE):
                _flush(current_buffer, sections, current_type, current_header_depth)
            current_type = SectionType.QUOTE
            current_header_depth = 0
            current_buffer.append(raw_line)
            continue

        # List item
        #todo: Nested Lists
        if _LIST_RE.match(stripped):
            if current_type not in (SectionType.NONE, SectionType.LIST):
                _flush(current_buffer, sections, current_type, current_header_depth)
            current_type = SectionType.LIST
            current_header_depth = 0
            current_buffer.append(raw_line)
            continue

        # Default to paragraph text, append line (preserve original spacing)
        if current_type not in (SectionType.NONE, SectionType.PARAGRAPH):
            _flush(current_buffer, sections, current_type, current_header_depth)
        current_type = SectionType.PARAGRAPH
        current_header_depth = 0
        current_buffer.append(raw_line)

    # Flush tail
    if current_type != SectionType.NONE:
        _flush(current_buffer, sections, current_type, current_header_depth)

    return sections
