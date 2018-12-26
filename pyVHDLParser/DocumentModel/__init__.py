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
from pathlib import Path

from pyVHDLParser.Base               import ParserException
from pyVHDLParser.Token.Parser       import Tokenizer
from pyVHDLParser.Blocks             import TokenToBlockParser
from pyVHDLParser.Groups             import StartOfDocumentGroup, EndOfDocumentGroup, BlockToGroupParser
from pyVHDLParser.Groups.DesignUnit  import EntityGroup, ArchitectureGroup, PackageBodyGroup, PackageGroup
from pyVHDLParser.Groups.Reference   import LibraryGroup, UseGroup
from pyVHDLParser.VHDLModel          import Document as DocumentModel


class GroupParserException(ParserException):
	def __init__(self, message, group):
		super().__init__(message)
		self._group = group


class Document(DocumentModel):
	def __init__(self, file):
		from pyVHDLParser.DocumentModel.Reference import Use, Library

		super().__init__()
		self.__libraries  : list[Library] = []
		self.__uses       : list[Use] =     []

		if isinstance(file, Path):
			self._filePath = file
		elif isinstance(file, str):
			self._filePath = Path(file)
		else:
			raise ValueError("Unsoppurted type for parameter type.")

	def Parse(self, content=None):
		if (content is None):
			if (not self._filePath.exists()):
				raise GroupParserException("File '{0!s}' does not exist.".format(self._filePath))

			with self._filePath.open('r') as fileHandle:
				content = fileHandle.read()

		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
		vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream)
		vhdlGroupStream = BlockToGroupParser.Transform(vhdlBlockStream)
		groups =          [group for group in vhdlGroupStream]
		firstGroup =      groups[0]
		lastGroup =       groups[-1]

		if (not isinstance(firstGroup, StartOfDocumentGroup)):
			raise GroupParserException("Expected group is not a StartOfDocumentGroup.", firstGroup)
		elif (not isinstance(lastGroup, EndOfDocumentGroup)):
			raise GroupParserException("Expected group is not an EndOfDocumentGroup.", lastGroup)

		# run recursively (node, group)
		self.stateParse(self, firstGroup)

	@classmethod
	def stateParse(cls, document, startOfDocumentGroup):
		from pyVHDLParser.DocumentModel.Reference   import Library as LibraryModel, Use as UseModel
		# from pyVHDLParser.DocumentModel.DesignUnit  import Context as ContextModel
		from pyVHDLParser.DocumentModel.DesignUnit  import Entity as EntityModel, Architecture as ArchitectureModel
		from pyVHDLParser.DocumentModel.DesignUnit  import Package as PackageModel, PackageBody as PackageBodyModel

		GROUP_TO_MODEL = {
			LibraryGroup:       LibraryModel,
			UseGroup:           UseModel,
			# ContextGroup:       ContextModel,
			EntityGroup:        EntityModel,
			ArchitectureGroup:  ArchitectureModel,
			PackageGroup:       PackageModel,
			PackageBodyGroup:   PackageBodyModel,
			# ConfigurationModel
		}

		for subGroup in startOfDocumentGroup.GetSubGroups():
			for group in GROUP_TO_MODEL:
				# TODO: compare to a direct dictionar match with exception fallback on whitespace
				if isinstance(subGroup, group):
					GROUP_TO_MODEL[group].stateParse(document, subGroup)
					break

	def AddLibrary(self, library):
		self.__libraries.append(library)

	def AddUse(self, use):
		self.__uses.append(use)

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

	def AddPackage(self, package):
		self._packages.append(package)

	def AddPackageBody(self, packageBody):
		self._packageBodies.append(packageBody)

	def Print(self, indent=0):
		_indent = "  " * indent
		if (len(self.__libraries) > 0):
			for library in self.__libraries:
				print("{indent}-- unused LIBRARY {lib};".format(indent=_indent, lib=library))
		if (len(self.__uses) > 0):
			for use in self.__uses:
				print("{indent}-- unused USE {lib}.{pack}.{obj};".format(indent=_indent, lib=use.Library, pack=use.Package, obj=use.Item))
		print()
		for entity in self._entities:
			entity.Print()
		print()
		for architecture in self._architectures:
			architecture.Print()
		print()
		for package in self._packages:
			package.Print()
		print()
		for packageBody in self._packageBodies:
			packageBody.Print()

#
# class _GroupIterator:
# 	def __init__(self, parserState, groupGenerator: Iterator):
# 		self._parserState =     parserState
# 		self._groupIterator =   iter(FastForward(groupGenerator))
#
# 	def __iter__(self):
# 		return self
#
# 	def __next__(self):
# 		nextGroup = self._groupIterator.__next__()
# 		self._parserState.CurrentGroup = nextGroup
# 		return nextGroup
#
# class GroupToModelParser:
#
#
# 	@staticmethod
# 	def _TokenGenerator(currentGroup, groupIterator):
# 		groupType = type(currentGroup)
#
# 		for token in currentGroup:
# 			yield token
# 		for group in groupIterator:
# 			if isinstance(group, groupType):
# 				for token in group:
# 					yield token
# 				if (not group.MultiPart):
# 					break
#
# 		def __iter__(self):
# 			if self.CurrentGroup.MultiPart:
# 				return iter(GroupToModelParser._TokenGenerator(self.CurrentGroup, self.GroupIterator))
# 			else:
# 				return iter(self.CurrentGroup)

