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
from pydecor                                import export
from typing                                 import List

from pyVHDLModel.VHDLModel                  import Architecture as ArchitectureVHDLModel

from pyVHDLParser.Token.Keywords            import IdentifierToken
from pyVHDLParser.Blocks                    import BlockParserException
from pyVHDLParser.Blocks.Object.Constant    import ConstantDeclarationBlock
from pyVHDLParser.Blocks.Structural         import Architecture as ArchitectureBlocks
from pyVHDLParser.Groups                    import ParserState
from pyVHDLParser.DocumentModel.Reference   import Library, PackageReference

__all__ = []
__api__ = __all__

DEBUG = True

@export
class Architecture(ArchitectureVHDLModel):
	def __init__(self, architectureName, entityName):
		super().__init__()
		self._name =    architectureName
		self._entity =  entityName

	@classmethod
	def stateParse(cls, parserState: ParserState): #document, group):
		# cls.stateParseArchitectureName(parserState)
		#
		# for block in parserState.GroupIterator:
		# 	if isinstance(block, Constant.ConstantBlock):
		# 		raise NotImplementedError()
		# 	# elif isinstance(block, ArchitectureBlock.ConcurrentBeginBlock):
		# 	# 	raise NotImplementedError()
		# 	elif isinstance(block, ArchitectureBlock.EndBlock):
		# 		break
		# else:
		# 	raise BlockParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParseArchitectureName(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, ArchitectureBlock.NameBlock)

		tokenIterator = iter(parserState)

		# iterate architetures NameBlock to find the architecture name
		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				architectureName = token.Value
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				entityName = token.Value
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		oldNode = parserState.CurrentNode
		architecture = cls(architectureName, entityName)

		parserState.CurrentNode.AddArchitecture(architecture)
		parserState.CurrentNode = architecture
		parserState.CurrentNode.AddLibraryReferences(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.PackageReferences)

		oldNode.Libraries.clear()
		oldNode.PackageReferences.clear()

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraryReferences.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._packageReferences.append(use)


	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraryReferences:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._packageReferences:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}ARCHITECTURE {YELLOW}{name}{NOCOLOR} {DARK_CYAN}OF{NOCOLOR} {GREEN}{entity}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, entity=self._entity, **Console.Foreground))
		print("{indent}{DARK_CYAN}BEGIN{NOCOLOR}".format(indent=indentation, **Console.Foreground))
		print("{indent}{DARK_CYAN}END ARCHITECTURE{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))
