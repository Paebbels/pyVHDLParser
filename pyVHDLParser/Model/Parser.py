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
# from pyVHDLParser.Blocks.Common import LinebreakBlock, EmptyLineBlock
# from pyVHDLParser.Blocks.Document      import StartOfDocumentBlock
# from pyVHDLParser.Model import Document
# from pyVHDLParser.Model.Structural import Entity

# def MultiPartIterator(currentBlock, blockIterator):
# 	def __Generator(currentBlock, blockIterator):
# 		blockType = type(currentBlock)
#
# 		for token in currentBlock:
# 			yield token
# 		for block in blockIterator:
# 			if isinstance(block, blockType):
# 				for token in block:
# 					yield token
# 				if (not block.MultiPart):
# 					break
#
# 	if currentBlock.MultiPart:
# 		return iter(__Generator(currentBlock, blockIterator))
# 	else:
# 		return iter(currentBlock)
from pyVHDLParser.Blocks.Document import StartOfDocumentBlock


class BlockToModelParser:
	@classmethod
	def Transform(cls, document, blockGenerator, debug=False):
		startState = document.__class__.stateParse
		parser = cls.BlockParserState(startState, document, blockGenerator, debug=debug).GetGenerator()

	@staticmethod
	def _Generator(currentBlock, blockIterator):
		blockType = type(currentBlock)

		for token in currentBlock:
			yield token
		for block in blockIterator:
			if isinstance(block, blockType):
				for token in block:
					yield token
				if (not block.MultiPart):
					break

	class BlockParserState:
		def __init__(self, startState, document, blockGenerator, debug):
			blockIterator =       iter(blockGenerator)
			firstBlock =          next(blockIterator)
			assert isinstance(firstBlock, StartOfDocumentBlock)

			self._stack =         []
			self.NextState =      startState
			self.BlockIterator =  blockIterator
			self.CurrentBlock =   next(blockIterator)
			self.Document =       document
			self.CurrentNode =    document

			self.debug =          debug

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

		def __iter__(self):
			if self.CurrentBlock.MultiPart:
				return iter(BlockToModelParser._Generator(self.CurrentBlock, self.BlockIterator))
			else:
				return iter(self.CurrentBlock)

		def __str__(self):
			return self.NextState.__func__.__qualname__

		def Pop(self, n=1):
			top = None
			for i in range(n):
				top = self._stack.pop()
			self.NextState =    top[0]
			self.CurrentNode =  top[1]

		def GetGenerator(self):
			for i in range(10):
				if self.debug: print("  state={state!s: <50}  block={block!s: <40}   ".format(state=self, block=self.CurrentBlock))
				self.NextState(self)


				# execute a state
				# self.NextState(self)
