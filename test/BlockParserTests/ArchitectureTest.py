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
from pyVHDLParser.Blocks.Common               import LinebreakBlock, EmptyLineBlock, WhitespaceBlock, IndentationBlock
from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Structural           import Architecture
from test.TestCase                            import TestCase as TestCaseBase
from test.Counter                             import Counter


class TestCase(TestCaseBase):
	__NAME__ =      "Architecture declarations"
	__FILENAME__ =  "Architecture.vhdl"

	def __init__(self):
		pass

	@classmethod
	def GetExpectedBlocks(cls):
		counter = cls.GetExpectedBlocksAfterStrip()
		counter.AddType(EmptyLineBlock, 15)
		counter.AddType(LinebreakBlock, 78)
		counter.AddType(IndentationBlock, 43)
		counter.AddType(WhitespaceBlock, 5)
		return counter

	@classmethod
	def GetExpectedBlocksAfterStrip(cls):
		counter = Counter()
		counter.AddType(StartOfDocumentBlock, 1)
		counter.AddType(Architecture.NameBlock, 63)
		counter.AddType(Architecture.BeginBlock, 27)
		counter.AddType(Architecture.EndBlock, 36)
		counter.AddType(EndOfDocumentBlock, 1)
		return counter
