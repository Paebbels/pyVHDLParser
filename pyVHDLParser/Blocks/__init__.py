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
from typing                         import List, Callable, Iterator, Generator, Tuple, Any, Optional, Dict, Type

from pyTooling.Decorators           import export
from pyTooling.MetaClasses          import ExtendedType
from pyTooling.TerminalUI           import LineTerminal

from pyVHDLParser                   import StartOfDocument, EndOfDocument, StartOfSnippet, EndOfSnippet
from pyVHDLParser.Base              import ParserException
from pyVHDLParser.Token             import CharacterToken, Token, WhitespaceToken, IndentationToken, LinebreakToken, CommentToken, TokenIterator
from pyVHDLParser.Token             import WordToken, EndOfDocumentToken, StartOfDocumentToken, ValuedToken
from pyVHDLParser.Token.Keywords    import LibraryKeyword, UseKeyword, ContextKeyword, EntityKeyword, ArchitectureKeyword, PackageKeyword, BoundaryToken, KeywordToken


BLOCK_PARSER_STATE = Callable[["TokenToBlockParser"], None]

@export
class BlockParserException(ParserException):
	"""Base-class for exceptions when reading tokens and generating blocks."""

	_token: Optional[Token]   #: Token that was involved in an exception situation

	def __init__(self, message: str, token: Optional[Token]):
		super().__init__(message)
		self._token = token

	@property
	def Token(self) -> Optional[Token]:
		"""Returns the token involved in an exception situation."""
		return self._token


