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
from pyVHDLParser.Blocks.Reporting.Assert import AssertBlock
from pyVHDLParser.Blocks.Reporting.Report import ReportBlock
from pyVHDLParser.Groups                  import ParserState, Group, BlockParserException


class AssertGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		marker = parserState.Block
		if parserState.Block.MultiPart:
			for block in parserState.GetBlockIterator:
				if (isinstance(block, AssertBlock) and not block.MultiPart):
					marker2 = block
					break
			else:
				raise BlockParserException("End of multi parted constant declaration not found.", block)
		else:
			marker2 = marker

		parserState.NextGroup = cls(parserState.LastGroup, marker, marker2)
		parserState.Pop()
		return


class ReportGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		marker = parserState.Block
		if parserState.Block.MultiPart:
			for block in parserState.GetBlockIterator:
				if (isinstance(block, ReportBlock) and not block.MultiPart):
					marker2 = block
					break
			else:
				raise BlockParserException("End of multi parted constant declaration not found.", block)
		else:
			marker2 = marker

		parserState.NextGroup = cls(parserState.LastGroup, marker, marker2)
		parserState.Pop()
		return


class SignalAssignmentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))
