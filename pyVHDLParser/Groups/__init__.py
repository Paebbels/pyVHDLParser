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
from types                                  import FunctionType
from typing import Iterator, Callable, List, Generator, Any, Dict

from pyTerminalUI                           import LineTerminal

from pydecor.decorators                     import export

from pyVHDLParser                           import StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base                      import ParserException
from pyVHDLParser.Blocks                    import Block, CommentBlock, StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common             import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Reference          import Context, Library, Use
from pyVHDLParser.Blocks.Sequential         import Package, PackageBody
from pyVHDLParser.Blocks.Structural         import Entity, Architecture, Configuration

__all__ = []
__api__ = __all__


@export
class GroupParserException(ParserException):
	def __init__(self, message: str, block: Block):
		super().__init__(message)
		self._block = block


@export
class BlockToGroupParser:
	"""Wrapping class to offer some class methods."""

	@staticmethod
	def Transform(blockGenerator: Generator[Block, Any, None]) -> Generator['Group', Any, None]:
		"""Returns a generator, that reads from a token generator and emits a chain of blocks."""

		state = ParserState(blockGenerator)
		return state.GetGenerator()


@export
class BlockIterator:
	def __init__(self, parserState, blockGenerator: Iterator):
		self._parserState: ParserState = parserState
		#self._blockIterator             = iter(FastForward(groupGenerator))
		self._blockIterator             = iter(blockGenerator)

	def __iter__(self) -> 'BlockIterator':
		return self

	def __next__(self) -> 'Block':
		nextBlock = self._blockIterator.__next__()
		self._parserState.Block = nextBlock
		return nextBlock


@export
class ParserState:
	"""Represents the current state of a block-to-group parser."""

	_iterator:   Iterator
	_stack:      List[Callable]
	_blockMarker: Block

	Block:       Block
	NextState:   Callable
	ReIssue:     bool

	NewBlock:    Block
	NewGroup:    'Group'
	LastGroup:   'Group'
	NextGroup:   'Group'

	def __init__(self, blockGenerator: Generator[Block, Any, None]):
		"""Initializes the parser state."""

		self._iterator =    iter(BlockIterator(self, blockGenerator))   # XXX: review iterator vs. generator
		self._stack =       []
		self._blockMarker = None

		startBlock =        next(self._iterator)
		startGroup =        StartOfDocumentGroup(startBlock)

		if (not isinstance(startBlock, StartOfDocumentBlock)):
			raise GroupParserException("First block is not a StartOfDocumentBlock.", startBlock)

		self.Block =        None
		self.NextState =    StartOfDocumentGroup.stateDocument
		self.ReIssue =      False
		self.NewBlock =     None
		self.NewGroup =     None
		self.LastGroup =    None
		self.NextGroup =    startGroup

	@property
	def PushState(self) -> 'Group':
		return self.NextState
	@PushState.setter
	def PushState(self, value: Callable):
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
	def GetBlockIterator(self):    # FIXME: what return type?
		return self._iterator

	# XXX: implement this method
	# def __iter__(self):
	# 	return self._iterator

	# def __iter__(self):
	# 	if self.Block.MultiPart:
	# 		return iter(BlockToGroupParser._TokenGenerator(self.Block, self.BlockIterator))
	# 	else:
	# 		return iter(self.Block)

	@property
	def BlockMarker(self) -> 'Block':
		if ((self.NewBlock is not None) and (self._blockMarker is self.Block)):
			# if self.debug: print("  {DARK_GREEN}@BlockMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._blockMarker, self.NewBlock, **Console.Foreground))
			self._blockMarker = self.NewBlock
		return self._blockMarker
	@BlockMarker.setter
	def BlockMarker(self, value: Block):
		# if self.debug: print("  {DARK_GREEN}@BlockMarker: {0!s} --> {GREEN}{1!s}{NOCOLOR}".format(self._blockMarker, value, **Console.Foreground))
		self._blockMarker = value

	def __eq__(self, other: Callable) -> bool:
		"""Return true if parser state is equal to the second operand."""
		return self.NextState is other

	def __str__(self) -> str:
		return self.NextState.__func__.__qualname__

	def Pop(self, n: int=1):
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
			raise GroupParserException("Group '{group1}' not supported in {group2}.".format(
				group1=self.NewGroup.__class__,
				group2=self.NextGroup.__class__.__qualname__
			), self.Block)

		self.NextGroup._subGroups[self.NewGroup.__class__].append(self.NewGroup)

	def GetGenerator(self):  # XXX: return type
		from pyVHDLParser.Groups            import GroupParserException

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
				LineTerminal().WriteDryRun("{DARK_GRAY}reissue state={state!s: <50}  block={block!s: <40}     {NOCOLOR}".format(state=self, block=self.Block, **LineTerminal.Foreground))
				self.NextState(self)

				# yield a new group
				if (self.NewGroup is not None):
					yield self.NewGroup
					self.LastGroup = self.NewGroup
					self.NewGroup = None

					if (isinstance(self.Block, EndOfDocumentBlock) and isinstance(self.LastGroup, EndOfDocumentGroup)):
						return

		else:
			raise GroupParserException("Unexpected end of document.", self.Block)


