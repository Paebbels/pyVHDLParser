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
from types                          import FunctionType
from typing                         import List, Callable, Iterator, Generator

from pydecor.decorators             import export
from pyTerminalUI                   import LineTerminal

from pyVHDLParser                   import StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base              import ParserException
from pyVHDLParser.Token             import CharacterToken, Token, SpaceToken, IndentationToken, LinebreakToken, CommentToken, TokenIterator
from pyVHDLParser.Token             import WordToken, EndOfDocumentToken, StartOfDocumentToken
from pyVHDLParser.Token.Keywords    import LibraryKeyword, UseKeyword, ContextKeyword, EntityKeyword, ArchitectureKeyword, PackageKeyword

__all__ = []
__api__ = __all__


@export
class BlockParserException(ParserException):
	"""Base-class for exceptions when reading tokens and generating blocks."""

	_token: Token = None   #: Token that was involved in an exception situation

	def __init__(self, message, token):
		super().__init__(message)
		self._token = token

	@property
	def Token(self) -> Token:
		"""Returns the token involved in an exception situation."""
		return self._token


@export
class TokenToBlockParser:
	"""Wrapping class to offer some class methods."""

	@staticmethod
	def Transform(tokenGenerator: Iterator[Token]) -> Generator['Block', Token, None]:
		"""Returns a generator, that reads from a token generator and emits a chain of blocks."""

		state = ParserState(tokenGenerator)
		return state.GetGenerator()


