from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('no tag')
        if type(self.children) != list:
            raise ValueError('wrong children format, it should be a list')
        if len(self.children) == 0:
            raise ValueError('list children is empty')
        for child in self.children:
            if type(child) != ParentNode and type(child)!= LeafNode:
                raise ValueError('list children contains incorrect data type')
            
        return f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda child: child.to_html(), self.children))}</{self.tag}>"