@export
class MetaGroup(type):
	"""Register all state*** methods in an array called '__STATES__'"""
	def __new__(cls, className, baseClasses, classMembers: dict):
		states = []
		for memberName, memberObject in classMembers.items():
			if (isinstance(memberObject, FunctionType) and (memberName[:5] == "state")):
				states.append(memberObject)

		classMembers['__STATES__'] = states
		return super().__new__(cls, className, baseClasses, classMembers)


@export
class Group(metaclass=MetaGroup):
	__STATES__ = None

	_previousGroup:  'Group'                   #: Reference to the previous group.
	NextGroup:       'Group'                   #: Reference to the next group.
	InnerGroup:      'Group'                   #: Reference to the first inner group.
	_subGroups:      Dict[MetaGroup, 'Group']  #: References to all inner groups by group type.

	StartBlock:      Block                     #: Reference to the first block in the scope of this group.
	EndBlock:        Block                     #: Reference to the last block in the scope of this group.
	MultiPart:       bool                      #: True, if this group has multiple parts.

	def __init__(self, previousGroup: 'Group', startBlock: Block, endBlock: Block=None):
		previousGroup.NextGroup = self
		self._previousGroup =     previousGroup
		self.NextGroup =          None
		self.InnerGroup =         None
		self._subGroups =         {}

		self.StartBlock =         startBlock
		self.EndBlock =           startBlock if (endBlock is None) else endBlock
		self.MultiPart =          False

	def __len__(self) -> int:
		return self.EndBlock.EndToken.End.Absolute - self.StartBlock.StartToken.Start.Absolute + 1

	def __iter__(self):   # XXX: return type; iterator vs. generator
		block = self.StartBlock
		print("group={0}({1})  start={2!s}  end={3!s}".format(self.__class__.__name__, self.__class__.__module__, self.StartBlock.StartToken, self.EndBlock.EndToken))
		while (block is not self.EndBlock):
			yield block
			if (block.NextBlock is None):
				raise GroupParserException("Token after {0!r} <- {1!r} <- {2!r} is empty (None).".format(block, block.PreviousToken, block.PreviousToken.PreviousToken), block)
			block = block.NextBlock

		yield self.EndBlock

	def __repr__(self) -> str:
		buffer = "undefined block content"
		# buffer = buffer.replace("\t", "\\t")
		# buffer = buffer.replace("\n", "\\n")
		return buffer

	def __str__(self) -> str:
		return "{{{groupName:.<156s}  at {start!s} .. {end!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			start=self.StartBlock.StartToken.Start,
			end=self.EndBlock.EndToken.End
		)

	def GetSubGroups(self, groupTypes=None):  # XXX: return type
		group = self.InnerGroup
		while (group is not None):
			yield group
			group = group.NextGroup

	@property
	def PreviousGroup(self) -> 'Group':
		return self._previousGroup
	@PreviousGroup.setter
	def PreviousGroup(self, value: 'Group'):
		self._previousGroup = value
		value.NextGroup = self

	@property
	def Length(self) -> int:
		return len(self)

	@property
	def States(self) -> List[Callable]:
		return self.__STATES__


@export
class StartOfGroup(Group):
	def __init__(self, startBlock: Block):
		self._previousGroup = None
		self.NextGroup =      None
		self.InnerGroup =     None
		self._subGroups =     {}

		self.StartBlock =     startBlock
		self.EndBlock =       None
		self.MultiPart =      False

	# TODO: needs review: should TokenIterator be used?
	def __iter__(self):
		yield self.StartBlock

	def __len__(self) -> int:
		return 0

	def __str__(self) -> str:
		return "{{{groupName:.<156s}  at {start!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			start=self.StartBlock.StartToken.Start
		)


@export
class EndOfGroup(Group):
	def __init__(self, endBlock: Block):
		self._previousGroup = None
		self.NextGroup =      None
		self.StartBlock =     None
		self.EndBlock =       endBlock
		self.MultiPart =      False

	# TODO: needs review: should TokenIterator be used?
	def __iter__(self):
		yield self.EndBlock

	def __len__(self) -> int:
		return 0

	def __str__(self) -> str:
		return "{{{groupName:.<156s}  at                      .. {end!s}}}".format(
			groupName="{module}.{classname}  ".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__
			),
			end=self.EndBlock.EndToken.Start
		)


@export
class StartOfDocumentGroup(StartOfGroup, StartOfDocument):
	def __init__(self, startBlock: Block):
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
	def stateDocument(cls, parserState: ParserState):
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

		raise GroupParserException("Expected keywords: architecture, context, entity, library, package, use. Found '{block!s}'.".format(
			block=currentBlock.__class__.__qualname__
		), currentBlock)


@export
class EndOfDocumentGroup(EndOfGroup, EndOfDocument):
	pass

@export
class StartOfSnippetGroup(StartOfGroup, StartOfSnippet):
	pass

@export
class EndOfSnippetGroup(EndOfGroup, EndOfSnippet):
	pass
