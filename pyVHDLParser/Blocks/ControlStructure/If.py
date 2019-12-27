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
from pyVHDLParser.Decorators          import Export
from pyVHDLParser.Token               import CharacterToken, LinebreakToken, SpaceToken, IndentationToken, CommentToken, MultiLineCommentToken, SingleLineCommentToken
from pyVHDLParser.Token.Keywords      import StringToken, BoundaryToken, IfKeyword, ThenKeyword, ElsIfKeyword, ElseKeyword
from pyVHDLParser.Blocks              import TokenParserException, Block, CommentBlock, ParserState
from pyVHDLParser.Blocks.Common       import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic      import SequentialBeginBlock
from pyVHDLParser.Blocks.Generic1     import EndBlock as EndBlockBase
from pyVHDLParser.Blocks.Expression   import ExpressionBlockEndedByKeywordORClosingRoundBracket

__all__ = []
__api__ = __all__


@Export
class EndBlock(EndBlockBase):
	KEYWORD =       IfKeyword
	EXPECTED_NAME = KEYWORD.__KEYWORD__


@Export
class ThenBlock(SequentialBeginBlock):
	END_BLOCK = EndBlock

	@classmethod
	def stateThenKeyword(cls, parserState: ParserState):
		cls.stateSequentialRegion(parserState)

	@classmethod
	def stateSequentialRegion(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			if (tokenValue == "elsif"):
				newToken =                ElsIfKeyword(token)
				parserState.NewToken =    newToken
				parserState.TokenMarker = newToken
				parserState.NextState =   ElsIfConditionBlock.stateElsIfKeyword
				return
			elif (tokenValue == "else"):
				newToken =                ElseKeyword(token)
				parserState.NewToken =    newToken
				parserState.NewBlock =    ElseBlock(parserState.LastBlock, newToken)
				parserState.TokenMarker = None
				parserState.NextState =   ElseBlock.stateElseKeyword
				return

		super().stateSequentialRegion(parserState)


@Export
class ElseBlock(SequentialBeginBlock):
	END_BLOCK = EndBlock

	@classmethod
	def stateElseKeyword(cls, parserState: ParserState):
		cls.stateSequentialRegion(parserState)


@Export
class ExpressionBlockEndedByThen(ExpressionBlockEndedByKeywordORClosingRoundBracket):
	EXIT_KEYWORD = ThenKeyword
	EXIT_BLOCK =   ThenBlock


@Export
class IfConditionBlock(Block):
	@classmethod
	def stateIfKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   ThenBlock.stateThenKeyword
			parserState.PushState =   ExpressionBlockEndedByThen.stateExpression
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return
		else:
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			parserState.NextState =   ThenBlock.stateThenKeyword
			parserState.PushState =   ExpressionBlockEndedByThen.stateExpression
			parserState.TokenMarker = parserState.Token
			parserState.NextState(parserState)
			return

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, LinebreakToken):
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
		else:
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			parserState.NextState =   ThenBlock.stateThenKeyword
			parserState.PushState =   ExpressionBlockEndedByThen.stateExpression
			parserState.TokenMarker = parserState.Token
			parserState.NextState(parserState)
			return


@Export
class ElsIfConditionBlock(Block):
	@classmethod
	def stateElsIfKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   ThenBlock.stateThenKeyword
			parserState.PushState =   ExpressionBlockEndedByThen.stateExpression
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return
		else:
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			parserState.NextState =   ThenBlock.stateThenKeyword
			parserState.PushState =   ExpressionBlockEndedByThen.stateExpression
			parserState.TokenMarker = parserState.Token
			parserState.NextState(parserState)
			return

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, LinebreakToken):
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
		else:
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			parserState.NextState =   ThenBlock.stateThenKeyword
			parserState.PushState =   ExpressionBlockEndedByThen.stateExpression
			parserState.TokenMarker = parserState.Token
			parserState.NextState(parserState)
			return
