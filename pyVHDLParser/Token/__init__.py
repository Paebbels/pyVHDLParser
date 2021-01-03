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
from typing import Iterator

from pydecor.decorators       import export

from pyVHDLParser             import SourceCodePosition, StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base        import ParserException

__all__ = []
__api__ = __all__



__CHARACTER_TRANSLATION = {
	"\r": "«\\r»",
	"\n": "«\\n»",
	"\t": "«\\t»",
#	" ":  "« »"
}

@export
def CharacterTranslation(value: str, oneLiner: bool = False) -> str:
	buffer = ""
	charIterator = iter(value)
	try:
		while char := next(charIterator):
			if (char == "\r"):
				nextChar = next(charIterator)
				if (nextChar == "\n"):
					buffer += "«\\r\\n»"
					if not oneLiner:
						buffer += "\n"
				else:
					buffer += "«\\n»"
					if not oneLiner:
						buffer += "\n"

					if (nextChar == "\t"):
						buffer += "«\\n»"
					else:
						buffer += nextChar
			elif (char == "\n"):
				buffer += "«\\n»"
				if not oneLiner:
					buffer += "\n"
			elif (char == "\t"):
				buffer += "«\\t»"
			else:
				buffer += char
	except StopIteration:
		pass

	return buffer


@export
class TokenIterator:
	startToken:         'Token'
	currentToken:       'Token'
	stopToken:          'Token'
	inclusiveStopToken: bool

	state:        int     #: internal states: 0 = normal, 1 = reached stopToken, 2 = reached EndOfToken

	def __init__(self, startToken: 'Token', inclusiveStartToken: bool=False, inclusiveStopToken: bool=True, stopToken: 'Token'=None):
		self.startToken =         startToken
		self.currentToken =       startToken if inclusiveStartToken else startToken.NextToken
		self.stopToken =          stopToken
		self.inclusiveStopToken = inclusiveStopToken

		self.state =              0

	def __iter__(self) -> 'TokenIterator':
		return self

	def __next__(self) -> 'Token':
		# in last call of '__next__', the last token in the sequence was returned
		if (self.state > 0):
			raise StopIteration(self.state)

		token = self.currentToken
		if token is self.stopToken:
			if not self.inclusiveStopToken:
				raise StopIteration(1)
			else:
				self.currentToken = None
				self.state = 1
		elif isinstance(self.currentToken, EndOfToken):
			if not self.inclusiveStopToken:
				raise StopIteration(2)
			else:
				self.currentToken = None
				self.state = 2
		else:
			self.currentToken = token.NextToken
			if (self.currentToken is None):
				raise ParserException("Found open end while iterating token sequence.")  # FIXME: how to append last token?

		return token


@export
class TokenReverseIterator:
	startToken:   'Token'
	currentToken: 'Token'
	stopToken:    'Token'

	state:        int     #: internal states: 0 = normal, 1 = reached stopToken, 2 = reached EndOfToken

	def __init__(self, startToken: 'Token', inclusiveStartToken: bool=False, inclusiveStopToken: bool=True, stopToken: 'Token'=None):
		self.startToken =         startToken
		self.currentToken =       startToken if inclusiveStartToken else startToken.PreviousToken
		self.stopToken =          stopToken
		self.inclusiveStopToken = inclusiveStopToken

		self.state =              0

	def __iter__(self) -> 'TokenReverseIterator':
		return self

	def __next__(self) -> 'Token':
		# in last call of '__next__', the last token in the sequence was returned
		if (self.state > 0):
			raise StopIteration(self.state)

		token = self.currentToken
		if token is self.stopToken:
			self.state = 1
			if not self.inclusiveStopToken:
				raise StopIteration(self.state)
			else:
				self.currentToken = None
		elif isinstance(self.currentToken, EndOfToken):
			self.state = 2
			if not self.inclusiveStopToken:
				raise StopIteration(self.state)
			else:
				self.currentToken = None
		else:
			self.currentToken = token.PreviousToken
			if (self.currentToken is None):
				raise ParserException("Found open end while iterating token sequence.")  # FIXME: how to append last token?

		return token


