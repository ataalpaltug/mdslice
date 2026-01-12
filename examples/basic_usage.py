import json
from mdslice import parse_markdown_file
from pathlib import Path


def main():
    readme_path = Path(__file__).parent.parent / "README.md"
    md_doc = parse_markdown_file(Path(__file__).parent / "sample.md")

    for sec in md_doc.sections:
        print(sec)

    print(md_doc.to_dict())


if __name__ == "__main__":
    main()
