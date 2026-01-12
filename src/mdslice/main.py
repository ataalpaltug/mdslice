from __future__ import annotations

from pathlib import Path
from typing import Union

from .models import MarkdownDocument
from .parser import parse_lines


def parse_markdown_file(file_path: Path) -> MarkdownDocument:
    """
    Parses a markdown file into a MarkdownDocument object.

    This function takes the path to a markdown file, validates it, reads its
    content, and processes it to create a `MarkdownDocument` object. The parsed
    document will have its associated file path added for reference.

    :param file_path: Path to the markdown file to be parsed.
    :type file_path: Path
    :return: Parsed markdown document.
    :rtype: MarkdownDocument
    """
    file_path = check_path(file_path)
    with open(file_path, "r", encoding="utf-8") as fid:
        md_doc = parse_lines(fid)
    md_doc.add_path(file_path)
    return md_doc


def from_text(text: str) -> MarkdownDocument:
    """
    Parse the given text into a MarkdownDocument.

    This function takes a string input, splits it into lines while maintaining
    line endings, and then processes those lines to generate a `MarkdownDocument`
    object, which represents the parsed structure of the input Markdown text.

    :param text: The text content to be processed. It is expected to be a string
        containing Markdown content.
    :return: A `MarkdownDocument` object representing the structured form of the
        input Markdown text.
    """
    lines = text.splitlines(keepends=True)
    return parse_lines(lines)


def check_path(file_path: Union[Path, str]) -> Path:
    """
    Checks the validity of a given file path. Converts the input to a Path object
    if it is provided as a string. Verifies that the file path exists.

    :param file_path: The file path to check. It can be a string or a Path object.
    :type file_path: Union[Path, str]
    :raises FileNotFoundError: If the provided file path does not exist.
    :return: The input file path converted to a Path object.
    :rtype: Path
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    return file_path
