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
from pyVHDLParser.Blocks.Common               import LinebreakBlock, EmptyLineBlock, WhitespaceBlock, IndentationBlock
from pyVHDLParser.Blocks.Comment              import SingleLineCommentBlock, MultiLineCommentBlock
from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Structural           import Architecture
from pyVHDLParser.Blocks.List                 import SensitivityList
from pyVHDLParser.Blocks.Sequential           import Process
from test.TestCase                            import TestCase as TestCaseBase
from test.Counter                             import Counter


class TestCase(TestCaseBase):
	__NAME__ =      "Process declarations"
	__FILENAME__ =  "Process.vhdl"

	def __init__(self):
		pass

	@classmethod
	def GetExpectedBlocks(cls):
		counter = cls.GetExpectedBlocksAfterStrip()
		counter.AddType(EmptyLineBlock, 6)
		counter.AddType(LinebreakBlock, 23)
		counter.AddType(IndentationBlock, 29)
		counter.AddType(SingleLineCommentBlock, 9)
		return counter

	@classmethod
	def GetExpectedBlocksAfterStrip(cls):
		counter = Counter()
		counter.AddType(StartOfDocumentBlock, 1)
		counter.AddType(Architecture.NameBlock, 1)
		counter.AddType(Architecture.BeginBlock, 1)
		counter.AddType(Process.OpenBlock, 7)
		counter.AddType(Process.OpenBlock2, 2)
		counter.AddType(SensitivityList.OpenBlock, 7)
		counter.AddType(SensitivityList.ItemBlock, 8)
		counter.AddType(SensitivityList.DelimiterBlock, 1)
		counter.AddType(SensitivityList.CloseBlock, 7)
		counter.AddType(Process.BeginBlock, 7)
		counter.AddType(Process.EndBlock, 7)
		counter.AddType(Architecture.EndBlock, 1)
		counter.AddType(EndOfDocumentBlock, 1)
		return counter
