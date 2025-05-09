from enum import Enum

class TextType(Enum):
    NORMAL = 'normal'   # text
    BOLD = 'bold'       # **text**
    ITALIC = 'italic'   # _text_
    CODE = 'code'       # `text`
    LINK = 'link'       # [anchor text](url)
    IMG = 'image'       # ![alt text](url)

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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
