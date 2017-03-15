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
# from pyVHDLParser.Groups.Common import LinebreakGroup, EmptyLineGroup
# from pyVHDLParser.Groups.Document      import StartOfDocumentGroup
# from pyVHDLParser.DocumentModel import Document
# from pyVHDLParser.DocumentModel.Structural import Entity

# def MultiPartIterator(currentGroup, groupIterator):
# 	def __Generator(currentGroup, groupIterator):
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
# 	if currentGroup.MultiPart:
# 		return iter(__Generator(currentGroup, groupIterator))
# 	else:
# 		return iter(currentGroup)
from typing                         import Iterator

from pyVHDLParser                   import DocumentModel
from pyVHDLParser.Groups.Document   import StartOfDocumentGroup, EndOfDocumentGroup
from pyVHDLParser.Groups            import BlockParserException
from pyVHDLParser.Filters.Comment   import FastForward


# __ALL__ = [GroupToModelParser]


class _GroupIterator:
	def __init__(self, parserState, groupGenerator: Iterator):
		self._parserState =     parserState
		self._groupIterator =   iter(FastForward(groupGenerator))

	def __iter__(self):
		return self

	def __next__(self):
		nextGroup = self._groupIterator.__next__()
		self._parserState.CurrentGroup = nextGroup
		return nextGroup

class GroupToModelParser:
	@classmethod
	def Transform(cls, document, groupGenerator, debug=False):
		DocumentModel.DEBUG = debug

		startState = document.__class__.stateParse
		parser = cls.GroupParserState(startState, document, groupGenerator, debug=debug)
		parser.Run()

	@staticmethod
	def _TokenGenerator(currentGroup, groupIterator):
		groupType = type(currentGroup)

		for token in currentGroup:
			yield token
		for group in groupIterator:
			if isinstance(group, groupType):
				for token in group:
					yield token
				if (not group.MultiPart):
					break

	class GroupParserState:
		class StackItem(tuple):
			def __repr__(self):
				return "nxSt={0} / curN={1}".format(self[0].__func__.__qualname__, self[1].__class__.__name__)

		def __init__(self, startState, document, groupGenerator, debug):
			groupIterator = _GroupIterator(self, groupGenerator)
			firstGroup = groupIterator.__next__()
			assert isinstance(firstGroup, StartOfDocumentGroup)

			self._stack =         []
			self.NextState =      startState
			self.GroupIterator =  groupIterator
			self.CurrentGroup =   None  # next(groupIterator)
			self.Document =       document
			self.CurrentNode =    document

			self.debug = debug

		@property
		def PushState(self):
			return self.NextState

		@PushState.setter
		def PushState(self, value):
			stackItem = self.StackItem((
				self.NextState,
				self.CurrentNode
			))
			self._stack.append(stackItem)
			self.NextState = value

		def __iter__(self):
			if self.CurrentGroup.MultiPart:
				return iter(GroupToModelParser._TokenGenerator(self.CurrentGroup, self.GroupIterator))
			else:
				return iter(self.CurrentGroup)

		def __str__(self):
			return self.NextState.__func__.__qualname__

		def Pop(self, n=1):
			top = None
			for i in range(n):
				top = self._stack.pop()
			self.NextState = top[0]
			self.CurrentNode = top[1]

		def ReIssue(self):
			self.NextState(self)

		def Run(self):
			for group in self.GroupIterator:
				# self.CurrentGroup = group
				# if self.debug: print("  state={state!s: <50}  group={group!s: <40}   ".format(state=self, group=group))

				if isinstance(group, EndOfDocumentGroup):
					break

				self.NextState(self)
			else:
				raise BlockParserException("", None)
