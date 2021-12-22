# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from pyTooling.Decorators         import export

from pyVHDLParser.Blocks          import CommentBlock
from pyVHDLParser.Blocks.Common   import WhitespaceBlock, LinebreakBlock, IndentationBlock
from pyVHDLParser.Groups          import ParserState, GroupParserException, Group


@export
class CommentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if (not isinstance(block, CommentBlock)):
				parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block)
				parserState.Pop()
				parserState.ReIssue =   True
				return

		raise GroupParserException("End of library clause not found.", block)


@export
class WhitespaceGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		for block in parserState.GetBlockIterator:
			if (not isinstance(block, (WhitespaceBlock, LinebreakBlock, IndentationBlock))):
				parserState.NextGroup = cls(parserState.LastGroup, parserState.BlockMarker, block.PreviousBlock)
				parserState.Pop()
				parserState.ReIssue =   True
				return

		raise GroupParserException("End of library clause not found.", block)
