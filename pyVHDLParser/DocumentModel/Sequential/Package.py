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
from typing                                 import List

from pyVHDLParser.Token.Keywords            import IdentifierToken
from pyVHDLParser.Blocks                    import TokenParserException
# from pyVHDLParser.Blocks.List                       import GenericList as GenericListBlocks
# from pyVHDLParser.Blocks.ObjectDeclaration.Constant import ConstantBlock
from pyVHDLParser.Blocks.Sequential         import Package as PackageBlock  # , Function as FunctionBlock
from pyVHDLParser.VHDLModel                 import Package as PackageModel
# from pyVHDLParser.DocumentModel.Sequential.Function import Function
# from pyVHDLParser.DocumentModel.ObjectDeclaration   import Constant
from pyVHDLParser.DocumentModel.Reference   import Library, Use
from pyVHDLParser.DocumentModel             import ParserState
from pyVHDLParser.Functions                 import Console


class Package(PackageModel):
	def __init__(self, packageName):
		super().__init__()
		self._name = packageName

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, PackageBlock.NameBlock)
		cls.stateParsePackageName(parserState)

		for block in parserState.GroupIterator:
			if isinstance(block, GenericListBlocks.OpenBlock):
				parserState.PushState = cls.stateParseGenericList
				parserState.ReIssue()
			elif isinstance(block, ConstantBlock):
				parserState.PushState = Constant.stateParse
				parserState.ReIssue()
			elif isinstance(block, FunctionBlock.NameBlock):
				parserState.PushState = Function.stateParse
				parserState.ReIssue()
			elif isinstance(block, PackageBlock.EndBlock):
				break
			else:
				raise TokenParserException("Block '{0!r}' not supported in a package.".format(block), block)
		else:
			raise TokenParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParsePackageName(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, PackageBlock.NameBlock)

		tokenIterator = iter(parserState)
		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise TokenParserException("", None)

		oldNode = parserState.CurrentNode
		package = cls(packageName)

		parserState.CurrentNode.AddPackage(package)
		parserState.CurrentNode = package
		parserState.CurrentNode.AddLibraryReferences(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.Uses)

		oldNode.Libraries.clear()
		oldNode.Uses.clear()

	@classmethod
	def stateParseGenericList(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, GenericListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, GenericListBlocks.ItemBlock):
				cls.stateParseGeneric(parserState)
			elif isinstance(block, GenericListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParseGeneric(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, GenericListBlocks.ItemBlock)

		tokenIterator = iter(parserState)
		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				genericName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddGeneric(genericName)

	def AddLibraryReferences(self, libraries : List[Library]):
		if ((DEBUG is True) and (len(libraries) > 0)): print("{DARK_CYAN}Adding libraries to package {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for library in libraries:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(library, **Console.Foreground))
			self._libraryReferences.append(library._library)

	def AddUses(self, uses : List[Use]):
		if ((DEBUG is True) and (len(uses) > 0)): print("{DARK_CYAN}Adding uses to package {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for use in uses:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(use, **Console.Foreground))
			self._uses.append(use)

	def AddGeneric(self, generic):
		if DEBUG: print("{DARK_CYAN}Adding generic to package {GREEN}{0}{NOCOLOR}:\n  {YELLOW}{1}{NOCOLOR} : {2}".format(self._name, generic, "", **Console.Foreground))
		self._genericItems.append(generic)

	def AddConstant(self, constant):
		if DEBUG: print("{DARK_CYAN}Adding constant to package {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, constant, **Console.Foreground))
		self._declaredItems.append(constant)

	def AddFunction(self, function):
		if DEBUG: print("{DARK_CYAN}Adding function to package {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, function, **Console.Foreground))
		self._declaredItems.append(function)

	def AddProcedure(self, procedure):
		if DEBUG: print("{DARK_CYAN}Adding procedure to package {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, procedure, **Console.Foreground))
		self._declaredItems.append(procedure)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for use in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{item}{NOCOLOR};".format(indent=indentation, lib=use._library, pack=use._package, item=use._item, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}PACKAGE{NOCOLOR} {YELLOW}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, **Console.Foreground))
		if (len(self._genericItems) > 0):
			print("{indent}  {DARK_CYAN}GENERIC{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for generic in self._genericItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=generic, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation))
		if (len(self._declaredItems) > 0):
			for item in self._declaredItems:
				item.Print(indent+1)
		print("{indent}{DARK_CYAN}END PACKAGE{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))

