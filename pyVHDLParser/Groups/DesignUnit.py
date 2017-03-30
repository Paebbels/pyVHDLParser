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
from pyVHDLParser.Blocks                    import CommentBlock
from pyVHDLParser.Blocks.Common             import LinebreakBlock, IndentationBlock, EmptyLineBlock
from pyVHDLParser.Blocks.Document           import EndOfDocumentBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Constant import ConstantBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Signal import SignalBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Variable import VariableBlock
from pyVHDLParser.Blocks.Reference import Context
from pyVHDLParser.Blocks.Reference.Library  import LibraryBlock
from pyVHDLParser.Blocks.Reference.Use      import UseBlock
from pyVHDLParser.Blocks.Sequential import Package, PackageBody, Function, Procedure
from pyVHDLParser.Blocks.Structural import Entity, Architecture, Component, Configuration
from pyVHDLParser.Groups                    import BlockParserState, BlockParserException, Group
from pyVHDLParser.Groups.Comment            import CommentGroup, WhitespaceGroup
from pyVHDLParser.Groups.ObjectDeclaration import ConstantGroup, VariableGroup, SignalGroup
from pyVHDLParser.Groups.Reference          import LibraryGroup, UseGroup
from pyVHDLParser.Functions                 import Console

# Type alias for type hinting
from pyVHDLParser.Groups.Sequential import ProcedureGroup, FunctionGroup


ParserState = BlockParserState


class ContextGroup(Group):
	__SIMPLE_BLOCKS__ = {
		LibraryBlock:             LibraryGroup,
		UseBlock:                 UseGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Context.NameBlock):
			return
		elif isinstance(currentBlock, Context.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		elif isinstance(currentBlock, CommentBlock):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		else:
			for block in cls.__SIMPLE_BLOCKS__:
				if isinstance(currentBlock, block):
					group = cls.__SIMPLE_BLOCKS__[block]
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class EntityGroup(Group):
	__SIMPLE_BLOCKS__ = {
		LibraryBlock:             LibraryGroup,
		UseBlock:                 UseGroup
	}
	__COMPOUND_BLOCKS__ = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Entity.NameBlock):
			return
		elif isinstance(currentBlock, Entity.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		elif isinstance(currentBlock, CommentBlock):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
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
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class ArchitectureGroup(Group):
	__SIMPLE_BLOCKS__ = {
		LibraryBlock:             LibraryGroup,
		UseBlock:                 UseGroup,
		ConstantBlock:            ConstantGroup,
		# SharedVariableBlock:            VariableGroup,
		SignalBlock:              SignalGroup
	}
	__COMPOUND_BLOCKS__ = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Architecture.NameBlock):
			return
		elif isinstance(currentBlock, Architecture.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		elif isinstance(currentBlock, CommentBlock):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
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
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class PackageGroup(Group):
	__SIMPLE_BLOCKS__ = {
		LibraryBlock:             LibraryGroup,
		UseBlock:                 UseGroup,
		ConstantBlock:            ConstantGroup,
		# SharedVariableBlock:            VariableGroup,
		SignalBlock:              SignalGroup
	}
	__COMPOUND_BLOCKS__ = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Package.NameBlock):
			return
		elif isinstance(currentBlock, Package.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		elif isinstance(currentBlock, CommentBlock):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
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
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class PackageBodyGroup(Group):
	__SIMPLE_BLOCKS__ = {
		LibraryBlock:             LibraryGroup,
		UseBlock:                 UseGroup,
		ConstantBlock:            ConstantGroup,
		# SharedVariableBlock:            VariableGroup,
		SignalBlock:              SignalGroup
	}
	__COMPOUND_BLOCKS__ = {
		Function.NameBlock:       FunctionGroup,
		Procedure.NameBlock:      ProcedureGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, PackageBody.NameBlock):
			return
		elif isinstance(currentBlock, PackageBody.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				else:
					print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		elif isinstance(currentBlock, CommentBlock):
			print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				else:
					print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
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
					parserState.NewGroup =    group(parserState.LastGroup, parserState.BlockMarker, currentBlock)
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class ComponentGroup(Group):
	__SIMPLE_BLOCKS__ = {
		# LibraryBlock:             LibraryGroup,
		# UseBlock:                 UseGroup
	}
	__COMPOUND_BLOCKS__ = {
		# Function.NameBlock:       FunctionGroup,
		# Procedure.NameBlock:      ProcedureGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Component.NameBlock):
			return
		elif isinstance(currentBlock, Component.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
			return
		elif isinstance(currentBlock, CommentBlock):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup =  CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue =   True
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
					parserState.PushState =   group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)

class ConfigurationGroup(Group):
	__SIMPLE_BLOCKS__ = {
		# LibraryBlock: LibraryGroup,
		# UseBlock: UseGroup
	}
	__COMPOUND_BLOCKS__ = {
		# Function.NameBlock: FunctionGroup,
		# Procedure.NameBlock: ProcedureGroup
	}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, Configuration.NameBlock):
			return
		elif isinstance(currentBlock, Configuration.EndBlock):
			parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, parserState.Block)
			parserState.Pop()
			parserState.BlockMarker = None
			return
		elif isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup = WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue = True
			return
		elif isinstance(currentBlock, CommentBlock):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, CommentBlock)):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NewGroup = CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.ReIssue = True
			return
		else:
			for block in cls.__SIMPLE_BLOCKS__:
				if isinstance(currentBlock, block):
					group = cls.__SIMPLE_BLOCKS__[block]
					parserState.PushState = group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue = True
					return

			for block in cls.__COMPOUND_BLOCKS__:
				if isinstance(currentBlock, block):
					group = cls.__COMPOUND_BLOCKS__[block]
					parserState.PushState = group.stateParse
					parserState.BlockMarker = currentBlock
					parserState.ReIssue = True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			from pyVHDLParser.Groups.Document import EndOfDocumentGroup
			parserState.NewGroup = EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("End of context declaration not found.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)