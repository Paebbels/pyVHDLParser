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
from pyVHDLParser.Token.Keywords            import IdentifierToken, AllKeyword
from pyVHDLParser.Blocks                    import TokenParserException
from pyVHDLParser.Blocks.Reference          import Library as LibraryBlocks, Use as UseBlocks
from pyVHDLParser.VHDLModel                 import LibraryReference as LibraryReferenceModel, Use as UseModel
from pyVHDLParser.DocumentModel             import GroupParserException


class Library(LibraryReferenceModel):
	def __init__(self, libraryName):
		super().__init__()
		self._library = libraryName

	@classmethod
	def stateParse(cls, currentNode, group):
		for block in group:
			if isinstance(block, LibraryBlocks.StartBlock):
				pass
			elif isinstance(block, LibraryBlocks.LibraryNameBlock):
				libraryName = block.StartToken.Value
				library = cls(libraryName)
				print("Found library '{0}'. Adding to current node '{1!s}'.".format(libraryName, currentNode))
				currentNode.AddLibrary(library)
			elif isinstance(block, LibraryBlocks.EndBlock):
				return
			else:
				raise GroupParserException("Unexpected block type in LibraryGroup.")

		raise GroupParserException("End of use clause not found.")

	def __str__(self):
		return self._library


class Use(UseModel):
	def __init__(self, libraryName, packageName, itemName):
		super().__init__()
		self._library = libraryName
		self._package = packageName
		self._item =    itemName

	@classmethod
	def stateParse(cls, currentNode, group):
		for block in group:
			if isinstance(block, UseBlocks.StartBlock):
				pass
			elif isinstance(block, UseBlocks.ReferenceNameBlock):
				tokenIterator = iter(block)

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
						objectName = token.Value
						break
					elif isinstance(token, AllKeyword):
						objectName = "ALL"
						break
				else:
					raise TokenParserException("", None)

				use = cls(libraryName, packageName, objectName)
				currentNode.AddUse(use)
			elif isinstance(block, UseBlocks.EndBlock):
				return
			else:
				raise GroupParserException("Unexpected block type in LibraryGroup.")

		raise GroupParserException("End of use clause not found.")

	def __str__(self):
		return "{0}.{1}".format(self._library, self._package)
