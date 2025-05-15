from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag and not self.value:
            raise ValueError
        elif not self.tag: # just text
            return self.value
        elif not self.value: # could be an img
            if self.tag == "img":
                text = '' # img value = None
            else: raise ValueError
        else: # all other tags must have text
            text = self.value
        
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"
    