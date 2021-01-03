# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python functions:   A streaming VHDL parser
#
# Description:
# ------------------------------------
#		TODO:
#
# License:
# ==============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
# load dependencies
from pydecor.decorators           import export

from pyVHDLParser.Token           import CharacterToken, WordToken, SpaceToken, LinebreakToken, IndentationToken, ExtendedIdentifier
from pyVHDLParser.Token           import CommentToken, MultiLineCommentToken, SingleLineCommentToken
from pyVHDLParser.Token.Keywords  import BoundaryToken, DelimiterToken, OpeningRoundBracketToken, ClosingRoundBracketToken
from pyVHDLParser.Token.Keywords  import IdentifierToken, AllKeyword
from pyVHDLParser.Blocks          import BlockParserException, Block, CommentBlock, ParserState, SkipableBlock
from pyVHDLParser.Blocks.Common   import LinebreakBlock, IndentationBlock, WhitespaceBlock

__all__ = []
__api__ = __all__


@export
class OpenBlock(Block):
	@classmethod
	def stateOpeningParenthesis(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			if (token <= "all"):
				parserState.NewToken =    AllKeyword(token)
				parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   CloseBlock.stateAllKeyword
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   ItemBlock.stateItemRemainder
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   ItemBlock.stateItemRemainder
			return
		elif isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected keyword ALL or signal name (identifier).", token)


@export
class ItemBlock(Block):
	@classmethod
	def stateItemRemainder(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.Counter += 1
			elif (token == ")"):
				parserState.NewToken =      OpeningRoundBracketToken(token)
				parserState.Counter -= 1
				if (parserState.Counter == 0):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					parserState.Pop()
					parserState.TokenMarker = parserState.NewToken
				else:
					parserState.NewToken =    ClosingRoundBracketToken(token)
			elif (token == ";"):
				if (parserState.Counter == 1):
					parserState.NewToken =    DelimiterToken(token)
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					_ =                       DelimiterBlock(parserState.NewBlock, parserState.NewToken)
					parserState.NextState =   DelimiterBlock.stateItemDelimiter
				else:
					raise BlockParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)


@export
class DelimiterBlock(SkipableBlock):
	def __init__(self, previousBlock, startToken):
		super().__init__(previousBlock, startToken, startToken)

	@classmethod
	def stateItemDelimiter(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(token)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   ItemBlock.stateItemRemainder
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   ItemBlock.stateItemRemainder
			return
		elif isinstance(token, SpaceToken):
			parserState.NextState =   OpenBlock.stateOpeningParenthesis
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = token
			parserState.NextState =   OpenBlock.stateOpeningParenthesis
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected signal name (identifier).", token)


@export
class CloseBlock(Block):
	@classmethod
	def stateAllKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ")")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected ')' or whitespace after keyword ALL.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected  '(' after keyword PROCESS."
		if (isinstance(token, CharacterToken) and (token == ")")):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                       LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)
