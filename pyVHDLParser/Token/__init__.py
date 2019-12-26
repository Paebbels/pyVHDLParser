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
from pyVHDLParser import SourceCodePosition, StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet


class Token:
	def __init__(self, previousToken, start, end=None):
		previousToken.NextToken = self
		self._previousToken : Token =               previousToken
		self.NextToken      : Token =               None
		self.Start          : SourceCodePosition =  start
		self.End            : SourceCodePosition =  end

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
		self.Value : str =  value

	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other
	def __hash__(self):       return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + self.Value + "'  ",
				pos=self.Start
			)


# class SuperToken(Token):
# 	def __init__(self, startToken, endToken=None):
# 		super().__init__(startToken.PreviousToken, startToken.Start, endToken.End if endToken else None)
# 		self.StartToken = startToken
# 		self.EndToken =   endToken
#
# 	def __iter__(self):
# 		token = self.StartToken
# 		while (token is not self.EndToken):
# 			yield token
# 			token = token.NextToken
# 		yield self.EndToken


class StartOfToken(Token):
	def __init__(self):
		self._previousToken =     None
		self._nextToken =         None
		self.Start =              SourceCodePosition(1, 1, 1)
		self.End =                None

	def __len__(self):
		return 0

	def __str__(self):
		return "<{name}>".format(
				name=self.__class__.__name__
			)

class EndOfToken(Token):
	def __init__(self, previousToken, end):
		previousToken.NextToken =     self
		self._previousToken : Token = previousToken
		self._nextToken =             None
		self.Start =                  None
		self.End =                    end

	def __len__(self):
		return 0

	def __str__(self):
		return "<{name}>".format(
				name=self.__class__.__name__
			)


class StartOfDocumentToken(StartOfToken, StartOfDocument):  pass
class EndOfDocumentToken(EndOfToken, EndOfDocument):        pass
class StartOfSnippetToken(StartOfToken, StartOfSnippet):    pass
class EndOfSnippetToken(EndOfToken, EndOfSnippet):          pass


class CharacterToken(ValuedToken):
	def __init__(self, previousToken, value, start):
		super().__init__(previousToken, value, start=start, end=start)

	def __len__(self):
		return 1

	__CHARACTER_TRANSLATION__ = {
		"\r":    "\\r",
		"\n":    "\\n",
		"\t":    "\\t",
		" ":     "SPACE"
	}

	def __str__(self):
		return "<{name: <50}  {char:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			char="'" + self.__repr__() + "'  ",
			pos=self.Start
		)

	def __repr__(self):
		if (self.Value in self.__CHARACTER_TRANSLATION__):
			return self.__CHARACTER_TRANSLATION__[self.Value]
		else:
			return self.Value


class FusedCharacterToken(CharacterToken):
	def __init__(self, previousToken, value, start, end):
		super().__init__(previousToken, value, start=start)
		self.End = end

	def __len__(self):
		return len(self.Value)

	def __str__(self):
		return "<{name: <50}  {char:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			char="'" + self.__repr__() + "'  ",
			pos=self.Start
		)

	def __repr__(self):
		return self.Value


class SpaceToken(ValuedToken):
	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


class StringToken(ValuedToken):
	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other
	def __le__(self, other):  return self.Value.lower() == other
	def __ge__(self, other):  return self.Value.upper() == other
	def __hash__(self):       return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


class VHDLToken(ValuedToken):   pass
class CommentToken(VHDLToken):
	def __str__(self):
		value = self.Value
		value = value.replace("\n", "\\n")
		value = value.replace("\r", "\\r")
		value = value.replace("\t", "\\t")
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + value + "'  ",
				pos=self.Start
			)


class LiteralToken(VHDLToken):
	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other
	def __hash__(self):       return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value=self.Value + "  ",
			pos=self.Start
		)


class IntegerLiteralToken(LiteralToken):  pass
class RealLiteralToken(LiteralToken):     pass


class CharacterLiteralToken(LiteralToken):
	def __init__(self, previousToken, value, start, end):
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


class StringLiteralToken(LiteralToken):
	def __init__(self, previousToken, value, start, end):
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="\"" + self.Value + "\"  ",
			pos=self.Start
		)

class BitStringLiteralToken(LiteralToken):
	def __init__(self, previousToken, value, start, end):
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
			value="\"" + self.Value + "\"  ",
			pos=self.Start
		)


class ExtendedIdentifier(VHDLToken):
	def __init__(self, previousToken, value, start, end):
		super().__init__(previousToken, value, start=start, end=end)

	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other
	def __hash__(self):       return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + self.Value + "'  ",
				pos=self.Start
			)


class SingleLineCommentToken(CommentToken): pass
class MultiLineCommentToken(CommentToken):  pass
class DirectiveToken(CommentToken):         pass


class LinebreakToken(VHDLToken):
	def __str__(self):
		return "<{name:-<111} at {pos!r}>".format(
				name=self.__class__.__name__ + "  ",
				pos=self.Start
			)


class IndentationToken(SpaceToken):
	def __str__(self):
		value = self.Value
		value = value.replace("\t", "\\t")
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + value + "'  ",
				pos=self.Start
			)
