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
from pyVHDLParser.Decorators  import Export
from pyVHDLParser             import SourceCodePosition, StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet

__all__ = []
__api__ = __all__


@Export
class Token:
	"""Base-class for all token classes."""

	_previousToken :  'Token' =             None    #: Reference to the previous token
	_NextToken :      'Token' =             None    #: Reference to the next token
	Start :           SourceCodePosition =  None    #: Position for the token start
	End :             SourceCodePosition =  None    #: Position for the token end

	def __init__(self, previousToken : 'Token', start : SourceCodePosition, end :SourceCodePosition = None):
		"""
		Initializes a token object.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.
		"""

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


@Export
class ValuedToken(Token):
	"""
	Base-class for all *valued* token.

	A ValuedToken contains a :attr:`Value` field for the underlying string from the source code file.
	"""

	Value : str = None  #: String value of this token.

	def __init__(self, previousToken, value, start, end=None):
		"""Initializes a *valued* token object."""

		super().__init__(previousToken, start, end)
		self.Value : str =  value

	def __eq__(self, other : str):
		"""Return true if the internal value is equal to the second operand."""
		return self.Value == other

	def __ne__(self, other : str):
		"""Return true if the internal value is unequal to the second operand."""
		return self.Value != other

	def __hash__(self):
		return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + self.Value + "'  ",
				pos=self.Start
			)


@Export
class StartOfToken(Token):
	"""Base-class for meta-tokens representing the start of a token stream."""

	def __init__(self):
		"""Initializes a StartOfToken object."""

		self._previousToken =     None
		self._nextToken =         None
		self.Start =              SourceCodePosition(1, 1, 1)
		self.End =                None

	def __len__(self):
		"""Returns always 0."""
		return 0

	def __str__(self):
		return "<{name}>".format(
				name=self.__class__.__name__
			)


@Export
class EndOfToken(Token):
	"""Base-class for meta-tokens representing the end of a token stream."""

	def __init__(self, previousToken, end):
		"""Initializes a EndOfToken object."""

		previousToken.NextToken =     self
		self._previousToken : Token = previousToken
		self._nextToken =             None
		self.Start =                  None
		self.End =                    end

	def __len__(self):
		"""Returns always 0."""
		return 0

	def __str__(self):
		return "<{name}>".format(
				name=self.__class__.__name__
			)


@Export
class StartOfDocumentToken(StartOfToken, StartOfDocument):
	pass

@Export
class EndOfDocumentToken(EndOfToken, EndOfDocument):
	pass

@Export
class StartOfSnippetToken(StartOfToken, StartOfSnippet):
	pass

@Export
class EndOfSnippetToken(EndOfToken, EndOfSnippet):
	pass


@Export
class CharacterToken(ValuedToken):
	"""Token representing a single character."""

	def __init__(self, previousToken, value, start):
		"""
		Initializes a CharacterToken object.

		This class is used for single characters, thus: :attr:`Start` = :attr:`End`.
		"""
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


@Export
class FusedCharacterToken(CharacterToken):
	"""Token representing a double (or triple) character."""

	def __init__(self, previousToken, value, start, end):
		"""Initializes a FusedCharacterToken object."""
		super().__init__(previousToken, value, start=start)
		self.End = end

	# FIXME: check if base-base class implementation could solve this question.
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


@Export
class SpaceToken(ValuedToken):
	"""Token representing a space (space or tab)."""
	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


@Export
class WordToken(ValuedToken):
	"""Token representing a string."""

	def __eq__(self, other : str):  return self.Value == other
	def __ne__(self, other : str):  return self.Value != other
	def __le__(self, other : str):  return self.Value.lower() == other
	def __ge__(self, other : str):  return self.Value.upper() == other
	def __hash__(self):       return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


@Export
class VHDLToken(ValuedToken):
	"""Base-class for all VHDL specific tokens."""

@Export
class CommentToken(VHDLToken):
	"""Base-class for comment tokens."""

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


@Export
class SingleLineCommentToken(CommentToken):
	"""Token representing a single-line comment."""


@Export
class MultiLineCommentToken(CommentToken):
	"""Token representing a multi-line comment."""


@Export
class LiteralToken(VHDLToken):
	"""base-class for all literals in VHDL."""

	def __eq__(self, other):  return self.Value == other
	def __ne__(self, other):  return self.Value != other
	def __hash__(self):       return super().__hash__()

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value=self.Value + "  ",
			pos=self.Start
		)


@Export
class IntegerLiteralToken(LiteralToken):
	"""Token representing an integer literal."""

@Export
class RealLiteralToken(LiteralToken):
	"""Token representing a real literal."""


@Export
class CharacterLiteralToken(LiteralToken):
	"""Token representing a character literal in VHDL."""

	def __init__(self, previousToken, value, start, end):
		"""
		Initializes a CharacterLiteralToken object.

		Single quotes are omitted in the :attr:`Value`.
		"""
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


@Export
class StringLiteralToken(LiteralToken):
	"""Token representing a string literal in VHDL."""

	def __init__(self, previousToken, value, start, end):
		"""
		Initializes a CharacterLiteralToken object.

		Double quotes are omitted in the :attr:`Value`.
		"""
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="\"" + self.Value + "\"  ",
			pos=self.Start
		)


@Export
class BitStringLiteralToken(LiteralToken):
	"""Token representing a bit-string literal in VHDL."""

	def __init__(self, previousToken, value, start, end):
		"""
		Initializes a BitStringLiteralToken object.

		Double quotes are omitted in the :attr:`Value`.
		"""
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
			value="\"" + self.Value + "\"  ",
			pos=self.Start
		)


@Export
class ExtendedIdentifier(VHDLToken):
	"""Token representing an extended identifier in VHDL."""


@Export
class DirectiveToken(CommentToken):
	pass


@Export
class LinebreakToken(VHDLToken):
	"""Token representing a linebreak in the source code file."""

	def __str__(self):
		return "<{name:-<111} at {pos!r}>".format(
				name=self.__class__.__name__ + "  ",
				pos=self.Start
			)


@Export
class IndentationToken(SpaceToken):
	"""Token representing an indentation in a source code line."""

	def __str__(self):
		value = self.Value
		value = value.replace("\t", "\\t")
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + value + "'  ",
				pos=self.Start
			)
