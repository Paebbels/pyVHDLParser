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
from pyVHDLParser.Blocks.Exception   import BlockParserException
from pyVHDLParser.Blocks.List        import GenericList as GenericListBlocks, PortList as PortListBlocks
from pyVHDLParser.Blocks.ObjectDeclaration import Constant
from pyVHDLParser.Token.Keywords     import ArchitectureKeyword, IdentifierToken
from pyVHDLParser.Blocks.Structural  import Architecture as ArchitectureBlock
from pyVHDLParser.Model.VHDLModel    import Architecture as ArchitectureModel
from pyVHDLParser.Model.Parser       import BlockToModelParser

# Type alias for type hinting
ParserState = BlockToModelParser.BlockParserState


class Architecture(ArchitectureModel):
	def __init__(self, architectureName, entityName):
		super().__init__()
		self._name =    architectureName
		self._entity =  entityName

	@classmethod
	def stateParse(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, ArchitectureBlock.NameBlock)
		cls.stateParseArchitectureName(parserState)

		for block in parserState.BlockIterator:
			if isinstance(block, Constant.ConstantBlock):
				raise NotImplementedError()
			# elif isinstance(block, ArchitectureBlock.BeginBlock):
			# 	raise NotImplementedError()
			elif isinstance(block, ArchitectureBlock.EndBlock):
				break
		else:
			raise BlockParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParseArchitectureName(cls, parserState: ParserState):
		assert isinstance(parserState.CurrentBlock, ArchitectureBlock.NameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				architectureName = token.Value
				break
		else:
			raise BlockParserException("", None)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				entityName = token.Value
				break
		else:
			raise BlockParserException("", None)

		oldNode = parserState.CurrentNode
		architecture = cls(architectureName, entityName)

		parserState.CurrentNode.AddArchitecture(architecture)
		parserState.CurrentNode = architecture
		parserState.CurrentNode.AddLibraries(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.Uses)

		oldNode.Libraries.clear()
		oldNode.Uses.clear()

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraries.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._uses.append(use)


	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}LIBRARY {lib};".format(indent=indentation, lib=lib))
		for lib, pack, obj in self._uses:
			print("{indent}USE {lib}.{pack}.{obj};".format(indent=indentation, lib=lib, pack=pack, obj=obj))
		print()
		print("{indent}ARCHITECTURE {name} OF {entity} IS".format(indent=indentation, name=self._name, entity=self._entity))
		print("{indent}BEGIN".format(indent=indentation))
		print("{indent}END ARCHITECTURE;".format(indent=indentation, name=self._name))

