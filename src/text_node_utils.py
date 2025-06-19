import re

from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
	if not isinstance(text_node.text_type, TextType):
		raise Exception("text node text type is not a member of TextType")
	if text_node.text_type == TextType.TEXT:
		leaf_node = LeafNode(None, text_node.text)
		return leaf_node
	if text_node.text_type == TextType.BOLD:
		leaf_node = LeafNode("b", text_node.text)
		return leaf_node
	if text_node.text_type == TextType.ITALIC:
		leaf_node = LeafNode("i", text_node.text)
		return leaf_node
	if text_node.text_type == TextType.CODE:
		leaf_node = LeafNode("code", text_node.text)
		return leaf_node
	if text_node.text_type == TextType.LINK:
		leaf_node = LeafNode("a", text_node.text, {"href": text_node.url})
		return leaf_node
	if text_node.text_type == TextType.IMAGE:
		leaf_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		return leaf_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type == TextType.TEXT:
			strings = node.text.split(delimiter)
			if len(strings) % 2 != 1:
				raise Exception(f"Invalid Markdown syntax: {repr(node)} missing closing '{delimiter}' delimiter")
			for index, value in enumerate(strings):
				if len(value) > 0:
					if index % 2 == 0:
						new_nodes.append(TextNode(value, TextType.TEXT))
					else:
						new_nodes.append(TextNode(value, text_type))
		else:
			new_nodes.append(node)
	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
    	if node.text_type == TextType.TEXT:
    		images = extract_markdown_images(node.text)
    		if len(images) == 0:
    			new_nodes.append(node)
    		else:
    			text = node.text
    			for image in images:
    				alt_text = image[0]
    				url = image[1]
    				sections = text.split(f"![{alt_text}]({url})", 1)
    				if len(sections) != 2:
    					raise ValueError("invalid markdown, image section not closed")
    				if sections[0] != "":
    					new_nodes.append(TextNode(sections[0], TextType.TEXT))
    				new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    				text = sections[1]
    			if len(text) != 0:
    				new_nodes.append(TextNode(text, TextType.TEXT))
    	else:
    		new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
    	if node.text_type == TextType.TEXT:
    		links = extract_markdown_links(node.text)
    		if len(links) == 0:
    			new_nodes.append(node)
    		else:
    			text = node.text
    			for link in links:
    				alt_text = link[0]
    				url = link[1]
    				sections = text.split(f"[{alt_text}]({url})", 1)
    				if len(sections) != 2:
    					raise ValueError("invalid markdown, link section not closed")
    				if sections[0] != "":
    					new_nodes.append(TextNode(sections[0], TextType.TEXT))
    				new_nodes.append(TextNode(alt_text, TextType.LINK, url))
    				text = sections[1]
    			if text != "":
    				new_nodes.append(TextNode(text, TextType.TEXT))
    	else:
    		new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
	text_nodes = [TextNode(text, TextType.TEXT)]
	text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
	text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
	text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
	text_nodes = split_nodes_image(text_nodes)
	text_nodes = split_nodes_link(text_nodes)
	return text_nodes
