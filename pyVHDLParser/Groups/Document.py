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
from pyVHDLParser.Blocks.Document           import EndOfDocumentBlock
from pyVHDLParser.Blocks.Reference.Library  import LibraryBlock
from pyVHDLParser.Blocks.Reference.Use      import UseBlock
from pyVHDLParser.Groups                    import BlockParserException, Group
from pyVHDLParser.Groups.Comment            import CommentGroup, LibraryGroup, UseGroup
from pyVHDLParser.Groups.Parser             import BlockToGroupParser
from pyVHDLParser.Functions                 import Console

# Type alias for type hinting
ParserState = BlockToGroupParser.BlockParserState


class StartOfDocumentGroup(Group):
	def __init__(self, startBlock):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartBlock =         startBlock
		self.EndToken =           startBlock
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartBlock

	def __len__(self):
		return 0

	def __str__(self):
		return "[StartOfDocumentGroup]"

	@classmethod
	def stateDocument(cls, parserState: ParserState):
		block = parserState.Block

		print("{YELLOW}{0!s}{NOCOLOR}".format(block, **Console.Foreground))

		errorMessage = "Expected keywords: architecture, context, entity, library, package, use."
		if isinstance(parserState.Block, CommentBlock):
			parserState.NewGroup =    CommentGroup(parserState.LastGroup, parserState.NewBlock)
		elif isinstance(parserState.Block, LibraryBlock):
			parserState.NewGroup = LibraryGroup(parserState.LastGroup, parserState.NewBlock)
		elif isinstance(parserState.Block, UseBlock):
			parserState.NewGroup = UseGroup(parserState.LastGroup, parserState.NewBlock)
		elif isinstance(block, EndOfDocumentBlock):
			parserState.NewGroup =      EndOfDocumentGroup(block)
			return
		else:  # tokenType
			raise BlockParserException(errorMessage, block)


class EndOfDocumentGroup(Group):
	def __init__(self, endBlock):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartBlock =         endBlock
		self.EndToken =           endBlock
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartBlock

	def __len__(self):
		return 0

	def __str__(self):
		return "[EndOfDocumentGroup]"
