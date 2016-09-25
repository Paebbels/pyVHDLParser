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
from pyVHDLParser.Blocks.Common import LinebreakBlock, EmptyLineBlock
from pyVHDLParser.Blocks.Document      import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Exception import BlockParserException
from pyVHDLParser.Functions import Console
from pyVHDLParser.Token.Tokens import EndOfDocumentToken


class TokenToBlockParser:
	@classmethod
	def Transform(cls, rawTokenGenerator, debug=False):
		iterator =    iter(rawTokenGenerator)
		firstToken =  next(iterator)
		firstBlock =  StartOfDocumentBlock(firstToken)
		startState =  StartOfDocumentBlock.stateDocument
		return cls.__TokenParserState(startState, firstBlock, debug=debug).GetGenerator(iterator)


	class __TokenParserState:
		def __init__(self, startState, startBlock, debug):
			self._stack =       []
			self._tokenMarker = None
			self.NextState =    startState
			self.Counter =      0
			self.Token =        startBlock.StartToken
			self.NewToken =     None
			self.NewBlock =     startBlock
			self.LastBlock =    None

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
			if (self.NewToken is not None):
				if (self._tokenMarker is self.Token):
					if self.debug: print("  update marker: {0!s} -> {1!s}".format(self._tokenMarker, self.NewToken))
					self._tokenMarker = self.NewToken
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
			for token in iterator:
				if self.debug: print("  state={state!s: <50}  token={token!s: <40}   ".format(state=self, token=token))

				# overwrite an existing token and connect the next token with the new one
				if (self.NewToken is not None):
					# print("{GREEN}NewToken: {token}{NOCOLOR}".format(token=self.NewToken, **Console.Foreground))
					# update topmost TokenMarker
					if (self._tokenMarker is token.PreviousToken):
						if self.debug: print("  update marker: {0!s} -> {1!s}".format(self._tokenMarker, self.NewToken))
						self._tokenMarker = self.NewToken

					token.PreviousToken = self.NewToken
					self.NewToken =       None

				self.Token = token
				# an empty marker means: fill on next yield run
				if (self._tokenMarker is None):
					if self.debug: print("  new marker: None -> {0!s}".format(token))
					self._tokenMarker = token

				# a new block is assembled
				while (self.NewBlock is not None):
					if (isinstance(self.NewBlock, LinebreakBlock) and isinstance(self.LastBlock, (LinebreakBlock, EmptyLineBlock))):
						self.LastBlock = EmptyLineBlock(self.LastBlock, self.NewBlock.StartToken)
						self.LastBlock.NextBlock = self.NewBlock.NextBlock
					else:
						self.LastBlock = self.NewBlock

					self.NewBlock =  self.NewBlock.NextBlock
					yield self.LastBlock

				# execute a state
				self.NextState(self)

				if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			else:
				if (isinstance(self.Token, EndOfDocumentToken) and isinstance(self.NewBlock, EndOfDocumentBlock)):
					yield self.NewBlock
				else:
					raise BlockParserException("Unexpected end of document.", self.Token)
