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
from pyVHDLParser.Blocks.ObjectDeclaration.Constant import ConstantBlock
from pyVHDLParser.Blocks.Sequential import Function
from pyVHDLParser.Blocks.Sequential import Package
from pyVHDLParser.Blocks.Sequential import PackageBody
from pyVHDLParser.Blocks.Sequential import Procedure
from pyVHDLParser.Groups            import Group, BlockParserException
from pyVHDLParser.Groups.Parser     import BlockToGroupParser
from pyVHDLParser.Groups.Sequential import FunctionGroup, ProcedureGroup

# Type alias for type hinting
ParserState = BlockToGroupParser.BlockParserState


class ContextGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class EntityGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ArchitectureGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ComponentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class ConfigurationGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class PackageGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block, Package.NameBlock)

		simpleBlocks = {
			# ConstantBlock:         ConstantGroup,
		}

		compoundBlocks = {
			Function.NameBlock:    FunctionGroup,
			Procedure.NameBlock:   ProcedureGroup
		}

		for block in parserState.GroupIterator:
			for blk in simpleBlocks:
				if isinstance(block, blk):
					group = simpleBlocks[blk]
					parserState.PushState = group.stateParse
					parserState.BlockMarker = block
					parserState.ReIssue()

			for blk in compoundBlocks:
				if isinstance(block, blk):
					group = compoundBlocks[blk]
					parserState.NewGroup = group(parserState.LastGroup, parserState.BlockMarker, block)
					parserState.PushState = group.stateParse
					parserState.BlockMarker = block
					parserState.ReIssue()

			if isinstance(block, Package.EndBlock):

				return

		raise BlockParserException("End of package not found.", block)


class PackageBodyGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.Block, PackageBody.NameBlock)

		simpleBlocks = {
			# ConstantBlock:         ConstantGroup,
		}

		compoundBlocks = {
			Function.NameBlock:    FunctionGroup,
			Procedure.NameBlock:   ProcedureGroup
		}

		for block in parserState.GroupIterator:
			for blk in simpleBlocks:
				if isinstance(block, blk):
					group = simpleBlocks[blk]
					parserState.PushState = group.stateParse
					parserState.BlockMarker = block
					parserState.ReIssue()

			for blk in compoundBlocks:
				if isinstance(block, blk):
					group = compoundBlocks[blk]
					parserState.NewGroup = group(parserState.LastGroup, parserState.BlockMarker, block)
					parserState.PushState = group.stateParse
					parserState.BlockMarker = block
					parserState.ReIssue()

			if isinstance(block, Package.EndBlock):

				return

		raise BlockParserException("End of package body not found.", block)
