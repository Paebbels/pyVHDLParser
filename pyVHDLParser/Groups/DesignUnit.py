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
from pyVHDLParser.Blocks.Common             import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Reference          import Context
from pyVHDLParser.Blocks.Reference.Library  import LibraryBlock
from pyVHDLParser.Blocks.Reference.Use      import UseBlock
from pyVHDLParser.Blocks.Reference.Context  import EndBlock as ContextEndBlock
from pyVHDLParser.Blocks.Sequential         import Package, PackageBody
from pyVHDLParser.Blocks.Structural         import Entity, Architecture
from pyVHDLParser.Groups                    import Group, BlockParserException
from pyVHDLParser.Groups.Comment            import CommentGroup
from pyVHDLParser.Groups.Parser             import BlockToGroupParser
from pyVHDLParser.Functions                 import Console


# Type alias for type hinting
from pyVHDLParser.Groups.Reference import LibraryGroup, UseGroup
from pyVHDLParser.TypeSystem import Package


ParserState = BlockToGroupParser.BlockParserState


class ContextGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block.PreviousBlock, Context.NameBlock)

		for block in parserState.BlockIterator:
			if isinstance(parserState.Block, CommentBlock):
				parserState.NewGroup =    CommentGroup(parserState.LastGroup, parserState.NewBlock)
				return
			elif isinstance(parserState.Block, (LinebreakBlock, IndentationBlock)):
				print(parserState.Block)
				return
			elif isinstance(block, LibraryBlock):
				parserState.PushState =   LibraryGroup.stateParse
				parserState.Block =       block
				parserState.BlockMarker = block
				parserState.ReIssue()
				return
			elif isinstance(block, UseBlock):
				parserState.PushState =   UseGroup.stateParse
				parserState.Block =       block
				parserState.BlockMarker = block
				parserState.ReIssue()
				return
			elif isinstance(block, ContextEndBlock):
				parserState.NewGroup =    cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of context declaration not found.", block)


class EntityGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block.PreviousBlock, Entity.NameBlock)

		for block in parserState.BlockIterator:
			if isinstance(block, Entity.EndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of entity declaration not found.", block)


class ArchitectureGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block.PreviousBlock, Architecture.NameBlock)

		for block in parserState.BlockIterator:
			if isinstance(block, Architecture.EndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of context declaration not found.", block)


class PackageGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block.PreviousBlock, Package.NameBlock)

		for block in parserState.BlockIterator:
			if isinstance(block, Package.EndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of context declaration not found.", block)


class PackageBodyGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block.PreviousBlock, PackageBody.NameBlock)

		for block in parserState.BlockIterator:
			if isinstance(block, PackageBody.EndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of context declaration not found.", block)


class ComponentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		raise NotImplementedError("Parsing component blocks ...")

		assert isinstance(parserState.Block.PreviousBlock, Entity.NameBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, Entity.EndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of entity declaration not found.", block)


class ConfigurationGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		raise NotImplementedError("Parsing configuration blocks ...")

		assert isinstance(parserState.Block.PreviousBlock, Configuration.NameBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, Configuration.EndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of entity declaration not found.", block)
