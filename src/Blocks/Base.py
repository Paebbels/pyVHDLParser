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
from src.Token.Parser import CharacterToken
from src.Token.Keywords import *


class Block:
	def __init__(self, previousBlock, startToken, endToken=None, multiPart=False):
		previousBlock.NextBlock = self
		self._previousBlock =     previousBlock
		self._nextBlock =         None
		self.StartToken =         startToken
		self._endToken =          endToken
		self.MultiPart =          multiPart

	def __len__(self):
		return self.EndToken.End.Absolute - self.StartToken.Start.Absolute + 1

	def __iter__(self):
		token = self.StartToken
		# print("start={0!s}  end={1!s}".format(self.StartToken, self.EndToken))
		while (token is not self.EndToken):
			yield token
			if (token.NextToken is None):
				raise ParserException("Token after {0} <- {1} <- {2} is None.".format(token, token.PreviousToken, token.PreviousToken.PreviousToken), token)
			token = token.NextToken

		yield self.EndToken

	def __repr__(self):
		buffer = ""
		for token in self:
			if isinstance(token, CharacterToken):
				buffer += repr(token)
			else:
				buffer += token.Value

		buffer = buffer.replace("\t", "\\t")
		buffer = buffer.replace("\n", "\\n")
		return buffer

	def __str__(self):
		return "[{blockName: <30s} '{stream!r: <60s}' at {start!s} .. {end!s}]".format(
			blockName=type(self).__name__,
			stream=self,
			start=self.StartToken.Start,
			end=self.EndToken.End
		)

	@property
	def PreviousBlock(self):
		return self._previousBlock
	@PreviousBlock.setter
	def PreviousBlock(self, value):
		self._previousBlock = value
		value.NextBlock = self

	@property
	def NextBlock(self):
		return self._nextBlock
	@NextBlock.setter
	def NextBlock(self, value):
		self._nextBlock = value

	@property
	def EndToken(self):
		return self._endToken
	@EndToken.setter
	def EndToken(self, value):
		self._endToken = value

	@property
	def Length(self):
		return len(self)