@export
class ParserState:
	"""Represents the current state of a token-to-block parser."""

	_iterator:     Iterator[Token]
	_stack:        List[Callable]
	_tokenMarker:  Token

	Token:         Token
	NextState:     Callable
	ReIssue:       bool
	NewToken:      Token
	NewBlock:      'Block'
	LastBlock:     'Block'
	Counter:       int

	def __init__(self, tokenGenerator):
		"""Initializes the parser state."""

		self._iterator =    iter(tokenGenerator)
		self._stack =       []
		self._tokenMarker = None

		startToken =        next(self._iterator)
		startBlock =        StartOfDocumentBlock(startToken)

		if (not isinstance(startToken, StartOfDocumentToken)):
			raise BlockParserException("First token is not a StartOfDocumentToken.", startToken)

		self.Token =        startBlock.StartToken
		self.NextState =    StartOfDocumentBlock.stateDocument
		self.ReIssue =      False
		self.NewToken =     None
		self.NewBlock =     startBlock
		self.LastBlock =    None
		self.Counter =      0


	@property
	def PushState(self) -> Callable:
		return self.NextState
	@PushState.setter
	def PushState(self, value):
		self._stack.append((
			self.NextState,
			self.Counter
		))
		LineTerminal().WriteDebug("  pushed: " + str(self.NextState))
		self.NextState =    value
		self._tokenMarker =  None

	@property
	def TokenMarker(self) -> Token:
		if ((self.NewToken is not None) and (self._tokenMarker is self.Token)):
			LineTerminal().WriteDebug("  {DARK_GREEN}@TokenMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._tokenMarker, self.NewToken, **LineTerminal.Foreground))
			self._tokenMarker = self.NewToken
		return self._tokenMarker
	@TokenMarker.setter
	def TokenMarker(self, value):
		self._tokenMarker = value

	def __eq__(self, other) -> bool:
		"""Implement a '==' operator for the current state."""
		return self.NextState is other

	def __str__(self) -> str:
		"""Returns the current state (function name) as str."""
		return "{state}".format(state=self.NextState.__func__.__qualname__)

	def __repr__(self) -> str:
		"""Returns the current state (full) as str."""
		return "{state}\n  token:   {token}\n  Marker: {marker}\n  NewToken: {newToken}\n  newBlock: {newBlock}".format(
			state=self.NextState.__func__.__qualname__,
			token=self.Token,
			marker=self.TokenMarker,
			newToken=self.NewToken,
			newBlock=self.NewBlock,
		)

	def Pop(self, n=1, tokenMarker=None):
		top = None
		for i in range(n):
			top = self._stack.pop()
			LineTerminal().WriteDebug("popped: " + str(top[0]))
		self.NextState =    top[0]
		self.Counter =      top[1]
		self._tokenMarker = tokenMarker


	def GetGenerator(self) -> Generator['Block', Token, None]:
		from pyVHDLParser.Token             import EndOfDocumentToken
		from pyVHDLParser.Blocks            import BlockParserException, EndOfDocumentBlock
		from pyVHDLParser.Blocks.Common     import LinebreakBlock, EmptyLineBlock

		for token in self._iterator:
			# set parserState.Token to current token
			self.Token = token

			# overwrite an existing token and connect the next token with the new one
			if (self.NewToken is not None):
				# print("{MAGENTA}NewToken: {token}{NOCOLOR}".format(token=self.NewToken, **Console.Foreground))
				# update topmost TokenMarker
				if (self._tokenMarker is token.PreviousToken):
					# XXX: LineTerminal().WriteDebug("  update token marker: {0!s} -> {1!s}".format(self._tokenMarker, self.NewToken))
					self._tokenMarker = self.NewToken

				token.PreviousToken = self.NewToken
				self.NewToken =       None

			# an empty marker means: fill on next yield run
			if (self._tokenMarker is None):
				LineTerminal().WriteDebug("  new token marker: None -> {0!s}".format(token))
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

			# if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			# XXX: LineTerminal().WriteDebug("    {DARK_GRAY}state={state!s: <50}  token={token!s: <40}{NOCOLOR}   ".format(state=self, token=token, **LineTerminal.Foreground))
			# execute a state
			self.NextState(self)

		else:
			if (isinstance(self.Token, EndOfDocumentToken) and isinstance(self.NewBlock, EndOfDocumentBlock)):
				yield self.NewBlock
			else:
				raise BlockParserException("Unexpected end of document.", self.Token)


@export
class MetaBlock(type):
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
			if (isinstance(memberObject, FunctionType) and (memberName[:5] == "state")):
				states.append(memberObject)

		classMembers['__STATES__'] = states

		block = super().__new__(cls, className, baseClasses, classMembers)
		cls.BLOCKS.append(block)
		return block


@export
class BlockIterator:
	startBlock:   'Block'
	currentBlock: 'Block'
	stopBlock:    'Block'

	state:        int     #: internal states: 0 = normal, 1 = reached stopBlock, 2 = reached EndOfBlock

	def __init__(self, startBlock: 'Block', inclusiveStartBlock: bool=False, stopBlock: 'Block'=None):
		self.startBlock =   startBlock
		self.currentBlock = startBlock if inclusiveStartBlock else startBlock.NextBlock
		self.stopBlock =    stopBlock

		self.state =        0

	def __iter__(self) -> 'BlockIterator':
		return self

	def __next__(self) -> 'Block':
		# in last call of '__next__', the last block in the sequence was returned
		if (self.state > 0):
			raise StopIteration(self.state)

		block = self.currentBlock
		if block is self.stopToken:
			self.currentBlock = None
			self.state =        1
		elif isinstance(self.currentBlock, EndOfBlock):
			self.currentBlock = None
			self.state =        2
		else:
			self.currentBlock = block.NextBlock
			if (self.currentBlock is None):
				raise ParserException("Found open end while iterating block sequence.")  # FIXME: how to append last block?

		return block


@export
class BlockReverseIterator:
	startBlock:   'Block'
	currentBlock: 'Block'
	stopBlock:    'Block'

	state:        int     #: internal states: 0 = normal, 1 = reached stopBlock, 2 = reached EndOfBlock

	def __init__(self, startBlock: 'Block', inclusiveStartBlock: bool=False, stopBlock: 'Block'=None):
		self.startBlock =   startBlock
		self.currentBlock = startBlock if inclusiveStartBlock else startBlock.NextBlock
		self.stopBlock =    stopBlock

		self.state =        0

	def __iter__(self) -> 'BlockReverseIterator':
		return self

	def __next__(self) -> 'Block':
		# in last call of '__next__', the last block in the sequence was returned
		if (self.state > 0):
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
			if (self.currentBlock is None):
				raise ParserException("Found open end while iterating block sequence.")  # FIXME: how to append last block?

		return block


@export
class Block(metaclass=MetaBlock):
	"""
	Base-class for all :term:`block` classes.
	"""

	__STATES__:      List =   None   #: List of all `state...` methods in this class.

	_previousBlock: 'Block' = None   #: Reference to the previous block.
	NextBlock:      'Block' = None   #: Reference to the next block.
	StartToken:     Token =   None   #: Reference to the first token in the scope of this block.
	EndToken:       Token =   None   #: Reference to the last token in the scope of this block.
	MultiPart:      bool =    None   #: True, if this block has multiple parts.

	def __init__(self, previousBlock, startToken, endToken=None, multiPart=False):
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

	def GetIterator(self, stopBlock: 'Block'=None) -> BlockIterator:
		return BlockIterator(self, stopBlock=stopBlock)

	def GetReverseIterator(self, stopBlock: 'Block'=None) -> BlockReverseIterator:
		return BlockReverseIterator(self, stopBlock=stopBlock)

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
	def stateError(cls, parserState: ParserState):
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

	def __init__(self, endToken):
		self._previousBlock =     None
		self.NextBlock =          None
		self.StartToken =         None
		self.EndToken =           endToken
		self.MultiPart =          False

	# TODO: needs review: should TokenIterator be used?
	def __iter__(self):
		yield self.EndToken

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
	def stateDocument(cls, parserState: ParserState):
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
				if (tokenValue == keyword.__KEYWORD__):
					newToken =                keyword(token)
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock =    EndOfDocumentBlock(token)
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
