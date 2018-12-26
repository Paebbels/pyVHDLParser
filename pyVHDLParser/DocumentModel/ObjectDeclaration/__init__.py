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
from pyVHDLParser.Token.Keywords                    import IdentifierToken
from pyVHDLParser.Blocks                            import TokenParserException
from pyVHDLParser.Blocks.Object.Constant import ConstantBlock
from pyVHDLParser.VHDLModel                         import Constant as ConstantBase
from pyVHDLParser.DocumentModel.Parser              import GroupToModelParser
from pyVHDLParser.Functions                         import Console

# Type alias for type hinting
ParserState = GroupToModelParser.GroupParserState


class Constant(ConstantBase):
	def __init__(self, constantName):
		super().__init__()
		self._name = constantName

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, ConstantBlock)

		cls.stateParseConstantName(parserState)

		parserState.Pop()

	@classmethod
	def stateParseConstantName(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, ConstantBlock)

		tokenIterator = iter(parserState)
		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				constantName = token.Value
				break
		else:
			raise TokenParserException("Constant name (identifier) not found.", None)

		constant = cls(constantName)

		parserState.CurrentNode.AddConstant(constant)
		parserState.CurrentNode = constant

	def __str__(self):
		return "{GREEN}{0}{NOCOLOR} : {YELLOW}{1}{NOCOLOR}".format(self._name, self._subType, **Console.Foreground)

	def Print(self, indent=0):
		indentation = "  " * indent
		print("{indent}{DARK_CYAN}CONSTANT {GREEN}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR} := xxx;".format(indent=indentation, name=self._name, type="", **Console.Foreground))
