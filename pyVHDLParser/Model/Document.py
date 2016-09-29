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
from pyVHDLParser.Blocks.Reference  import Library, Use, Context
from pyVHDLParser.Blocks.Structural import Entity, Architecture, Component
from pyVHDLParser.Blocks.Sequential import Package, PackageBody
from pyVHDLParser.Model.VHDLModel   import Document as DocumentModel
from pyVHDLParser.Model.Reference   import Library as LibraryModel, Use as UseModel
from pyVHDLParser.Model.Structural  import Entity as EntityModel, Architecture as ArchitectureModel
from pyVHDLParser.Model.Parser      import BlockToModelParser

# Type alias for type hinting
ParserState = BlockToModelParser.BlockParserState


class Document(DocumentModel):
	def __init__(self):
		super().__init__()
		self.__libraries = []
		self.__uses =      []

	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.CurrentBlock
		if isinstance(block, Library.LibraryBlock):
			parserState.PushState = LibraryModel.Library.stateParse
			parserState.ReIssue()
		elif isinstance(block, Use.UseBlock):
			parserState.PushState = UseModel.Use.stateParse
			parserState.ReIssue()
		elif isinstance(block, Entity.NameBlock):
			parserState.PushState = EntityModel.Entity.stateParse
			parserState.ReIssue()
		elif isinstance(block, Architecture.NameBlock):
			parserState.PushState = ArchitectureModel.Architecture.stateParse
			parserState.ReIssue()
		elif isinstance(block, Package.NameBlock):
			pass
		elif isinstance(block, PackageBody.NameBlock):
			pass
		else:
			pass
			# parserState.CurrentBlock = next(parserState.BlockIterator)

	def AddLibrary(self, libraryName):
		self.__libraries.append(libraryName)

	def AddUse(self, libraryName, packageName, objectName):
		self.__uses.append((libraryName, packageName, objectName))

	@property
	def Libraries(self):
		return self.__libraries

	@property
	def Uses(self):
		return self.__uses

	def AddEntity(self, entity):
		self._entities.append(entity)

	def AddArchitecture(self, architecture):
		self._architectures.append(architecture)

	def Print(self, indent=0):
		if (len(self.__libraries) > 0):
			for lib in self.__libraries:
				print("{indent}-- unused LIBRARY {lib};".format(indent="  " * indent, lib=lib))
		if (len(self.__uses) > 0):
			for lib, pack, obj in self.__uses:
				print("{indent}-- unused USE {lib}.{pack}.{obj};".format(indent="  " * indent, lib=lib, pack=pack, obj=obj))
		print()
		for entity in self._entities:
			entity.Print()
		print()
		for architecture in self._architectures:
			architecture.Print()


