import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_notag(self):
        node = LeafNode(None, 'Goodbye, world!')
        self.assertEqual(node.to_html(), f'{node.value}')

    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), f'<p>{node.value}</p>')

    def test_leaf_to_html_link1(self):
        node = LeafNode('img', None, {'src': 'https://www.anImg.com', 'alt': 'Could it be!?'})
        self.assertEqual(node.to_html(), f'<img src="{node.props['src']}" alt="{node.props['alt']}"></img>')

    def test_leaf_to_html_link2(self):
        node = LeafNode('img', '', {'src': 'https://www.anImg.com', 'alt': 'Could it be!?'})
        self.assertEqual(node.to_html(), f'<img src="{node.props['src']}" alt="{node.props['alt']}"></img>')

    def test_leaf_to_html_noval(self):
        node = LeafNode('code', '')
        try:
            self.assertNotEqual(node.to_html(), '<code></code>')
        except ValueError:
            self.assertEqual(node.__repr__(), '<code> </>')


if __name__ == "__main__":
    unittest.main()
    