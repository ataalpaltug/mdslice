# mdslice

`mdslice` is a lightweight Python package for slicing, parsing, and manipulating Markdown files. It parses Markdown content into a structured object model, allowing you to easily access headers, paragraphs, code blocks, and other elements.

## Features

- **Structured Parsing**: Converts Markdown into a `MarkdownDocument` composed of `ParsedSection` objects.
- **Section Categorization**: Identifies various Markdown elements like headers, code blocks, lists, tables, images, and quotes.
- **Flexible Input**: Parse from files or directly from strings.
- **Export to Dictionary**: Convert parsed documents to a dictionary format for easy JSON serialization.

## Installation

You can install `mdslice` using `pip`:

```bash
pip install mdslice
```

Or using `uv`:

```bash
uv add mdslice
```

## Quick Start

### Parsing a Markdown File

```python
from pathlib import Path
from mdslice import parse_markdown_file

# Parse a file
doc = parse_markdown_file(Path("README.md"))

# Iterate through sections
for section in doc.sections:
    print(f"Type: {section.type.name}, Content: {section.content[:50]}...")
```

### Parsing Markdown Text

```python
from mdslice import from_text

md_text = """
# My Title
This is a paragraph.

\```python
print("Hello World")
\```
"""

doc = from_text(md_text)

# Access headers
headers = doc.headers()
for header in headers:
    print(f"Header (Level {header.depth}): {header.content}")
```

## Advanced Usage

### Filtering Headers by Depth

```python
# Get only H1 and H2 headers
top_headers = doc.headers(min_depth=1, max_depth=2)
```

### Finding a Specific Section

```python
from mdslice import SectionType

# Find the first Python code block
python_block = doc.find(lambda s: s.type == SectionType.CODE and s.meta.get("lang") == "python")

if python_block:
    print(f"Found code:\n{python_block.content}")
```

### Converting to Dictionary

```python
import json

doc_dict = doc.to_dict()
print(json.dumps(doc_dict, indent=2))
```

## Models

### `MarkdownDocument`
The main container for a parsed Markdown file.
- `sections`: List of `ParsedSection` objects.
- `path`: Optional `Path` to the source file.
- `headers(min_depth, max_depth)`: Returns a filtered list of header sections.
- `find(predicate)`: Finds the first section matching the predicate.
- `to_dict()`: Converts the document to a serializable dictionary.

### `ParsedSection`
Represents a single element in the Markdown document.
- `type`: A `SectionType` enum value.
- `content`: The raw text content of the section.
- `depth`: The header level (1-6) for headers, 0 otherwise.
- `meta`: Dictionary containing metadata (e.g., `lang` for code blocks).

### `SectionType`
An enum representing the type of section:
- `HEADER`
- `PARAGRAPH`
- `CODE`
- `LIST`
- `TABLE`
- `IMAGE`
- `QUOTE`
- `INFO`
- `NONE`

## Development

`mdslice` uses `uv` for dependency management and `nox` for multi-version testing.

## License

MIT
