from __future__ import annotations

import unittest
from mdslice import ParsedSection, SectionType


class TestModels(unittest.TestCase):
    def test_section_type_membership(self):
        # Basic sanity: all expected names exist
        names = {e.name for e in SectionType}
        self.assertTrue({
            "NONE",
            "HEADER",
            "INFO",
            "PARAGRAPH",
            "LIST",
            "CODE",
            "TABLE",
            "IMAGE",
            "QUOTE",
        }.issubset(names))

    def test_parsed_section_is_header_and_defaults(self):
        # Non-header defaults to header_depth 0
        p = ParsedSection(type=SectionType.PARAGRAPH, content="Hello")
        self.assertFalse(p.is_header())
        self.assertEqual(p.header_depth, 0)

        # Header marks is_header True and has explicit depth
        h = ParsedSection(type=SectionType.HEADER, content="Title", header_depth=2)
        self.assertTrue(h.is_header())
        self.assertEqual(h.header_depth, 2)

    def test_parsed_section_str_formats(self):
        h = ParsedSection(type=SectionType.HEADER, content="Title", header_depth=3)
        self.assertEqual(str(h), "<HEADER h3: 'Title'>")

        p = ParsedSection(type=SectionType.PARAGRAPH, content="Some text")
        self.assertEqual(str(p), "<PARAGRAPH: 'Some text'>")