@export
class Token:
	"""Base-class for all token classes."""

	_previousToken:  'Token'              #: Reference to the previous token
	NextToken:       'Token'             = None #: Reference to the next token
	Start:           SourceCodePosition   #: Position for the token start
	End:             SourceCodePosition   #: Position for the token end

	def __init__(self, previousToken: 'Token', start: SourceCodePosition, end :SourceCodePosition = None):
		"""
		Initializes a token object.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.
		"""

		previousToken.NextToken = self
		self._previousToken =     previousToken
		self.NextToken =          None
		self.Start =              start
		self.End =                end

	def __len__(self) -> int:
		return self.End.Absolute - self.Start.Absolute + 1

	def GetIterator(self, inclusiveStartToken:bool=False, inclusiveStopToken:bool=True, stopToken:'Token'=None) -> Iterator['Token']:
		return TokenIterator(self, inclusiveStartToken=inclusiveStartToken, inclusiveStopToken=inclusiveStopToken, stopToken=stopToken)

	def GetReverseIterator(self, inclusiveStartToken:bool=False, inclusiveStopToken:bool=True, stopToken:'Token'=None) -> Iterator['Token']:
		return TokenReverseIterator(self, inclusiveStartToken=inclusiveStartToken, inclusiveStopToken=inclusiveStopToken, stopToken=stopToken)

	@property
	def PreviousToken(self) -> 'Token':
		return self._previousToken
	@PreviousToken.setter
	def PreviousToken(self, value: 'Token'):
		self._previousToken = value
		value.NextToken =     self

	@property
	def Length(self) -> int:
		return len(self)

	def __str__(self) -> str:
		return "{name} at {pos}".format(
			name=self.__class__.__qualname__,
			pos=str(self.Start)
		)

	def __repr__(self) -> str:
		return self.__str__()


@export
class ValuedToken(Token):
	"""
	Base-class for all *valued* token.

	A ValuedToken contains a :attr:`Value` field for the underlying string from the source code file.
	"""

	Value: str  #: String value of this token.

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition=None):
		"""Initializes a *valued* token object."""

		super().__init__(previousToken, start, end)
		self.Value = value

	def __iter__(self) -> Iterator[str]:
		return iter(self.Value)

	def __eq__(self, other: str) -> bool:
		"""Return true if the internal value is equal to the second operand."""
		return self.Value == other

	def __ne__(self, other: str) -> bool:
		"""Return true if the internal value is unequal to the second operand."""
		return self.Value != other

	def __hash__(self):
		return super().__hash__()

	def __str__(self) -> str:
		return self.Value

	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + CharacterTranslation(self.Value) + "'  ",
				pos=self.Start
			)



@export
class StartOfToken(Token):
	"""Base-class for meta-tokens representing the start of a token stream."""

	def __init__(self):
		"""Initializes a StartOfToken object."""

		self._previousToken = None
		self.NextToken =      None
		self.Start =          SourceCodePosition(1, 1, 1)
		self.End =            None

	def __len__(self) -> int:
		"""Returns always 0."""
		return 0

	def __str__(self) -> str:
		return "<{name}>".format(
				name=self.__class__.__name__
			)


@export
class EndOfToken(Token):
	"""Base-class for meta-tokens representing the end of a token stream."""

	def __init__(self, previousToken: Token, end: SourceCodePosition):
		"""Initializes a EndOfToken object."""
		super().__init__(previousToken, start=end, end=end)

	def __len__(self) -> int:
		"""Returns always 0."""
		return 0

	def __str__(self) -> str:
		return "<{name}>".format(
				name=self.__class__.__name__
			)


@export
class StartOfDocumentToken(StartOfToken, StartOfDocument):
	pass

@export
class EndOfDocumentToken(EndOfToken, EndOfDocument):
	pass

@export
class StartOfSnippetToken(StartOfToken, StartOfSnippet):
	pass

@export
class EndOfSnippetToken(EndOfToken, EndOfSnippet):
	pass


