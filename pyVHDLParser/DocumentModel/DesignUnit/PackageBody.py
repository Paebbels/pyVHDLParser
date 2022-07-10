# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2022 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from pydecor                                import export
from typing                                 import List

from pyVHDLModel.SyntaxModel                import PackageBody as PackageBodyVHDLModel

import pyVHDLParser.Blocks.InterfaceObject
from pyVHDLParser.Token.Keywords            import IdentifierToken
from pyVHDLParser.Blocks                    import BlockParserException
from pyVHDLParser.Blocks.List               import GenericList as GenericListBlocks, PortList as PortListBlocks
from pyVHDLParser.Blocks.Object.Constant    import ConstantDeclarationBlock
from pyVHDLParser.Blocks.Sequential         import PackageBody as PackageBodyBlock
from pyVHDLParser.Groups                    import ParserState
from pyVHDLParser.DocumentModel.Reference   import LibraryClause, PackageReference


DEBUG = True

@export
class PackageBody(PackageBodyVHDLModel):
	def __init__(self, packageBodyName):
		super().__init__()
		self._name = packageBodyName

	@classmethod
	def stateParse(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, PackageBodyBlock.NameBlock)
		cls.stateParsePackageBodyName(parserState)

		for block in parserState.GroupIterator:
			if isinstance(block, GenericListBlocks.OpenBlock):
				parserState.PushState = cls.stateParseGenericList
				parserState.ReIssue()
			elif isinstance(block, PortListBlocks.OpenBlock):
				parserState.PushState = cls.stateParsePortList
				parserState.ReIssue()
			elif isinstance(block, ConstantBlock):
				parserState.PushState = Constant.stateParse
				parserState.ReIssue()
			elif isinstance(block, Function.BeginBlock):
				parserState.PushState = Function.stateParse
				parserState.ReIssue()
			elif isinstance(block, PackageBodyBlock.EndBlock):
				break
			else:
				raise BlockParserException("Block '{0!r}' not supported in a package body.".format(block), block)  # FIXME: change to DOMParserException
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParsePackageBodyName(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, PackageBodyBlock.NameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		oldNode = parserState.CurrentNode
		packageBody = cls(packageName)

		parserState.CurrentNode.AddPackageBody(packageBody)
		parserState.CurrentNode = packageBody
		parserState.CurrentNode.AddLibraryReferences(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.PackageReferences)

		oldNode.Libraries.clear()
		oldNode.PackageReferences.clear()

	@classmethod
	def stateParseGenericList(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, GenericListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock):
				cls.stateParseGeneric(parserState)
			elif isinstance(block, GenericListBlocks.CloseBlock):
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		parserState.Pop()

	@classmethod
	def stateParseGeneric(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				genericName = token.Value
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		parserState.CurrentNode.AddGeneric(genericName)

	@classmethod
	def stateParsePortList(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, PortListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock):
				cls.stateParsePort(parserState)
			elif isinstance(block, PortListBlocks.CloseBlock):
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		parserState.Pop()

	@classmethod
	def stateParsePort(cls, parserState: ParserState): #document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				portName = token.Value
				break
		else:
			raise BlockParserException("", None)  # FIXME: change to DOMParserException

		parserState.CurrentNode.AddPort(portName)

	def AddLibraries(self, libraries: List[LibraryClause]):
		if ((DEBUG is True) and (len(libraries) > 0)): print("{DARK_CYAN}Adding libraries to package body {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for library in libraries:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(library, **Console.Foreground))
			self._libraries.append(library._library)

	def AddUses(self, uses: List[PackageReference]):
		if ((DEBUG is True) and (len(uses) > 0)): print("{DARK_CYAN}Adding uses to package body {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for use in uses:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(use, **Console.Foreground))
			self._packageReferences.append(use)

	def AddConstant(self, constant):
		if DEBUG: print("{DARK_CYAN}Adding constant to package body {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, constant, **Console.Foreground))
		self._declaredItems.append(constant)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._packageReferences:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}PACKAGE BODY{NOCOLOR} {GREEN}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, **Console.Foreground))
		if (len(self._declaredItems) > 0):
			for item in self._declaredItems:
				item.Print(indent+1)
		print("{indent}{DARK_CYAN}END PACKAGE BODY{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))
