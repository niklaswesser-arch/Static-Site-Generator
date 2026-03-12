import unittest

from htmlnode import HTMLNode

node = HTMLNode("a", "Click me", None, {"href": "https://www.boot.dev"})
print(node.props_to_html())

print(node)