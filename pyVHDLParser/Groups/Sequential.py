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
from pyVHDLParser.Blocks import CommentBlock
from pyVHDLParser.Blocks.Common import LinebreakBlock, IndentationBlock, EmptyLineBlock
from pyVHDLParser.Blocks.Document import EndOfDocumentBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Constant import ConstantBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Variable import VariableBlock
from pyVHDLParser.Blocks.Reference.Use import UseBlock
from pyVHDLParser.Blocks.Sequential import Function, Procedure
from pyVHDLParser.Groups import BlockParserState, Group, BlockParserException


# Type alias for type hinting
from pyVHDLParser.Groups.Comment import WhitespaceGroup, CommentGroup
from pyVHDLParser.Groups.ObjectDeclaration import ConstantGroup, VariableGroup
from pyVHDLParser.Groups.Reference import UseGroup
from pyVHDLParser.Token.Keywords import EndToken


ParserState = BlockParserState


class FunctionGroup(Group):
	__SIMPLE_BLOCKS__ = {
		UseBlock:                 UseGroup,
		ConstantBlock:            ConstantGroup,
		VariableBlock:            VariableGroup
	}
	# __COMPOUND_BLOCKS__ = {
	# 	# Function.NameBlock:       FunctionGroup,
	# 	Procedure.NameBlock:      ProcedureGroup
	# }

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    [],
			UseGroup:           [],
			FunctionGroup:      [],
			ProcedureGroup:     []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		__COMPOUND_BLOCKS__ = {
			Function.NameBlock:       FunctionGroup,
			Procedure.NameBlock: ProcedureGroup
		}

		if isinstance(currentBlock, Function.NameBlock):
			return
		elif isinstance(currentBlock, Function.NameBlock2):
			if isinstance(currentBlock.EndToken, EndToken):
				print("semicolon found -> function prototype")
				parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
				parserState.Pop()

			return
		elif isinstance(currentBlock, Function.BeginBlock):
			return
		elif isinstance(currentBlock, Function.EndBlock):
			parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			parserState.PushState = WhitespaceGroup.stateParse
			parserState.NextGroup = WhitespaceGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue = True
			return
		elif isinstance(currentBlock, CommentBlock):
			parserState.PushState = CommentGroup.stateParse
			parserState.NextGroup = CommentGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue = True
			return
		else:
			for block in cls.__SIMPLE_BLOCKS__:
				if isinstance(currentBlock, block):
					group = cls.__SIMPLE_BLOCKS__[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for block in __COMPOUND_BLOCKS__:
				if isinstance(currentBlock, block):
					group =                   __COMPOUND_BLOCKS__[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class ProcedureGroup(Group):
	__SIMPLE_BLOCKS__ = {
		UseBlock:                 UseGroup,
		ConstantBlock:            ConstantGroup,
		VariableBlock:            VariableGroup
	}
	__COMPOUND_BLOCKS__ = {
		Function.NameBlock:       FunctionGroup,
		# Procedure.NameBlock:      ProcedureGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    [],
			UseGroup:           [],
			FunctionGroup:      [],
			ProcedureGroup:     []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Procedure.NameBlock):
			return
		elif isinstance(currentBlock, Procedure.EndBlock):
			parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			parserState.PushState = WhitespaceGroup.stateParse
			parserState.NextGroup = WhitespaceGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue = True
			return
		elif isinstance(currentBlock, CommentBlock):
			parserState.PushState = CommentGroup.stateParse
			parserState.NextGroup = CommentGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue = True
			return
		else:
			for block in cls.__SIMPLE_BLOCKS__:
				if isinstance(currentBlock, block):
					group = cls.__SIMPLE_BLOCKS__[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for block in cls.__COMPOUND_BLOCKS__:
				if isinstance(currentBlock, block):
					group =                   cls.__COMPOUND_BLOCKS__[block]
					parserState.NextGroup =    group(parserState.LastGroup, parserState.BlockMarker, currentBlock)
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class IfGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class IfBranchGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ElsIfBranchGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ElseBranchGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class CaseGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ChoiceGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ForLoopGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class WhileLoopGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class NextGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ExitGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ReturnGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class VariableAssignmentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class SignalAssignmentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))
