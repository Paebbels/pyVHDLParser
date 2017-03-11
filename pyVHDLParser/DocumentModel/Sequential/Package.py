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
from pyVHDLParser.Blocks.Exception   import BlockParserException
from pyVHDLParser.Blocks.List        import GenericList as GenericListBlocks, PortList as PortListBlocks
from pyVHDLParser.Blocks.ObjectDeclaration import Constant
from pyVHDLParser.Functions import Console
from pyVHDLParser.Token.Keywords     import IdentifierToken
from pyVHDLParser.Blocks.Sequential  import Package as PackageBlock
from pyVHDLParser.DocumentModel.VHDLModel    import Package as PackageModel
from pyVHDLParser.DocumentModel.Parser       import BlockToModelParser

# Type alias for type hinting
ParserState = BlockToModelParser.BlockParserState


class Package(PackageModel):
	def __init__(self, packageName):
		super().__init__()
		self._name = packageName

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, PackageBlock.NameBlock)
		cls.stateParsePackageName(parserState)

		for block in parserState.BlockIterator:
			if isinstance(block, GenericListBlocks.OpenBlock):
				parserState.PushState = cls.stateParseGenericList
				parserState.ReIssue()
			elif isinstance(block, PortListBlocks.OpenBlock):
				parserState.PushState = cls.stateParsePortList
				parserState.ReIssue()
			elif isinstance(block, Constant.ConstantBlock):
				raise NotImplementedError()
			elif isinstance(block, PackageBlock.EndBlock):
				break
		else:
			raise BlockParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParsePackageName(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, PackageBlock.NameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise BlockParserException("", None)

		oldNode = parserState.CurrentNode
		package = cls(packageName)

		parserState.CurrentNode.AddPackage(package)
		parserState.CurrentNode = package
		parserState.CurrentNode.AddLibraries(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.Uses)

		oldNode.Libraries.clear()
		oldNode.Uses.clear()

	@classmethod
	def stateParseGenericList(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, GenericListBlocks.OpenBlock)

		for block in parserState.BlockIterator:
			if isinstance(block, GenericListBlocks.ItemBlock):
				cls.stateParseGeneric(parserState)
			elif isinstance(block, GenericListBlocks.CloseBlock):
				break
		else:
			raise BlockParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParseGeneric(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, GenericListBlocks.ItemBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				genericName = token.Value
				break
		else:
			raise BlockParserException("", None)

		parserState.CurrentNode.AddGeneric(genericName)

	@classmethod
	def stateParsePortList(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, PortListBlocks.OpenBlock)

		for block in parserState.BlockIterator:
			if isinstance(block, PortListBlocks.ItemBlock):
				cls.stateParsePort(parserState)
			elif isinstance(block, PortListBlocks.CloseBlock):
				break
		else:
			raise BlockParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParsePort(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, PortListBlocks.ItemBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				portName = token.Value
				break
		else:
			raise BlockParserException("", None)

		parserState.CurrentNode.AddPort(portName)

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraries.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._uses.append(use)

	def AddGeneric(self, generic):
		self._genericItems.append(generic)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}PACKAGE{NOCOLOR} {YELLOW}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, **Console.Foreground))
		if (len(self._genericItems) > 0):
			print("{indent}  {DARK_CYAN}GENERIC{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for generic in self._genericItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=generic, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation))
		print("{indent}{DARK_CYAN}END PACKAGE{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))

