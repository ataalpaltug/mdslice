from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mdslice import parse_markdown_file, SectionType
from tests.constants import MD_SAMPLE


class TestParser(unittest.TestCase):
    def _write_temp_md(self, tmp_dir: str, name: str, content: str) -> Path:
        md_path = Path(tmp_dir) / name
        md_path.write_text(content, encoding="utf-8")
        return md_path

    def test_parse_markdown_document_and_path(self):
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "sample.md", MD_SAMPLE)
            md_doc = parse_markdown_file(md_path)

            # Path retained
            self.assertEqual(Path(md_path), md_doc.path)

            # Ensure we have multiple sections parsed
            self.assertEqual(len(md_doc.sections), 7)

            # Validate first section is a header h1
            first = md_doc.sections[0]
            self.assertEqual(first.type, SectionType.HEADER)
            self.assertEqual(first.depth, 1)
            self.assertEqual(first.content, "Title")

            # Validate paragraph aggregation
            para = next(s for s in md_doc.sections if s.type == SectionType.PARAGRAPH)
            self.assertIn("Paragraph line 1", para.content)
            self.assertIn("continues here", para.content)

            # Validate list grouping
            lst = next(s for s in md_doc.sections if s.type == SectionType.LIST)
            self.assertIn("- item one", lst.content)
            self.assertIn("- item two", lst.content)

            # Validate quote grouping
            quote = next(s for s in md_doc.sections if s.type == SectionType.QUOTE)
            self.assertIn("> quote line 1", quote.content)
            self.assertIn("> quote line 2", quote.content)

            # Validate code block preserves fences
            code = next(s for s in md_doc.sections if s.type == SectionType.CODE)
            self.assertTrue(code.content.startswith("```\n"))
            self.assertTrue(code.content.rstrip("\n").endswith("\n```"))

            # Validate table grouping
            table = next(s for s in md_doc.sections if s.type == SectionType.TABLE)
            self.assertIn("| h1 | h2 |", table.content)
            self.assertIn("|----|----|", table.content)

            # Validate image detection
            image = next(s for s in md_doc.sections if s.type == SectionType.IMAGE)
            self.assertEqual(image.content.strip(), "![alt](path/to/img.png)")

    def test_blank_line_and_nbsp_flush(self):
        content = """Paragraph before

&nbsp
Paragraph after
"""
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "nbsp.md", content)
            doc = parse_markdown_file(md_path)
            paras = [s for s in doc.sections if s.type == SectionType.PARAGRAPH]
            self.assertEqual(len(paras), 2)

    def test_switching_blocks_flushes(self):
        content = """First line
- list item
Second para
"""
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "flush.md", content)
            doc = parse_markdown_file(md_path)
            types = [s.type for s in doc.sections]
            # Expect: paragraph, list, paragraph
            self.assertEqual(types, [SectionType.PARAGRAPH, SectionType.LIST, SectionType.PARAGRAPH])

    def test_empty_file_produces_no_sections(self):
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "empty.md", "")
            doc = parse_markdown_file(md_path)
            self.assertEqual(doc.sections, [])

    def test_multiple_headers(self):
        content = """# H1
## H2
### H3
#### H4
##### H5
###### H6
"""
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "headers.md", content)
            doc = parse_markdown_file(md_path)
            depths = [s.depth for s in doc.sections if s.type == SectionType.HEADER]
            self.assertEqual(depths, [1, 2, 3, 4, 5, 6])

    def test_complex_code_blocks(self):
        content = """```python
def foo():
    pass
```
~~~javascript
console.log("hello");
~~~
"""
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "code.md", content)
            doc = parse_markdown_file(md_path)
            codes = [s for s in doc.sections if s.type == SectionType.CODE]
            self.assertEqual(len(codes), 2)
            self.assertEqual(codes[0].meta, {"lang": "python"})
            self.assertEqual(codes[1].meta, {"lang": "javascript"})

    def test_mixed_content_without_blank_lines(self):
        content = """# Header
Paragraph
- List
> Quote
| Table |
![Image](img.png)
"""
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "mixed.md", content)
            doc = parse_markdown_file(md_path)
            types = [s.type for s in doc.sections]
            expected = [
                SectionType.HEADER,
                SectionType.PARAGRAPH,
                SectionType.LIST,
                SectionType.QUOTE,
                SectionType.TABLE,
                SectionType.IMAGE
            ]
            self.assertEqual(types, expected)

    def test_setext_headers(self):
        content = """Title 1
=======
Title 2
-------
Paragraph
"""
        with TemporaryDirectory() as td:
            md_path = self._write_temp_md(td, "setext.md", content)
            doc = parse_markdown_file(md_path)
            headers = [s for s in doc.sections if s.type == SectionType.HEADER]
            self.assertEqual(len(headers), 2)
            self.assertEqual(headers[0].content, "Title 1")
            self.assertEqual(headers[0].depth, 1)
            self.assertEqual(headers[1].content, "Title 2")
            self.assertEqual(headers[1].depth, 2)


if __name__ == "__main__":
    unittest.main()
