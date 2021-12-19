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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
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
from pyTooling.Decorators               import export

from pyVHDLParser.Blocks.Reference    import Library, Use
from pyVHDLParser.Groups              import ParserState, GroupParserException, Group


@export
class LibraryGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if isinstance(block, Library.EndBlock):
				parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise GroupParserException("End of library clause not found.", block)


@export
class UseGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if isinstance(block, Use.EndBlock):
				parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				return

		raise GroupParserException("End of library clause not found.", block)
