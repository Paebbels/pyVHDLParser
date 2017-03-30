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
from pyVHDLParser.Blocks import CommentBlock, Block
from pyVHDLParser.Blocks.Common import LinebreakBlock, IndentationBlock, EmptyLineBlock
from pyVHDLParser.Blocks.Document           import EndOfDocumentBlock
from pyVHDLParser.Blocks.Reference          import Context
from pyVHDLParser.Blocks.Reference.Library  import LibraryBlock
from pyVHDLParser.Blocks.Reference.Use      import UseBlock
from pyVHDLParser.Blocks.Structural         import Entity, Architecture, Configuration
from pyVHDLParser.Blocks.Sequential         import Package, PackageBody
from pyVHDLParser.Groups                    import BlockParserState, BlockParserException, Group
from pyVHDLParser.Groups.Comment            import CommentGroup, WhitespaceGroup
from pyVHDLParser.Groups.Reference          import LibraryGroup, UseGroup
from pyVHDLParser.Groups.DesignUnit         import ContextGroup, EntityGroup, ArchitectureGroup, PackageGroup, PackageBodyGroup, ConfigurationGroup
from pyVHDLParser.Functions                 import Console

# Type alias for type hinting
ParserState = BlockParserState


class StartOfDocumentGroup(Group):
	def __init__(self, startBlock):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartBlock =         startBlock
		self.EndBlock =           startBlock
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartBlock

	def __len__(self):
		return 0

	def __str__(self):
		return "{{{groupName:.<156s}  at {start!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			start=self.StartBlock.StartToken.Start
		)

	__SIMPLE_BLOCKS__ = {
		LibraryBlock:             LibraryGroup,
		UseBlock:                 UseGroup
	}
	__COMPOUND_BLOCKS__ = {
		Context.NameBlock:        ContextGroup,
		Entity.NameBlock:         EntityGroup,
		Architecture.NameBlock:   ArchitectureGroup,
		Package.NameBlock:        PackageGroup,
		PackageBody.NameBlock:    PackageBodyGroup,
		Configuration.NameBlock:  ConfigurationGroup
	}

	@classmethod
	def stateDocument(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			# print("consuming {0!s}".format(currentBlock))
			for block in parserState.GetBlockIterator:
				if (not isinstance(block, (LinebreakBlock, EmptyLineBlock, IndentationBlock))):
					break
				# else:
				# 	print("consuming {0!s}".format(block))
			else:
				raise BlockParserException("End of document found.", block)

			parserState.NextGroup =  WhitespaceGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.BlockMarker = block
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

			parserState.NextGroup =    CommentGroup(parserState.LastGroup, currentBlock, parserState.Block.PreviousBlock)
			parserState.BlockMarker = block
			parserState.ReIssue =     True
			return
		else:
			for block in cls.__SIMPLE_BLOCKS__:
				if isinstance(currentBlock, block):
					group =                   cls.__SIMPLE_BLOCKS__[block]
					parserState.PushState =   group.stateParse
					parserState.NextGroup =   group(parserState.LastGroup, block)
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for block in cls.__COMPOUND_BLOCKS__:
				if isinstance(currentBlock, block):
					group =                   cls.__COMPOUND_BLOCKS__[block]
					parserState.PushState =   group.stateParse
					parserState.NextGroup =   group(parserState.LastGroup, block)
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

		if isinstance(currentBlock, EndOfDocumentBlock):
			parserState.NextGroup =    EndOfDocumentGroup(currentBlock)
			return

		raise BlockParserException("Expected keywords: architecture, context, entity, library, package, use. Found '{block!s}'.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


class EndOfDocumentGroup(Group):
	def __init__(self, endBlock):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartBlock : Block = endBlock
		self.EndBlock   : Block = endBlock
		self.MultiPart  =         False

	def __iter__(self):
		yield self.StartBlock

	def __len__(self):
		return 0

	def __str__(self):
		return "{{{groupName:.<156s}  at                      .. {end!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			end=self.EndBlock.StartToken.Start
		)
