import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_notag(self):
        node = ParentNode(None, None)
        try:
            node.to_html()
        except ValueError as err:
            self.assertEqual(repr(err), repr(ValueError('no tag')))

    def test_children_error1(self):
        node = ParentNode('div', 7)
        try:
            node.to_html()
        except ValueError as err:
            self.assertEqual(
                repr(err), 
                repr(ValueError('wrong children format, it should be a list'))
                )

    def test_children_error2(self):
        node = ParentNode('div', [])
        try:
            node.to_html()
        except ValueError as err:
            self.assertEqual(repr(err), repr(ValueError('list children is empty')))

    def test_children_error3(self):
        child = LeafNode('p', 'child')
        node = ParentNode('div', [child, 7])
        try:
            node.to_html()
        except ValueError as err:
            self.assertEqual(
                repr(err), 
                repr(ValueError('list children contains incorrect data type'))
                )
            
    def test_to_html_with_children(self):
        child_node = LeafNode('span', 'child')
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode('b', 'grandchild')
        child_node = ParentNode('span', [grandchild_node])
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span></div>',
        )


if __name__ == '__main__':
    unittest.main()
