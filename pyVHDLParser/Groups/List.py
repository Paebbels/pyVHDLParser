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
from pyVHDLParser.Decorators        import Export
from pyVHDLParser.Blocks            import CommentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import LinebreakBlock, IndentationBlock
import pyVHDLParser.Blocks.InterfaceObject
from pyVHDLParser.Blocks.List       import GenericList, ParameterList, PortList, SensitivityList
from pyVHDLParser.Groups            import ParserState, BlockParserException, Group, EndOfDocumentGroup
from pyVHDLParser.Groups.Comment    import WhitespaceGroup, CommentGroup

__all__ = []
__api__ = __all__


@Export
class GenericListGroup(Group):
	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:         [],
			WhitespaceGroup:      [],
			GenericListItemGroup: []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, GenericList.OpenBlock):
			return
		elif isinstance(currentBlock, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock):
			parserState.PushState =   GenericListItemGroup.stateParse
			parserState.NextGroup =   GenericListItemGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, GenericList.CloseBlock):
			parserState.Pop()
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

		raise BlockParserException("End of generic list not found.", currentBlock)


@Export
class GenericListItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if isinstance(block, GenericList.DelimiterBlock):
				parserState.Pop()
				return
			elif isinstance(block, GenericList.CloseBlock):
				# parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				parserState.ReIssue = True
				return

		raise BlockParserException("End of generic not found.", block)


@Export
class GenericMapGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@Export
class GenericMapItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@Export
class PortListGroup(Group):
	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    [],
			PortListItemGroup:  []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, PortList.OpenBlock):
			return
		elif isinstance(currentBlock, (pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock, PortList.DelimiterBlock)):
			return
		elif isinstance(currentBlock, PortList.CloseBlock):
			parserState.Pop()
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

		raise BlockParserException("End of generic list not found.", currentBlock)


@Export
class PortListItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if isinstance(block, PortList.DelimiterBlock):
				parserState.Pop()
				return
			elif isinstance(block, PortList.CloseBlock):
				# parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				parserState.ReIssue = True
				return

		raise BlockParserException("End of port not found.", block)


@Export
class PortMapGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@Export
class PortMapItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@Export
class ParameterListGroup(Group):
	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:           [],
			WhitespaceGroup:        [],
			ParameterListItemGroup: []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, ParameterList.OpenBlock):
			return
		elif isinstance(currentBlock, (ParameterList.ItemBlock, ParameterList.DelimiterBlock)):
			return
		elif isinstance(currentBlock, ParameterList.CloseBlock):
			parserState.Pop()
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

		raise BlockParserException("End of generic list not found.", currentBlock)


@Export
class ParameterListItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if isinstance(block, ParameterList.DelimiterBlock):
				parserState.Pop()
				return
			elif isinstance(block, ParameterList.CloseBlock):
				# parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				parserState.ReIssue = True
				return

		raise BlockParserException("End of parameter not found.", block)


@Export
class ParameterMapGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@Export
class ParameterMapItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


@Export
class SensitivityListGroup(Group):
	def __init__(self, previousGroup, startBlock, endBlock=None):
		super().__init__(previousGroup, startBlock, endBlock)

		self._subGroups = {
			CommentGroup:             [],
			WhitespaceGroup:          [],
			SensitivityListItemGroup: []
		}

	@classmethod
	def stateParse(cls, parserState: ParserState):
		currentBlock = parserState.Block

		if isinstance(currentBlock, SensitivityList.OpenBlock):
			return
		elif isinstance(currentBlock, (SensitivityList.ItemBlock, SensitivityList.DelimiterBlock)):
			return
		elif isinstance(currentBlock, SensitivityList.CloseBlock):
			parserState.Pop()
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

		raise BlockParserException("End of generic list not found.", currentBlock)


@Export
class SensitivityListItemGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))
