# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from typing                   import Iterator, Optional as Nullable

from pyTooling.Decorators     import export
from pyTooling.MetaClasses    import ExtendedType

from pyVHDLParser             import SourceCodePosition, StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base        import ParserException


@export
def CharacterTranslation(value: str, oneLiner: bool = False) -> str:
	buffer = ""
	charIterator = iter(value)
	try:
		while char := next(charIterator):
			if char == "\r":
				nextChar = next(charIterator)
				if nextChar == "\n":
					buffer += "«\\r\\n»"
					if not oneLiner:
						buffer += "\n"
				else:
					buffer += "«\\n»"
					if not oneLiner:
						buffer += "\n"

					if nextChar == "\t":
						buffer += "«\\n»"
					else:
						buffer += nextChar
			elif char == "\n":
				buffer += "«\\n»"
				if not oneLiner:
					buffer += "\n"
			elif char == "\t":
				buffer += "«\\t»"
			else:
				buffer += char
	except StopIteration:
		pass

	return buffer


@export
class TokenIterator(metaclass=ExtendedType, useSlots=True):
	"""A token iterator to iterate tokens in ascending/forward order."""

	_startToken:          'Token'            #: First token for the iteration.
	_currentToken:        'Token'            #: Next token to return.
	_stopToken:           Nullable['Token']  #: Token to stop iteration at or before.
	_inclusiveStartToken: bool               #: If true, the first returned token is the start token, otherwise one token after.
	_inclusiveStopToken:  bool               #: If true, the last returned token is the stop token, otherwise one token before.

	state:                int                #: Internal states: 0 = normal, 1 = reached stopToken, 2 = reached EndOfToken

	def __init__(self, startToken: 'Token', inclusiveStartToken: bool=False, inclusiveStopToken: bool=True, stopToken: 'Token'=None):
		"""
		Initializes an ascending/forward iterator for a double-linked chain of tokens.

		:param startToken:          First token to start the iteration at or after.
		:param inclusiveStartToken: If true, the first returned token is the start token, otherwise one token after.
		:param inclusiveStopToken:  If true, the last returned token is the stop token, otherwise one token before.
		:param stopToken:           Token to stop iteration at or before.
		"""
		self._startToken =          startToken
		self._currentToken =        startToken if inclusiveStartToken else startToken.NextToken
		self._stopToken =           stopToken
		self._inclusiveStartToken = inclusiveStartToken
		self._inclusiveStopToken =  inclusiveStopToken

		self.state =                0

	def __iter__(self) -> 'TokenIterator':
		"""
		Return itself to fulfil the iterator protocol.

		:returns: Itself.
		"""
		return self

	def __next__(self) -> 'Token':
		"""
		Returns the next token in the token-chain.

		:returns: Next token.
		"""
		# in last call of '__next__', the last token in the sequence was returned
		if self.state > 0:
			raise StopIteration(self.state)

		token = self._currentToken
		if token is self._stopToken:
			if not self._inclusiveStopToken:
				raise StopIteration(1)
			else:
				self._currentToken = None
				self.state = 1
		elif isinstance(self._currentToken, EndOfToken):
			if not self._inclusiveStopToken:
				raise StopIteration(2)
			else:
				self._currentToken = None
				self.state = 2
		else:
			self._currentToken = token.NextToken
			if self._currentToken is None:
				raise ParserException("Found open end while iterating token sequence.")  # FIXME: how to append last token?

		return token

	@property
	def StartToken(self) -> 'Token':
		"""
		A read-only property to return the iterators start token.

		:return: First token of the iterator.
		"""
		return self._startToken

	@property
	def CurrentToken(self) -> 'Token':
		"""
		A read-only property to return the iterators current token.

		:return: Current token of the iterator.
		"""
		return self._currentToken

	@property
	def StopToken(self) -> 'Token':
		"""
		A read-only property to return the iterators stop token.

		:return: Last token of the iterator.
		"""
		return self._stopToken

	def Reset(self) -> None:
		self._currentToken = self._startToken if self._inclusiveStartToken else self._startToken.NextToken


