class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props  # A dictionary of key-value pairs representing the attributes of the HTML tag. 
                            # For example, a link (<a> tag) might have {'href': 'https://www.google.com'}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            return ' ' + ' '.join(map(
                lambda item: f'{item}="{self.props[item]}"', self.props
            ))
        return ''
        
    def __repr__(self):
        if self.tag:
            output = f'<{self.tag}>'
        else:
            output = '< >'

        if self.props:
            output = output[:-1] + f'{self.props_to_html()}>'
        if self.value:
            output += f' {self.value}'
        if self.children:
            output += f' <{self.children}>'
        return output + ' </>'
    