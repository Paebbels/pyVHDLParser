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
from pyVHDLParser.Blocks.List               import SensitivityList
from pyVHDLParser.Token.Keywords            import *
from pyVHDLParser.Token.Parser              import *
from pyVHDLParser.Blocks                    import TokenParserException, Block
from pyVHDLParser.Blocks.Common             import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Comment            import SingleLineCommentBlock, MultiLineCommentBlock
from pyVHDLParser.Blocks.Generic            import EndBlock as EndBlockBase
from pyVHDLParser.Blocks.ControlStructure   import If, Case, ForLoop, WhileLoop
from pyVHDLParser.Blocks.Reporting          import Report
from pyVHDLParser.Blocks.Sequential         import Process
from pyVHDLParser.Blocks.ObjectDeclaration  import Constant, Variable
from pyVHDLParser.Blocks.Parser             import TokenToBlockParser

# Type alias for type hinting
ParserState = TokenToBlockParser.TokenParserState


class OpenBlock(Block):
	@classmethod
	def stateProcessKeyword(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected '(' or whitespace after keyword "
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
				parserState.NewToken =    BoundaryToken(token)
				_ =                       SensitivityList.OpenBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   OpenBlock2.stateAfterSensitivityList
				parserState.PushState =   SensitivityList.OpenBlock.stateOpeningParenthesis
				parserState.Counter =     1
				return
			elif (token == "\n"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace1
			return

		raise TokenParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected '(' after PROCESS keyword."
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
				parserState.NewToken =    BoundaryToken(token)
				_ =                       SensitivityList.OpenBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   OpenBlock2.stateAfterSensitivityList
				parserState.PushState =   SensitivityList.OpenBlock.stateOpeningParenthesis
				parserState.Counter =     1
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				if (not isinstance(parserState.LastBlock, MultiLineCommentBlock)):
					parserState.NewBlock =  OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken, multiPart=True)
					_ =                     LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				else:
					parserState.NewBlock =  LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise TokenParserException(errorMessage, token)


class OpenBlock2(Block):
	@classmethod
	def stateAfterSensitivityList(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =      LinebreakToken(token)
				parserState.NewBlock =      LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker =   None
				parserState.NextState =     cls.stateWhitespace1
				parserState.PushState =     LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.PushState =     SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
			elif (token == "/"):
				parserState.PushState =     MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =        BoundaryToken(token)
			parserState.TokenMarker =     parserState.NewToken
			parserState.NextState =       cls.stateWhitespace1
			return
		elif isinstance(token, StringToken):
			if (token <= "is"):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      OpenBlock2(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
				return
			else:
				parserState.NextState =     cls.stateDeclarativeRegion
				parserState.NextState(parserState)
				return

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected BEGIN after IS keyword."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =      LinebreakToken(token)
				if (not isinstance(parserState.LastBlock, MultiLineCommentBlock)):
					parserState.NewBlock =    OpenBlock2(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken, multiPart=True)
					_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				else:
					parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker =   None
				parserState.PushState =     LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =      OpenBlock2(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker =   None
				parserState.PushState =     SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
			elif (token == "/"):
				parserState.NewBlock =      OpenBlock2(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker =   None
				parserState.PushState =     MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =        BoundaryToken(token)
			parserState.NewBlock =        WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =     None
			return
		elif isinstance(token, StringToken):
			if (token <= "is"):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      OpenBlock2(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return
			else:
				parserState.NextState =     cls.stateDeclarativeRegion
				parserState.NextState(parserState)
				return

		raise TokenParserException(errorMessage, token)

	@classmethod
	def stateDeclarativeRegion(cls, parserState: ParserState):
		errorMessage = "Expected one of these keywords: generic, port, is, begin, end."
		token = parserState.Token
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			keyword = token.Value.lower()
			if (keyword == "constant"):
				newToken =              ConstantKeyword(token)
				parserState.PushState = Constant.ConstantBlock.stateConstantKeyword
			elif (keyword == "variable"):
				newToken =              VariableKeyword(token)
				parserState.PushState = Variable.VariableBlock.stateVariableKeyword
			elif (keyword == "begin"):
				parserState.NewToken =  BeginKeyword(token)
				parserState.NewBlock =  BeginBlock(parserState.LastBlock, parserState.NewToken)
				parserState.NextState = BeginBlock.stateBeginKeyword
				return
			elif (keyword == "is"):
				parserState.NewToken =  IsKeyword(token)
				parserState.NewBlock =  OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				# parserState.NextState = BeginBlock.stateBeginKeyword
				return
			else:
				raise TokenParserException(errorMessage, token)

			parserState.NewToken =      newToken
			parserState.TokenMarker =   newToken
			return

		raise TokenParserException(errorMessage, token)

class BeginBlock(Block):
	@classmethod
	def stateBeginKeyword(cls, parserState: ParserState):
		errorMessage = "Expected label or one of these keywords: if, case, for, while, report, end."
		token = parserState.Token
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			keyword = token.Value.lower()
			if (keyword == "if"):
				newToken =                IfKeyword(token)
				parserState.PushState =   If.IfConditionBlock.stateIfKeyword
			elif (keyword == "case"):
				newToken =                CaseKeyword(token)
				parserState.PushState =   Case.CaseBlock.stateCaseKeyword
			elif (keyword == "for"):
				newToken =                ForKeyword(token)
				parserState.PushState =   ForLoop.RangeBlock.stateForKeyword
			elif (keyword == "while"):
				newToken =                WhileKeyword(token)
				parserState.PushState =   WhileLoop.ConditionBlock.stateWhileKeyword
			elif (keyword == "report"):
				newToken =                ReportKeyword(token)
				parserState.PushState =   Report.ReportBlock.stateReportKeyword
			elif (keyword == "end"):
				newToken = EndKeyword(token)
				parserState.NextState =   EndBlock.stateEndKeyword
			else:
				raise TokenParserException(errorMessage, token)

			parserState.NewToken = newToken
			parserState.TokenMarker = newToken
			return

		raise TokenParserException(errorMessage, token)


class EndBlock(EndBlockBase):
	KEYWORD =             ProcessKeyword
	KEYWORD_IS_OPTIONAL = True
	EXPECTED_NAME =       KEYWORD.__KEYWORD__
