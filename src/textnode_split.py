import re

from textnode import TextType, TextNode


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)] # split function accepts list of nodes
    splits = [
        split_nodes_bold,
        split_nodes_italic,
        split_nodes_code,
        split_nodes_link,
        split_nodes_image
    ]
    for split in splits:
        nodes = split(nodes)
    return nodes

def split_nodes_bold(old_nodes):
    return split_nodes_delimiter(old_nodes, '**', TextType.BOLD)

def split_nodes_italic(old_nodes):
    return split_nodes_delimiter(old_nodes, '_', TextType.ITALIC)

def split_nodes_code(old_nodes):
    return split_nodes_delimiter(old_nodes, '`', TextType.CODE)

def split_nodes_delimiter(nodes, delimiter, text_type):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # we are only working with text types
            continue                # for other types we change nothing

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax: missing closing delimiter")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_helper(old_nodes, TextType.IMAGE, extract_markdown_images, '!')
        
def split_nodes_link(old_nodes):
    return split_nodes_helper(old_nodes, TextType.LINK, extract_markdown_links, '')

def extract_markdown_images(text):
    return re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def split_nodes_helper(nodes, type, func, excl):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT: # only working with text types
            new_nodes.append(node)
            continue

        delimiters = func(node.text)
        if delimiters == []: # no images detected
            new_nodes.append(node)
            continue

        after = node.text
        for anchor, link in delimiters:
            before, after = after.split(f'{excl}[{anchor}]({link})', 1) # splits to before and after an image
            if before != '':
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, type, link))
        if after != '':
            new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes
