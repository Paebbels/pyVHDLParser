# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
#
# ==============================================================================
# Authors:          Patrick Lehmann
#
# Python Module:    TODO
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
class SourceCodePosition:
	def __init__(self, row, column, absolute):
		self.Row =       row
		self.Column =    column
		self.Absolute =  absolute

	def __repr__(self):
		return "{0}:{1}".format(self.Row, self.Column)

	def __str__(self):
		return "(line: {0: >3}, col: {1: >2})".format(self.Row, self.Column)


class Token:
	def __init__(self, previousToken, start, end=None):
		previousToken.NextToken = self
		self._previousToken =     previousToken
		self.NextToken =          None
		self.Start =              start
		self.End =                end

	def __len__(self):
		return self.End.Absolute - self.Start.Absolute + 1

	@property
	def PreviousToken(self):
		return self._previousToken
	@PreviousToken.setter
	def PreviousToken(self, value):
		self._previousToken = value
		value.NextToken =     self

	@property
	def Length(self):
		return len(self)

	def __str__(self):
		return repr(self) + " at " + str(self.Start)

class ValuedToken(Token):
	def __init__(self, previousToken, value, start, end=None):
		super().__init__(previousToken, start, end)
		self.Value =  value


class SuperToken(Token):
	def __init__(self, startToken, endToken=None):
		super().__init__(startToken.PreviousToken, startToken.Start, endToken.End if endToken else None)
		self.StartToken = startToken
		self.EndToken =   endToken

	def __iter__(self):
		token = self.StartToken
		while (token is not self.EndToken):
			yield token
			token = token.NextToken
		yield self.EndToken

class StartOfDocumentToken(Token):
	def __init__(self):
		self._previousToken =     None
		self._nextToken =         None
		self.Start =              SourceCodePosition(1, 1, 1)
		self.End =                None

	def __len__(self):
		return 0

	def __str__(self):
		return "<StartOfDocumentToken>"


class EndOfDocumentToken(Token):
	def __init__(self, previousToken, end):
		super().__init__(previousToken, start=end)

	def __len__(self):
		return 0

	def __str__(self):
		return "<EndOfDocumentToken>"


class CharacterToken(ValuedToken):
	def __init__(self, previousToken, value, start):
		if (len(value) != 1):    raise ValueError()
		super().__init__(previousToken, value, start=start, end=start)

	def __len__(self):
		return 1

	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other

	__CHARACTER_TRANSLATION__ = {
		"\r":    "\\r",
		"\n":    "\\n",
		"\t":    "\\t",
		" ":     "SPACE"
	}

	def __str__(self):
		return "<CharacterToken '{char}' at {pos!r}>".format(
						char=self.__repr__(), pos=self.Start)

	def __repr__(self):
		if (self.Value in self.__CHARACTER_TRANSLATION__):
			return self.__CHARACTER_TRANSLATION__[self.Value]
		else:
			return self.Value


class SpaceToken(ValuedToken):
	def __str__(self):
		return "<SpaceToken '{value}' at {pos!r}>".format(
						value=self.Value, pos=self.Start)

class DelimiterToken(ValuedToken):
	def __str__(self):
		return "<DelimiterToken '{value}' at {pos!r}>".format(
						value=self.Value, pos=self.Start)

class NumberToken(ValuedToken):
	def __str__(self):
		return "<NumberToken '{value}' at {pos!r}>".format(
						value=self.Value, pos=self.Start)

class StringToken(ValuedToken):
	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other
	def __le__(self, other):  return self.Value.lower() == other
	def __ge__(self, other):  return self.Value.upper() == other

	def __str__(self):
		return "<StringToken '{value}' at {pos!r}>".format(
						value=self.Value, pos=self.Start)
