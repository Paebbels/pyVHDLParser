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

from pyVHDLParser.Token                   import CharacterToken, WordToken, SpaceToken, LinebreakToken, IndentationToken, CommentToken, MultiLineCommentToken, SingleLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords          import BoundaryToken, DelimiterToken, ClosingRoundBracketToken, IdentifierToken
from pyVHDLParser.Token.Keywords          import ConstantKeyword, SignalKeyword, VariableKeyword, TypeKeyword
from pyVHDLParser.Blocks                  import BlockParserException, Block, CommentBlock, ParserState, SkipableBlock
from pyVHDLParser.Blocks.Common           import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic1         import CloseBlock as CloseBlockBase
from pyVHDLParser.Blocks.InterfaceObject  import InterfaceSignalBlock, InterfaceConstantBlock, InterfaceVariableBlock


@export
class OpenBlock(Block):
	@classmethod
	def stateParameterKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "(")):
			parserState.NewToken =    BoundaryToken(fromExistingToken=token)
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

		raise BlockParserException("Expected '(' or whitespace after keyword PARAMETER.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "(")):
			parserState.NewToken =    BoundaryToken(fromExistingToken=token)
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

		raise BlockParserException("Expected '(' after keyword PARAMETER.", token)

	@classmethod
	def stateOpeningParenthesis(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			if (token <= "constant"):
				parserState.NewToken =    ConstantKeyword(fromExistingToken=token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateConstantKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token <= "variable"):
				parserState.NewToken =    VariableKeyword(fromExistingToken=token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   ParameterListInterfaceVariableBlock.stateVariableKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token <= "signal"):
				parserState.NewToken =    SignalKeyword(fromExistingToken=token)
				parserState.NextState =   DelimiterBlock.stateItemDelimiter
				parserState.PushState =   ParameterListInterfaceSignalBlock.stateSignalKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			else:
				parserState.NewToken =    IdentifierToken(fromExistingToken=token)
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateObjectName
				parserState.TokenMarker = parserState.NewToken
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

		raise BlockParserException("Expected interface element name (identifier).", token)


@export
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
					parserState.NewToken =    BoundaryToken(fromExistingToken=token)
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					_ =                       CloseBlock(parserState.NewBlock, parserState.NewToken)
					parserState.Pop()
					parserState.TokenMarker = None
				else:
					parserState.NewToken =    ClosingRoundBracketToken(fromExistingToken=token)
					# parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.NewToken)
					# parserState.Pop()
			elif (token == ";"):
				if (parserState.Counter == 1):
					parserState.NewToken =    DelimiterToken(fromExistingToken=token)
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
			tokenValue = token.Value.lower()
			if (tokenValue == "constant"):
				parserState.NewToken =    ConstantKeyword(fromExistingToken=token)
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateConstantKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (tokenValue == "variable"):
				parserState.NewToken =    VariableKeyword(fromExistingToken=token)
				parserState.PushState =   ParameterListInterfaceVariableBlock.stateVariableKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (tokenValue == "signal"):
				parserState.NewToken =    SignalKeyword(fromExistingToken=token)
				parserState.PushState =   ParameterListInterfaceSignalBlock.stateSignalKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (tokenValue == "type"):
				parserState.NewToken =    TypeKeyword(fromExistingToken=token)
				parserState.PushState =   ParameterListInterfaceTypeBlock.stateTypeKeyword
				parserState.TokenMarker = parserState.NewToken
				return
			elif (tokenValue == "procedure"):
				raise NotImplementedError("Generic procedures are not supported.")
			elif (tokenValue == "function"):
				raise NotImplementedError("Generic functions are not supported.")
			elif (tokenValue == "impure"):
				raise NotImplementedError("Generic impure functions are not supported.")
			elif (tokenValue == "pure"):
				raise NotImplementedError("Generic pure functions are not supported.")
			else:
				parserState.NewToken =    IdentifierToken(fromExistingToken=token)
				parserState.PushState =   ParameterListInterfaceConstantBlock.stateObjectName
				parserState.TokenMarker = parserState.NewToken
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

		raise BlockParserException("Expected parameter name (identifier).", token)


@export
class CloseBlock(CloseBlockBase):
	pass


@export
class ParameterListInterfaceConstantBlock(InterfaceConstantBlock):
	DELIMITER_BLOCK = DelimiterBlock


@export
class ParameterListInterfaceVariableBlock(InterfaceVariableBlock):
	DELIMITER_BLOCK = DelimiterBlock


@export
class ParameterListInterfaceSignalBlock(InterfaceSignalBlock):
	DELIMITER_BLOCK = DelimiterBlock
