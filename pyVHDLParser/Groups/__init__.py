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
# load dependencies
from types                                  import FunctionType
from typing                                 import Iterator

from pyTerminalUI                           import LineTerminal

from pyVHDLParser.Decorators                import Export
from pyVHDLParser                           import StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base                      import ParserException
from pyVHDLParser.Blocks                    import Block, CommentBlock, StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common             import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Reference          import Context, Library, Use
from pyVHDLParser.Blocks.Sequential         import Package, PackageBody
from pyVHDLParser.Blocks.Structural         import Entity, Architecture, Configuration

__all__ = []
__api__ = __all__


@Export
class BlockParserException(ParserException):
	def __init__(self, message, block):
		super().__init__(message)
		self._block = block


@Export
class BlockToGroupParser:
	@staticmethod
	def Transform(blockGenerator, debug=False):
		return ParserState(blockGenerator, debug=debug).GetGenerator()


# @staticmethod
# def _TokenGenerator(currentGroup, groupIterator):
# 	groupType = type(currentGroup)
#
# 	for token in currentGroup:
# 		yield token
# 	for group in groupIterator:
# 		if isinstance(group, groupType):
# 			for token in group:
# 				yield token
# 			if (not group.MultiPart):
# 				break


@Export
class _BlockIterator:
	def __init__(self, parserState, blockGenerator: Iterator):
		self._parserState : ParserState = parserState
		#self._blockIterator             = iter(FastForward(groupGenerator))
		self._blockIterator             = iter(blockGenerator)

	def __iter__(self):
		return self

	def __next__(self):
		nextBlock = self._blockIterator.__next__()
		self._parserState.Block = nextBlock
		return nextBlock


@Export
class ParserState:
	def __init__(self, blockGenerator, debug):
		self.NextState =            StartOfDocumentGroup.stateDocument
		self.ReIssue =              False
		self.Block        : Block = None
		self.NewBlock     : Block = None
		self.LastGroup    : Group = None

		self._stack =               []
		self._iterator =            iter(_BlockIterator(self, blockGenerator))
		self._blockMarker : Block = None
		self.NextGroup    : Group = StartOfDocumentGroup(next(self._iterator))
		self.NewGroup     : Group = None

		self.debug        : bool =  debug

		if (not isinstance(self.NextGroup.StartBlock, StartOfDocumentBlock)):
			raise BlockParserException("First block is not a StartOfDocumentBlock.", self.NextGroup.StartBlock)

	@property
	def PushState(self):
		return self.NextState
	@PushState.setter
	def PushState(self, value):
		assert (self.NextGroup is not None)
		self._stack.append((
			self.NextState,
			self._blockMarker,
			self.NextGroup
		))
		self.NextState =    value
		self._blockMarker = None
		self.NextGroup =    None

	@property
	def GetBlockIterator(self):
		return self._iterator

	# def __iter__(self):
	# 	return self._iterator

	# def __iter__(self):
	# 	if self.Block.MultiPart:
	# 		return iter(BlockToGroupParser._TokenGenerator(self.Block, self.BlockIterator))
	# 	else:
	# 		return iter(self.Block)

	@property
	def BlockMarker(self):
		if ((self.NewBlock is not None) and (self._blockMarker is self.Block)):
			# if self.debug: print("  {DARK_GREEN}@BlockMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._blockMarker, self.NewBlock, **Console.Foreground))
			self._blockMarker = self.NewBlock
		return self._blockMarker
	@BlockMarker.setter
	def BlockMarker(self, value):
		# if self.debug: print("  {DARK_GREEN}@BlockMarker: {0!s} --> {GREEN}{1!s}{NOCOLOR}".format(self._blockMarker, value, **Console.Foreground))
		self._blockMarker = value

	def __eq__(self, other):
		return self.NextState is other

	def __str__(self):
		return self.NextState.__func__.__qualname__

	def Pop(self, n=1):
		self.NewGroup =     self.NextGroup

		top = None
		for i in range(n):
			top = self._stack.pop()
		self.NextState =    top[0]
		self._blockMarker = top[1]
		self.NextGroup =    top[2]
		# print("{MAGENTA}appending {0!s} to {1!s}{NOCOLOR}".format(self.NewGroup.__class__.__qualname__, self.NextGroup.__class__,**Console.Foreground))
		if (self.NextGroup.InnerGroup is None):
			self.NextGroup.InnerGroup = self.NewGroup
		if (self.NewGroup.__class__ not in self.NextGroup._subGroups):
			raise BlockParserException("Group '{group1}' not supported in {group2}.".format(
				group1=self.NewGroup.__class__,
				group2=self.NextGroup.__class__.__qualname__
			), self.Block)

		self.NextGroup._subGroups[self.NewGroup.__class__].append(self.NewGroup)

	def GetGenerator(self):
		from pyVHDLParser.Groups            import BlockParserException

		# yield StartOfDocumentGroup
		self.LastGroup = self.NextGroup
		yield self.LastGroup

		for block in self._iterator:
			# an empty marker means: set on next yield run
			if (self._blockMarker is None):
				# if self.debug: print("  new block marker: None -> {0!s}".format(block))
				self._blockMarker = block

			# if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			# execute a state and reissue execution if needed
			self.ReIssue = True
			while self.ReIssue:
				self.ReIssue = False
				if self.debug: print("{DARK_GRAY}state={state!s: <50}  block={block!s: <40}     {NOCOLOR}".format(state=self, block=self.Block, **LineTerminal.Foreground))
				self.NextState(self)

				# yield a new group
				if (self.NewGroup is not None):
					yield self.NewGroup
					self.LastGroup = self.NewGroup
					self.NewGroup = None

					if (isinstance(self.Block, EndOfDocumentBlock) and isinstance(self.LastGroup, EndOfDocumentGroup)):
						return

		else:
			raise BlockParserException("Unexpected end of document.", self.Block)


