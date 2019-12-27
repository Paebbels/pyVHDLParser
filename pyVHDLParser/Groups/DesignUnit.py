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
from collections                              import ChainMap
from itertools                                import chain

from pyVHDLParser.Decorators                  import Export
from pyVHDLParser.Blocks                      import CommentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common               import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.List                 import GenericList, ParameterList, PortList
from pyVHDLParser.Blocks.Object.Constant      import ConstantBlock
from pyVHDLParser.Blocks.Object.Signal        import SignalBlock
from pyVHDLParser.Blocks.Reference            import Context, Library, Use
from pyVHDLParser.Blocks.Reporting.Assert     import AssertBlock
from pyVHDLParser.Blocks.Sequential           import Package, PackageBody, Function, Procedure, Process
from pyVHDLParser.Blocks.Structural           import Entity, Architecture, Component, Configuration
from pyVHDLParser.Groups                      import BlockParserException, Group, EndOfDocumentGroup, ParserState
from pyVHDLParser.Groups.Comment              import CommentGroup, WhitespaceGroup
from pyVHDLParser.Groups.Concurrent           import AssertGroup
from pyVHDLParser.Groups.List                 import GenericListGroup, ParameterListGroup, PortListGroup
from pyVHDLParser.Groups.Object               import ConstantGroup, SignalGroup
from pyVHDLParser.Groups.Reference            import LibraryGroup, UseGroup
from pyVHDLParser.Groups.Sequential.Function  import FunctionGroup
from pyVHDLParser.Groups.Sequential.Procedure import ProcedureGroup
from pyVHDLParser.Groups.Sequential.Process   import ProcessGroup
from pyVHDLParser.Functions                   import Console

__all__ = []
__api__ = __all__


@Export
class ContextGroup(Group):
	SIMPLE_BLOCKS = {
		Library.StartBlock:    LibraryGroup,
		Use.StartBlock:        UseGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    [],
			LibraryGroup:       [],
			UseGroup:           []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Context.NameBlock):
			return
		elif isinstance(currentBlock, Context.EndBlock):
			parserState.NextGroup =   cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
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
			for block in cls.SIMPLE_BLOCKS:
				if isinstance(currentBlock, block):
					group = cls.SIMPLE_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@Export
