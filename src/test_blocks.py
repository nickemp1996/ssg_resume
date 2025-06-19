import unittest

from blocktype import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToTextBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

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

class TestBlocks(unittest.TestCase):
	def test_is_heading(self):
		block = "# Level 1 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_is_heading2(self):
		block = "## Level 2 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_is_heading3(self):
		block = "### Level 3 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_is_heading4(self):
		block = "#### Level 4 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_is_heading5(self):
		block = "##### Level 5 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_is_heading6(self):
		block = "###### Level 6 heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_is_heading7(self):
		block = "####### This is just a paragraph"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

	def test_is_code(self):
		block = "```\nThis is a code block\n```"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.CODE)

	def test_is_not_code(self):
		block = "```This is not code"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

	def test_is_quote(self):
		block = ">Quote 1\n>Quote 2\n>Quote 3"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.QUOTE)

	def test_is_not_quote(self):
		block = ">Quote 1\n>Quote 2\nQuote 3"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

	def test_is_unordered_list(self):
		block = "- item 1\n- item 2\n- item 3"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.ULIST)

	def test_is_not_unordered_list(self):
		block = "- item 1\n-item 2\n- item 3"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

	def test_is_ordered_list(self):
		block = "1. item 1\n2. item 2\n3. item 3"
		block_type = block_to_block_type(block)
		print(block_type)
		self.assertEqual(block_type, BlockType.OLIST)

	def test_is_not_unordered_list(self):
		block = "1. item 1\n2. item 2\n4. item 3"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()