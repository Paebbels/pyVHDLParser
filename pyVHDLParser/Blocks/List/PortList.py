# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
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
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
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
from pyVHDLParser.Blocks.Expression       import ExpressionBlockEndedByCharORClosingRoundBracket
from pyVHDLParser.Token                   import CharacterToken, LinebreakToken, IndentationToken, CommentToken, MultiLineCommentToken, SingleLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords          import BoundaryToken, EndToken, SignalKeyword, DelimiterToken
from pyVHDLParser.Token.Keywords          import IdentifierToken
from pyVHDLParser.Token.Parser            import SpaceToken, StringToken
from pyVHDLParser.Blocks                  import TokenParserException, Block, CommentBlock, ParserState, SkipableBlock
from pyVHDLParser.Blocks.Common           import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic1         import CloseBlock as CloseBlockBase
from pyVHDLParser.Blocks.InterfaceObject  import InterfaceSignalBlock


class CloseBlock(CloseBlockBase):
	pass


class DelimiterBlock(SkipableBlock):
	@classmethod
	def stateItemDelimiter(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, StringToken):
			if (token <= "signal"):
				parserState.NewToken =    SignalKeyword(token)
				parserState.PushState =   PortListInterfaceSignalBlock.stateSignalKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.PushState =   PortListInterfaceSignalBlock.stateObjectName
				parserState.TokenMarker = parserState.NewToken
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =     PortListInterfaceSignalBlock.stateObjectName
			return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     OpenBlock.stateOpeningParenthesis
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   token
			parserState.NextState =     OpenBlock.stateOpeningParenthesis
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			# parserState.NextState =     cls.stateWhitespace1
			return

		raise TokenParserException("Expected port name (identifier).", token)


class DefaultValueExpressionBlock(ExpressionBlockEndedByCharORClosingRoundBracket):
	EXIT_CHAR =  ";"
	EXIT_TOKEN = DelimiterToken
	EXIT_BLOCK = DelimiterBlock


class PortListInterfaceSignalBlock(InterfaceSignalBlock):
	DELIMITER_BLOCK = DelimiterBlock
	EXPRESSION =      DefaultValueExpressionBlock


class OpenBlock(Block):
	@classmethod
	def statePortKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =   CloseBlock.stateClosingParenthesis
			parserState.PushState =   cls.stateOpeningParenthesis
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

		raise TokenParserException("Expected '(' or whitespace after keyword PORT.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =   CloseBlock.stateClosingParenthesis
			parserState.PushState =   cls.stateOpeningParenthesis
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

		raise TokenParserException("Expected '(' after keyword PORT.", token)

	@classmethod
	def stateOpeningParenthesis(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == ")")):
			# if (parserState.TokenMarker != token):
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
			parserState.Pop()
			parserState.TokenMarker = token
			return
		elif isinstance(token, StringToken):
			if (token <= "signal"):
				parserState.NewToken =    SignalKeyword(token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   PortListInterfaceSignalBlock.stateSignalKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   PortListInterfaceSignalBlock.stateObjectName
				parserState.TokenMarker = parserState.NewToken
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   PortListInterfaceSignalBlock.stateObjectName
			return
		elif isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = token
			# parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			# parserState.NextState =   cls.stateWhitespace1
			return

		raise TokenParserException("Expected interface signal name (identifier) or keyword: SIGNAL.", token)
