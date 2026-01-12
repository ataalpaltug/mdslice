from __future__ import annotations

from typing import List, Optional, Iterable, Any

from .constants import (
    _HEADER_RE,
    _FENCE_OPEN_RE,
    _FENCE_CLOSE_RE,
    _SETEXT_H1_RE,
    _SETEXT_H2_RE,
    PATTERNS,
)
from .models import ParsedSection, SectionType, MarkdownDocument


def _flush(
    buffer: List[str],
    md: MarkdownDocument,
    sec_type: SectionType,
    header_depth: int = 0,
    meta: Optional[dict[str, Any]] = None,
) -> None:
    """
    Flushes the provided buffer content into a MarkdownDocument section and clears the buffer.

    This function processes the accumulated text content in the buffer and appends it as a
    section to the specified MarkdownDocument instance. It is primarily responsible for creating
    a section with the given type, content, header depth, and optional metadata. Once the section
    is added, the buffer is cleared to allow for subsequent content accumulation.

    :param buffer: A list of strings representing the accumulated content to process and add
        to the MarkdownDocument. If empty, no operation will be performed.
    :param md: The MarkdownDocument instance to which the new section will be added.
    :param sec_type: The SectionType defining the type of section to be created.
    :param header_depth: The depth of the section's header, often based on its hierarchical
        level. Default is 0.
    :param meta: An optional dictionary containing metadata associated with the section.

    :return: None
    """
    if not buffer:
        return
    content = "".join(buffer).rstrip("\n")
    md.add_section(
        ParsedSection(type=sec_type, content=content, depth=header_depth, meta=meta)
    )
    buffer.clear()


def parse_lines(lines: Iterable[str]) -> MarkdownDocument:
    """
    Parses an iterable of strings into a structured Markdown document.

    This function processes lines of text and constructs a `MarkdownDocument` object by
    interpreting various Markdown elements such as headers, code blocks, lists, tables,
    and paragraphs. It handles both fenced and indented code blocks, Setext-style headers,
    and other Markdown-specific features. The function ensures each recognized Markdown
    section is appropriately parsed and added to the hierarchical structure of the output.

    :param lines: An iterable of strings representing lines of a Markdown document.
        Each string should represent a single line, and newlines should already be stripped.
    :return: A `MarkdownDocument` instance containing the structured representation of
        the parsed Markdown input.
    :rtype: MarkdownDocument
    """
    md = MarkdownDocument()
    current_buffer: List[str] = []
    current_type: SectionType = SectionType.NONE
    current_header_depth = 0

    in_code_block = False
    fence_char: str = ""
    fence_len: int = 0
    code_lang: Optional[str] = None

    def flush_current():
        nonlocal md, current_type, current_header_depth, code_lang
        if current_type == SectionType.NONE:
            return

        meta = (
            {"lang": code_lang}
            if current_type == SectionType.CODE and code_lang
            else None
        )
        _flush(current_buffer, md, current_type, current_header_depth, meta=meta)
        current_type = SectionType.NONE
        current_header_depth = 0
        code_lang = None

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
                flush_current()
                in_code_block = False
                fence_char = ""
                fence_len = 0
            continue

        # Blank line flushes
        if stripped == "" or stripped == "&nbsp;":
            flush_current()
            continue

        m_open = _FENCE_OPEN_RE.match(stripped)
        if m_open:
            flush_current()
            fence = m_open.group(1)
            rest = (m_open.group(2) or "").strip()
            code_lang = rest.split()[0] if rest else None
            in_code_block = True
            current_type = SectionType.CODE
            fence_char = fence[0]
            fence_len = len(fence)
            current_buffer.append(raw_line)
            continue

        # Header
        m_header = _HEADER_RE.match(stripped)
        if m_header:
            flush_current()
            hashes, content = m_header.groups()
            md.add_section(
                ParsedSection(SectionType.HEADER, content.strip(), depth=len(hashes))
            )
            continue

        # Setext Header
        m1 = _SETEXT_H1_RE.match(stripped)
        m2 = _SETEXT_H2_RE.match(stripped)
        if (m1 or m2) and current_type == SectionType.PARAGRAPH:
            # Re-interpret previous paragraph as header
            content = "".join(current_buffer).strip()
            current_buffer.clear()
            current_type = SectionType.NONE
            depth = 1 if m1 else 2
            md.add_section(ParsedSection(SectionType.HEADER, content, depth=depth))
            continue

        # Pattern search for list, table, etc.
        matched = False
        for regex, sec_type in PATTERNS:
            if regex.match(stripped):
                if sec_type == SectionType.IMAGE:
                    flush_current()
                    md.add_section(ParsedSection(sec_type, stripped))
                else:
                    if current_type not in (SectionType.NONE, sec_type):
                        flush_current()
                    current_type = sec_type
                    current_buffer.append(raw_line)
                matched = True
                break

        # Flush last section
        if not matched:
            if current_type not in (SectionType.NONE, SectionType.PARAGRAPH):
                flush_current()
            current_type = SectionType.PARAGRAPH
            current_buffer.append(raw_line)

    flush_current()
    return md
