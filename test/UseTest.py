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
from pyVHDLParser.Blocks.Common              import LinebreakBlock, EmptyLineBlock, WhitespaceBlock, IndentationBlock
from pyVHDLParser.Blocks.Comment             import SingleLineCommentBlock
from pyVHDLParser.Blocks.Document            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Reference.Use       import UseBlock#, UseNameBlock, UseDelimiterBlock, UseEndBlock
from test.Counter                   import Counter


class TestCase:
	__NAME__ =      "Use clauses"
	__FILENAME__ =  "Use.vhdl"

	def __init__(self):
		pass

	@classmethod
	def GetExpectedBlocks(cls):
		counter = cls.GetExpectedBlocksAfterStrip()
		counter.AddType(EmptyLineBlock, 7)
		counter.AddType(LinebreakBlock, 19)
		counter.AddType(IndentationBlock, 12)
		counter.AddType(WhitespaceBlock, 2)
		counter.AddType(SingleLineCommentBlock, 7)
		return counter

	@classmethod
	def GetExpectedBlocksAfterStrip(cls):
		counter = Counter()
		counter.AddType(StartOfDocumentBlock, 1)
		counter.AddType(UseBlock, 11)
		# counter.AddType(UseNameBlock, 14)
		# counter.AddType(UseDelimiterBlock, 3)
		# counter.AddType(UseEndBlock, 11)
		counter.AddType(EndOfDocumentBlock, 1)
		return counter