@export
class CharacterToken(ValuedToken):
	"""Token representing a single character."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition):
		"""
		Initializes a CharacterToken object.

		This class is used for single characters, thus: :attr:`Start` = :attr:`End`.
		"""
		super().__init__(previousToken, value, start=start, end=start)

	def __len__(self) -> int:
		return 1

	def __repr__(self) -> str:
		return "<{name: <50}  {char:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			char="'" + CharacterTranslation(self.Value) + "'  ",
			pos=self.Start
		)



@export
class FusedCharacterToken(CharacterToken):
	"""Token representing a double (or triple) character."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""Initializes a FusedCharacterToken object."""
		super().__init__(previousToken, value, start=start)
		self.End = end

	# FIXME: check if base-base class implementation could solve this question.
	def __len__(self) -> int:
		return len(self.Value)

	def __repr__(self) -> str:
		return "<{name: <50}  {char:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			char="'" + self.Value + "'  ",
			pos=self.Start
		)


@export
class SpaceToken(ValuedToken):
	"""Token representing a space (space or tab)."""
	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


@export
class WordToken(ValuedToken):
	"""Token representing a string."""

	def __eq__(self, other: str) -> bool:
		"""Return true if the internal value is equal to the second operand."""
		return self.Value == other

	def __ne__(self, other: str) -> bool:
		"""Return true if the internal value is unequal to the second operand."""
		return self.Value != other

	def __le__(self, other: str) -> bool:
		"""Return true if the internal value is equivalent (lower case, string compare) to the second operand."""
		return self.Value.lower() == other

	def __ge__(self, other: str) -> bool:
		"""Return true if the internal value is equivalent (upper case, string compare) to the second operand."""
		return self.Value.upper() == other

	def __hash__(self):
		return super().__hash__()

	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


@export
class VHDLToken(ValuedToken):
	"""Base-class for all VHDL specific tokens."""

@export
class CommentToken(VHDLToken):
	"""Base-class for comment tokens."""

	def __repr__(self) -> str:
		value = self.Value
		value = value.replace("\n", "\\n")
		value = value.replace("\r", "\\r")
		value = value.replace("\t", "\\t")
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + value + "'  ",
				pos=self.Start
			)


@export
class SingleLineCommentToken(CommentToken):
	"""Token representing a single-line comment."""


@export
class MultiLineCommentToken(CommentToken):
	"""Token representing a multi-line comment."""


@export
class LiteralToken(VHDLToken):
	"""Base-class for all literals in VHDL."""

	def __eq__(self, other: str):  return self.Value == other
	def __ne__(self, other: str):  return self.Value != other
	def __hash__(self):
		return super().__hash__()

	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value=self.Value + "  ",
			pos=self.Start
		)


@export
class IntegerLiteralToken(LiteralToken):
	"""Token representing an integer literal."""

@export
class RealLiteralToken(LiteralToken):
	"""Token representing a real literal."""


@export
class CharacterLiteralToken(LiteralToken):
	"""Token representing a character literal in VHDL."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a CharacterLiteralToken object.

		Single quotes are omitted in the :attr:`Value`.
		"""
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="'" + self.Value + "'  ",
			pos=self.Start
		)


@export
class StringLiteralToken(LiteralToken):
	"""Token representing a string literal in VHDL."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a CharacterLiteralToken object.

		Double quotes are omitted in the :attr:`Value`.
		"""
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
			name=self.__class__.__name__,
			value="\"" + self.Value + "\"  ",
			pos=self.Start
		)


@export
class BitStringLiteralToken(LiteralToken):
	"""Token representing a bit-string literal in VHDL."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a BitStringLiteralToken object.

		Double quotes are omitted in the :attr:`Value`.
		"""
		super().__init__(previousToken, value[1:-1], start=start, end=end)

	def __repr__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
			value="\"" + self.Value + "\"  ",
			pos=self.Start
		)


@export
class ExtendedIdentifier(VHDLToken):
	"""Token representing an extended identifier in VHDL."""


@export
class DirectiveToken(CommentToken):
	pass


@export
class LinebreakToken(VHDLToken):
	"""Token representing a linebreak in the source code file."""

	def __repr__(self) -> str:
		return "<{name:-<111} at {pos!r}>".format(
				name=self.__class__.__name__ + "  ",
				pos=self.Start
			)


@export
class IndentationToken(SpaceToken):
	"""Token representing an indentation in a source code line."""

	def __repr__(self) -> str:
		value = self.Value
		value = value.replace("\t", "\\t")
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + value + "'  ",
				pos=self.Start
			)
