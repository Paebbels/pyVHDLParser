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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany                                                            #
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
from pyTooling.Decorators           import export

from pyVHDLParser.Token             import SpaceToken, LinebreakToken, CommentToken, IndentationToken, SingleLineCommentToken, MultiLineCommentToken
from pyVHDLParser.Token             import WordToken, ExtendedIdentifier, CharacterToken
from pyVHDLParser.Token.Keywords    import BoundaryToken, IdentifierToken, EndToken, WhenKeyword
from pyVHDLParser.Blocks            import Block, ParserState, CommentBlock, BlockParserException
from pyVHDLParser.Blocks.Common     import LinebreakBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic1   import EndOfStatementBlock
from pyVHDLParser.Blocks.Expression import ExpressionBlockEndedBySemicolon


@export
class EndBlock(EndOfStatementBlock):
	pass


@export
class ExitConditionBlock(ExpressionBlockEndedBySemicolon):
	END_BLOCK = EndBlock


@export
class ExitBlock(Block):
	@classmethod
	def stateExitKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			# parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
			# parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected ';' or whitespace after keyword EXIT.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, WordToken):
			if (token <= "when"):
				parserState.NewToken =    WhenKeyword(token)
				parserState.NextState =   cls.stateWhenKeyword
				return
			else:
				parserState.NewToken =    IdentifierToken(token)
				# parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   cls.stateExitLoopLabel
				return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   cls.stateExitLoopLabel
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected ';', keyword WHEN or loop label.", token)

	@classmethod
	def stateExitLoopLabel(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			# parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			# parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace2
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace2
			return

		raise BlockParserException("Expected ';' or whitespace after loop label.", token)

	@classmethod
	def stateWhitespace2(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif (isinstance(token, WordToken) and (token <= "when")):
			parserState.NewToken =    WhenKeyword(token)
			parserState.NextState =   cls.stateWhenKeyword
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected ';' or keyword WHEN.", token)

	@classmethod
	def stateWhenKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if  (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
				parserState.Pop()
				return
			elif  (token == "("):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   EndBlock.stateError
				parserState.PushState =   ExitConditionBlock.stateExpression
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace3
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace3
			return

		raise BlockParserException("Expected ';' or whitespace after keyword RETURN.", token)

	@classmethod
	def stateWhitespace3(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and  (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
			parserState.Pop()
			return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =  cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                     LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =  LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (
			isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return
		else:
			parserState.NewBlock = cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			parserState.NextState =   EndBlock.stateError
			parserState.PushState =   ExitConditionBlock.stateExpression
			parserState.TokenMarker = parserState.Token
			parserState.NextState(parserState)
			return
