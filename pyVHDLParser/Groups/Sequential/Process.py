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
from collections                          import ChainMap
from itertools                            import chain

from pyTooling.Decorators                 import export

from pyVHDLParser.Blocks                  import CommentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common           import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.List             import SensitivityList, GenericList, ParameterList
from pyVHDLParser.Blocks.Object.Variable  import VariableDeclarationBlock
from pyVHDLParser.Blocks.Object.Constant  import ConstantDeclarationBlock
from pyVHDLParser.Blocks.Reference        import Use
from pyVHDLParser.Blocks.Reporting.Report import ReportBlock
from pyVHDLParser.Blocks.Sequential       import Process
from pyVHDLParser.Groups                  import ParserState, Group, GroupParserException, EndOfDocumentGroup
from pyVHDLParser.Groups.Comment          import WhitespaceGroup, CommentGroup
from pyVHDLParser.Groups.List             import GenericListGroup, ParameterListGroup, SensitivityListGroup
from pyVHDLParser.Groups.Object           import ConstantGroup, VariableGroup
from pyVHDLParser.Groups.Reference        import UseGroup


@export
class ProcessGroup(Group):
	DECLARATION_SIMPLE_BLOCKS = {
		Use.StartBlock:           UseGroup,
		ConstantDeclarationBlock: ConstantGroup,
		VariableDeclarationBlock: VariableGroup
	}
	DECLARATION_COMPOUND_BLOCKS = {
		# Process.NameBlock:       ProcessGroup,
		# Procedure.NameBlock:      ProcedureGroup
	}
	STATEMENT_SIMPLE_BLOCKS = {
		# ReportBlock:              ReportGroup
	}
	STATEMENT_COMPOUND_BLOCKS = {
		# If.OpenBlock:        IfGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = dict(ChainMap(
			{v: [] for v in chain(
				self.DECLARATION_SIMPLE_BLOCKS.values(),
				self.DECLARATION_COMPOUND_BLOCKS.values(),
				self.STATEMENT_SIMPLE_BLOCKS.values(),
				self.STATEMENT_COMPOUND_BLOCKS.values()
			)},
			{CommentGroup: [],
			 WhitespaceGroup: []
			 }
		))

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		# consume OpenBlock
		if isinstance(currentBlock, Process.OpenBlock):
			parserState.NextGroup =   cls(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.NextState =   cls.stateParseSensitivityList
			return
		else:
			raise GroupParserException("Begin of process expected.", currentBlock)

	@classmethod
	def stateParseSensitivityList(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, SensitivityList.OpenBlock):
			parserState.NextState =   cls.stateParseDeclarations
			parserState.PushState =   SensitivityListGroup.stateParse
			parserState.NextGroup =   SensitivityListGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			parserState.PushState =   WhitespaceGroup.stateParse
			parserState.NextGroup =   WhitespaceGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, CommentBlock):
			parserState.PushState =   CommentGroup.stateParse
			parserState.NextGroup =   CommentGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise GroupParserException("End of process sensitivity list not found.", currentBlock)

	@classmethod
	def stateParseDeclarations(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Process.BeginBlock):
			parserState.NextState =   cls.stateParseStatements
			return
		elif isinstance(currentBlock, Process.EndBlock):
			parserState.NextGroup =   cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			parserState.PushState =   WhitespaceGroup.stateParse
			parserState.NextGroup =   WhitespaceGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, CommentBlock):
			parserState.PushState =   CommentGroup.stateParse
			parserState.NextGroup =   CommentGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		else:
			for block in cls.DECLARATION_SIMPLE_BLOCKS:
				if isinstance(currentBlock, block):
					group = cls.DECLARATION_SIMPLE_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for block in cls.DECLARATION_COMPOUND_BLOCKS:
				if isinstance(currentBlock, block):
					group =                   cls.DECLARATION_COMPOUND_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise GroupParserException("End of process declarative region not found.", currentBlock)

	@classmethod
	def stateParseStatements(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Process.EndBlock):
			parserState.NextGroup =   cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			parserState.PushState =   WhitespaceGroup.stateParse
			parserState.NextGroup =   WhitespaceGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, CommentBlock):
			parserState.PushState =   CommentGroup.stateParse
			parserState.NextGroup =   CommentGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		else:
			for block in cls.STATEMENT_SIMPLE_BLOCKS:
				if isinstance(currentBlock, block):
					group = cls.STATEMENT_SIMPLE_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for block in cls.STATEMENT_COMPOUND_BLOCKS:
				if isinstance(currentBlock, block):
					group =                   cls.STATEMENT_COMPOUND_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise GroupParserException("End of process declaration not found.", currentBlock)



@export
class IfGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class IfBranchGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class ElsIfBranchGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class ElseBranchGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class CaseGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class ChoiceGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class ForLoopGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class WhileLoopGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class NextGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class ExitGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class ReturnGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class VariableAssignmentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@export
class SignalAssignmentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))
