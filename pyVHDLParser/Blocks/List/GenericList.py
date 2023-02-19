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
from pyTooling.Decorators                 import export

from pyVHDLParser.Token                   import CharacterToken, LinebreakToken, IndentationToken, CommentToken, MultiLineCommentToken, SingleLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords          import BoundaryToken, ConstantKeyword, TypeKeyword, DelimiterToken
from pyVHDLParser.Token.Keywords          import IdentifierToken
from pyVHDLParser.Token.Parser            import SpaceToken, WordToken
from pyVHDLParser.Blocks                  import BlockParserException, Block, CommentBlock, ParserState, SkipableBlock
from pyVHDLParser.Blocks.Common           import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic1         import CloseBlock as CloseBlockBase
from pyVHDLParser.Blocks.Expression       import ExpressionBlockEndedByCharORClosingRoundBracket
from pyVHDLParser.Blocks.InterfaceObject  import InterfaceConstantBlock, InterfaceTypeBlock


@export
class CloseBlock(CloseBlockBase):
	pass


@export
class DelimiterBlock(SkipableBlock):
	@classmethod
	def stateItemDelimiter(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			if (token <= "constant"):
				parserState.NewToken =    ConstantKeyword(fromExistingToken=token)
				parserState.PushState =   GenericListInterfaceConstantBlock.stateConstantKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token <= "type"):
				parserState.NewToken =    TypeKeyword(fromExistingToken=token)
				parserState.PushState =   GenericListInterfaceTypeBlock.stateTypeKeyword
				parserState.TokenMarker = parserState.NewToken
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
				parserState.NewToken =    IdentifierToken(fromExistingToken=token)
				parserState.PushState =   GenericListInterfaceConstantBlock.stateObjectName
				parserState.TokenMarker = parserState.NewToken
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   GenericListInterfaceConstantBlock.stateObjectName
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
			# parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected generic name (identifier).", token)


@export
class DefaultValueExpressionBlock(ExpressionBlockEndedByCharORClosingRoundBracket):
	EXIT_CHAR =  ";"
	EXIT_TOKEN = DelimiterToken
	EXIT_BLOCK = DelimiterBlock


@export
class GenericListInterfaceConstantBlock(InterfaceConstantBlock):
	DELIMITER_BLOCK = DelimiterBlock
	EXPRESSION =      DefaultValueExpressionBlock


@export
class GenericListInterfaceTypeBlock(InterfaceTypeBlock):
	DELIMITER_BLOCK = DelimiterBlock


@export
class OpenBlock(Block):
	@classmethod
	def stateGenericKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(fromExistingToken=token)
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

		raise BlockParserException("Expected '(' or whitespace after keyword GENERIC.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =      BoundaryToken(fromExistingToken=token)
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =     CloseBlock.stateClosingParenthesis
			parserState.PushState =     cls.stateOpeningParenthesis
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
			parserState.NewToken =      BoundaryToken(fromExistingToken=token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected '(' after keyword GENERIC.", token)

	@classmethod
	def stateOpeningParenthesis(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == ")")):
			# if (parserState.TokenMarker != token):
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
			parserState.Pop(1, token)
			return
		elif isinstance(token, WordToken):
			if (token <= "constant"):
				parserState.NewToken =    ConstantKeyword(fromExistingToken=token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   GenericListInterfaceConstantBlock.stateConstantKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token <= "type"):
				parserState.NewToken =    TypeKeyword(fromExistingToken=token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   GenericListInterfaceTypeBlock.stateTypeKeyword
				parserState.TokenMarker = parserState.NewToken
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
				parserState.NewToken =    IdentifierToken(fromExistingToken=token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   GenericListInterfaceConstantBlock.stateObjectName
				parserState.TokenMarker = parserState.NewToken
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   GenericListInterfaceConstantBlock.stateObjectName
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

		raise BlockParserException("Expected interface constant name (identifier) or keyword: CONSTANT, TYPE, PROCEDURE, FUNCTION, PURE, IMPURE.", token)
