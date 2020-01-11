from unittest                   import TestCase

from flags                      import Flags
from pyMetaClasses import Singleton

from pyVHDLParser.Token         import StartOfDocumentToken, EndOfDocumentToken, Token
from pyVHDLParser.Token.Parser  import Tokenizer
from pyVHDLParser.Blocks        import StartOfDocumentBlock, EndOfDocumentBlock, TokenToBlockParser, MetaBlock, Block


class Initializer(metaclass=Singleton):
	def __init__(self):
		for block in MetaBlock.BLOCKS:
			try:
				block.__cls_init__()
			except AttributeError:
				pass


class Result(Flags):
	Pass = 1,
	Fail = 2


class StreamingTests(TestCase):
	_TESTCASES = []

	def setUp(self):
		self.skipTest("This is a base-class.")

	def test_TokenSequence(self) -> None:
		for test in self._TESTCASES:
			with self.subTest(msg=test['name']):
				tokenStream = Tokenizer.GetVHDLTokenizer(test['code'])

				for pair in zip(tokenStream, test['tokenstream']['tokens']):
					self.assertIsInstance(pair[0], pair[1][0])
					if pair[1][1] is not None:
						self.assertTrue(pair[0] == pair[1][1])

	def test_TokenLinking(self) -> None:
		for test in self._TESTCASES:
			with self.subTest(msg=test['name']):
				tokenStream = Tokenizer.GetVHDLTokenizer(test['code'])

				tokenIterator = iter(tokenStream)
				startToken = next(tokenIterator)

				self.assertIsInstance(startToken, StartOfDocumentToken,
				                      msg="First token is not StartOfDocumentToken: {token}".format(token=startToken))
				self.assertIsNone(startToken.PreviousToken, msg="First token has no open start.")

				lastToken: Token = startToken
				endToken: Token = None

				for token in tokenIterator:
					if isinstance(token, EndOfDocumentToken):
						endToken = token
						break

					self.assertEqual(lastToken.NextToken, token,
					                 msg="Last token is not connected to the current token: {token}".format(token=token))
					self.assertEqual(lastToken, token.PreviousToken,
					                 msg="Current token is not connected to lastToken: {token}".format(token=token))

					lastToken = token
				else:
					self.fail(msg="No EndOfDocumentToken found.")

				self.assertIsInstance(endToken, EndOfDocumentToken,
				                      msg="End token is not EndOfDocumentToken: {token}".format(token=endToken))
				self.assertEqual(lastToken.NextToken, endToken,
				                 msg="Last token is not connected to the end token: {token}".format(token=token))
				self.assertEqual(lastToken, endToken.PreviousToken,
				                 msg="End token is not connected to lastToken: {token}".format(token=token))
				self.assertIsNone(endToken.NextToken, msg="End token has no open end: {token}".format(token=endToken.NextToken))

	def test_BlockSequence(self) -> None:
		for test in self._TESTCASES:
			with self.subTest(msg=test['name']):
				tokenStream = Tokenizer.GetVHDLTokenizer(test['code'])
				blockStream = TokenToBlockParser.Transform(tokenStream)

				for pair in zip(blockStream, test['blockstream']['blocks']):
					self.assertIsInstance(pair[0], pair[1][0])

	def test_BlockLinking(self) -> None:
		for test in self._TESTCASES:
			with self.subTest(msg=test['name']):
				tokenStream = Tokenizer.GetVHDLTokenizer(test['code'])
				blockStream = TokenToBlockParser.Transform(tokenStream)

				blockIterator = iter(blockStream)
				firstBlock = next(blockIterator)

				self.assertIsInstance(firstBlock, StartOfDocumentBlock,
				                      msg="First block is not StartOfDocumentBlock: {block}".format(block=firstBlock))

				startToken = firstBlock.StartToken
				self.assertIsInstance(startToken, StartOfDocumentToken,
				                      msg="First token is not StartOfDocumentToken: {token}".format(token=startToken))

				lastBlock: Block = firstBlock
				endBlock: Block = None
				lastToken: Token = startToken

				for block in blockIterator:
					if isinstance(block, EndOfDocumentBlock):
						endBlock = block
						break

					# Block checks
					self.assertEqual(lastBlock.NextBlock, block,
					                 msg="Last block is not connected to the current block: {block}".format(block=block))
					self.assertEqual(lastBlock, block.PreviousBlock,
					                 msg="Current block is not connected to last block: {block}".format(block=block))

					# Token checks
					tokenIterator = iter(block)

					for token in tokenIterator:
						self.assertIsNotNone(token.NextToken, msg="Token has an open end (token).".format(token=token.NextToken))
						self.assertEqual(lastToken.NextToken, token, msg="Last token is not connected to the current token.")
						self.assertIsNotNone(token.PreviousToken, msg="Token has an open end (PreviousToken).")
						self.assertEqual(token.PreviousToken, lastToken, msg="Current token is not connected to lastToken.")

						lastToken = token

					lastBlock = block
				else:
					self.fail(msg="No EndOfDocumentBlock found.")

				# Block checks
				self.assertIsInstance(endBlock, EndOfDocumentBlock,
				                      msg="End block is not EndOfDocumentblock: {token}".format(token=endBlock))
				self.assertIsInstance(endBlock.EndToken, EndOfDocumentToken,
				                      msg="End block's token is not EndOfDocumentToken: {token}".format(
					                      token=endBlock.EndToken))

				# Token checks
				self.assertEqual(lastToken.NextToken, endBlock.EndToken, msg="Last token is not connected to the end token.")
				self.assertEqual(lastToken, endBlock.EndToken.PreviousToken, msg="End token is not connected to lastToken.")
				self.assertIsNone(endBlock.EndToken.NextToken,
				                  msg="End token has no open end: {token}".format(token=endBlock.EndToken.NextToken))
