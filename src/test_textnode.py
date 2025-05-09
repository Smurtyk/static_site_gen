import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_same(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is another text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, 'http://localhost:8888')
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
