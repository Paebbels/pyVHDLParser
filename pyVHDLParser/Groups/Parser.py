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
from pyVHDLParser.Functions         import Console


class BlockToGroupParser:
	@classmethod
	def Transform(cls, rawTokenGenerator, debug=False):
		from pyVHDLParser.Groups.Document import StartOfDocumentGroup

		iterator =    iter(rawTokenGenerator)
		firstBlock =  next(iterator)
		firstGroup =  StartOfDocumentGroup(firstBlock)
		startState =  StartOfDocumentGroup.stateDocument
		return cls.BlockParserState(startState, firstGroup, debug=debug).GetGenerator(iterator)


	class BlockParserState:
		def __init__(self, startState, startGroup, debug):
			self._stack =       []
			self._tokenMarker = None
			self.NextState =    startState
			self.Counter =      0
			self.Block =        startGroup.StartBlock
			self.NewBlock =     None
			self.NewGroup =     startGroup
			self.LastGroup =    None

			self.debug =        debug

		@property
		def PushState(self):
			return self.NextState
		@PushState.setter
		def PushState(self, value):
			self._stack.append((
				self.NextState,
				self._tokenMarker,
				self.Counter
			))
			self.NextState =    value
			self._tokenMarker =  None

		@property
		def TokenMarker(self):
			if ((self.NewBlock is not None) and (self._tokenMarker is self.Block)):
				if self.debug: print("  {DARK_GREEN}@TokenMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._tokenMarker, self.NewBlock, **Console.Foreground))
				self._tokenMarker = self.NewBlock
			return self._tokenMarker
		@TokenMarker.setter
		def TokenMarker(self, value):
			self._tokenMarker = value

		def __eq__(self, other):
			return self.NextState == other

		def __str__(self):
			return self.NextState.__func__.__qualname__

		def Pop(self, n=1):
			top = None
			for i in range(n):
				top = self._stack.pop()
			self.NextState =    top[0]
			self._tokenMarker = top[1]
			self.Counter =      top[2]

		def GetGenerator(self, iterator):
			from pyVHDLParser.Groups.Document   import EndOfDocumentGroup
			from pyVHDLParser.Groups            import BlockParserException
			from pyVHDLParser.Blocks.Document   import EndOfDocumentBlock

			for token in iterator:
				# overwrite an existing token and connect the next token with the new one
				if (self.NewBlock is not None):
					# print("{GREEN}NewToken: {token}{NOCOLOR}".format(token=self.NewToken, **Console.Foreground))
					# update topmost TokenMarker
					if (self._tokenMarker is token.PreviousToken):
						if self.debug: print("  update marker: {0!s} -> {1!s}".format(self._tokenMarker, self.NewBlock))
						self._tokenMarker = self.NewBlock

					token.PreviousToken = self.NewBlock
					self.NewBlock =       None

				self.Block = token
				# an empty marker means: fill on next yield run
				if (self._tokenMarker is None):
					if self.debug: print("  new marker: None -> {0!s}".format(token))
					self._tokenMarker = token

				# a new group is assembled
				while (self.NewGroup is not None):
					# if (isinstance(self.NewGroup, LinebreakGroup) and isinstance(self.LastGroup, (LinebreakGroup, EmptyLineGroup))):
					# 	self.LastGroup = EmptyLineGroup(self.LastGroup, self.NewGroup.StartToken)
					# 	self.LastGroup.NextGroup = self.NewGroup.NextGroup
					# else:
					self.LastGroup = self.NewGroup

					self.NewGroup =  self.NewGroup.NextGroup
					yield self.LastGroup

				# if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
				if self.debug: print("  state={state!s: <50}  token={token!s: <40}   ".format(state=self, token=token))
				# execute a state
				self.NextState(self)

			else:
				if (isinstance(self.Block, EndOfDocumentBlock) and isinstance(self.NewGroup, EndOfDocumentGroup)):
					yield self.NewGroup
				else:
					raise BlockParserException("Unexpected end of document.", self.Block)
