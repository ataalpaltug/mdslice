from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, auto
from pathlib import Path
from typing import Optional, Any, List, Callable


class SectionType(IntEnum):
    """
    Represents different types of sections used within a document or content structure.

    This enumeration provides constants to identify and differentiate sections.
    """

    NONE = auto()
    HEADER = auto()
    INFO = auto()
    PARAGRAPH = auto()
    LIST = auto()
    CODE = auto()
    TABLE = auto()
    IMAGE = auto()
    QUOTE = auto()


# @dataclass(slots=True) todo: check memory with slots
@dataclass
class ParsedSection:
    """
    Represents a parsed section of a document.

    This class is used to model a section of a document that has been parsed.
    It holds details about the section's type, content, depth in the document
    hierarchy, and any associated metadata. This is useful for organizing and
    processing structured documents.

    :ivar type: The type of the section, typically indicating
        its role (e.g., HEADER, PARAGRAPH, etc.).
    :type type: SectionType
    :ivar content: The textual content of the section.
    :type content: str
    :ivar depth: The hierarchical depth of the section within the
        document, defaulting to 0 if not specified.
    :type depth: int
    :ivar meta: Additional metadata associated with the section,
        such as attributes or properties. Default is None if no
        metadata is provided.
    :type meta: Optional[dict[str, Any]]
    """

    type: SectionType
    content: str
    depth: int = 0
    meta: Optional[dict[str, Any]] = None

    def is_header(self) -> bool:
        return self.type == SectionType.HEADER

    def __str__(self) -> str:
        return f"<{self.type.name}: {self.content!r}>"


class MarkdownDocument:
    """
    Represents a markdown document composed of parsed sections and an optional file path.

    This class provides functionality to manage the structure of a markdown document,
    including adding sections, associating a file path, and converting the document
    into a dictionary format. It also supports filtering and searching operations
    on the document's headers or sections.

    :ivar sections: A list of parsed sections that compose the markdown document.
    :type sections: List[ParsedSection]
    :ivar path: An optional file path associated with the markdown document.
    :type path: Optional[Path]
    """

    def __init__(
        self,
        sections: Optional[List[ParsedSection]] = None,
        f_path: Optional[Path] = None,
    ) -> None:
        self.path: Optional[Path] = f_path
        if sections is None:
            self.sections: List[ParsedSection] = []
        else:
            self.sections = sections

    def add_section(self, section: ParsedSection) -> None:
        if isinstance(section, ParsedSection):
            self.sections.append(section)

    def add_path(self, f_path: Path) -> None:
        self.path = f_path

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path) if self.path is not None else None,
            "sections": [
                {
                    "type": s.type.name,
                    "content": s.content,
                    "header_depth": s.depth,
                    **({"meta": s.meta} if s.meta is not None else {}),
                }
                for s in self.sections
            ],
        }

    def headers(
        self, min_depth: Optional[int] = None, max_depth: Optional[int] = None
    ) -> List[ParsedSection]:
        result = [s for s in self.sections if s.type == SectionType.HEADER]
        if min_depth is not None:
            result = [s for s in result if s.depth >= min_depth]
        if max_depth is not None:
            result = [s for s in result if s.depth <= max_depth]
        return result

    def find(
        self, predicate: Callable[[ParsedSection], bool]
    ) -> Optional[ParsedSection]:
        return next((s for s in self.sections if predicate(s)), None)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, f_path: Path) -> None:
        if isinstance(f_path, str):
            self._path = Path(f_path)
        self._path = f_path

    def of_type(self): ...

    def __getitem__(self): ...

    def __iter__(self): ...

    def search(self): ...

    """Should allow the user to search by regex"""

    def plain_markdown(self): ...

    """Should reconstruct markdown from the self.sections"""
