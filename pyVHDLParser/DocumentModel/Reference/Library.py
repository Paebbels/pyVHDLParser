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
# Copyright 2007-2016 Patrick Lehmann - Dresden, Germany
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
from pyVHDLParser.Blocks.Reference.Library import LibraryNameBlock, LibraryEndBlock, LibraryBlock
from pyVHDLParser.DocumentModel.VHDLModel   import LibraryReference as LibraryBase
from pyVHDLParser.DocumentModel.Parser      import BlockToModelParser

# Type alias for type hinting
ParserState = BlockToModelParser.BlockParserState


class Library(LibraryBase):
	def __init__(self):
		super().__init__()

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, LibraryBlock)
		for block in parserState.BlockIterator:
			if isinstance(block, LibraryNameBlock):
				parserState.CurrentNode.AddLibrary(block.StartToken.Value)
			elif isinstance(block, LibraryEndBlock):
				break

		parserState.Pop()
		# parserState.CurrentBlock = None
