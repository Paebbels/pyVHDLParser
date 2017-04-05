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
from typing                                 import Iterator

from pyVHDLParser.Base                      import ParserException
from pyVHDLParser.Groups                    import Group, StartOfDocumentGroup, EndOfDocumentGroup
from pyVHDLParser.Groups.DesignUnit         import EntityGroup, ArchitectureGroup, PackageBodyGroup, PackageGroup
from pyVHDLParser.Groups.Reference          import LibraryGroup, UseGroup
from pyVHDLParser.VHDLModel                 import Document as DocumentModel
from pyVHDLParser.Functions                 import Console


class GroupParserException(ParserException):
	def __init__(self, message, group):
		super().__init__(message)
		self._group = group


class GroupToModelParser:
	@staticmethod
	def Transform(document, groupGenerator, debug=False):
		parser = ParserState(document, groupGenerator, debug=debug)
		parser.Run()

# @staticmethod
# def _TokenGenerator(currentModel, modelIterator):
# 	modelType = type(currentModel)
#
# 	for token in currentModel:
# 		yield token
# 	for model in modelIterator:
# 		if isinstance(model, modelType):
# 			for token in model:
# 				yield token
# 			if (not model.MultiPart):
# 				break

class _GroupIterator:
	def __init__(self, parserState, groupGenerator: Iterator):
		self._parserState : ParserState = parserState
		self._groupIterator             = iter(groupGenerator)

	def __iter__(self):
		return self

	def __next__(self):
		nextGroup = self._groupIterator.__next__()
		self._parserState.Group = nextGroup
		return nextGroup


class ParserState:
	def __init__(self, document, groupGenerator, debug):
		self.NextState =            document.stateParse
		self.CurrentNode =          document
		self._document  =           document
		self._stack =               []
		self._iterator =            iter(_GroupIterator(self, groupGenerator))
		self.Group        : Group = next(self._iterator)
		self.ReIssue =              False

		self.debug        : bool =  debug

		if (not isinstance(self.Group, StartOfDocumentGroup)):
			raise GroupParserException("First group is not a StartOfDocumentGroup.", self.Group)

	@property
	def PushState(self):
		return self.NextState
	@PushState.setter
	def PushState(self, value):
		self._stack.append((
			self.NextState,
			self.CurrentNode
		))
		self.NextState =    value

	@property
	def GetGroupIterator(self):
		return self._iterator

	# def __iter__(self):
	# 	return self._iterator

	# def __iter__(self):
	# 	if self.Group.MultiPart:
	# 		return iter(GroupToModelParser._TokenGenerator(self.Group, self.GroupIterator))
	# 	else:
	# 		return iter(self.Group)


	def __eq__(self, other):
		return self.NextState is other

	def __str__(self):
		return self.NextState.__func__.__qualname__

	def Pop(self, n=1):
		print("Leaving {0!s}.".format(self.NextState))
		top = None
		for i in range(n):
			top = self._stack.pop()
		self.NextState =    top[0]
		self.CurrentNode =  top[1]

	def Run(self):
		for group in self._iterator:
			# if self.debug: print("  state={state!s: <50}  group={group!s: <40}   ".format(state=self, group=group))

			# if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			# execute a state and reissue execution if needed
			self.ReIssue = True
			while self.ReIssue:
				self.ReIssue = False
				if self.debug: print("{DARK_GRAY}state={state!s: <50}  group={group!s: <40}     {NOCOLOR}".format(state=self, group=self.Group, **Console.Foreground))
				self.NextState(self)

				if isinstance(self.Group, EndOfDocumentGroup):
					break
		else:
			raise GroupParserException("Unexpected end of document.", self.Group)


class Document(DocumentModel):
	def __init__(self):
		super().__init__()
		self.__libraries = []
		self.__uses =      []

	@classmethod
	def stateParse(cls, parserState: ParserState):
		from pyVHDLParser.DocumentModel.Reference               import Library as LibraryModel, Use as UseModel
		from pyVHDLParser.DocumentModel.Structural.Entity       import Entity as EntityModel
		from pyVHDLParser.DocumentModel.Structural.Architecture import Architecture as ArchitectureModel
		from pyVHDLParser.DocumentModel.Sequential              import Package as PackageModel, PackageBody as PackageBodyModel

		group = parserState.Group

		if isinstance(group, LibraryGroup):
			parserState.PushState = LibraryModel.stateParse
			parserState.ReIssue =   True
		elif isinstance(group, UseGroup):
			parserState.PushState = UseModel.stateParse
			parserState.ReIssue =   True
		elif isinstance(group, EntityGroup):
			parserState.PushState = EntityModel.stateParse
			parserState.ReIssue =   True
		elif isinstance(group, ArchitectureGroup):
			parserState.PushState = ArchitectureModel.stateParse
			parserState.ReIssue =   True
		# elif isinstance(group, PackageGroup):
		# 	parserState.PushState = PackageModel.stateParse
		# 	parserState.ReIssue =   True
		# elif isinstance(group, PackageBodyGroup):
		# 	parserState.PushState = PackageBodyModel.stateParse
		# 	parserState.ReIssue =   True
		else:
			pass
			# parserState.CurrentBlock = next(parserState.BlockIterator)

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

