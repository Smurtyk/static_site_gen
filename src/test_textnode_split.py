import unittest

from textnode import TextType, TextNode
from functions import split_nodes_delimiter
from functions import extract_markdown_images, extract_markdown_links
from functions import split_nodes_image, split_nodes_link
from functions import text_to_textnodes


class TestSplitTextNodes(unittest.TestCase):
    def test_single_node(self):
        node = TextNode('This is text with a `code block` word', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], '`', TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" word", TextType.TEXT) 
            ]
        
        self.assertEqual(split_nodes, expected)

    def test_double_node(self):
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

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_images(self):
        text = 'This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)'

        self.assertEqual(
            [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')],
            extract_markdown_images(text)
        )
        self.assertEqual([], extract_markdown_images(text.replace('!', '')))
        self.assertEqual([], extract_markdown_images('Some random ![text] with no (image) linked'))

    def test_extract_links(self):
        text = 'This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)'

        self.assertEqual([], extract_markdown_links(text))
        self.assertEqual(
            [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')],
            extract_markdown_links(text.replace('!', ''))
        )

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        self.assertEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            extract_markdown_links(text)
        )
        self.assertEqual([], extract_markdown_links(text.replace(']', '] ')))

class TestSplitUrlNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            'This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)',
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode('This is text with an ', TextType.TEXT),
                TextNode('image', TextType.IMAGE, 'https://i.imgur.com/zjjcJKZ.png'),
                TextNode(' and another ', TextType.TEXT),
                TextNode('second image', TextType.IMAGE, 'https://i.imgur.com/3elNhQu.png'),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)',
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode('This is text with a link ', TextType.TEXT),
                TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
                TextNode(' and ', TextType.TEXT),
                TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),
            ],
            new_nodes,
        )

    def test_split_combination(self):
        nodes = [
            TextNode('Start1 [anchor1](link1) ![alt1](source1)', TextType.TEXT),
            TextNode('Start2 ![alt2](source2) [anchor2](link2)', TextType.TEXT),
        ]
        new_nodes = split_nodes_image(split_nodes_link(nodes))
        newer_nodes = split_nodes_link(split_nodes_image(nodes))
        self.assertListEqual(
            [
                TextNode('Start1 ', TextType.TEXT), TextNode('anchor1', TextType.LINK, 'link1'),
                TextNode(' ', TextType.TEXT), TextNode('alt1', TextType.IMAGE, 'source1'),
                TextNode('Start2 ', TextType.TEXT), TextNode('alt2', TextType.IMAGE, 'source2'),
                TextNode(' ', TextType.TEXT), TextNode('anchor2', TextType.LINK, 'link2'),
            ],
            new_nodes
        )
        self.assertListEqual(new_nodes, newer_nodes)

    def test_split_notext(self):
        link_node = TextNode('[anchor1](link1)[anchor2](link2)', TextType.TEXT)
        link_split = split_nodes_link([link_node])
        self.assertListEqual(
            [TextNode('anchor1', TextType.LINK, 'link1'), TextNode('anchor2', TextType.LINK, 'link2')],
            link_split
            )

        img_node = TextNode('![alt1](source1)![alt2](source2)', TextType.TEXT)
        img_split = split_nodes_image([img_node])
        self.assertListEqual(
            [TextNode('alt1', TextType.IMAGE, 'source1'), TextNode('alt2', TextType.IMAGE, 'source2')],
            img_split
        )

    def test_split_wrong_format(self):
        node = TextNode('Text and incorrect ![image]((format)', TextType.TEXT)
        split = split_nodes_image([node])
        self.assertListEqual(split, [node])

class TestTextToNodes(unittest.TestCase):
    def test_conv(self):
        nodes = text_to_textnodes(
             'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], 
            nodes
        )


if __name__ == '__main__':
    unittest.main()