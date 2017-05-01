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
# Copyright 2007-2017 Patrick Lehmann - Dresden, Germany
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
from pyVHDLParser.Blocks.InterfaceObject import InterfaceSignalBlock, InterfaceConstantBlock, InterfaceVariableBlock
from pyVHDLParser.Token import CharacterToken, LinebreakToken, IndentationToken, CommentToken, MultiLineCommentToken, SingleLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords import BoundaryToken, DelimiterToken, ClosingRoundBracketToken, ConstantKeyword, SignalKeyword, VariableKeyword
from pyVHDLParser.Token.Keywords      import IdentifierToken
from pyVHDLParser.Token.Parser        import SpaceToken, StringToken
from pyVHDLParser.Blocks              import TokenParserException, Block, CommentBlock, ParserState, SkipableBlock
from pyVHDLParser.Blocks.Common       import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic1 import CloseBlock as CloseBlockBase


class OpenBlock(Block):
	@classmethod
	def stateParameterKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =   CloseBlock.stateClosingParenthesis
			parserState.PushState =   cls.stateOpeningParenthesis
			parserState.Counter =     1
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

		raise TokenParserException("Expected '(' or whitespace after keyword PARAMETER.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.PushState =   cls.stateOpeningParenthesis
			parserState.Counter =     1
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
			parserState.NewBlock =      CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise TokenParserException("Expected '(' after keyword PARAMETER.", token)

	@classmethod
	def stateOpeningParenthesis(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, StringToken):
			if (token <= "constant"):
				parserState.NewToken =    ConstantKeyword(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateConstantKeyword
				return
			elif (token <= "variable"):
				parserState.NewToken =    VariableKeyword(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   ParameterListInterfaceVariableBlock.stateVariableKeyword
				return
			elif (token <= "signal"):
				parserState.NewToken =    SignalKeyword(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   ParameterListInterfaceSignalBlock.stateSignalKeyword
				return
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateObjectName
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   ParameterListInterfaceConstantBlock.stateObjectName
			return
		elif isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = token
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			return

		raise TokenParserException("Expected interface element name (identifier).", token)


class ItemBlock(Block):
	@classmethod
	def stateItemRemainder(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.Counter += 1
			elif (token == ")"):
				parserState.Counter -= 1
				if (parserState.Counter == 0):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					_ =                       CloseBlock(parserState.NewBlock, parserState.NewToken)
					parserState.Pop()
					parserState.TokenMarker = None
				else:
					parserState.NewToken =    ClosingRoundBracketToken(token)
					# parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.NewToken)
					# parserState.Pop()
			elif (token == ";"):
				if (parserState.Counter == 1):
					parserState.NewToken =    DelimiterToken(token)
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					_ =                       DelimiterBlock(parserState.NewBlock, parserState.NewToken)
					parserState.NextState =   DelimiterBlock.stateItemDelimiter
				else:
					raise TokenParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)


class DelimiterBlock(SkipableBlock):
	def __init__(self, previousBlock, startToken):
		super().__init__(previousBlock, startToken, startToken)

	@classmethod
	def stateItemDelimiter(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, StringToken):
			if (token <= "constant"):
				parserState.NewToken =    ConstantKeyword(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateConstantKeyword
				return
			elif (token <= "type"):
				parserState.NewToken =    TypeKeyword(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.PushState =   ParameterListInterfaceTypeBlock.stateTypeKeyword
				return
			elif (token <= "procedure"):
				raise NotImplementedError("Generic procedures are not supported.")
			elif (token <= "function"):
				raise NotImplementedError("Generic functions are not supported.")
			elif (token <= "impure"):
				raise NotImplementedError("Generic impure functions are not supported.")
			elif (token <= "pure"):
				raise NotImplementedError("Generic pure functions are not supported.")
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateObjectName
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   ParameterListInterfaceConstantBlock.stateObjectName
			return
		elif isinstance(token, SpaceToken):
			parserState.TokenMarker = token
			parserState.NextState =   ItemBlock.stateItemRemainder
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = token
			parserState.NextState =   ItemBlock.stateItemRemainder
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			return

		raise TokenParserException("Expected parameter name (identifier).", token)


class CloseBlock(CloseBlockBase):
	pass


class ParameterListInterfaceConstantBlock(InterfaceConstantBlock):
	DELIMITER_BLOCK = DelimiterBlock


class ParameterListInterfaceVariableBlock(InterfaceVariableBlock):
	DELIMITER_BLOCK = DelimiterBlock


class ParameterListInterfaceSignalBlock(InterfaceSignalBlock):
	DELIMITER_BLOCK = DelimiterBlock
