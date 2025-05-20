import unittest

from blocks import markdown_to_blocks
from blocks import BlockType, block_to_block_type
from blocks import markdown_to_html_node


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        block = """##### Some heading"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

        block = """```x = 7\nprint(x)```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

        block = """>Are you talking to me?\n>ARE YOU TALKING TO ME!?"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

        block = """- first\n- second\n- third"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED)

        block = """1. first\n2. second\n3. third"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_header(self):
        md = """### **Header 1**

######     Header 2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3><b>Header 1</b></h3><h6>Header 2</h6></div>"
        )

    def test_codeblock(self):
        md = """   
```
This is text that _should_ remain
the **same** even with inline stuff
```   
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_quote(self):
        md = """
>**I am the danger.**
>A guy opens his door and gets shot, and you think that of me?
>No. 
>**I am the one who knocks!**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote><b>I am the danger.</b> A guy opens his door and gets shot, and you think that of me? No. <b>I am the one who knocks!</b></blockquote></div>'
        )

    def test_lists(self):
        md = """
- unordered
- list
- example

1. ordered
2. list
3. example
"""


        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>unordered</li><li>list</li><li>example</li></ul><ol><li>ordered</li><li>list</li><li>example</li></ol></div>'
        )


if __name__ == '__main__':
    unittest.main()