@export
class TokenReverseIterator(metaclass=ExtendedType, useSlots=True):
	"""A token iterator to iterate tokens in descending/backward order."""

	_startToken:          'Token'            #: First token for the iteration.
	_currentToken:        'Token'            #: Next token to return.
	_stopToken:           Nullable['Token']  #: Token to stop iteration at or before.
	_inclusiveStartToken: bool               #: If true, the first returned token is the start token, otherwise one token after.
	_inclusiveStopToken:  bool               #: If true, the last returned token is the stop token, otherwise one token before.

	state:                int                #: Internal states: 0 = normal, 1 = reached stopToken, 2 = reached StartOfToken

	def __init__(self, startToken: 'Token', inclusiveStartToken: bool=False, inclusiveStopToken: bool=True, stopToken: 'Token'=None):
		"""
		Initializes a descending/backward iterator for a double-linked chain of tokens.

		:param startToken:          First token to start the iteration at or after.
		:param inclusiveStartToken: If true, the first returned token is the start token, otherwise one token after.
		:param inclusiveStopToken:  If true, the last returned token is the stop token, otherwise one token before.
		:param stopToken:           Token to stop iteration at or before.
		"""
		self._startToken =          startToken
		self._currentToken =        startToken if inclusiveStartToken else startToken.PreviousToken
		self._stopToken =           stopToken
		self._inclusiveStartToken = inclusiveStartToken
		self._inclusiveStopToken =  inclusiveStopToken

		self.state =                0

	def __iter__(self) -> 'TokenReverseIterator':
		"""
		Return itself to fulfil the iterator protocol.

		:returns: Itself.
		"""
		return self

	def __next__(self) -> 'Token':
		"""
		Returns the previous token in the token-chain.

		:returns: Previous token.
		"""
		# in last call of '__next__', the last token in the sequence was returned
		if self.state > 0:
			raise StopIteration(self.state)

		token = self._currentToken
		if token is self._stopToken:
			self.state = 1
			if not self._inclusiveStopToken:
				raise StopIteration(self.state)
			else:
				self._currentToken = None
		elif isinstance(self._currentToken, EndOfToken):
			self.state = 2
			if not self._inclusiveStopToken:
				raise StopIteration(self.state)
			else:
				self._currentToken = None
		else:
			self._currentToken = token.PreviousToken
			if self._currentToken is None:
				raise ParserException("Found open end while iterating token sequence.")  # FIXME: how to append last token?

		return token

	@property
	def StartToken(self) -> 'Token':
		"""
		A read-only property to return the iterators start token.

		:return: First token of the iterator.
		"""
		return self._startToken

	@property
	def CurrentToken(self) -> 'Token':
		"""
		A read-only property to return the iterators current token.

		:return: Current token of the iterator.
		"""
		return self._currentToken

	@property
	def StopToken(self) -> 'Token':
		"""
		A read-only property to return the iterators stop token.

		:return: Last token of the iterator.
		"""
		return self._stopToken

	def Reset(self) -> None:
		self._currentToken = self._startToken if self._inclusiveStartToken else self._startToken.PreviousToken