class EntityGroup(Group):
	DECLARATION_SIMPLE_BLOCKS = {
		GenericList.OpenBlock:  GenericListGroup,
		PortList.OpenBlock:     PortListGroup,
		Use.StartBlock:         UseGroup,
		ConstantBlock:          ConstantGroup
	}
	DECLARATION_COMPOUND_BLOCKS = {}
	STATEMENT_SIMPLE_BLOCKS = {
		AssertBlock:             AssertGroup
	}
	STATEMENT_COMPOUND_BLOCKS = {
		Process.OpenBlock:       ProcessGroup,
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
		if isinstance(currentBlock, Entity.NameBlock):
			parserState.NextGroup =   cls(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.NextState =   cls.stateParseGenerics
			return
		else:
			raise BlockParserException("Begin of entity expected.", currentBlock)

	@classmethod
	def stateParseGenerics(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, GenericList.OpenBlock):
			parserState.NextState =   cls.stateParsePorts
			parserState.PushState =   GenericListGroup.stateParse
			parserState.NextGroup =   GenericListGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, PortList.OpenBlock):
			parserState.NextState =   cls.stateParseDeclarations
			parserState.PushState =   PortListGroup.stateParse
			parserState.NextGroup =   PortListGroup(parserState.LastGroup, currentBlock)
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

		raise BlockParserException("End of generic clause not found.", currentBlock)

	@classmethod
	def stateParsePorts(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, PortList.OpenBlock):
			parserState.NextState =   cls.stateParseDeclarations
			parserState.PushState =   PortListGroup.stateParse
			parserState.NextGroup =   PortListGroup(parserState.LastGroup, currentBlock)
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

		raise BlockParserException("End of port clause not found.", currentBlock)

	@classmethod
	def stateParseDeclarations(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Entity.BeginBlock):
			parserState.NextState =   cls.stateParseStatements
			return
		elif isinstance(currentBlock, Entity.EndBlock):
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

		raise BlockParserException("End of entity declarative region not found.", currentBlock)

	@classmethod
	def stateParseStatements(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Entity.EndBlock):
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

		raise BlockParserException("End of entity declaration not found.", currentBlock)


@Export
class ArchitectureGroup(Group):
	DECLARATION_SIMPLE_BLOCKS = {
		Use.StartBlock:           UseGroup,
		ConstantBlock:            ConstantGroup,
		# SharedVariableBlock:            VariableGroup,
		SignalBlock:              SignalGroup
	}
	DECLARATION_COMPOUND_BLOCKS = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}
	STATEMENT_SIMPLE_BLOCKS = {
		AssertBlock:              AssertGroup
	}
	STATEMENT_COMPOUND_BLOCKS = {
		Process.OpenBlock:        ProcessGroup
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

		if isinstance(currentBlock, Architecture.NameBlock):
			parserState.NextState =   cls.stateParseDeclarations
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
		elif isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup =   EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of architecture declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)

	@classmethod
	def stateParseDeclarations(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Architecture.BeginBlock):
			parserState.NextState =   cls.stateParseStatements
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

		raise BlockParserException("End of architecture declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)

	@classmethod
	def stateParseStatements(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Architecture.EndBlock):
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

		raise BlockParserException("End of architecture declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@Export
class PackageGroup(Group):
	DECLARATION_SIMPLE_BLOCKS = {
		Library.StartBlock:       LibraryGroup,
		Use.StartBlock:           UseGroup,
		ConstantBlock:            ConstantGroup,
		# SharedVariableBlock:            VariableGroup,
		SignalBlock:              SignalGroup
	}
	DECLARATION_COMPOUND_BLOCKS = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = dict(ChainMap(
			{v: [] for v in chain(
				self.DECLARATION_SIMPLE_BLOCKS.values(),
				self.DECLARATION_COMPOUND_BLOCKS.values()
			)},
			{CommentGroup: [],
			 WhitespaceGroup: []
			 }
		))

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Package.NameBlock):
			return
		elif isinstance(currentBlock, Package.EndBlock):
			parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
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

		raise BlockParserException("End of package declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@Export
class PackageBodyGroup(Group):
	DECLARATION_SIMPLE_BLOCKS = {
		Library.StartBlock:       LibraryGroup,
		Use.StartBlock:           UseGroup,
		ConstantBlock:            ConstantGroup,
		# SharedVariableBlock:            VariableGroup,
		SignalBlock:              SignalGroup
	}
	DECLARATION_COMPOUND_BLOCKS = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = dict(ChainMap(
			{v: [] for v in chain(
				self.DECLARATION_SIMPLE_BLOCKS.values(),
				self.DECLARATION_COMPOUND_BLOCKS.values()
			)},
			{CommentGroup: [],
			 WhitespaceGroup: []
			 }
		))

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, PackageBody.NameBlock):
			return
		elif isinstance(currentBlock, PackageBody.EndBlock):
			parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
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
					parserState.NextGroup =   group(parserState.LastGroup, parserState.BlockMarker, currentBlock)
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of package body declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@Export
class ComponentGroup(Group):
	SIMPLE_BLOCKS = {
		# LibraryBlock:             LibraryGroup,
		# UseBlock:                 UseGroup
	}
	COMPOUND_BLOCKS = {
		# Function.NameBlock:       FunctionGroup,
		# Procedure.NameBlock:      ProcedureGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Component.NameBlock):
			return
		elif isinstance(currentBlock, Component.EndBlock):
			parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
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
			for block in cls.SIMPLE_BLOCKS:
				if isinstance(currentBlock, block):
					group = cls.SIMPLE_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for block in cls.COMPOUND_BLOCKS:
				if isinstance(currentBlock, block):
					group =                   cls.COMPOUND_BLOCKS[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of component declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@Export
class ConfigurationGroup(Group):
	SIMPLE_BLOCKS = {
		# LibraryBlock: LibraryGroup,
		# UseBlock: UseGroup
	}
	COMPOUND_BLOCKS = {
		# Function.NameBlock: FunctionGroup,
		# Procedure.NameBlock: ProcedureGroup
	}

	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Configuration.NameBlock):
			return
		elif isinstance(currentBlock, Configuration.EndBlock):
			parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
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
			for block in cls.SIMPLE_BLOCKS:
				if isinstance(currentBlock, block):
					group = cls.SIMPLE_BLOCKS[block]
					parserState.PushState = group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue = True
					return

			for block in cls.COMPOUND_BLOCKS:
				if isinstance(currentBlock, block):
					group = cls.COMPOUND_BLOCKS[block]
					parserState.PushState = group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue = True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of configuration declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)
