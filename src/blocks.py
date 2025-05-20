from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode
from textnode_split import text_to_text_nodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED = 'unordered_list'
    ORDERED = 'ordered_list'

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    processed_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != '':
            processed_blocks.append(stripped)
    return processed_blocks

def block_to_block_type(block):
    lines = block.split('\n')

    # Heading: starts with 1-6 '#' followed by space
    if lines[0].startswith('#'):
        header, _, rest = lines[0].partition(' ')
        if 1 <= len(header) <= 6 and all(c == '#' for c in header):
            return BlockType.HEADING

    # Code block: starts and ends with ```
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE

    # Quote: every line starts with '>'
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED

    # Ordered list: every line starts with 'N. ' where N is incrementing
    if all(
        line.startswith(f"{i+1}. ") for i, line in enumerate(lines)
    ): return BlockType.ORDERED

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                new_node = paragraph_to_html_node(block)
            case BlockType.HEADING:
                new_node = heading_to_html_node(block)
            case BlockType.CODE:
                new_node = code_to_html_node(block)
            case BlockType.QUOTE:
                new_node = quote_to_html_node(block)
            case BlockType.UNORDERED:
                new_node = unordered_to_html_node(block)
            case BlockType.ORDERED:
                new_node = ordered_to_html_node(block)
        html_nodes.append(new_node)

    return ParentNode('div', html_nodes)

def text_to_parent_node(tag, text):
    html_nodes = []
    text_nodes = text_to_text_nodes(text)
    for node in text_nodes:
        html_nodes.append(
            text_node_to_html_node(node)
        )
    return ParentNode(tag, html_nodes)

def block_to_lines(block):
    return (line.strip() for line in block.split('\n'))

# deletes from each line everything before, and including, the first appearance of 'symbol' char
def clean_lines(lines, symbol):
    return (line.split(symbol, 1)[1].lstrip() for line in lines)

def paragraph_to_html_node(block):
    lines = block_to_lines(block)
    return text_to_parent_node('p', ' '.join(lines))

def heading_to_html_node(block):
    count = 1
    for char in block[1:]:
        if char == '#':
            count += 1
        else: break
    tag = f'h{count}'

    lines = block_to_lines(block[count+1:])
    return text_to_parent_node(tag, ' '.join(lines))

def code_to_html_node(code):
    html_node = LeafNode('code', code[3:-3])
    return ParentNode('pre', [html_node])

def quote_to_html_node(block):
    lines = clean_lines(block_to_lines(block), '>')
    return text_to_parent_node('blockquote', ' '.join(lines))

def list_to_html_node(tag, block):
    children = []
    lines = clean_lines(block_to_lines(block), ' ')
    for line in lines:
        children.append(
            text_to_parent_node('li', line)
        )
    return ParentNode(tag, children)

def unordered_to_html_node(block):
    return list_to_html_node('ul', block)

def ordered_to_html_node(block):
    return list_to_html_node('ol', block)