@export
class TokenToBlockParser(metaclass=ExtendedType, slots=True):
	"""Represents the current state of a token-to-block parser."""

	_iterator:              Iterator['Token']
	_stack:                 List[Tuple[BLOCK_PARSER_STATE, int, int]]
	_tokenMarker:           Optional['Token']
	_disableDocumentChecks: bool
	_lastBlock:             Optional['Block']

	Token:                  'Token'
	NextState:              BLOCK_PARSER_STATE
	# ReIssue:                bool
	NewToken:               Optional['Token']
	NewBlock:               Optional['Block']
	Counter:                int
	TokenCounter:           int

	def __init__(self, tokenGenerator: Iterator['Token'], disableDocumentChecks: bool = False):
		"""Initializes the parser state."""

		self._iterator =              iter(tokenGenerator)
		self._stack =                 []
		self._tokenMarker =           None
		self._disableDocumentChecks = disableDocumentChecks
		self._lastBlock =             None

		startToken =        next(self._iterator)

		if not self._disableDocumentChecks and not isinstance(startToken, StartOfDocumentToken):
			raise BlockParserException("First token is not a StartOfDocumentToken.", startToken)

		startBlock =        StartOfDocumentBlock(startToken)

		self.Token =        startBlock.StartToken
		self.NextState =    StartOfDocumentBlock.stateDocument
		# self.ReIssue =      False
		self.NewToken =     None
		self.NewBlock =     startBlock
		self.Counter =      0
		self.TokenCounter = 0

	@property
	def PushState(self) -> BLOCK_PARSER_STATE:
		return self.NextState

	@PushState.setter
	def PushState(self, value: BLOCK_PARSER_STATE):
		self._stack.append((
			self.NextState,
			self.Counter,
			self.TokenCounter,
		))
		LineTerminal().WriteDebug("  pushed: " + str(self.NextState))
		self.NextState =    value
		self._tokenMarker =  None

	@property
	def TokenMarker(self) -> 'Token':
		if (self.NewToken is not None) and (self._tokenMarker is self.Token):
			LineTerminal().WriteDebug("  {DARK_GREEN}@TokenMarker: {0!s} => {GREEN}{1!s}{NOCOLOR}".format(self._tokenMarker, self.NewToken, **LineTerminal.Foreground)) # type: ignore
			self._tokenMarker = self.NewToken
		assert self._tokenMarker is not None
		return self._tokenMarker

	@TokenMarker.setter
	def TokenMarker(self, value: Optional['Token']):
		self._tokenMarker = value

	@property
	def LastBlock(self) -> 'Block':
		assert self._lastBlock is not None
		return self._lastBlock

	@LastBlock.setter
	def LastBlock(self, value: 'Block'):
		self._lastBlock = value

	def __eq__(self, other: Any) -> bool:
		"""Implement a '==' operator for the current state."""
		return self.NextState is other

	def __ne__(self, other: Any) -> bool:
		"""Implement a '!=' operator for the current state."""
		return self.NextState is not other

	def __str__(self) -> str:
		"""Returns the current state (function name) as str."""
		return f"{self.NextState.__qualname__}"

	def __repr__(self) -> str:
		"""Returns the current state (full) as str."""
		return "{state}\n  token:   {token}\n  Marker: {marker}\n  NewToken: {newToken}\n  newBlock: {newBlock}".format(
			state=self.NextState.__qualname__,
			token=self.Token,
			marker=self.TokenMarker,
			newToken=self.NewToken,
			newBlock=self.NewBlock,
		)

	def Pop(self, n: int = 1, tokenMarker: Optional['Token'] = None) -> None:
		top: Optional[Tuple[BLOCK_PARSER_STATE, int, int]] = None
		for _ in range(n):
			top = self._stack.pop()
			LineTerminal().WriteDebug("popped: " + str(top[0]))
		assert top is not None
		self.NextState, self.Counter, self.TokenCounter = top
		self._tokenMarker = tokenMarker


	def HandleNonCodeTokens(self, currentBlock: Optional[Type["Block"]], multiPart: bool = True) -> bool:
		from pyVHDLParser.Blocks.Whitespace import LinebreakBlock, IndentationBlock, WhitespaceBlock
		token = self.Token

		if isinstance(token, CommentToken):
			# Create a multipart instance of the current block if there are dangling tokens
			if self.TokenCounter > 0 and currentBlock is not None:
				self.NewBlock = currentBlock(self.LastBlock, self.TokenMarker, endToken=token.PreviousToken, multiPart=multiPart)
				_ =             CommentBlock(self.NewBlock, token)
			else:
				self.NewBlock = CommentBlock(self.LastBlock, token)
			self.TokenMarker = None
			return True


		if isinstance(token, LinebreakToken):
			# Create a multipart instance of the current block if there are dangling tokens
			if self.TokenCounter > 0 and currentBlock is not None:
				self.NewBlock = currentBlock(self.LastBlock, self.TokenMarker, endToken=token.PreviousToken, multiPart=multiPart)
				_ =             LinebreakBlock(self.NewBlock, token)
			else:
				self.NewBlock = LinebreakBlock(self.LastBlock, token)
			self.TokenMarker = None
			return True


		if isinstance(token, IndentationToken):
			# Create a multipart instance of the current block if there are dangling tokens
			if self.TokenCounter > 0 and currentBlock is not None:
				self.NewBlock = currentBlock(self.LastBlock, self.TokenMarker, endToken=token.PreviousToken, multiPart=multiPart)
				_ =             IndentationBlock(self.NewBlock, token)
			else:
				self.NewBlock = IndentationBlock(self.LastBlock, token)
			self.TokenMarker = None
			return True


		if isinstance(token, WhitespaceToken):
			self.NewToken =    BoundaryToken(fromExistingToken=token)
			# Create a multipart instance of the current block if there are dangling tokens
			if self.TokenCounter > 0 and currentBlock is not None:
				self.NewBlock = currentBlock(self.LastBlock, self.TokenMarker, endToken=self.NewToken.PreviousToken, multiPart=multiPart)
				_ =             WhitespaceBlock(self.NewBlock, self.NewToken)
			else:
				self.NewBlock = WhitespaceBlock(self.LastBlock, self.NewToken)
			self.TokenMarker = None
			return True

		return False


	def ReparseFromTokenMarker(self, startState: BLOCK_PARSER_STATE) -> None:
		# The start token is mandatory.
		# Note that `parserState.TokenMarker.PreviousToken` is NOT updated, so the original linking is not broken.
		startToken = StartOfDocumentToken()
		startToken.NextToken = self._tokenMarker

		# Create a new parser with the tokens gathered since the last block was created
		iterator = TokenIterator(startToken, stopToken=self.Token, inclusiveStartToken=True, inclusiveStopToken=True)
		newParser = TokenToBlockParser(iterator, disableDocumentChecks=True)
		# Do not create the StartOfDocumentBlock and forward some settings from the original parser
		newParser.NewBlock = None
		newParser.LastBlock = self.LastBlock
		newParser.NextState = self.NextState
		newParser.PushState = startState

		# Parse all previously unhandled tokens
		allBlocks = list(newParser())

		# Take the results and apply them to the original parser.
		# The caller has to return, before adding new tokens/blocks!
		self.NewBlock =     allBlocks[0] if len(allBlocks) > 0 else None
		self.NewToken =     newParser.NewToken
		self.NextState =    newParser.NextState
		self.TokenMarker =  newParser._tokenMarker
		self.TokenCounter = newParser.TokenCounter


	def _ApplyNewToken(self) -> None:
		if self.NewToken is None:
			return

		if self._tokenMarker is self.Token.PreviousToken:
			self._tokenMarker = self.NewToken

		self.Token.PreviousToken = self.NewToken
		self.NewToken = None


	def _ApplyNewBlock(self) -> Generator['Block', None, None]:
		from pyVHDLParser.Blocks.Whitespace     import LinebreakBlock, EmptyLineBlock

		# a new block is assembled
		while self.NewBlock is not None:
			if isinstance(self.NewBlock, LinebreakBlock) and isinstance(self.LastBlock, (LinebreakBlock, EmptyLineBlock)):
				self.LastBlock = EmptyLineBlock(self.LastBlock, self.NewBlock.StartToken)
				self.LastBlock.NextBlock = self.NewBlock.NextBlock
			else:
				self.LastBlock = self.NewBlock

			self.NewBlock = self.NewBlock.NextBlock
			self.TokenCounter = 0
			yield self.LastBlock


	def __call__(self) -> Generator['Block', 'Token', None]:
		from pyVHDLParser.Token             import EndOfDocumentToken

		for token in self._iterator:
			# set parserState.Token to current token
			self.Token = token

			# overwrite an existing token and connect the next token with the new one
			self._ApplyNewToken()

			# count the number of tokens in a block
			self.TokenCounter += 1

			# an empty marker means: fill on next yield run
			if self._tokenMarker is None:
				LineTerminal().WriteDebug("  new token marker: None -> {0!s}".format(token))
				self._tokenMarker = token

			# a new block is assembled
			yield from self._ApplyNewBlock()

			# if self.debug: print("{MAGENTA}------ iteration end ------{NOCOLOR}".format(**Console.Foreground))
			# XXX: LineTerminal().WriteDebug("    {DARK_GRAY}state={state!s: <50}  token={token!s: <40}{NOCOLOR}   ".format(state=self, token=token, **LineTerminal.Foreground))
			# execute a state
			self.NextState(self)


		yield from self._ApplyNewBlock()

		if not self._disableDocumentChecks and not (isinstance(self.Token, EndOfDocumentToken) and isinstance(self.LastBlock, EndOfDocumentBlock)):
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

	def __new__(cls, className: str, baseClasses: Tuple[type], classMembers: Dict[str, Any]):
		# """Register all state*** methods in a list called `__STATES__`."""
		states: List[FunctionType] = []
		for memberName, memberObject in classMembers.items():
			if isinstance(memberObject, FunctionType) and (memberName[:5] == "state"):
				states.append(memberObject)

		block = super().__new__(cls, className, baseClasses, classMembers, slots=True)
		block.__STATES__ = states # type: ignore

		cls.BLOCKS.append(block) # type: ignore

		return block


