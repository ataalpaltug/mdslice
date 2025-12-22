from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, auto
from pathlib import Path
from typing import Optional, Any, List, Callable


class SectionType(IntEnum):
    NONE = auto()
    HEADER = auto()
    INFO = auto()
    PARAGRAPH = auto()
    LIST = auto()
    CODE = auto()
    TABLE = auto()
    IMAGE = auto()
    QUOTE = auto()


#@dataclass(slots=True) todo: check memory with slots
@dataclass
class ParsedSection:
    """A parsed, typed chunk of Markdown content.

    - For non-header sections, `header_depth` remains 0.
    - For headers, `header_depth` is 1-6 according to the leading `#` count.
    - Optional `meta` can carry extra information (e.g., code block language).
    """
    type: SectionType
    content: str
    header_depth: int = 0
    meta: Optional[dict[str, Any]] = None

    def is_header(self) -> bool:
        return self.type == SectionType.HEADER

    def __str__(self) -> str:
        if self.type == SectionType.HEADER:
            return f"<HEADER h{self.header_depth}: {self.content!r}>"
        return f"<{self.type.name}: {self.content!r}>"


class MarkdownDocument:
    """Object-oriented representation of a Markdown file and its parsed sections."""
    # todo: Front Matter support
    # todo: make this class Context Managers

    def __init__(
        self,
        sections: Optional[List[ParsedSection]] = None,
        path: Optional[Path] = None,
    ) -> None:
        self.path: Optional[Path] = path
        if sections is None:
            self.sections: List[ParsedSection] = []
        else:
            self.sections = sections

    def add_section(self, section: ParsedSection) -> None:
        if isinstance(section, ParsedSection):
            self.sections.append(section)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path) if self.path is not None else None,
            "sections": [
                {
                    "type": s.type.name,
                    "content": s.content,
                    "header_depth": s.header_depth,
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
            result = [s for s in result if s.header_depth >= min_depth]
        if max_depth is not None:
            result = [s for s in result if s.header_depth <= max_depth]
        return result

    def find(
        self, predicate: Callable[[ParsedSection], bool]
    ) -> Optional[ParsedSection]:
        return next((s for s in self.sections if predicate(s)), None)

    # End of class

    def of_type(self):
        ...

    def __getitem__(self): ...

    def __iter__(self): ...

    def search(self): ...
    '''Should allow the user to search by regex'''

    def plain_markdown(self): ...
    '''Should reconstruct markdown from the self.sections'''

    @classmethod
    def _unused(cls):
        # placeholder to keep search/replace boundaries clear (no-op)
        return None