@export
class Token(metaclass=ExtendedType, useSlots=True):
	"""Base-class for all token classes."""

	_previousToken:  'Token'              #: Reference to the previous token (backward pointer)
	NextToken:       Nullable['Token']    #: Reference to the next token (forward pointer)
	Start:           SourceCodePosition   #: Position in the file for the token start
	End:             SourceCodePosition   #: Position in the file for the token end

	def __init__(self, previousToken: 'Token', start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a new token object and links it with the previous token.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.

		:param previousToken: The previous token, so the double-linked list can be created.
		:param start:         The source code position for the token's first character.
		:param end:           The source code position for the token's last character.
		"""
		previousToken.NextToken = self
		self._previousToken =     previousToken
		self.NextToken =          None
		self.Start =              start
		self.End =                end

	def __len__(self) -> int:
		"""
		Returns the length of a token in characters.

		:return: Length of the token.
		"""
		return self.End.Absolute - self.Start.Absolute + 1

	def GetIterator(self, inclusiveStartToken: bool = False, inclusiveStopToken: bool = True, stopToken: 'Token' = None) -> Iterator['Token']:
		"""
		Creates an iterator to iterate tokens in ascending/forward order following the :data:`pyVHDLParser.Token.Token.NextToken` references.

		:param inclusiveStartToken: If true, the start token is also returned by the iterator. |br|
		                            By default, it's excluded.
		:param inclusiveStopToken:  If true, the stop token is also returned by the iterator. |br|
		                            By default, it's included.
		:param stopToken:           Optional stop token, where the iterator stops. |br|
		                            By default, it iterates until :class:`pyVHDLParser.Token.EndOfToken` is found.
		:return:                    An :class:`ascending/forward iterator <pyVHDLParser.Token.TokenIterator>` on tokens.
		"""
		return TokenIterator(self, inclusiveStartToken=inclusiveStartToken, inclusiveStopToken=inclusiveStopToken, stopToken=stopToken)

	def GetReverseIterator(self, inclusiveStartToken: bool = False, inclusiveStopToken: bool = True, stopToken: 'Token' = None) -> Iterator['Token']:
		"""
		Creates an iterator to iterate tokens in descending/backward order following the :data:`pyVHDLParser.Token.Token._previousToken` references.

		:param inclusiveStartToken: If true, the start token is also returned by the iterator. |br|
		                            By default, it's excluded.
		:param inclusiveStopToken:  If true, the stop token is also returned by the iterator. |br|
		                            By default, it's included.
		:param stopToken:           Optional stop token, where the iterator stops. |br|
		                            By default, it iterates until :class:`pyVHDLParser.Token.StartOfToken` is found.
		:return:                    A :class:`descending/backward iterator <pyVHDLParser.Token.TokenReverseIterator>` on tokens.
		"""
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
		"""
		A read-only property to return the length of the token.

		:return: Length of the token.
		"""
		return self.__len__()

	def __str__(self) -> str:
		return f"{self.__class__.__qualname__} at {self.Start!s}"

	def __repr__(self) -> str:
		return self.__str__()


@export
class ValuedToken(Token):
	"""
	Base-class for all *valued* token.

	A ValuedToken contains a :attr:`Value` field for the underlying string from the source code file.
	"""

	Value: str  #: String value of the token.

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a new *valued* token object and links it with the previous token.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.

		:param previousToken: The previous token, so the double-linked list can be created.
		:param value:         The string value of the token.
		:param start:         The source code position for the token's first character.
		:param end:           The source code position for the token's last character.
		"""
		super().__init__(previousToken, start, end)
		self.Value = value

	def __iter__(self) -> Iterator[str]:
		"""
		Returns an iterator to iterate the token's internal value.

		:returns: Iterator to iterate the token's string value.
		"""
		return iter(self.Value)

	def __eq__(self, other: str) -> bool:
		"""
		Returns true, if the token's internal value is equal to the second operand.

		:param other:      Parameter to compare against.
		:returns:          ``True``, if token's value and second operand are equal.
		:raises TypeError: If second operand is not of type :py:class:`str`.
		"""
		if isinstance(other, str):
			return self.Value == other
		else:
			raise TypeError(f"Second operand of type '{other.__class__.__name__}' is not supported by equal operator.")

	def __ne__(self, other: str) -> bool:
		"""
		Returns true, if the token's internal value is unequal to the second operand.

		:param other:      Parameter to compare against.
		:returns:          ``True``, if token's value and second operand are unequal.
		:raises TypeError: If second operand is not of type :py:class:`str`.
		"""
		if isinstance(other, str):
			return self.Value != other
		else:
			raise TypeError(f"Second operand of type '{other.__class__.__name__}' is not supported by unequal operator.")

	def __hash__(self):
		return super().__hash__()

	def __str__(self) -> str:
		return self.Value

	def __repr__(self) -> str:
		value = "'" + CharacterTranslation(self.Value) + "'  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


@export
class StartOfToken(Token):
	"""Base-class for meta-tokens representing the start of a token stream."""

	def __init__(self):
		"""
		Initializes the first token object in a chain of tokens.

		As this is the first token in the token-chain, :data:`_previousToken` is set to ``None``, the :data:`Start` is set
		to :pycode:`SourceCodePosition(0, 0, 0)` and :data:`End` is set to :data:`Start`.
		"""
		self._previousToken = None
		self.NextToken =      None
		self.Start =          SourceCodePosition(0, 0, 0)
		self.End =            self.Start

	def __len__(self) -> int:
		"""
		Returns the length of the meta-token. It's always 0.

		:return: Returns always 0.
		"""
		return 0

	def __str__(self) -> str:
		return f"<{self.__class__.__name__}>"


@export
class EndOfToken(Token):
	"""Base-class for meta-tokens representing the end of a token stream."""

	def __init__(self, previousToken: Token, end: SourceCodePosition):
		"""
		Initializes the last token object in a chain of tokens.

		As this is the last token in the token-chain, only the previous token and its end position are needed as parameters.

		:param previousToken: The previous token, so the double-linked list can be created.
		:param end:           The source code position for the token's last character.
		"""
		super().__init__(previousToken, start=end, end=end)

	def __len__(self) -> int:
		"""
		Returns the length of the meta-token. It's always 0.

		:return: Returns always 0.
		"""
		return 0

	def __str__(self) -> str:
		return f"<{self.__class__.__name__}>"


@export
class StartOfDocumentToken(StartOfToken, StartOfDocument):
	"""
	A meta-token, that represents the start of a token-chain if the tokenizer was applied to a whole source code document.
	"""


@export
class EndOfDocumentToken(EndOfToken, EndOfDocument):
	"""
	A meta-token, that represents the end of a token-chain if the tokenizer was applied to a whole source code document.
	"""


@export
class StartOfSnippetToken(StartOfToken, StartOfSnippet):
	"""A meta-token, that represents the start of a token-chain if the tokenizer was applied to a source code snippet."""


@export
class EndOfSnippetToken(EndOfToken, EndOfSnippet):
	"""A meta-token, that represents the end of a token-chain if the tokenizer was applied to a source code snippet."""


@export
class CharacterToken(ValuedToken):
	"""Token representing a single character."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition):
		"""
		Initializes a new *valued* token object and links it with the previous token.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.

		:param previousToken: The previous token, so the double-linked list can be created.
		:param value:         The string value of the token.
		:param start:         The source code position for the token's first character.
		:param end:           The source code position for the token's last character.
		"""

		"""
		Initializes a CharacterToken object.

		This class is used for single characters, thus: :attr:`Start` = :attr:`End`.
		"""
		super().__init__(previousToken, value, start=start, end=start)

	def __len__(self) -> int:
		"""
		Returns the length of a character token. It's always 1.

		:return: Returns always 1.
		"""
		return 1

	def __repr__(self) -> str:
		char = "'" + CharacterTranslation(self.Value) + "'  "
		return f"<{self.__class__.__name__: <50}  {char:.<59} at {self.Start!r}>"


@export
class FusedCharacterToken(CharacterToken):
	"""Token representing a double (or triple) character."""

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a new *valued* token object and links it with the previous token.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.

		:param previousToken: The previous token, so the double-linked list can be created.
		:param value:         The string value of the token.
		:param start:         The source code position for the token's first character.
		:param end:           The source code position for the token's last character.
		"""
		"""Initializes a FusedCharacterToken object."""
		super().__init__(previousToken, value, start=start)
		self.End = end

	# FIXME: check if base-base class implementation could solve this question.
	def __len__(self) -> int:
		"""
		Returns the length of a fused-character token.

		:return: Length of the token.
		"""
		return self.End.Absolute - self.Start.Absolute + 1

	def __repr__(self) -> str:
		char = "'" + self.Value + "'  "
		return f"<{self.__class__.__name__: <50}  {char:.<59} at {self.Start!r}>"


@export
class WhitespaceToken(ValuedToken):
	"""Token representing a whitespace (space or tab)."""

	def __repr__(self) -> str:
		value = "'" + self.Value + "'  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


@export
class WordToken(ValuedToken):
	"""
	First-pass token representing a string.

	In a second pass, this token is replaced by an identifier token or keyword token.
	"""
	_lowerValue: str  #: Pre-converted value to lower case string.

	def __init__(self, previousToken: Token, value: str, start: SourceCodePosition, end: SourceCodePosition):
		"""
		Initializes a new word-token object and links it with the previous token.

		While initialization, the following additional tasks are done:

		* link this token to previous token.
		* link previous token to this token.

		:param previousToken: The previous token, so the double-linked list can be created.
		:param value:         The string value of the token.
		:param start:         The source code position for the token's first character.
		:param end:           The source code position for the token's last character.
		"""
		super().__init__(previousToken, value, start, end)
		self._lowerValue = value.lower()

	def __eq__(self, other: str) -> bool:
		"""
		Returns true, if the token's internal value is equal to the second operand.

		:param other:      Parameter to compare against.
		:returns:          ``True``, if token's value and second operand are equal.
		"""
		return self.Value == other

	def __ne__(self, other: str) -> bool:
		"""
		Returns true, if the token's internal value is unequal to the second operand.

		:param other:      Parameter to compare against.
		:returns:          ``True``, if token's value and second operand are unequal.
		"""
		return self.Value != other

	def __le__(self, other: str) -> bool:
		"""
		Returns true, if the token's internal value is equivalent (lower case, string compare) to the second operand.

		:param other:      Parameter to compare against.
		:returns:          ``True``, if token's lower case value and second operand are equal.
		"""
		return self._lowerValue == other

	# def __ge__(self, other: str) -> bool:
	# 	"""
	# 	Returns true, if the token's internal value is equivalent (upper case, string compare) to the second operand.
	#
	# 	:param other:      Parameter to compare against.
	# 	:returns:          ``True``, if token's upper case value and second operand are equal.
	# 	"""
	# 	return self.Value.upper() == other

	def __repr__(self) -> str:
		value = "'" + self.Value + "'  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


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
		value = "'" + value + "'  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


@export
class SingleLineCommentToken(CommentToken):
	"""Token representing a single-line comment."""


@export
class MultiLineCommentToken(CommentToken):
	"""Token representing a multi-line comment."""


@export
class LiteralToken(VHDLToken):
	"""Base-class for all literals in VHDL."""

	def __repr__(self) -> str:
		value = self.Value + "  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


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
		value = "'" + self.Value + "'  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


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
		value = "\"" + self.Value + "\"  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


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
		value = "\"" + self.Value + "\"  "
		return f"<{self.__class__.__name__: <50}  {value:.<59} at {self.Start!r}>"


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
		return f"<{self.__class__.__name__ + '  ':-<111} at {self.Start!r}>"


@export
class IndentationToken(WhitespaceToken):
	"""Token representing an indentation in a source code line."""

	def __repr__(self) -> str:
		value = self.Value
		value = value.replace("\t", "\\t")
		return f"""<{self.__class__.__name__: <50}  {"'" + value + "'  ":.<59} at {self.Start!r}>"""