@export
class BlockIterator:
	_startBlock:         'Block'
	_currentBlock:       'Block'
	_stopBlock:          Optional['Block']
	_inclusiveStopBlock: bool

	_state:              int     #: internal states: 0 = normal, 1 = reached stopBlock, 2 = reached EndOfBlock

	def __init__(self, startBlock: 'Block', inclusiveStartBlock: bool=False, inclusiveStopBlock: bool=True, stopBlock: Optional['Block']=None):
		self._startBlock =         startBlock
		if inclusiveStartBlock:
			self._currentBlock =    self._startBlock
		else:
			assert self._startBlock.NextBlock is not None
			self._currentBlock =    self._startBlock.NextBlock
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
				self._state = 1
		elif isinstance(self._currentBlock, EndOfBlock):
			if not self._inclusiveStopBlock:
				raise StopIteration(2)
			else:
				self._state = 2
		else:
			if block.NextBlock is None:
				raise ParserException("Found open end while iterating block sequence.")  # FIXME: how to append last block?
			self._currentBlock = block.NextBlock

		return block

	@property
	def StartBlock(self) -> 'Block':
		return self._startBlock

	@property
	def CurrentBlock(self) -> 'Block':
		return self._currentBlock

	@property
	def StopBlock(self) -> Optional['Block']:
		return self._stopBlock

	def Reset(self):
		self._currentBlock = self._startBlock


