from typing import List, Tuple
from unittest                   import TestCase

from flags                      import Flags
from pyMetaClasses import Singleton

from pyVHDLParser.Base import ParserException
from pyVHDLParser.Token         import StartOfDocumentToken, EndOfDocumentToken, Token
from pyVHDLParser.Token.Parser import Tokenizer, TokenizerException
from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock, TokenToBlockParser, MetaBlock, Block, \
	BlockParserException


class Initializer(metaclass=Singleton):
	def __init__(self):
		print("Init all blocks.")
		for block in MetaBlock.BLOCKS:
			try:
				block.__cls_init__()
			except AttributeError:
				pass


class Result(Flags):
	Pass = 1,
	Fail = 2


class tc_dummy:
	def skipTest(self, reason=None):
		pass
	def fail(self, msg=""):
		pass
	def assertEqual(self, left, right, msg=""):
		pass
	def assertIsInstance(self, obj, typ, msg=""):
		pass
	def assertIsNotInstance(self, obj, typ, msg=""):
		pass
	def assertTrue(self, obj, msg=""):
		pass
	def assertIsNone(self, obj, msg=""):
		pass
	def assertIsNotNone(self, obj, msg=""):
		pass


class Struct1:
	tokens:     List[Tuple[Token, str]] = None
	result:     Result =                  None
	exception:  ParserException =         None

	def __init__(self, tokenList, result=Result.Pass, exception=None):
		self.tokens =     tokenList
		self.result =     result
		self.exception =  exception


class Struct2:
	blocks:     List[Tuple[Block, str]] = None
	result:     Result =                  None
	exception:  ParserException =         None

	def __init__(self, blockList, result=Result.Pass, exception=None):
		self.blocks =     blockList
		self.result =     result
		self.exception =  exception


class Struct3:
	name: str = None
	code: str = None
	tokenstream: Struct1 = None
	blockstream: Struct2 = None


class TokenSequence(tc_dummy): #, Struct3):
	def test_TokenSequence(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)

		tokenIterator = iter(tokenStream)
		listIterator = iter(self.tokenstream.tokens)

		try:
			while True:
				token = next(tokenIterator)
				item = next(listIterator)

				self.assertIsInstance(
					token, item[0],
					msg="Token has not expected type.\n  Actual:   {actual}\n  Expected: {expected}".format(
						actual=token.__class__.__qualname__,
						expected=item[0].__qualname__
					)
				)
				if item[1] is not None:
					if token != item[1]:
						self.fail(
							msg="The token's value does not match.\n  Actual:   {actual}\n  Expected: {expected}".format(
								actual=token.Value,
								expected=item[1]
							)
						)

		except TokenizerException as ex:
			self.fail(msg="Unexpected 'TokenizerException' ({ex!s}) at {pos}".format(ex=ex, pos=ex.Position))
		except StopIteration:
			pass
		except AssertionError:
			raise
		except Exception as ex:
			self.fail(msg="Unexpected exception '{exname}' := {ex!s}.".format(ex=ex, exname=ex.__class__.__qualname__))


class TokenLinking(tc_dummy): #, Struct3):
	def test_TokenLinking(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)

		tokenIterator = iter(tokenStream)
		startToken = next(tokenIterator)

		self.assertIsInstance(startToken, StartOfDocumentToken, msg="First token is not StartOfDocumentToken: {token}".format(token=startToken))
		self.assertIsNone(startToken.PreviousToken, msg="First token has no open start.")

		lastToken: Token = startToken
		endToken: Token = None

		for token in tokenIterator:
			if isinstance(token, EndOfDocumentToken):
				endToken = token
				break

			self.assertEqual(lastToken.NextToken, token, msg="Last token is not connected to the current token: {token}".format(token=token))
			self.assertEqual(lastToken, token.PreviousToken, msg="Current token is not connected to lastToken: {token}".format(token=token))

			lastToken = token
		else:
			self.fail(msg="No EndOfDocumentToken found.")

		self.assertIsInstance(endToken, EndOfDocumentToken, msg="End token is not EndOfDocumentToken: {token}".format(token=endToken))
		self.assertEqual(lastToken.NextToken, endToken, msg="Last token is not connected to the end token: {token}".format(token=token))
		self.assertEqual(lastToken, endToken.PreviousToken, msg="End token is not connected to lastToken: {token}".format(token=token))
		self.assertIsNone(endToken.NextToken, msg="End token has no open end: {token}".format(token=endToken.NextToken))


class BlockSequence(tc_dummy): #, Struct3):
	def test_BlockSequence(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
		blockStream = TokenToBlockParser.Transform(tokenStream)

		blockIterator = iter(blockStream)
		listIterator =  iter(self.blockstream.blocks)

		try:
			while True:
				block = next(blockIterator)
				item =  next(listIterator)

				self.assertIsInstance(
					block, item[0],
				  msg="Block has not expected type.\n  Actual:   {actual}\n  Expected: {expected}".format(
						actual=block.__class__.__qualname__,
						expected=item[0].__qualname__
				  )
				)
				if item[1] is not None:
					blockValue = repr(block)
					if blockValue != item[1]:
						self.fail(
							msg="The token's value does not match.\n  Actual:   {actual}\n  Expected: {expected}".format(
								actual=blockValue,
								expected=item[1]
							)
						)

		except TokenizerException as ex:
			self.fail(msg="Unexpected 'TokenizerException' at {pos}".format(pos=ex.Position))
		except BlockParserException as ex:
			self.fail(msg="Unexpected 'BlockParserException' at {pos}".format(pos=ex.Position))
		except StopIteration:
			pass
		except AssertionError:
			raise
		except Exception as ex:
			self.fail(msg="Unexpected exception '{exname}' := {ex!s}.".format(ex=ex, exname=ex.__class__.__qualname__))


class BlockLinking(tc_dummy): #, Struct3):
	def test_BlockLinking(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
		blockStream = TokenToBlockParser.Transform(tokenStream)

		blockIterator = iter(blockStream)
		firstBlock = next(blockIterator)

		self.assertIsInstance(firstBlock, StartOfDocumentBlock, msg="First block is not StartOfDocumentBlock: {block}".format(block=firstBlock))

		startToken = firstBlock.StartToken
		self.assertIsInstance(startToken, StartOfDocumentToken, msg="First token is not StartOfDocumentToken: {token}".format(token=startToken))

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
		self.assertIsInstance(endBlock, EndOfDocumentBlock, msg="End block is not EndOfDocumentblock: {token}".format(token=endBlock))
		self.assertIsInstance(endBlock.EndToken, EndOfDocumentToken, msg="End block's token is not EndOfDocumentToken: {token}".format(
			                      token=endBlock.EndToken))

		# Token checks
		self.assertEqual(lastToken.NextToken, endBlock.EndToken, msg="Last token is not connected to the end token.")
		self.assertEqual(lastToken, endBlock.EndToken.PreviousToken, msg="End token is not connected to lastToken.")
		self.assertIsNone(endBlock.EndToken.NextToken, msg="End token has no open end: {token}".format(token=endBlock.EndToken.NextToken))


class LinkingTests(TokenLinking, BlockLinking):
	pass

class Foo(tc_dummy):
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

class StreamingTests(TestCase, Foo):
	pass
