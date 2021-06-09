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
from pathlib                              import Path
from typing                               import List, Union

from pydecor.decorators                   import export
from pyVHDLModel.VHDLModel                import Document as DocumentModel

from pyVHDLParser.Base                    import ParserException
from pyVHDLParser.Token.Parser            import Tokenizer
from pyVHDLParser.Blocks                  import TokenToBlockParser, BlockParserException
from pyVHDLParser.Groups import StartOfDocumentGroup, EndOfDocumentGroup, BlockToGroupParser, Group, GroupParserException
from pyVHDLParser.Groups.Comment          import WhitespaceGroup
from pyVHDLParser.Groups.DesignUnit       import ContextGroup, EntityGroup, ArchitectureGroup, PackageBodyGroup, PackageGroup
from pyVHDLParser.Groups.Reference        import LibraryGroup, UseGroup
from pyVHDLParser.DocumentModel.Reference import Library, PackageReference

__all__ = []
__api__ = __all__


@export
class DOMParserException(ParserException):
	def __init__(self, message, group):
		super().__init__(message)
		self._group = group


@export
class Document(DocumentModel):
	__libraries:  List[Library]
	__uses:       List[PackageReference]

	def __init__(self, file: Union[Path, str]):  # FIXME: parameter type
		if isinstance(file, Path):
			filePath = file
		elif isinstance(file, str):
			filePath = Path(file)
		else:
			raise ValueError("Unsupported type for parameter 'file'.")

		super().__init__(filePath)

		self.__libraries =  []
		self.__uses  =      []

	def Parse(self, content=None):  # FIXME: parameter type
		if (content is None):
			if (not self._path.exists()):
				raise DOMParserException("File '{0!s}' does not exist.".format(self._path))\
					from FileNotFoundError(str(self._path))

			with self._path.open('r') as fileHandle:
				content = fileHandle.read()

		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
		vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream)
		vhdlGroupStream = BlockToGroupParser.Transform(vhdlBlockStream)
		try:
			groups =          [group for group in vhdlGroupStream]
		except BlockParserException as ex:
			raise DOMParserException("Error while parsing and indexing the source code.", ex.Group) from ex
		except GroupParserException as ex:
			raise DOMParserException("Unexpected ParserException.", ex.Block) from ex
		except ParserException as ex:
			raise DOMParserException("Unexpected ParserException.", ex.Position) from ex
		except Exception as ex:
			raise DOMParserException("Unexpected exception.", None) from ex

		firstGroup =      groups[0]
		lastGroup =       groups[-1]

		if (not isinstance(firstGroup, StartOfDocumentGroup)):
			raise DOMParserException("Expected group is not a StartOfDocumentGroup.", firstGroup)
		elif (not isinstance(lastGroup, EndOfDocumentGroup)):
			raise DOMParserException("Expected group is not an EndOfDocumentGroup.", lastGroup)

		# run recursively (node, group)
		self.stateParse(self, firstGroup)

	@classmethod
	def stateParse(cls, document, startOfDocumentGroup: Group):
		from pyVHDLParser.DocumentModel.Reference               import Library as LibraryModel, PackageReference as UseModel
		from pyVHDLParser.DocumentModel.DesignUnit.Context      import Context as ContextModel
		from pyVHDLParser.DocumentModel.DesignUnit.Entity       import Entity as EntityModel
		from pyVHDLParser.DocumentModel.DesignUnit.Architecture import Architecture as ArchitectureModel
		from pyVHDLParser.DocumentModel.DesignUnit.Package      import Package as PackageModel
		from pyVHDLParser.DocumentModel.DesignUnit.PackageBody  import PackageBody as PackageBodyModel

		GROUP_TO_MODEL = {
			LibraryGroup:       LibraryModel,
			UseGroup:           UseModel,
			ContextGroup:       ContextModel,
			EntityGroup:        EntityModel,
			ArchitectureGroup:  ArchitectureModel,
			PackageGroup:       PackageModel,
			PackageBodyGroup:   PackageBodyModel,
			# ConfigurationModel
		}

		for subGroup in startOfDocumentGroup.GetSubGroups():
			if isinstance(subGroup, (WhitespaceGroup)):
				pass
			for group in GROUP_TO_MODEL:
				# TODO: compare to a direct dictionary match with exception fallback on whitespace
				if isinstance(subGroup, group):
					GROUP_TO_MODEL[group].stateParse(document, subGroup)
					break

	def AddLibrary(self, library):  # FIXME: parameter type
		self.__libraries.append(library)

	def AddUse(self, use):  # FIXME: parameter type
		self.__uses.append(use)

	@property
	def Libraries(self):
		return self.__libraries

	@property
	def Uses(self):
		return self.__uses

	def AddContext(self, context):  # FIXME: parameter type
		self._contexts.append(context)

	def AddEntity(self, entity):  # FIXME: parameter type
		self._entities.append(entity)

	def AddArchitecture(self, architecture):  # FIXME: parameter type
		self._architectures.append(architecture)

	def AddPackage(self, package):  # FIXME: parameter type
		self._packages.append(package)

	def AddPackageBody(self, packageBody):  # FIXME: parameter type
		self._packageBodies.append(packageBody)

	def Print(self, indent: int=0):
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