@export
class BlockReverseIterator:
	_startBlock:          'Block'
	_currentBlock:        'Block'
	_stopBlock:           Optional['Block']
	_inclusiveStopBlock:  bool

	_state:               int     #: internal states: 0 = normal, 1 = reached stopBlock, 2 = reached StartOfBlock

	def __init__(self, startBlock: 'Block', inclusiveStartBlock: bool=False, inclusiveStopBlock: bool=False, stopBlock: Optional['Block']=None):
		self.startBlock =        startBlock
		if inclusiveStartBlock:
			self._currentBlock =  self._startBlock
		else:
			assert self._startBlock.PreviousBlock is not None
			self._currentBlock =  self._startBlock.PreviousBlock
		self._stopBlock =        stopBlock
		self._inclusiveStopBlock = inclusiveStopBlock

		self._state =        0

	def __iter__(self) -> 'BlockReverseIterator':
		return self

	def __next__(self) -> 'Block':
		# in last call of '__next__', the last block in the sequence was returned
		if self._state > 0:
			raise StopIteration(self._state)

		block = self._currentBlock
		if block is self._stopBlock:
			self._state =        1
			if not self._inclusiveStopBlock:
				raise StopIteration(self._state)
		elif isinstance(self._currentBlock, StartOfBlock):
			self._state =        2
			if not self._inclusiveStopBlock:
				raise StopIteration(self._state)
		else:
			if block.PreviousBlock is None:
				raise ParserException("Found open end while iterating block sequence.")  # FIXME: how to append last block?
			self._currentBlock = block.PreviousBlock

		return block


