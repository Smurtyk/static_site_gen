from textnode import TextNode, TextType
from blocks import markdown_to_html_node


def main():
    node1 = TextNode("Here's Jonny!", TextType.BOLD)
    print(node1.__repr__())
    node2 = TextNode("Here's Jonny!", TextType.BOLD)
    print(node2)
    print(node1 == node2)


if __name__ == '__main__':
    main()
    