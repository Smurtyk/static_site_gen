import unittest

from textnode import TextType, TextNode
from textnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_same(self):
        node = TextNode('This is a text node', TextType.TEXT)
        self.assertEqual(node, node)

    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode('This is a text node', TextType.TEXT)
        node2 = TextNode('This is another text node', TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode('This is a text node', TextType.TEXT)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode('This is a text node', TextType.BOLD, 'http://localhost:8888')
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)


class TestTextToHTML(unittest.TestCase):
    def test_normal_to_html(self):
        node = TextNode('This is a text node', TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), node.text)
        
    def test_bold_to_html(self):
        node = TextNode('This text is in bold', TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), f'<b>{node.text}</b>')

    def test_italic_to_html(self):
        node = TextNode('This text is in italic', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), f'<i>{node.text}</i>')

    def test_code_to_html(self):
        node = TextNode('This is some code', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), f'<code>{node.text}</code>')

    def test_link_to_html(self):
        node = TextNode('This is an anchor text', TextType.LINK, 'www.link.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), f'<a href="{node.url}">{node.text}</a>')

    def test_image_to_html(self):
        node = TextNode('This is a picture', TextType.IMAGE, 'www.pic.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), f'<img src="{node.url}" alt="{node.text}"></img>')


if __name__ == '__main__':
    unittest.main()
