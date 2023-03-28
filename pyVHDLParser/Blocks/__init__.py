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
from types                          import FunctionType
from typing import List, Callable, Iterator, Generator, Tuple, Any

from pyTooling.Decorators           import export
from pyTooling.MetaClasses import ExtendedType
from pyTooling.TerminalUI           import LineTerminal

from pyVHDLParser                   import StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base              import ParserException
from pyVHDLParser.Token             import CharacterToken, Token, SpaceToken, IndentationToken, LinebreakToken, CommentToken, TokenIterator
from pyVHDLParser.Token             import WordToken, EndOfDocumentToken, StartOfDocumentToken
from pyVHDLParser.Token.Keywords    import LibraryKeyword, UseKeyword, ContextKeyword, EntityKeyword, ArchitectureKeyword, PackageKeyword


@export
class BlockParserException(ParserException):
	"""Base-class for exceptions when reading tokens and generating blocks."""

	_token: Token   #: Token that was involved in an exception situation

	def __init__(self, message, token):
		super().__init__(message)
		self._token = token

	@property
	def Token(self) -> Token:
		"""Returns the token involved in an exception situation."""
		return self._token


@export
class TokenToBlockParser(metaclass=ExtendedType, useSlots=True):
	"""Represents the current state of a token-to-block parser."""

	_iterator:     Iterator[Token]
	_stack:        List[Tuple[Callable[['TokenToBlockParser'], None], int]]
	_tokenMarker:  Token

	Token:         Token
	NextState:     Callable[['TokenToBlockParser'], None]
	# ReIssue:       bool
	NewToken:      Token
	NewBlock:      'Block'
	LastBlock:     'Block'
	Counter:       int

	def __init__(self, tokenGenerator: Iterator[Token]):
		"""Initializes the parser state."""

		self._iterator =    iter(tokenGenerator)
		self._stack =       []
		self._tokenMarker = None

		startToken =        next(self._iterator)

		if not isinstance(startToken, StartOfDocumentToken):
			raise BlockParserException("First token is not a StartOfDocumentToken.", startToken)

		startBlock =        StartOfDocumentBlock(startToken)

		self.Token =        startBlock.StartToken
		self.NextState =    StartOfDocumentBlock.stateDocument
		# self.ReIssue =      False
		self.NewToken =     None
		self.NewBlock =     startBlock
		self.LastBlock =    None
		self.Counter =      0

	@property
	def PushState(self) -> Callable[['TokenToBlockParser'], None]:
		return self.NextState

	@PushState.setter
	def PushState(self, value: Callable[['TokenToBlockParser'], None]):
		self._stack.append((
			self.NextState,
			self.Counter
		))
		LineTerminal().WriteDebug("  pushed: " + str(self.NextState))
		self.NextState =    value
		self._tokenMarker =  None

	@property
	def TokenMarker(self) -> Token:
		if (self.NewToken is not None) and (self._tokenMarker is self.Token):
			LineTerminal().WriteDebug("  {DARK_GREEN}@TokenMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._tokenMarker, self.NewToken, **LineTerminal.Foreground))
			self._tokenMarker = self.NewToken
		return self._tokenMarker

	@TokenMarker.setter
	def TokenMarker(self, value: Token):
		self._tokenMarker = value

	def __eq__(self, other: Any) -> bool:
		"""Implement a '==' operator for the current state."""
		return self.NextState is other

	def __ne__(self, other: Any) -> bool:
		"""Implement a '!=' operator for the current state."""
		return self.NextState is not other

	def __str__(self) -> str:
		"""Returns the current state (function name) as str."""
		return f"{self.NextState.__func__.__qualname__}"

	def __repr__(self) -> str:
		"""Returns the current state (full) as str."""
		return "{state}\n  token:   {token}\n  Marker: {marker}\n  NewToken: {newToken}\n  newBlock: {newBlock}".format(
			state=self.NextState.__func__.__qualname__,
			token=self.Token,
			marker=self.TokenMarker,
			newToken=self.NewToken,
			newBlock=self.NewBlock,
		)

	def Pop(self, n: int = 1, tokenMarker: Token = None) -> None:
		for i in range(n):
			top = self._stack.pop()
			LineTerminal().WriteDebug("popped: " + str(top[0]))
		self.NextState, self.Counter = top
		self._tokenMarker = tokenMarker

	def __call__(self) -> Generator['Block', Token, None]:
		from pyVHDLParser.Token             import EndOfDocumentToken
		from pyVHDLParser.Blocks.Common     import LinebreakBlock, EmptyLineBlock

		for token in self._iterator:
			# set parserState.Token to current token
			self.Token = token

			# overwrite an existing token and connect the next token with the new one
			if self.NewToken is not None:
				# print("{MAGENTA}NewToken: {token}{NOCOLOR}".format(token=self.NewToken, **Console.Foreground))
				# update topmost TokenMarker
				if self._tokenMarker is token.PreviousToken:
					# XXX: LineTerminal().WriteDebug("  update token marker: {0!s} -> {1!s}".format(self._tokenMarker, self.NewToken))
					self._tokenMarker = self.NewToken

				token.PreviousToken = self.NewToken
				self.NewToken =       None

			# an empty marker means: fill on next yield run
			if self._tokenMarker is None:
				LineTerminal().WriteDebug("  new token marker: None -> {0!s}".format(token))
				self._tokenMarker = token

			# a new block is assembled
			while self.NewBlock is not None:
				if isinstance(self.NewBlock, LinebreakBlock) and isinstance(self.LastBlock, (LinebreakBlock, EmptyLineBlock)):
					self.LastBlock = EmptyLineBlock(self.LastBlock, self.NewBlock.StartToken)
					self.LastBlock.NextBlock = self.NewBlock.NextBlock
				else:
					self.LastBlock = self.NewBlock

				self.NewBlock = self.NewBlock.NextBlock
				yield self.LastBlock

			# if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			# XXX: LineTerminal().WriteDebug("    {DARK_GRAY}state={state!s: <50}  token={token!s: <40}{NOCOLOR}   ".format(state=self, token=token, **LineTerminal.Foreground))
			# execute a state
			self.NextState(self)

		else:
			if isinstance(self.Token, EndOfDocumentToken) and isinstance(self.NewBlock, EndOfDocumentBlock):
				yield self.NewBlock
			else:
				raise BlockParserException("Unexpected end of document.", self.Token)


@export
class MetaBlock(ExtendedType):
	"""
	A :term:`meta-class` to construct *Block* classes.

	Modifications done by this meta-class:

	* Register all classes of type :class:`Block` or derived variants in a class field :attr:`Block.BLOCKS` in this meta-class.
	* Register all method of name `state....` in the constructed class' attribute :attr:`Block.__STATES__`.
	"""

	BLOCKS: List['Block'] = []     #: List of all classes of type :class:`Block` or derived variants

	def __new__(cls, className, baseClasses, classMembers: dict):
		# """Register all state*** methods in a list called `__STATES__`."""
		states = []
		for memberName, memberObject in classMembers.items():
			if isinstance(memberObject, FunctionType) and (memberName[:5] == "state"):
				states.append(memberObject)

		block = super().__new__(cls, className, baseClasses, classMembers, useSlots=True)
		block.__STATES__ = states

		cls.BLOCKS.append(block)

		return block


@export
class BlockIterator:
	_startBlock:         'Block'
	_currentBlock:       'Block'
	_stopBlock:          'Block'
	_inclusiveStopBlock: bool

	_state:              int     #: internal states: 0 = normal, 1 = reached stopBlock, 2 = reached EndOfBlock

	def __init__(self, startBlock: 'Block', inclusiveStartBlock: bool=False, inclusiveStopBlock: bool=True, stopBlock: 'Block'=None):
		self._startBlock =         startBlock if inclusiveStartBlock else startBlock.NextBlock
		self._currentBlock =       self._startBlock
		self._stopBlock =          stopBlock
		self._inclusiveStopBlock = inclusiveStopBlock

		self._state =              0

	def __iter__(self) -> 'BlockIterator':
		return self

	def __next__(self) -> 'Block':
		# in last call of '__next__', the last block in the sequence was returned
		if self._state > 0:
			raise StopIteration(self._state)

		block = self._currentBlock
		if block is self._stopBlock:
			if not self._inclusiveStopBlock:
				raise StopIteration(1)
			else:
				self._currentBlock = None
				self._state = 1
		elif isinstance(self._currentBlock, EndOfBlock):
			if not self._inclusiveStopBlock:
				raise StopIteration(2)
			else:
				self._currentBlock = None
				self._state = 2
		else:
			self._currentBlock = block.NextBlock
			if self._currentBlock is None:
				raise ParserException("Found open end while iterating block sequence.")  # FIXME: how to append last block?

		return block

	@property
	def StartBlock(self) -> 'Block':
		return self._startBlock

	@property
	def CurrentBlock(self) -> 'Block':
		return self._currentBlock

	@property
	def StopBlock(self) -> 'Block':
		return self._stopBlock

	def Reset(self):
		self._currentBlock = self._startBlock


@export
class BlockReverseIterator:
	startBlock:   'Block'
	currentBlock: 'Block'
	stopBlock:    'Block'

	state:        int     #: internal states: 0 = normal, 1 = reached stopBlock, 2 = reached StartOfBlock

	def __init__(self, startBlock: 'Block', inclusiveStartBlock: bool=False, stopBlock: 'Block'=None):
		self.startBlock =   startBlock
		self.currentBlock = startBlock if inclusiveStartBlock else startBlock.NextBlock
		self.stopBlock =    stopBlock

		self.state =        0

	def __iter__(self) -> 'BlockReverseIterator':
		return self

	def __next__(self) -> 'Block':
		# in last call of '__next__', the last block in the sequence was returned
		if self.state > 0:
			raise StopIteration(self.state)

		block = self.currentBlock
		if block is self.stopToken:
			self.currentBlock = None
			self.state =        1
		elif isinstance(self.currentBlock, EndOfBlock):
			self.currentBlock = None
			self.state =        2
		else:
			self.currentBlock = block.PreviousBlock
			if self.currentBlock is None:
				raise ParserException("Found open end while iterating block sequence.")  # FIXME: how to append last block?

		return block


@export
class Block(metaclass=MetaBlock):
	"""
	Base-class for all :term:`block` classes.
	"""

	__STATES__:      List    #: List of all `state...` methods in this class.

	_previousBlock: 'Block'  #: Reference to the previous block.
	NextBlock:      'Block'  #: Reference to the next block.
	StartToken:     Token    #: Reference to the first token in the scope of this block.
	EndToken:       Token    #: Reference to the last token in the scope of this block.
	MultiPart:      bool     #: True, if this block has multiple parts.

	def __init__(self, previousBlock: 'Block', startToken: Token, endToken: Token = None, multiPart: bool = False):
		"""Base-class constructor for a new block instance."""

		previousBlock.NextBlock =       self
		self._previousBlock = previousBlock
		self.NextBlock =      None
		self.StartToken =     startToken
		self.EndToken =       startToken if (endToken is None) else endToken
		self.MultiPart =      multiPart

	def __len__(self) -> int:
		"""Returns the length of a block in characters from :attr:`~Block.StartToken` to :attr:`~Block.EndToken`."""
		return self.EndToken.End.Absolute - self.StartToken.Start.Absolute + 1

	def __iter__(self) -> TokenIterator:
		"""Returns a token iterator that iterates from :attr:`~Block.StartToken` to :attr:`~Block.EndToken`."""
		return TokenIterator(self.StartToken, inclusiveStartToken=True, stopToken=self.EndToken)

	def GetIterator(self, inclusiveStartBlock: bool = False, inclusiveStopBlock: bool = True, stopBlock: 'Block'=None) -> BlockIterator:
		return BlockIterator(self, inclusiveStartBlock=inclusiveStartBlock, inclusiveStopBlock=inclusiveStopBlock, stopBlock=stopBlock)

	def GetReverseIterator(self, inclusiveStartBlock: bool = False, inclusiveStopBlock: bool = True, stopBlock: 'Block'=None) -> BlockReverseIterator:
		return BlockReverseIterator(self, inclusiveStartBlock=inclusiveStartBlock, inclusiveStopBlock=inclusiveStopBlock, stopBlock=stopBlock)

	def __str__(self) -> str:
		buffer = ""
		for token in self:
			if isinstance(token, CharacterToken):
				buffer += repr(token)
			else:
				try:
					buffer += token.Value
				except AttributeError:
					pass

		return buffer

	def __repr__(self) -> str:
		return "[{blockName: <50s} {stream: <62s} at {start!s} .. {end!s}]".format(
			blockName="{module}.{classname}{multiparted}".format(
				module=self.__module__.rpartition(".")[2],
				classname=self.__class__.__name__,
				multiparted=("*" if self.MultiPart else "")
			),
			stream="'" + self.__str__() + "'",
			start=self.StartToken.Start,
			end=self.EndToken.End
		)

	@property
	def PreviousBlock(self) -> 'Block':
		return self._previousBlock
	@PreviousBlock.setter
	def PreviousBlock(self, value: 'Block'):
		self._previousBlock = value
		value.NextBlock = self

	@property
	def Length(self) -> int:
		"""Returns the length of a block in characters from :attr:`~Block.StartToken` to :attr:`~Block.EndToken`."""
		return len(self)

	@property
	def States(self) -> List[Callable]:
		"""Returns a list of all `state...` methods in this class."""
		return self.__STATES__

	@classmethod
	def stateError(cls, parserState: TokenToBlockParser):
		"""Predefined state to catch error situations."""
		raise BlockParserException("Reached unreachable state!")


@export
class SkipableBlock(Block):
	"""Base-class for blocks that can be skipped in fast-forward scanning."""
	pass

@export
class FinalBlock(Block):
	"""Base-class for blocks that are final in a fast-forward scanning."""
	pass

@export
class CommentBlock(SkipableBlock):
	"""Base-class for all comment blocks."""
	pass


@export
class StartOfBlock(Block):
	"""Base-class for a first block in a sequence of double-linked blocks."""

	def __init__(self, startToken):
		self._previousBlock =     None
		self.NextBlock =          None
		self.StartToken =         startToken
		self.EndToken =           None
		self.MultiPart =          False

	# TODO: needs review: should TokenIterator be used?
	def __iter__(self):
		yield self.StartToken

	def __len__(self) -> int:
		return 0

	def __repr__(self) -> str:
		return "[{name}]".format(
			name=self.__class__.__name__
		)


@export
class EndOfBlock(Block):
	"""Base-class for a last block in a sequence of double-linked blocks."""

	def __init__(self, previousBlock, endToken):
		super().__init__(previousBlock, endToken)

	# TODO: needs review: should TokenIterator be used?
	def __iter__(self) -> Iterator[Token]:
		yield self.StartToken

	def __len__(self) -> int:
		return 0

	def __repr__(self) -> str:
		return "[{name}]".format(
			name=self.__class__.__name__
		)


@export
class StartOfDocumentBlock(StartOfBlock, StartOfDocument):
	"""First block in a sequence of double-linked blocks."""

	KEYWORDS = None

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Common     import IndentationBlock, WhitespaceBlock, LinebreakBlock
		from pyVHDLParser.Blocks.Reference  import Library, Use, Context
		from pyVHDLParser.Blocks.Sequential import Package
		from pyVHDLParser.Blocks.Structural import Entity, Architecture

		cls.KEYWORDS = {
			# Keyword             Transition
			LibraryKeyword:       Library.StartBlock.stateLibraryKeyword,
			UseKeyword:           Use.StartBlock.stateUseKeyword,
			ContextKeyword:       Context.NameBlock.stateContextKeyword,
			EntityKeyword:        Entity.NameBlock.stateEntityKeyword,
			ArchitectureKeyword:  Architecture.NameBlock.stateArchitectureKeyword,
			PackageKeyword:       Package.NameBlock.statePackageKeyword
		}

	@classmethod
	def stateDocument(cls, parserState: TokenToBlockParser):
		from pyVHDLParser.Blocks.Common     import IndentationBlock, WhitespaceBlock, LinebreakBlock

		token = parserState.Token
		if isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, WordToken):
			tokenValue = token.Value.lower()

			for keyword in cls.KEYWORDS:
				if tokenValue == keyword.__KEYWORD__:
					newToken =                keyword(fromExistingToken=token)
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock = EndOfDocumentBlock(parserState.LastBlock, token)
			return

		raise BlockParserException(
			"Expected one of these keywords: {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


@export
class EndOfDocumentBlock(EndOfBlock, EndOfDocument):
	"""Last block in a sequence of double-linked blocks."""
	pass

@export
class StartOfSnippetBlock(StartOfBlock, StartOfSnippet):
	pass

@export
class EndOfSnippetBlock(EndOfBlock, EndOfSnippet):
	pass
