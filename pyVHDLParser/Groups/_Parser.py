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
from typing                       import Iterator

from pyVHDLParser.Blocks          import Block
from pyVHDLParser.Blocks.Document import StartOfDocumentBlock
from pyVHDLParser.Groups import Group, BlockParserException
from pyVHDLParser.Filters.Comment import FastForward
from pyVHDLParser.Functions       import Console

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

class _BlockIterator:
	def __init__(self, parserState, blockGenerator: Iterator):
		self._parserState : BlockParserState  = parserState
		#self._blockIterator                   = iter(FastForward(groupGenerator))
		self._blockIterator                   = iter(blockGenerator)

	def __iter__(self):
		return self

	def __next__(self):
		nextBlock = self._blockIterator.__next__()
		self._parserState.Block = nextBlock
		return nextBlock


class BlockParserState:
	def __init__(self, blockGenerator, debug):
		from pyVHDLParser.Groups.Document import StartOfDocumentGroup

		self.NextState =            StartOfDocumentGroup.stateDocument
		self.ReIssue =              False
		self.Block        : Block = None
		self.NewBlock     : Block = None
		self.LastGroup    : Group = None

		self._stack =               []
		self._iterator =            iter(_BlockIterator(self, blockGenerator))
		self._blockMarker : Block = None
		self.NewGroup     : Group = StartOfDocumentGroup(next(self._iterator))

		self.debug =                debug

		if (not isinstance(self.NewGroup.StartBlock, StartOfDocumentBlock)):
			raise BlockParserException("First block is not a StartOfDocumentBlock.", self.NewGroup.StartBlock)

	@property
	def PushState(self):
		return self.NextState
	@PushState.setter
	def PushState(self, value):
		self._stack.append((
			self.NextState,
			self._blockMarker
		))
		self.NextState =    value
		self._blockMarker =  None

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
			if self.debug: print("  {DARK_GREEN}@BlockMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._blockMarker, self.NewBlock, **Console.Foreground))
			self._blockMarker = self.NewBlock
		return self._blockMarker
	@BlockMarker.setter
	def BlockMarker(self, value):
		if self.debug: print("  {DARK_GREEN}@BlockMarker: {0!s} ~> {GREEN}{1!s}{NOCOLOR}".format(self._blockMarker, self.NewBlock, **Console.Foreground))
		self._blockMarker = value

	def __eq__(self, other):
		return self.NextState is other

	def __str__(self):
		return self.NextState.__func__.__qualname__

	def Pop(self, n=1):
		top = None
		for i in range(n):
			top = self._stack.pop()
		self.NextState =    top[0]
		self._blockMarker = top[1]

	# def ReIssue(self):
	# 	self.NextState(self)

	def GetGenerator(self):
		from pyVHDLParser.Blocks.Document   import EndOfDocumentBlock
		from pyVHDLParser.Groups            import BlockParserException
		from pyVHDLParser.Groups.Document   import EndOfDocumentGroup

		# yield StartOfDocumentGroup
		self.LastGroup = self.NewGroup
		yield self.LastGroup

		for block in self._iterator:
			# overwrite an existing block and connect the next block with the new one
			# if (self.NewBlock is not None):
			# 	print("{GREEN}NewBlock: {block}{NOCOLOR}".format(block=self.NewBlock, **Console.Foreground))
			# 	# update topmost TokenMarker
			# 	if (self._blockMarker is block.PreviousToken):
			# 		if self.debug: print("  update block marker: {0!s} -> {1!s}".format(self._blockMarker, self.NewBlock))
			# 		self._blockMarker = self.NewBlock
			#
			# 	block.PreviousToken = self.NewBlock
			# 	self.NewBlock =       None

			# self.Block = block
			# an empty marker means: set on next yield run
			if (self._blockMarker is None):
				# if self.debug: print("  new block marker: None -> {0!s}".format(block))
				self._blockMarker = block

			# a new group is assembled
			# while (self.NewGroup is not None):
			# 	self.LastGroup = self.NewGroup
			#
			# 	self.NewGroup =  self.NewGroup.NextGroup
			# 	yield self.LastGroup

			if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			# execute a state and reissue execution if needed
			self.ReIssue = True
			while self.ReIssue:
				self.ReIssue = False
				print("{DARK_GRAY}state={state!s: <50}  block={block!s: <40}     {NOCOLOR}".format(state=self, block=self.Block, **Console.Foreground))
				self.NextState(self)



				# yield a new group
				self.LastGroup = self.NewGroup
				yield self.LastGroup

		else:
			if (isinstance(self.Block, EndOfDocumentBlock) and isinstance(self.NewGroup, EndOfDocumentGroup)):
				yield self.NewGroup
			else:
				raise BlockParserException("Unexpected end of document.", self.Block)