@export
class Block(metaclass=MetaBlock):
	"""
	Base-class for all :term:`block` classes.
	"""

	__STATES__:      List[Callable[[TokenToBlockParser], None]] #: List of all `state...` methods in this class.

	_previousBlock: Optional['Block']                           #: Reference to the previous block.
	NextBlock:      Optional['Block']                           #: Reference to the next block.
	StartToken:     Token                                       #: Reference to the first token in the scope of this block.
	EndToken:       Token                             #: Reference to the last token in the scope of this block.
	MultiPart:      bool                                        #: True, if this block has multiple parts.

	def __init__(self, previousBlock: 'Block', startToken: Token, endToken: Optional[Token] = None, multiPart: bool = False):
		"""Base-class constructor for a new block instance."""

		previousBlock.NextBlock =       self
		self._previousBlock = previousBlock
		self.NextBlock =      None
		self.StartToken =     startToken
		self.EndToken =       startToken if (endToken is None) else endToken
		self.MultiPart =      multiPart

	def __len__(self) -> int:
		"""Returns the length of a block in characters from :attr:`~Block.StartToken` to :attr:`~Block.EndToken`."""
		if self.EndToken is None:
			raise BlockParserException("Cannot get length of Block with an empty EndToken!", None)
		return self.EndToken.End.Absolute - self.StartToken.Start.Absolute + 1

	def __iter__(self) -> TokenIterator:
		"""Returns a token iterator that iterates from :attr:`~Block.StartToken` to :attr:`~Block.EndToken`."""
		return TokenIterator(self.StartToken, inclusiveStartToken=True, stopToken=self.EndToken)

	def GetIterator(self, inclusiveStartBlock: bool = False, inclusiveStopBlock: bool = True, stopBlock: Optional['Block']=None) -> BlockIterator:
		return BlockIterator(self, inclusiveStartBlock=inclusiveStartBlock, inclusiveStopBlock=inclusiveStopBlock, stopBlock=stopBlock)

	def GetReverseIterator(self, inclusiveStartBlock: bool = False, inclusiveStopBlock: bool = True, stopBlock: Optional['Block']=None) -> BlockReverseIterator:
		return BlockReverseIterator(self, inclusiveStartBlock=inclusiveStartBlock, inclusiveStopBlock=inclusiveStopBlock, stopBlock=stopBlock)

	def __str__(self) -> str:
		buffer: str = ""
		for token in self:
			if isinstance(token, CharacterToken):
				buffer += repr(token)
			else:
				try:
					buffer += token.Value # type: ignore
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
		assert self._previousBlock is not None
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
	def States(self) -> List[BLOCK_PARSER_STATE]:
		"""Returns a list of all `state...` methods in this class."""
		return self.__STATES__

	@classmethod
	def stateError(cls, parserState: TokenToBlockParser):
		"""Predefined state to catch error situations."""
		raise BlockParserException("Reached unreachable state!", None)


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

	def __init__(self, startToken: Token):
		self._previousBlock =     None
		self.NextBlock =          None
		self.StartToken =         startToken
		self.EndToken =           startToken
		self.MultiPart =          False

	def __len__(self) -> int:
		return 0

	def __repr__(self) -> str:
		return "[{name}]".format(
			name=self.__class__.__name__
		)


@export
class EndOfBlock(Block):
	"""Base-class for a last block in a sequence of double-linked blocks."""

	def __init__(self, previousBlock: Block, endToken: Token):
		super().__init__(previousBlock, endToken)

	def __len__(self) -> int:
		return 0

	def __repr__(self) -> str:
		return "[{name}]".format(
			name=self.__class__.__name__
		)


@export
class StartOfDocumentBlock(StartOfBlock, StartOfDocument):
	"""First block in a sequence of double-linked blocks."""

	KEYWORDS: Dict[Type[KeywordToken], BLOCK_PARSER_STATE]

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Reference  import Library, Use, Context
		from pyVHDLParser.Blocks.Sequential import Package
		from pyVHDLParser.Blocks.Structural import Entity, Architecture

		cls.KEYWORDS = {
			# Keyword             Transition
			LibraryKeyword:       Library.StartBlock.stateLibraryKeyword,
			UseKeyword:           Use.StartBlock.stateUseKeyword,
			ContextKeyword:       Context.StartBlock.stateContextKeyword,
			EntityKeyword:        Entity.NameBlock.stateEntityKeyword,
			ArchitectureKeyword:  Architecture.NameBlock.stateArchitectureKeyword,
			PackageKeyword:       Package.NameBlock.statePackageKeyword
		}

	@classmethod
	def stateDocument(cls, parserState: TokenToBlockParser):
		from pyVHDLParser.Blocks.Whitespace     import IndentationBlock, WhitespaceBlock, LinebreakBlock

		token = parserState.Token
		if isinstance(token, WhitespaceToken):
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

		assert isinstance(token, ValuedToken)
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
