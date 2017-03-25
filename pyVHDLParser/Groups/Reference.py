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
from pyVHDLParser.Blocks.Reference import Context
from pyVHDLParser.Blocks.Reference.Library  import LibraryEndBlock, LibraryBlock
from pyVHDLParser.Blocks.Reference.Use      import UseEndBlock, UseBlock
from pyVHDLParser.Blocks.Reference.Context  import EndBlock as ContextEndBlock
from pyVHDLParser.Groups                    import Group, BlockParserException
from pyVHDLParser.Groups.Comment import CommentGroup
from pyVHDLParser.Groups.Parser             import BlockToGroupParser
from pyVHDLParser.Functions import Console


# Type alias for type hinting
ParserState = BlockToGroupParser.BlockParserState


class LibraryGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block, LibraryBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, LibraryEndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of library clause not found.", block)


class UseGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block, UseBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, UseEndBlock):
				parserState.NewGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of library clause not found.", block)


class ContextGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block, Context.NameBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, CommentBlock):
				parserState.NewGroup =    CommentGroup(parserState.LastGroup, parserState.NewBlock)
			elif isinstance(block, LibraryBlock):
				parserState.PushState =   LibraryGroup.stateParse
				parserState.Block =       block
				parserState.BlockMarker = block
				parserState.ReIssue()
			elif isinstance(block, UseBlock):
				parserState.PushState =   UseGroup.stateParse
				parserState.Block =       block
				parserState.BlockMarker = block
				parserState.ReIssue()
			elif isinstance(block, ContextEndBlock):
				parserState.NewGroup =    cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise BlockParserException("End of context declaration not found.", block)
