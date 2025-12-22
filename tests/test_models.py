from __future__ import annotations

from mdslice import ParsedSection, SectionType


def test_section_type_membership():
    # Basic sanity: all expected names exist
    names = {e.name for e in SectionType}
    assert {
        "NONE",
        "HEADER",
        "INFO",
        "PARAGRAPH",
        "LIST",
        "CODE",
        "TABLE",
        "IMAGE",
        "QUOTE",
    }.issubset(names)


def test_parsed_section_is_header_and_defaults():
    # Non-header defaults to header_depth 0
    p = ParsedSection(type=SectionType.PARAGRAPH, content="Hello")
    assert not p.is_header()
    assert p.header_depth == 0

    # Header marks is_header True and has explicit depth
    h = ParsedSection(type=SectionType.HEADER, content="Title", header_depth=2)
    assert h.is_header()
    assert h.header_depth == 2


def test_parsed_section_str_formats():
    h = ParsedSection(type=SectionType.HEADER, content="Title", header_depth=3)
    assert str(h) == "<HEADER h3: 'Title'>"

    p = ParsedSection(type=SectionType.PARAGRAPH, content="Some text")
    assert str(p) == "<PARAGRAPH: 'Some text'>"
