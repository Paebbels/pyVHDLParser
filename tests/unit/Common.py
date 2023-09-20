# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from dataclasses                import dataclass
from typing                     import List, Tuple

from flags                      import Flags
from pyTooling.MetaClasses      import ExtendedType

from pyVHDLParser.Base          import ParserException
from pyVHDLParser.Token         import StartOfDocumentToken, EndOfDocumentToken, Token, CharacterTranslation
from pyVHDLParser.Token.Parser  import Tokenizer, TokenizerException
from pyVHDLParser.Blocks        import StartOfDocumentBlock, EndOfDocumentBlock, TokenToBlockParser, MetaBlock, Block, BlockParserException

from tests.Interfaces           import ITestcase as ITC

# XXX: move to pyVHDLParser.Blocks; call it from frontend
from tests.Linking import TokenizerChecks


class Initializer(metaclass=ExtendedType, singleton=True):
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


@dataclass
class ExpectedTokenStream:
	tokens:     List[Tuple[Token, str]]
	result:     Result =                  Result.Pass
	exception:  ParserException =         None


@dataclass
class ExpectedBlockStream:
	blocks:     List[Tuple[Block, str]]
	result:     Result =                  Result.Pass
	exception:  ParserException =         None


class ExpectedDataMixin:
	name:         str =                 None
	code:         str =                 None
	tokenStream:  ExpectedTokenStream = None
	blockStream:  ExpectedBlockStream = None

	@classmethod
	def setUpClass(cls):
		print(f"Starting testcases in {cls.__qualname__}.")

	def setUp(self):
		print("Starting another test.")


class ITestcase(ITC):
	tokenStream: ExpectedTokenStream
	blockStream: ExpectedBlockStream

class TokenLinking(ITestcase, TokenizerChecks):  # , ExpectedDataMixin):
	def test_TokenLinking(self) -> None:
		self.check_TokenLinking()

class TokenSequence(ITestcase): #, ExpectedDataMixin):
	def test_TokenSequence(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)

		tokenIterator = iter(tokenStream)
		listIterator = iter(self.tokenStream.tokens)

		try:
			while True:
				token = next(tokenIterator)
				item = next(listIterator)

				self.assertIsInstance(
					token, item[0],
					msg="Token has not expected type.\n  Actual:   {actual}     pos={pos!s}\n  Expected: {expected}".format(
						actual=token.__class__.__qualname__,
						pos=token.Start,
						expected=item[0].__qualname__
					)
				)
				if item[1] is not None:
					self.assertTrue(
						token == item[1],
						msg="The token's value does not match.\n  Context:  {context}\n  Actual:   {actual}\n  Expected: {expected}".format(
							context=f"at {token.Start!s}",
							actual=f"'{token!r}' of {token.__class__.__qualname__}",
							expected=f"'{item[1]}' of {item[0].__qualname__}"
						)
					)

		except TokenizerException as ex:
			self.fail(msg=f"Unexpected 'TokenizerException' ({ex!s}) at {ex.Position}")
		except StopIteration:
			pass
		except AssertionError:
			raise
		except Exception as ex:
			self.fail(msg=f"Unexpected exception '{ex.__class__.__qualname__}' := {ex!s}.")


class TokenLinking(ITestcase): #, ExpectedDataMixin):
	def test_TokenLinking(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)

		tokenIterator = iter(tokenStream)
		startToken =    next(tokenIterator)

		self.assertIsInstance(startToken, StartOfDocumentToken, msg=f"First token is not StartOfDocumentToken: {startToken}")
		self.assertIsNone(startToken.PreviousToken, msg="First token has no open start.")

		lastToken: Token = startToken
		endToken:  Token = None

		for token in tokenIterator:
			if isinstance(token, EndOfDocumentToken):
				endToken = token
				break

			self.assertIs(lastToken.NextToken, token, msg=f"Last token is not connected to the current token: {token}")
			self.assertIs(lastToken, token.PreviousToken, msg=f"Current token is not connected to lastToken: {token}")

			lastToken = token
		else:
			self.fail(msg="No EndOfDocumentToken found.")

		self.assertIsInstance(endToken, EndOfDocumentToken, msg=f"End token is not EndOfDocumentToken: {endToken}")
		self.assertIs(lastToken.NextToken, endToken, msg=f"Last token is not connected to the end token: {token}")
		self.assertIs(lastToken, endToken.PreviousToken, msg=f"End token is not connected to lastToken: {token}")
		self.assertIsNone(endToken.NextToken, msg=f"End token has no open end: {endToken.NextToken}")


