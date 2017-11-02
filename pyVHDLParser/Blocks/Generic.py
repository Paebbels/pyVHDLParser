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
from pyVHDLParser.Token           import LinebreakToken, CommentToken, IndentationToken
from pyVHDLParser.Token.Keywords import AssertKeyword, EndKeyword, ProcessKeyword, ReportKeyword, IfKeyword, ForKeyword, ReturnKeyword, NextKeyword, \
	ExitKeyword, ElsIfKeyword, ElseKeyword
from pyVHDLParser.Token.Parser    import SpaceToken, StringToken
from pyVHDLParser.Blocks          import TokenParserException, Block, CommentBlock, ParserState
from pyVHDLParser.Blocks.Common   import LinebreakBlock, WhitespaceBlock, IndentationBlock
from pyVHDLParser.Blocks.Generic1 import EndBlock


class ConcurrentBeginBlock(Block):
	END_BLOCK : EndBlock = None

	KEYWORDS = None

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Sequential       import Process
		from pyVHDLParser.Blocks.Reporting.Assert import AssertBlock

		cls.KEYWORDS = {
			# Keyword           Transition
			AssertKeyword:      AssertBlock.stateAssertKeyword,
			ProcessKeyword:     Process.OpenBlock.stateProcessKeyword,
		}

	@classmethod
	def stateConcurrentRegion(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			for keyword in cls.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken = keyword(token)
					parserState.PushState = cls.KEYWORDS[keyword]
					parserState.NewToken = newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "end"):
				parserState.NewToken =  EndKeyword(token)
				parserState.NextState = cls.END_BLOCK.stateEndKeyword
				return

		raise TokenParserException(
			"Expected one of these keywords: END, {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


class SequentialBeginBlock(Block):
	END_BLOCK : EndBlock = None

	KEYWORDS = None

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.ControlStructure.If        import IfConditionBlock, ElsIfConditionBlock, ElseBlock
		# from pyVHDLParser.Blocks.ControlStructure.Case      import CaseBlock
		from pyVHDLParser.Blocks.ControlStructure.Exit      import ExitBlock
		from pyVHDLParser.Blocks.ControlStructure.Next      import NextBlock
		from pyVHDLParser.Blocks.ControlStructure.Return    import ReturnBlock
		from pyVHDLParser.Blocks.ControlStructure.ForLoop   import IteratorBlock
		# from pyVHDLParser.Blocks.ControlStructure.WhileLoop import ConditionBlock
		from pyVHDLParser.Blocks.Reporting.Report           import ReportBlock

		cls.KEYWORDS = {
			# Keyword       Transition
			IfKeyword:      IfConditionBlock.stateIfKeyword,
			ElsIfKeyword:   ElsIfConditionBlock.stateElsIfKeyword,
			ElseKeyword:    ElseBlock.stateThenKeyword,
			# CaseKeyword:    CaseBlock.stateCaseKeyword,
			ForKeyword:     IteratorBlock.stateForKeyword,
			# WhileKeyword:   ConditionBlock.stateWhileKeyword,
			ReturnKeyword:  ReturnBlock.stateReturnKeyword,
			NextKeyword:    NextBlock.stateNextKeyword,
			ExitKeyword:    ExitBlock.stateExitKeyword,
			ReportKeyword:  ReportBlock.stateReportKeyword
		}

	@classmethod
	def stateSequentialRegion(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			for keyword in cls.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken = keyword(token)
					parserState.PushState = cls.KEYWORDS[keyword]
					parserState.NewToken = newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "end"):
				parserState.NewToken =  EndKeyword(token)
				parserState.NextState = cls.END_BLOCK.stateEndKeyword
				return

		raise TokenParserException(
			"Expected one of these keywords: END, {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


