import unittest

from textnode import TextType, TextNode
from functions import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_single(self):
        node = TextNode('This is text with a `code block` word', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], '`', TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" word", TextType.TEXT) 
            ]
        
        self.assertEqual(split_nodes, expected)

    def test_double(self):
        node = TextNode('This is text with a `code block` and another `code block`', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], '`', TextType.CODE)

        expected = [
            TextNode('This is text with a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and another ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            ]
        
        self.assertEqual(split_nodes, expected)

    def test_different_splits(self):
        node = TextNode('This text contains some **bold text** and some _italic text_', TextType.TEXT)
        split_nodes1 = split_nodes_delimiter(
            split_nodes_delimiter([node], '**', TextType.BOLD), '_', TextType.ITALIC
        )
        split_nodes2 = split_nodes_delimiter(
            split_nodes_delimiter([node], '_', TextType.ITALIC), '**', TextType.BOLD
        )

        expected = [
            TextNode('This text contains some ', TextType.TEXT),
            TextNode('bold text', TextType.BOLD),
            TextNode(' and some ', TextType.TEXT),
            TextNode('italic text', TextType.ITALIC),
            ]


        self.assertEqual(split_nodes1, expected)
        self.assertEqual(split_nodes2, expected)


if __name__ == '__main__':
    unittest.main()