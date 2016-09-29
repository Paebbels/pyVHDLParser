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
from pyVHDLParser.Base               import ParserException
from pyVHDLParser.Blocks.Exception import BlockParserException
from pyVHDLParser.Blocks.Reference.Use  import UseBlock, UseNameBlock, UseEndBlock
from pyVHDLParser.Model.VHDLModel       import Use as UseModel
from pyVHDLParser.Model.Parser          import BlockToModelParser

# Type alias for type hinting
from pyVHDLParser.Token.Keywords import IdentifierToken, AllKeyword


ParserState = BlockToModelParser.BlockParserState


class Use(UseModel):
	def __init__(self):
		super().__init__()

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, UseBlock)
		for block in parserState.BlockIterator:
			if isinstance(block, UseNameBlock):
				# parserState.CurrentBlock = block
				cls.stateParseTokens(parserState)
			elif isinstance(block, UseEndBlock):
				break
		else:
			raise BlockParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParseTokens(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, UseNameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				libraryName = token.Value
				break
		else:
			raise BlockParserException("", None)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise BlockParserException("", None)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				objectName = token.Value
				break
			elif isinstance(token, AllKeyword):
				objectName = "ALL"
				break
		else:
			raise BlockParserException("", None)

		parserState.CurrentNode.AddUse(libraryName, packageName, objectName)
