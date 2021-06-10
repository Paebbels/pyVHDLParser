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

from pyVHDLModel.VHDLModel                  import Context as ContextVHDLModel

from pyVHDLParser.Token.Keywords            import IdentifierToken
from pyVHDLParser.Blocks                    import BlockParserException
from pyVHDLParser.Blocks.Reference          import Context as ContextBlocks
from pyVHDLParser.Groups                    import ParserState
from pyVHDLParser.DocumentModel.Reference   import Library, PackageReference

__all__ = []
__api__ = __all__

DEBUG = True

@export
class Context(ContextVHDLModel):
	def __init__(self, contextName):
		super().__init__(contextName)

	@classmethod
	def stateParse(cls, document, group):
		# iterate blocks to find the contexts name
		for block in group:
			if isinstance(block, ContextBlocks.NameBlock):
				for token in block:
					if isinstance(token, IdentifierToken):
						contextName = token.Value
						break
				else:
					raise BlockParserException("ContextName not found.", None)  # FIXME: change to DOMParserException

				if (len(document.Libraries) != 0):
					raise BlockParserException("A context (library statements) is not allowed for a context declaration.", None)  # FIXME: change to DOMParserException
				if (len(document.PackageReferences) != 0):
					raise BlockParserException("A context (use statements) is not allowed for a context declaration.", None)  # FIXME: change to DOMParserException

				context = cls(contextName)
				print("Found context '{name}'. Adding to current node '{node!s}'.".format(name=contextName, node=document))
				document.AddContext(context)
				break


		subGroupIterator = iter(group.GetSubGroups())
		# subGroup =         next(subGroupIterator)
		#
		# if isinstance(subGroup, GenericListGroup):
		# 	cls.stateParseGenericList(document, subGroup)
		# 	subGroup = next(subGroupIterator)
		#
		# if isinstance(subGroup, PortListGroup):
		# 	cls.stateParsePortList(document, subGroup)
		# 	subGroup = next(subGroupIterator)

		# FIXME: how to check if everthing is consumed?


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

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraries.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._packageReferences.append(use)

	def AddGeneric(self, generic):
		self._genericItems.append(generic)

	def AddPort(self, port):
		self._portItems.append(port)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._packageReferences:
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
