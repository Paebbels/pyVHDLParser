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

from pyVHDLParser.Token           import WordToken, ExtendedIdentifier, LinebreakToken, MultiLineCommentToken
from pyVHDLParser.Token           import CommentToken, SpaceToken, CharacterToken, FusedCharacterToken
from pyVHDLParser.Token.Keywords  import IdentifierToken, BoundaryToken, VariableAssignmentKeyword, EndToken
from pyVHDLParser.Blocks          import Block, ParserState, CommentBlock, BlockParserException
from pyVHDLParser.Blocks.Common   import LinebreakBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic1 import EndOfStatementBlock

__all__ = []
__api__ = __all__


@export
class ObjectDeclarationBlock(Block):
	OBJECT_KIND =       ""
	EXPRESSION_BLOCK =  None
	END_BLOCK =         None

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(token)
			parserState.NextState =   cls.stateObjectName
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   cls.stateObjectName
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
			parserState.NewBlock =    CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected {0} name (identifier).".format(cls.OBJECT_KIND), token)

	@classmethod
	def stateObjectName(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ":")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateColon1
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace2
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace2
			return

		raise BlockParserException("Expected ':' or whitespace after {0} name.".format(cls.OBJECT_KIND), token)

	@classmethod
	def stateWhitespace2(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ":")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateColon1
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
			parserState.NewBlock =    CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected colon after {0} name.".format(cls.OBJECT_KIND), token)

	@classmethod
	def stateColon1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(token)
			parserState.NextState =   cls.stateSubtypeIndication
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

		raise BlockParserException("Expected subtype indication or whitespace after colon.", token)

	@classmethod
	def stateWhitespace3(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(token)
			parserState.NextState =   cls.stateSubtypeIndication
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
			parserState.NewBlock =    CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected subtype indication after colon.", token)

	@classmethod
	def stateSubtypeIndication(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, FusedCharacterToken) and (token == ":=")):
			parserState.NewToken =    VariableAssignmentKeyword(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.PushState =   cls.EXPRESSION_BLOCK.stateExpression
			parserState.TokenMarker = None
			parserState.Counter =     0
			return
		elif (isinstance(token, CharacterToken) and (token == ';')):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
			_ =                       cls.END_BLOCK(parserState.NewBlock, parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace4
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace4
			return

		raise BlockParserException("Expected ':=', ';' or whitespace after subtype indication.", token)

	@classmethod
	def stateWhitespace4(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, FusedCharacterToken) and (token == ":=")):
			parserState.NewToken =    VariableAssignmentKeyword(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.PushState =   cls.EXPRESSION_BLOCK.stateExpression
			parserState.TokenMarker = None
			parserState.Counter =     0
			return
		elif (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
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
			parserState.NewBlock =    CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected ':=' or ';' after subtype indication.", token)


@export
class ObjectDeclarationEndMarkerBlock(EndOfStatementBlock):
	pass