@Export
class MetaGroup(type):
	"""Register all state*** methods in an array called '__STATES__'"""
	def __new__(cls, className, baseClasses, classMembers : dict):
		states = []
		for memberName, memberObject in classMembers.items():
			if (isinstance(memberObject, FunctionType) and (memberName[:5] == "state")):
				states.append(memberObject)

		classMembers['__STATES__'] = states
		return super().__new__(cls, className, baseClasses, classMembers)


@Export
class Group(metaclass=MetaGroup):
	__STATES__ = None

	def __init__(self, previousGroup, startBlock, endBlock=None):
		previousGroup.NextGroup =               self
		self._previousGroup =                   previousGroup
		self.NextGroup  : Group =               None
		self.InnerGroup : Group =               None
		self._subGroups : {MetaGroup: Group} =  {}

		self.StartBlock : Block =               startBlock
		self.EndBlock   : Block =               startBlock if (endBlock is None) else endBlock
		self.MultiPart =                        False

	def __len__(self):
		return self.EndBlock.EndToken.End.Absolute - self.StartBlock.StartToken.Start.Absolute + 1

	def __iter__(self):
		block = self.StartBlock
		print("group={0}({1})  start={2!s}  end={3!s}".format(self.__class__.__name__, self.__class__.__module__, self.StartBlock.StartToken, self.EndBlock.EndToken))
		while (block is not self.EndBlock):
			yield block
			if (block.NextBlock is None):
				raise BlockParserException("Token after {0!r} <- {1!r} <- {2!r} is empty (None).".format(block, block.PreviousToken, block.PreviousToken.PreviousToken), block)
			block = block.NextBlock

		yield self.EndBlock

	def __repr__(self):
		buffer = "undefined block content"
		# buffer = buffer.replace("\t", "\\t")
		# buffer = buffer.replace("\n", "\\n")
		return buffer

	def __str__(self):
		return "{{{groupName:.<156s}  at {start!s} .. {end!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			start=self.StartBlock.StartToken.Start,
			end=self.EndBlock.EndToken.End
		)

	def GetSubGroups(self, groupTypes=None):
		group = self.InnerGroup
		while (group is not None):
			yield group
			group = group.NextGroup

	@property
	def PreviousGroup(self):
		return self._previousGroup
	@PreviousGroup.setter
	def PreviousGroup(self, value):
		self._previousGroup = value
		value.NextGroup = self

	@property
	def Length(self):
		return len(self)

	@property
	def States(self):
		return self.__STATES__


