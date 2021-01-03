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
from pydecor.decorators                   import export

from pyVHDLParser.Token                   import LinebreakToken, WordToken, SpaceToken, CommentToken, IndentationToken
from pyVHDLParser.Token.Keywords          import AssertKeyword, EndKeyword, ProcessKeyword, ReportKeyword, IfKeyword, ForKeyword, ReturnKeyword, NextKeyword, NullKeyword
from pyVHDLParser.Token.Keywords          import ExitKeyword, UseKeyword, SignalKeyword, ConstantKeyword, SharedKeyword, FunctionKeyword, ProcedureKeyword
from pyVHDLParser.Token.Keywords          import ImpureKeyword, PureKeyword, VariableKeyword, BeginKeyword, CaseKeyword
from pyVHDLParser.Blocks                  import BlockParserException, CommentBlock, ParserState, MetaBlock
from pyVHDLParser.Blocks.Common           import LinebreakBlock, WhitespaceBlock, IndentationBlock
from pyVHDLParser.Blocks.Object.Variable  import VariableDeclarationBlock
from pyVHDLParser.Blocks.Generic1         import EndBlock, BeginBlock

__all__ = []
__api__ = __all__


@export
class DeclarativeRegion(metaclass=MetaBlock):
	"""Base-class for all declarative region blocks."""

	BEGIN_BLOCK: BeginBlock = None
	END_BLOCK:   EndBlock =   None

	KEYWORDS = None

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Reference        import Use
		from pyVHDLParser.Blocks.Object.Constant  import ConstantDeclarationBlock
		from pyVHDLParser.Blocks.Sequential       import Procedure, Function

		cls.KEYWORDS = {
			# Keyword         Transition
			UseKeyword:       Use.StartBlock.stateUseKeyword,
			ConstantKeyword:  ConstantDeclarationBlock.stateConstantKeyword,
			FunctionKeyword:  Function.NameBlock.stateFunctionKeyword,
			ProcedureKeyword: Procedure.NameBlock.stateProcedureKeyword,
			ImpureKeyword:    Function.NameBlock.stateImpureKeyword,
			PureKeyword:      Function.NameBlock.statePureKeyword,
			# AliasKeyword:     Alias.NameBlock.stateAliasKeyword
		}


	@classmethod
	def stateDeclarativeRegion(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			blockType =                 IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =      blockType(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, WordToken):
			tokenValue = token.Value.lower()

			for keyword in cls.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken =                keyword(token)
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "begin"):
				parserState.NewToken =  BeginKeyword(token)
				parserState.NewBlock =  cls.BEGIN_BLOCK(parserState.LastBlock, parserState.NewToken)
				parserState.NextState = cls.BEGIN_BLOCK.stateStatementRegion
				return
			elif (tokenValue == "end"):
				parserState.NewToken =  EndKeyword(token)
				parserState.NextState = cls.END_BLOCK.stateEndKeyword
				return

		raise BlockParserException(
			"Expected one of these keywords: BEGIN, END, {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


@export
class ConcurrentDeclarativeRegion(DeclarativeRegion):
	"""Base-class for all concurrent declarative region blocks."""

	@classmethod
	def __cls_init__(cls):
		super().__cls_init__()

		from pyVHDLParser.Blocks.Object.Signal         import SignalDeclarationBlock
		from pyVHDLParser.Blocks.Object.SharedVariable import SharedVariableDeclarationBlock

		cls.KEYWORDS.update({
			# Keyword         Transition
			SignalKeyword:    SignalDeclarationBlock.stateSignalKeyword,
			SharedKeyword:    SharedVariableDeclarationBlock.stateSharedKeyword
		})


@export
class SequentialDeclarativeRegion(DeclarativeRegion):
	"""Base-class for all sequential declarative region blocks."""

	@classmethod
	def __cls_init__(cls):
		super().__cls_init__()

		# TODO: use key assignment: a[b] = c
		cls.KEYWORDS.update({
			# Keyword         Transition
			VariableKeyword:  VariableDeclarationBlock.stateVariableKeyword
		})


@export
class ConcurrentBeginBlock(BeginBlock):
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
	def stateStatementRegion(cls, parserState: ParserState):
		parserState.NextState = cls.stateConcurrentRegion
		parserState.NextState(parserState)

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
		elif isinstance(token, WordToken):
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

		raise BlockParserException(
			"Expected one of these keywords: END, {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


@export
class SequentialBeginBlock(BeginBlock):
	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.ControlStructure.If        import IfConditionBlock
		from pyVHDLParser.Blocks.ControlStructure.Case      import CaseBlock
		from pyVHDLParser.Blocks.ControlStructure.Exit      import ExitBlock
		from pyVHDLParser.Blocks.ControlStructure.Next      import NextBlock
		from pyVHDLParser.Blocks.ControlStructure.Return    import ReturnBlock
		from pyVHDLParser.Blocks.ControlStructure.ForLoop   import IteratorBlock
		# from pyVHDLParser.Blocks.ControlStructure.WhileLoop import ConditionBlock
		from pyVHDLParser.Blocks.Reporting.Report           import ReportBlock
		from pyVHDLParser.Blocks.ControlStructure.Null      import NullBlock

		cls.KEYWORDS = {
			# Keyword       Transition
			IfKeyword:      IfConditionBlock.stateIfKeyword,
			CaseKeyword:    CaseBlock.stateCaseKeyword,
			ForKeyword:     IteratorBlock.stateForKeyword,
			# WhileKeyword:   ConditionBlock.stateWhileKeyword,
			ReturnKeyword:  ReturnBlock.stateReturnKeyword,
			NextKeyword:    NextBlock.stateNextKeyword,
			ExitKeyword:    ExitBlock.stateExitKeyword,
			ReportKeyword:  ReportBlock.stateReportKeyword,
			NullKeyword:    NullBlock.stateNullKeyword
		}

	@classmethod
	def stateStatementRegion(cls, parserState: ParserState):
		cls.stateAnyRegion(parserState)

	@classmethod
	def stateSequentialRegion(cls, parserState: ParserState):
		cls.stateAnyRegion(parserState)

	@classmethod
	def stateAnyRegion(cls, parserState: ParserState):
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
		elif isinstance(token, WordToken):
			tokenValue = token.Value.lower()

			for keyword in cls.KEYWORDS:
				if (tokenValue == keyword.__KEYWORD__):
					newToken =                keyword(token)
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

			if (tokenValue == "end"):
				parserState.NewToken =  EndKeyword(token)
				parserState.NextState = cls.END_BLOCK.stateEndKeyword
				return

		raise BlockParserException(
			"Expected one of these keywords: END, {keywords}. Found: '{tokenValue}' at line {tokenPositionRow}:{tokenPositionColumn}.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value,
				tokenPositionRow=token.Start.Row,
				tokenPositionColumn=token.Start.Column
			), token)
