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
from typing                           import Type, Dict

from pyTooling.Decorators             import export

from pyVHDLParser.Token               import Token, CommentToken, WhitespaceToken, LinebreakToken, IndentationToken, ExtendedIdentifier, CharacterToken, ValuedToken
from pyVHDLParser.Token.Keywords      import WordToken, IdentifierToken, IsKeyword, UseKeyword, EndKeyword, ContextKeyword, LibraryKeyword, EndToken, DelimiterToken, KeywordToken
from pyVHDLParser.Blocks              import Block, BlockParserException, TokenToBlockParser, SkipableBlock, BLOCK_PARSER_STATE
from pyVHDLParser.Blocks.Region       import EndBlock as EndBlockBase


def _isNonCodeToken(token: Token) -> bool:
	return isinstance(token, (LinebreakToken, WhitespaceToken, IndentationToken, CommentToken))




@export
class DelimiterBlock(SkipableBlock):
	pass


@export
class StartBlock(Block):
	"""
	This block is used to disambiguate between context declarations and context references.

	The states in this class only check whether the token stream represents a declaration or a reference.
	They neither change :class:`Token`s nor do they create new :class:`Block`s.
	After a decision can be made, the unhandled tokens (everything between :attr:`parserState.TokenMarker` and the current token)
	are parsed a second time by either :attr:`ReferenceStartBlock.fromTokenMarker` or :attr:`DeclarationStartBlock.fromTokenMarker`.
	"""
	@classmethod
	def stateContextKeyword(cls, parserState: TokenToBlockParser):
		cls.stateWhitespace1(parserState)

	@classmethod
	def stateWhitespace1(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if _isNonCodeToken(token):
			parserState.NextState = cls.stateContextName
			return

		raise BlockParserException("Expected whitespace after keyword CONTEXT.", token)

	@classmethod
	def stateContextName(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if _isNonCodeToken(token):
			return

		if isinstance(token, (WordToken, ExtendedIdentifier)):
			parserState.NextState =     cls.stateWhitespaceOrSemicolonOrDot
			return

		raise BlockParserException("Expected context name (identifier).", token)

	@classmethod
	def stateWhitespaceOrSemicolonOrDot(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if _isNonCodeToken(token):
			parserState.NextState =        cls.stateIsOrSemicolonOrDot
			return

		if isinstance(token, CharacterToken) and token == ";":
			parserState.ReparseFromTokenMarker(ReferenceStartBlock.stateFromStartBlock)
			parserState.Pop()
			return
		elif isinstance(token, CharacterToken) and token == ".":
			parserState.ReparseFromTokenMarker(ReferenceStartBlock.stateFromStartBlock)
			return

		raise BlockParserException("Expected whitespace after context name (identifier).", token)

	@classmethod
	def stateIsOrSemicolonOrDot(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(cls):
			return

		if isinstance(token, WordToken) and (token == "is"):
			parserState.ReparseFromTokenMarker(DeclarationStartBlock.stateFromStartBlock)
			return
		elif isinstance(token, CharacterToken) and token == ";":
			parserState.ReparseFromTokenMarker(ReferenceStartBlock.stateFromStartBlock)
			parserState.Pop()
			return
		elif isinstance(token, CharacterToken) and token == ".":
			parserState.ReparseFromTokenMarker(ReferenceStartBlock.stateFromStartBlock)
			return

		raise BlockParserException("Expected context name (identifier).", token)


#
# Context references
#
@export
class ReferenceStartBlock(Block):
	@classmethod
	def stateFromStartBlock(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if isinstance(token, ContextKeyword):
			parserState.NextState =   cls.stateWhitespace
			return

		# The 'context' keyword was already detected. If it is not there anymore, we found a bug.
		assert False, "Expected keyword CONTEXT."

	@classmethod
	def stateContextKeyword(cls, parserState: TokenToBlockParser):
		cls.stateWhitespace(parserState)

	@classmethod
	def stateWhitespace(cls, parserState: TokenToBlockParser):
		if parserState.HandleNonCodeTokens(cls, multiPart=False):
			parserState.NextState =   ReferenceNameBlock.stateLibOrContextName
			return

		# This condition is also guaranteed. Otherwise `StartBlock.stateContextKeyword` would have thrown an error.
		assert False, "Expected whitespace after keyword CONTEXT."


@export
class ReferenceNameBlock(Block):
	KEYWORDS = None

	@classmethod
	def stateLibOrContextName(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(None):
			return

		if isinstance(token, WordToken):
			parserState.NewToken  = IdentifierToken(fromExistingToken=token)
			parserState.NextState = cls.stateCommaOrDotOrSemicolon
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState = cls.stateCommaOrDotOrSemicolon
			return

		raise BlockParserException("Expected context or library name (identifier).", token)

	@classmethod
	def stateCommaOrDotOrSemicolon(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(cls):
			return

		if isinstance(token, CharacterToken) and token == ".":
			parserState.NewToken =      DelimiterToken(fromExistingToken=token)
			parserState.NextState =     cls.stateContextName
			return
		elif isinstance(token, CharacterToken) and token == ";":
			parserState.NewToken =      EndToken(fromExistingToken=token)
			parserState.NewBlock =      ReferenceNameBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
			_ =                         ReferenceEndBlock(parserState.NewBlock, parserState.NewToken, parserState.NewToken)
			parserState.TokenMarker =   None
			parserState.Pop()
			return
		elif isinstance(token, CharacterToken) and token == ",":
			parserState.NewToken =      DelimiterToken(fromExistingToken=token)
			parserState.NewBlock =      ReferenceNameBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
			_ =                         DelimiterBlock(parserState.NewBlock, parserState.NewToken, parserState.NewToken)
			parserState.NextState =     cls.stateLibOrContextName
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected either a comma, a dot or a semicolon separating or concluding a context reference (character).", token)

	@classmethod
	def stateContextName(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(cls):
			return

		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(fromExistingToken=token)
			parserState.NewBlock =    ReferenceNameBlock(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.NextState =   cls.stateCommaOrSemicolon
			parserState.TokenMarker = None
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NewBlock =    ReferenceNameBlock(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.NextState =   cls.stateCommaOrSemicolon
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected context name (identifier).", token)

	@classmethod
	def stateCommaOrSemicolon(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(None):
			return

		if isinstance(token, CharacterToken) and token == ";":
			parserState.NewToken =      EndToken(fromExistingToken=token)
			parserState.NewBlock =      ReferenceEndBlock(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.TokenMarker =   None
			parserState.Pop()
			return
		elif isinstance(token, CharacterToken) and token == ",":
			parserState.NewToken =      DelimiterToken(fromExistingToken=token)
			parserState.NewBlock =      DelimiterBlock(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.NextState =     cls.stateLibOrContextName
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected either a comma or a semicolon separating or concluding a context reference (character).", token)


@export
class ReferenceEndBlock(Block):
	pass



#
# Context declarations
#
@export
class DeclarationStartBlock(Block):
	@classmethod
	def stateFromStartBlock(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if isinstance(token, ContextKeyword):
			parserState.NextState =   cls.stateWhitespace
			return

		# The 'context' keyword was already detected. If it is not there anymore, we found a bug.
		assert False, "Expected keyword CONTEXT."

	@classmethod
	def stateContextKeyword(cls, parserState: TokenToBlockParser):
		cls.stateWhitespace(parserState)

	@classmethod
	def stateWhitespace(cls, parserState: TokenToBlockParser):
		if parserState.HandleNonCodeTokens(cls):
			parserState.NextState =   cls.stateContextName
			return

		# This condition is also guaranteed. Otherwise `StartBlock.stateContextKeyword` would have thrown an error.
		assert False, "Expected whitespace after keyword CONTEXT."

	@classmethod
	def stateContextName(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(cls):
			return

		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(fromExistingToken=token)
			parserState.NextState =   cls.stateWhitespace2
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   cls.stateWhitespace2
			return

		# This condition is also guaranteed. Otherwise `StartBlock.stateWhitespace1` would have thrown an error.
		assert False, "Expected context name (identifier)."

	@classmethod
	def stateWhitespace2(cls, parserState: TokenToBlockParser):
		if parserState.HandleNonCodeTokens(cls):
			parserState.NextState =   cls.stateContextIs
			return

		# This condition is also guaranteed. Otherwise `StartBlock.stateContextName` would have thrown an error.
		assert False, "Expected whitespace after context name."

	@classmethod
	def stateContextIs(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(cls):
			return

		if isinstance(token, WordToken) and token == "is":
			parserState.NewToken =    IsKeyword(fromExistingToken=token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.NextState =   DeclarationBody.stateDeclarativeRegion
			parserState.TokenMarker = None
			return

		# This condition is also guaranteed. Otherwise `StartBlock.stateWhitespace2` would have thrown an error.
		assert False, "Expected keyword IS after context name."


@export
class DeclarationBody(Block):
	KEYWORDS: Dict[Type[KeywordToken], BLOCK_PARSER_STATE]

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Reference     import Use, Library

		cls.KEYWORDS = {
			# Keyword       Transition
			UseKeyword:     Use.StartBlock.stateUseKeyword,
			LibraryKeyword: Library.StartBlock.stateLibraryKeyword,
			ContextKeyword: ReferenceStartBlock.stateContextKeyword,
		}

	@classmethod
	def stateDeclarativeRegion(cls, parserState: TokenToBlockParser):
		token = parserState.Token

		if parserState.HandleNonCodeTokens(None):
			return

		if isinstance(token, WordToken):
			tokenValue = token.Value.lower()
			for keyword in cls.KEYWORDS:
				if tokenValue == keyword.__KEYWORD__:
					newToken =                keyword(fromExistingToken=token)
					parserState.PushState =   cls.KEYWORDS[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

			if tokenValue == "end":
				parserState.NewToken =    EndKeyword(fromExistingToken=token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   DeclarationEndBlock.stateEndKeyword
				return

		assert isinstance(token, ValuedToken)
		raise BlockParserException(
			"Expected one of these keywords: END, {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


@export
class DeclarationEndBlock(EndBlockBase):
	KEYWORD =       ContextKeyword
	EXPECTED_NAME = KEYWORD.__KEYWORD__
