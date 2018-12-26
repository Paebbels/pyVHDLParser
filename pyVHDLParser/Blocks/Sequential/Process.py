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
from pyVHDLParser.Token                     import CharacterToken, SpaceToken, LinebreakToken, CommentToken, IndentationToken, MultiLineCommentToken, SingleLineCommentToken
from pyVHDLParser.Token.Keywords            import StringToken, BoundaryToken, IsKeyword, UseKeyword, ConstantKeyword, ImpureKeyword, PureKeyword
from pyVHDLParser.Token.Keywords            import VariableKeyword, ProcessKeyword, BeginKeyword, FunctionKeyword, ProcedureKeyword
from pyVHDLParser.Blocks                    import Block, CommentBlock, TokenParserException, ParserState
from pyVHDLParser.Blocks.Common             import LinebreakBlock, IndentationBlock, WhitespaceBlock
# from pyVHDLParser.Blocks.ControlStructure   import If, Case, ForLoop, WhileLoop
from pyVHDLParser.Blocks.Generic            import SequentialBeginBlock, SequentialDeclarativeRegion
from pyVHDLParser.Blocks.Generic1           import EndBlock as EndBlockBase
from pyVHDLParser.Blocks.List               import SensitivityList


class EndBlock(EndBlockBase):
	KEYWORD =             ProcessKeyword
	KEYWORD_IS_OPTIONAL = True
	EXPECTED_NAME =       KEYWORD.__KEYWORD__


class BeginBlock(SequentialBeginBlock):
	END_BLOCK =   EndBlock


class DeclarativeRegion(SequentialDeclarativeRegion):
	BEGIN_BLOCK = BeginBlock
	END_BLOCK =   EndBlock


class OpenBlock(Block):
	@classmethod
	def stateProcessKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =   OpenBlock2.stateAfterSensitivityList
			parserState.PushState =   SensitivityList.OpenBlock.stateOpeningParenthesis
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

		raise TokenParserException("Expected '(' or whitespace after keyword PROCESS.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "(")):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =   OpenBlock2.stateAfterSensitivityList
			parserState.PushState =   SensitivityList.OpenBlock.stateOpeningParenthesis
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
		elif isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)

			for keyword in OpenBlock2.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken = keyword(token)
					parserState.NextState =  DeclarativeRegion.stateDeclarativeRegion
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "begin"):
				parserState.NewToken =    BeginKeyword(token)
				_ =                       BeginBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   BeginBlock.stateSequentialRegion
				return

		raise TokenParserException("Expected '(' after keyword PROCESS.", token)

# TODO: Find a better name
class OpenBlock2(Block):
	KEYWORDS = None

	# TODO: Merge with OpenBlock.KEYWORDS ??
	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Object             import ConstantDeclarationBlock, ConstantDeclarationEndMarkerBlock, VariableDeclarationBlock, VariableDeclarationEndMarkerBlock
		from pyVHDLParser.Blocks.Reference          import Use
		from pyVHDLParser.Blocks.Reporting          import Report
		from pyVHDLParser.Blocks.Sequential         import Procedure, Function

		cls.KEYWORDS = {
			# Keyword     Transition
			UseKeyword:       Use.StartBlock.stateUseKeyword,
			ConstantKeyword:  ConstantDeclarationBlock.stateConstantKeyword,
			VariableKeyword:  VariableDeclarationBlock.stateVariableKeyword,
			FunctionKeyword:  Function.NameBlock.stateFunctionKeyword,
			ProcedureKeyword: Procedure.NameBlock.stateProcedureKeyword,
			ImpureKeyword:    Function.NameBlock.stateImpureKeyword,
			PureKeyword:      Function.NameBlock.statePureKeyword
		}

	@classmethod
	def stateAfterSensitivityList(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			for keyword in OpenBlock2.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken =                keyword(token)
					parserState.NextState =   DeclarativeRegion.stateDeclarativeRegion
					parserState.PushState =   OpenBlock2.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "begin"):
				parserState.NewToken =    BeginKeyword(token)
				parserState.NewBlock =    BeginBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   BeginBlock.stateSequentialRegion
				return
			elif (tokenValue == "is"):
				parserState.NewToken =    IsKeyword(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   DeclarativeRegion.stateDeclarativeRegion
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise TokenParserException("Expected whitespace after keyword ENTITY.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			for keyword in cls.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken =                keyword(token)
					parserState.NextState =   DeclarativeRegion.stateDeclarativeRegion
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "begin"):
				parserState.NewToken =    BeginKeyword(token)
				parserState.NewBlock =    BeginBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   BeginBlock.stateSequentialRegion
				return
			elif (tokenValue == "is"):
				parserState.NewToken =    IsKeyword(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   DeclarativeRegion.stateDeclarativeRegion
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

		raise TokenParserException("Expected declarations or keyword IS after sensitivity list.", token)
