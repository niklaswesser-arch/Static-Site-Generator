import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
    
    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><p>Hello</p></div>',
        )
    
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_empty_children_list(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold"),
                                LeafNode(None, " and "),
                                LeafNode("i", "italic"),
                            ],
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>Bold</b> and <i>italic</i></p></section></div>",
        )
    
    def test_mixed_parent_and_leaf_children(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode("b", "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode("i", "Item 3")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li><b>Item 1</b></li><li>Item 2</li><li><i>Item 3</i></li></ul>",
        )
    
    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold headline"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold headline</b></h2>",
        )


if __name__ == "__main__":
    unittest.main()