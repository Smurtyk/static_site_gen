from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag and not self.value:
            raise ValueError('LeafNode has no tag and no value: cannot be converted to_html')
        elif not self.tag: # just text
            return self.value
        elif not self.value: # could be an img or an empty code block
            if self.tag == "img" or self.tag == 'code':
                text = '' # img value should always be None | empty code blocks are allowed
            else: raise ValueError('non image LeafNode has no value: cannot be converted to_html')
        else: # all other tags must have text
            text = self.value
        
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"
    