@Export
class StartOfGroup(Group):
	def __init__(self, startBlock):
		self._previousGroup =                   None
		self.NextGroup  : Group =               None
		self.InnerGroup : Group =               None
		self._subGroups : {MetaGroup: Group} =  {}

		self.StartBlock : Block =               startBlock
		self.EndBlock   : Block =               None
		self.MultiPart =                        False

	def __iter__(self):
		yield self.StartBlock

	def __len__(self):
		return 0

	def __str__(self):
		return "{{{groupName:.<156s}  at {start!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			start=self.StartBlock.StartToken.Start
		)


@Export
class EndOfGroup(Group):
	def __init__(self, endBlock):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartBlock : Block = None
		self.EndBlock   : Block = endBlock
		self.MultiPart  =         False

	def __iter__(self):
		yield self.EndBlock

	def __len__(self):
		return 0

	def __str__(self):
		return "{{{groupName:.<156s}  at                      .. {end!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			end=self.EndBlock.EndToken.Start
		)


@Export
class StartOfDocumentGroup(StartOfGroup, StartOfDocument):
	def __init__(self, startBlock):
		from pyVHDLParser.Groups.Comment      import CommentGroup, WhitespaceGroup
		from pyVHDLParser.Groups.DesignUnit   import ContextGroup, EntityGroup, ArchitectureGroup, PackageGroup, PackageBodyGroup, ConfigurationGroup
		from pyVHDLParser.Groups.Reference    import LibraryGroup, UseGroup

		super().__init__(startBlock)

		self._subGroups = {
			CommentGroup:       [],
			WhitespaceGroup:    [],
			LibraryGroup:       [],
			UseGroup:           [],
			ContextGroup:       [],
			EntityGroup:        [],
			ArchitectureGroup:  [],
			PackageGroup:       [],
			PackageBodyGroup:   [],
			ConfigurationGroup: []
		}

	@classmethod
	def stateDocument(cls, parserState : ParserState):
		from pyVHDLParser.Groups.DesignUnit     import ContextGroup, EntityGroup, ArchitectureGroup, PackageGroup, PackageBodyGroup, ConfigurationGroup
		from pyVHDLParser.Groups.Reference      import LibraryGroup, UseGroup
		from pyVHDLParser.Groups.Comment import CommentGroup, WhitespaceGroup

		SIMPLE_BLOCKS = {
			Library.StartBlock:       LibraryGroup,
			Use.StartBlock:           UseGroup
		}
		COMPOUND_BLOCKS = {
			Context.NameBlock:        ContextGroup,
			Entity.NameBlock:         EntityGroup,
			Architecture.NameBlock:   ArchitectureGroup,
			Package.NameBlock:        PackageGroup,
			PackageBody.NameBlock:    PackageBodyGroup,
			Configuration.NameBlock:  ConfigurationGroup
		}

		currentBlock = parserState.Block

		if isinstance(currentBlock, (LinebreakBlock, IndentationBlock)):
			parserState.PushState =   WhitespaceGroup.stateParse
			parserState.NextGroup =   WhitespaceGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		elif isinstance(currentBlock, CommentBlock):
			parserState.PushState =   CommentGroup.stateParse
			parserState.NextGroup =   CommentGroup(parserState.LastGroup, currentBlock)
			parserState.BlockMarker = currentBlock
			parserState.ReIssue =     True
			return
		else:
			for blk in SIMPLE_BLOCKS:
				if isinstance(currentBlock, blk):
					group =                   SIMPLE_BLOCKS[blk]
					parserState.PushState =   group.stateParse
					parserState.NextGroup =   group(parserState.LastGroup, currentBlock)
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			for blk in COMPOUND_BLOCKS:
				if isinstance(currentBlock, blk):
					group =                   COMPOUND_BLOCKS[blk]
					parserState.PushState =   group.stateParse
					parserState.NextGroup =   group(parserState.LastGroup, currentBlock)
					parserState.BlockMarker = currentBlock
					parserState.ReIssue =     True
					return

			if isinstance(currentBlock, EndOfDocumentBlock):
				parserState.NewGroup = EndOfDocumentGroup(currentBlock)
				return

		raise BlockParserException("Expected keywords: architecture, context, entity, library, package, use. Found '{block!s}'.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@Export
class EndOfDocumentGroup(EndOfGroup, EndOfDocument):
	pass

@Export
class StartOfSnippetGroup(StartOfGroup, StartOfSnippet):
	pass

@Export
class EndOfSnippetGroup(EndOfGroup, EndOfSnippet):
	pass
