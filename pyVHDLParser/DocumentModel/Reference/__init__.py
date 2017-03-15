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
from pyVHDLParser.Blocks                    import TokenParserException
from pyVHDLParser.Blocks.Reference.Library  import LibraryNameBlock, LibraryEndBlock
from pyVHDLParser.Blocks.Reference.Use      import UseBlock, UseNameBlock, UseEndBlock
from pyVHDLParser.DocumentModel.VHDLModel   import LibraryReference as LibraryReferenceModel, Use as UseModel
from pyVHDLParser.DocumentModel.Parser      import GroupToModelParser
from pyVHDLParser.Groups.Comment            import LibraryGroup
from pyVHDLParser.Token.Keywords            import IdentifierToken, AllKeyword

# Type alias for type hinting
ParserState = GroupToModelParser.GroupParserState


class Library(LibraryReferenceModel):
	def __init__(self, libraryName):
		super().__init__()
		self._library = libraryName

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, LibraryGroup)
		for block in parserState.GroupIterator:
			if isinstance(block, LibraryNameBlock):
				library = cls(block.StartToken.Value)
				parserState.CurrentNode.AddLibrary(library)
			elif isinstance(block, LibraryEndBlock):
				break

		parserState.Pop()

	def __str__(self):
		return self._library


class Use(UseModel):
	def __init__(self, libraryName, packageName, itemName):
		super().__init__()
		self._library = libraryName
		self._package = packageName
		self._item =    itemName

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
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParseTokens(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, UseNameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				libraryName = token.Value
				break
		else:
			raise TokenParserException("", None)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise TokenParserException("", None)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				itemName = token.Value
				break
			elif isinstance(token, AllKeyword):
				itemName = "ALL"
				break
		else:
			raise TokenParserException("", None)

		use = cls(libraryName, packageName, itemName)
		parserState.CurrentNode.AddUse(use)

	def __str__(self):
		return "{0}.{1}".format(self._library, self._package)
