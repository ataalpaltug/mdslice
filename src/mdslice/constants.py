from __future__ import annotations

import re


# Matches opening/closing fences of backticks or tildes

_HEADER_RE = re.compile(r"^(#{1,6})\s*(.*)$")
_FENCE_OPEN_RE = re.compile(r"^([`~]{3,})(.*)$")
_FENCE_CLOSE_RE = re.compile(r"^([`~]{3,})\s*$")
_TABLE_RE = re.compile(r"^\|.*\|\s*$")
_IMAGE_RE = re.compile(r"^!\[[^\]]*\]\([^\)]*\)")
_QUOTE_RE = re.compile(r"^>\s?")
_LIST_RE = re.compile(r"^(?:[*+-]|\d+\.)\s+")
_SETEXT_H1_RE = re.compile(r"^={3,}\s*$")
_SETEXT_H2_RE = re.compile(r"^-{3,}\s*$")
