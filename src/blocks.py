import re
from enum import Enum

from leafnode import LeafNode # HTML node with value and without children
from parentnode import ParentNode # HTML node without value, but with children
from textnode_split import text_to_text_nodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED = 'unordered_list'
    ORDERED = 'ordered_list'

def block_to_block_type(block):
    lines = block_to_lines(block)

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

# returns appropriate convert_block_to_parent_node function based on block_type
def block_type_to_html_func(type):
    match type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node
        case BlockType.HEADING:
            return heading_to_html_node
        case BlockType.CODE:
            return code_to_html_node
        case BlockType.QUOTE:
            return quote_to_html_node
        case BlockType.UNORDERED:
            return unordered_to_html_node
        case BlockType.ORDERED:
            return ordered_to_html_node

def markdown_to_blocks(markdown):
    # checks if the given text has any code in it, and if that code is marked correctly
    blocks = markdown.split('```')
    if len(blocks) == 1:
        return split_text(blocks[0])
    if len(blocks) % 2 == 0:
        raise Exception('code block not terminated')
    
    processed_blocks = []
    # splits blocks into text and code based on position, then splits text blocks further
    for text_block, code_block in zip(blocks[::2], blocks[1::2]):
        processed_blocks.extend(split_text(text_block))
        # surrounds code blocks with ``` for further processing, since it got lost in .split('```')
        processed_blocks.append(f'```{code_block}```')
    # returns everything in the original order
    return processed_blocks
    
# splits multiline text, without code, to separate blocks
def split_text(text_block):
    split_text = text_block.strip().split('\n\n')
    processed = []
    for text_segment in split_text:
        stripped = text_segment.strip()
        if stripped != '':
            processed.append(stripped)
    return processed

# basicly calls all other functions, does the same thing as text_to_parent_node just on a bigger scale
def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        to_html_func = block_type_to_html_func(block_type)
        html_nodes.append(
            to_html_func(block)
        )
    return ParentNode('div', html_nodes)

# extracts all html nodes from given text, then arranges them in a tree structure
def text_to_parent_node(tag, text):
    html_nodes = []
    text_nodes = text_to_text_nodes(text)
    for node in text_nodes:
        html_nodes.append(
            text_node_to_html_node(node)
        )
    return ParentNode(tag, html_nodes)

def block_to_lines(block):
    return [line.strip() for line in block.split('\n')]

# deletes from each line everything before, and including, the first appearance of 'symbol' char
def clean_lines(lines, symbol): 
    return [line.partition(symbol)[2].lstrip() for line in lines] # if it doesnt find given symbol returns an empty string

# handles regular paragraphs
def paragraph_to_html_node(block):
    lines = block_to_lines(block)
    return text_to_parent_node('p', ' '.join(lines))

# handles headings
# only the first line of a heading block is processed, the rest are discarded
def heading_to_html_node(block):
    match = re.match(r'^(#{1,6})\s+(.*)', block)
    count = len(match.group(1)) # num of '#' marks heading type and it's tag
    return text_to_parent_node(f'h{count}', match.group(2).rstrip())

# handles codeblocks
def code_to_html_node(block):
    html_node = LeafNode('code', block[3:-3].lstrip())
    return ParentNode('pre', [html_node])

# handles quotations
def quote_to_html_node(block):
    lines = clean_lines(block_to_lines(block), '>') # removes '>' from the start of each line
    return text_to_parent_node('blockquote', ' '.join(lines))

# handles lists (ul + ol)
def list_to_html_node(tag, block):
    children = []
    lines = clean_lines(block_to_lines(block), ' ') # removes '- ' or 'N. ' from the start of each line
    for line in lines:
        children.append(
            text_to_parent_node('li', line)
        )
    return ParentNode(tag, children)

def unordered_to_html_node(block):
    return list_to_html_node('ul', block)

def ordered_to_html_node(block):
    return list_to_html_node('ol', block)
