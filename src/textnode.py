from enum import Enum
from leafnode import LeafNode


class TextType(Enum):   # Markdown
    TEXT = 'text'   # text
    BOLD = 'bold'       # **text**
    ITALIC = 'italic'   # _text_
    CODE = 'code'       # `text`
    LINK = 'link'       # [anchor text](url)
    IMAGE = 'image'     # ![alt text](url)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', None, {'src': text_node.url, 'alt': text_node.text})
        case _: raise ValueError('unsupported text type')
        

class TextNode():
    def __init__(self, text, type, url=None):
        self.text = text
        self.text_type = type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ): return True
        return False
        
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
