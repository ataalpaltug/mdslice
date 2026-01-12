from __future__ import annotations

import unittest
from mdslice import ParsedSection, SectionType


class TestModels(unittest.TestCase):
    def test_section_type_membership(self):
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
        paragraph = ParsedSection(type=SectionType.PARAGRAPH, content="Hello")
        self.assertFalse(paragraph.is_header())
        self.assertEqual(paragraph.depth, 0)

        # Header marks is_header True and has explicit depth
        header = ParsedSection(type=SectionType.HEADER, content="Title", depth=2)
        self.assertTrue(header.is_header())
        self.assertEqual(header.depth, 2)

    def test_parsed_section_str_formats(self):
        header = ParsedSection(type=SectionType.HEADER, content="Title", depth=3)
        self.assertEqual(str(header), "<HEADER: 'Title'>")

        p = ParsedSection(type=SectionType.PARAGRAPH, content="Some text")
        self.assertEqual(str(p), "<PARAGRAPH: 'Some text'>")
