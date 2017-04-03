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
from pyVHDLParser.Blocks import CommentBlock
from pyVHDLParser.Blocks.Common import LinebreakBlock, IndentationBlock, EmptyLineBlock
from pyVHDLParser.Blocks.Document import EndOfDocumentBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Constant import ConstantBlock
from pyVHDLParser.Blocks.ObjectDeclaration.Variable import VariableBlock
from pyVHDLParser.Blocks.Reference.Use import UseBlock
from pyVHDLParser.Blocks.Sequential import Function, Procedure
from pyVHDLParser.Groups import BlockParserState, Group, BlockParserException


# Type alias for type hinting
from pyVHDLParser.Groups.Comment import WhitespaceGroup, CommentGroup
from pyVHDLParser.Groups.ObjectDeclaration import ConstantGroup, VariableGroup
from pyVHDLParser.Groups.Reference import UseGroup
from pyVHDLParser.Token.Keywords import EndToken


ParserState = BlockParserState


class AssertGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class SignalAssignmentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))
