from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional, Any


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