class BlockSequence(ITestcase): #, ExpectedDataMixin):
	def test_BlockSequence(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
		blockStream = TokenToBlockParser(tokenStream)()

		blockIterator = iter(blockStream)
		listIterator =  iter(self.blockStream.blocks)

		try:
			while True:
				block = next(blockIterator)
				item =  next(listIterator)

				self.assertIsInstance(
					block, item[0],
				  msg=f"Block has not expected type.\n  Actual:   {type(block).__qualname__}\n  Expected: {item[0].__qualname__}"
				)
				if item[1] is not None:
					blockValue = str(block)
					super().failIf(
						blockValue != item[1],
						msg="The blocks's value does not match.\n  Actual:   '{actual}'\n  Expected: '{expected}'".format(
							actual=CharacterTranslation(blockValue, oneLiner=True),
							expected=CharacterTranslation(item[1], oneLiner=True)
						)
					)

		except TokenizerException as ex:
			self.fail(msg=f"Unexpected 'TokenizerException' at {ex.Position}")
		except BlockParserException as ex:
			self.fail(msg=f"Unexpected 'BlockParserException' at {ex.Token.Start}")
		except StopIteration:
			pass
		except AssertionError:
			raise
		except Exception as ex:
			self.fail(msg=f"Unexpected exception '{ex.__class__.__qualname__}' := {ex!s}.")


class BlockSequenceWithParserError(ITestcase): #, ExpectedDataMixin):
	def test_BlockSequenceError(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
		blockStream = TokenToBlockParser(tokenStream)()

		blockIterator = iter(blockStream)
		listIterator =  iter(self.blockStream.blocks)

		with self.assertRaises(BlockParserException) as ex:
			try:
				while True:
					block = next(blockIterator)
					item =  next(listIterator)

					self.assertIsInstance(
						block, item[0],
					  msg=f"Block has not expected type.\n  Actual:   {block!s}\n  Expected: {item[0].__qualname__}"
					)
					if item[1] is not None:
						blockValue = str(block)
						super().failIf(
							blockValue != item[1],
							msg="The blocks's value does not match.\n  Actual:   '{actual}'\n  Expected: '{expected}'".format(
								actual=CharacterTranslation(blockValue, oneLiner=True),
								expected=CharacterTranslation(item[1], oneLiner=True)
							)
						)

			except TokenizerException as ex:
				self.fail(msg=f"Unexpected 'TokenizerException' at {ex.Position}")
			except BlockParserException:
				raise
			except StopIteration:
				pass
			except AssertionError:
				raise
			except Exception as ex:
				self.fail(msg=f"Unexpected exception '{ex.__class__.__qualname__}' := {ex!s}.")

		print(ex)

	def test_BlockLinking(self) -> None:
		# test['name']

		with self.assertRaises(BlockParserException) as ex:
			tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
			blockStream = TokenToBlockParser(tokenStream)()

			blockIterator = iter(blockStream)
			firstBlock = next(blockIterator)

			self.assertIsInstance(firstBlock, StartOfDocumentBlock, msg=f"First block is not StartOfDocumentBlock: {firstBlock}")

			startToken = firstBlock.StartToken
			self.assertIsInstance(startToken, StartOfDocumentToken, msg=f"First token is not StartOfDocumentToken: {startToken}")

			lastBlock: Block = firstBlock
			endBlock: Block = None
			lastToken: Token = startToken

			for block in blockIterator:
				if isinstance(block, EndOfDocumentBlock):
					endBlock = block
					break

				# Block checks
				self.assertIs(lastBlock.NextBlock, block,
				                 msg=f"Last block is not connected to the current block: {block}")
				self.assertIs(lastBlock, block.PreviousBlock,
				                 msg=f"Current block is not connected to last block: {block}")

				# Token checks
				tokenIterator = iter(block)

				for token in tokenIterator:
					self.assertIsNotNone(token.NextToken, msg="Token has an open end (token).")
					self.assertIs(lastToken.NextToken, token, msg="Last token is not connected to the current token.")
					self.assertIsNotNone(token.PreviousToken, msg="Token has an open end (PreviousToken).")
					self.assertIs(token.PreviousToken, lastToken, msg="Current token is not connected to lastToken.")

					lastToken = token

				lastBlock = block
			else:
				self.fail(msg="No EndOfDocumentBlock found.")

			# Block checks
			self.assertIsInstance(endBlock, EndOfDocumentBlock, msg=f"End block is not EndOfDocumentblock: {endBlock}")
			self.assertIsInstance(endBlock.EndToken, EndOfDocumentToken, msg=f"End block's token is not EndOfDocumentToken: {endBlock.EndToken}")

			# Token checks
			self.assertIs(lastToken.NextToken, endBlock.EndToken, msg="Last token is not connected to the end token.")
			self.assertIs(lastToken, endBlock.EndToken.PreviousToken, msg="End token is not connected to lastToken.")
			self.assertIsNone(endBlock.EndToken.NextToken, msg=f"End token has no open end: {endBlock.EndToken.NextToken}")


class BlockLinking(ITestcase): #, ExpectedDataMixin):
	def test_BlockLinking(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
		blockStream = TokenToBlockParser(tokenStream)()

		blockIterator = iter(blockStream)
		firstBlock = next(blockIterator)

		self.assertIsInstance(firstBlock, StartOfDocumentBlock, msg=f"First block is not StartOfDocumentBlock: {firstBlock}")

		startToken = firstBlock.StartToken
		self.assertIsInstance(startToken, StartOfDocumentToken, msg=f"First token is not StartOfDocumentToken: {startToken}")

		lastBlock: Block = firstBlock
		endBlock: Block = None
		lastToken: Token = startToken

		for block in blockIterator:
			if isinstance(block, EndOfDocumentBlock):
				endBlock = block
				break

			# Block checks
			self.assertIs(lastBlock.NextBlock, block,
			                 msg=f"Last block is not connected to the current block: {block}")
			self.assertIs(lastBlock, block.PreviousBlock,
			                 msg=f"Current block is not connected to last block: {block}")

			# Token checks
			tokenIterator = iter(block)

			for token in tokenIterator:
				self.assertIsNotNone(token.NextToken, msg="Token has an open end (token).")
				self.assertIs(lastToken.NextToken, token, msg="Last token is not connected to the current token.")
				self.assertIsNotNone(token.PreviousToken, msg="Token has an open end (PreviousToken).")
				self.assertIs(token.PreviousToken, lastToken, msg="Current token is not connected to lastToken.")

				lastToken = token

			lastBlock = block
		else:
			self.fail(msg="No EndOfDocumentBlock found.")

		# Block checks
		self.assertIsInstance(endBlock, EndOfDocumentBlock, msg=f"End block is not EndOfDocumentblock: {endBlock}")
		self.assertIsInstance(endBlock.EndToken, EndOfDocumentToken, msg=f"End block's token is not EndOfDocumentToken: {endBlock.EndToken}")

		# Token checks
		self.assertIs(lastToken.NextToken, endBlock.EndToken, msg="Last token is not connected to the end token.")
		self.assertIs(lastToken, endBlock.EndToken.PreviousToken, msg="End token is not connected to lastToken.")
		self.assertIsNone(endBlock.EndToken.NextToken, msg=f"End token has no open end: {endBlock.EndToken.NextToken}")


class LinkingTests(TokenLinking, BlockLinking):
	pass
