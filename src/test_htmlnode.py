import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), f"< > </>")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_full(self):
        child1 = HTMLNode('p', "first")
        child2 = HTMLNode('p', "seccond")
        node = HTMLNode('div', "filler text", [child1, child2], {"href": "https://www.google.com",})
        self.assertEqual(
            node.__repr__(),
            "<div href=\"https://www.google.com\"> filler text <[<p> first </>, <p> seccond </>]> </>"
        )


if __name__ == "__main__":
    unittest.main()
