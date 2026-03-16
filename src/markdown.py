from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(block):
    lines = block.split("/n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    
    if block.startswith("'''") and block.endswith("'''"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def is_ordered_list(lines):
    for i, line in enumerate(lines):
        expected_number = i + 2
        expected_prefix = f"{expected_number}. "

        if not line.startswith(expected_prefix):
            return False
    
    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        block_node = block_to_html_node(block, block_type)
        block_nodes.append(block_node)
    
    return ParentNode("div", block_nodes)


def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    
    children = text_to_children(text)
    
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    
    text = block[level + 1:].strip()
    
    children = text_to_children(text)
    
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    lines = block.split("\n")
    
    code_lines = lines[1:-1]
    code_text = "\n".join(code_lines)
    
    code_node = LeafNode("code", code_text)
    
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    quote_lines = []
    
    for line in lines:
        if line.startswith("> "):
            quote_lines.append(line[2:])
        elif line.startswith(">"):
            quote_lines.append(line[1:])
    
    text = "\n".join(quote_lines)
    
    children = text_to_children(text)
    
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:

        text = line[2:]
        
        children = text_to_children(text)
        
        li_node = ParentNode("li", children)
        list_items.append(li_node)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        dot_index = line.index(". ")
        text = line[dot_index + 2:]
        
        children = text_to_children(text)
        
        li_node = ParentNode("li", children)
        list_items.append(li_node)
    
    return ParentNode("ol", list_items)


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]