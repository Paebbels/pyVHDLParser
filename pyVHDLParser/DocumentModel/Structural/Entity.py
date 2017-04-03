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
from pyVHDLParser.Token.Keywords            import IdentifierToken
from pyVHDLParser.Blocks                    import TokenParserException
from pyVHDLParser.Blocks.List               import GenericList as GenericListBlocks, PortList as PortListBlocks
from pyVHDLParser.Blocks.Object  import Constant
from pyVHDLParser.Blocks.Structural         import Entity as EntityBlock
from pyVHDLParser.VHDLModel                 import Entity as EntityModel
from pyVHDLParser.DocumentModel.Parser      import GroupToModelParser
from pyVHDLParser.Functions                 import Console

# Type alias for type hinting
ParserState = GroupToModelParser.GroupParserState


class Entity(EntityModel):
	def __init__(self, entityName):
		super().__init__()
		self._name = entityName

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, EntityBlock.NameBlock)
		cls.stateParseEntityName(parserState)

		for block in parserState.GroupIterator:
			if isinstance(block, GenericListBlocks.OpenBlock):
				parserState.PushState = cls.stateParseGenericList
				parserState.ReIssue()
			elif isinstance(block, PortListBlocks.OpenBlock):
				parserState.PushState = cls.stateParsePortList
				parserState.ReIssue()
			elif isinstance(block, Constant.ConstantBlock):
				raise NotImplementedError()
			elif isinstance(block, EntityBlock.BeginBlock):
				raise NotImplementedError()
			elif isinstance(block, EntityBlock.EndBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParseEntityName(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, EntityBlock.NameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				entityName = token.Value
				break
		else:
			raise TokenParserException("", None)

		oldNode = parserState.CurrentNode
		entity = cls(entityName)

		parserState.CurrentNode.AddEntity(entity)
		parserState.CurrentNode = entity
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

	@classmethod
	def stateParsePortList(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, PortListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, PortListBlocks.ItemBlock):
				cls.stateParsePort(parserState)
			elif isinstance(block, PortListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParsePort(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentGroup, PortListBlocks.ItemBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				portName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddPort(portName)

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraries.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._uses.append(use)

	def AddGeneric(self, generic):
		self._genericItems.append(generic)

	def AddPort(self, port):
		self._portItems.append(port)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}ENTITY{NOCOLOR} {YELLOW}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(name=self._name, indent=indentation, **Console.Foreground))
		if (len(self._genericItems) > 0):
			print("{indent}  {DARK_CYAN}GENERIC{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for generic in self._genericItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=generic, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation, **Console.Foreground))
		if (len(self._portItems) > 0):
			print("{indent}  {DARK_CYAN}PORT{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for port in self._portItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=port, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation, **Console.Foreground))
		print("{indent}{DARK_CYAN}END ENTITY{NOCOLOR};".format(name=self._name, indent=indentation, **Console.Foreground))

