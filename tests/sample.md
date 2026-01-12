# Sample Markdown Document

This document contains examples of various Markdown elements supported by `mdslice`.

## Headers

Headers are defined using one to six `#` characters.

### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

## Paragraphs

This is a simple paragraph. It can span multiple lines
and contain various text formatting like **bold**, *italic*, and `inline code`.

Another paragraph separated by a blank line.

## Info Sections

> [!INFO]
> This is an information block. Note that the this section will be parsed as QUOTE.

## Lists

### Unordered List
* Item 1
* Item 2
    * Sub-item 2a
    * Sub-item 2b
* Item 3

### Ordered List
1. First item
2. Second item
3. Third item

## Code Blocks

```python
def hello_world():
    print("Hello, mdslice!")

hello_world()
```

```javascript
console.log("This is a javascript code block");
```

## Tables

| Feature | Description | Status |
| :--- | :--- | :--- |
| Parsing | Structured document parsing | Done |
| Slicing | Manipulating sections | In Progress |
| Formatting | Exporting to various formats | Planned |

## Images

![mdslice logo](https://raw.githubusercontent.com/ataalpaltug/mdslice/main/docs/logo.png)

## Quotes

> Markdown is a lightweight markup language with plain-text-formatting syntax.
> Its design allows it to be converted to many formats, but many toolchains
> simply convert it to HTML.
