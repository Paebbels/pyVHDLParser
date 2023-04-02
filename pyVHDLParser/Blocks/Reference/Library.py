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
from pyTooling.Decorators             import export

from pyVHDLParser.Token               import CharacterToken, SpaceToken, WordToken, LinebreakToken, CommentToken, IndentationToken, SingleLineCommentToken, MultiLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords      import BoundaryToken, IdentifierToken, EndToken, DelimiterToken
from pyVHDLParser.Blocks              import BlockParserException, Block, CommentBlock, TokenToBlockParser, FinalBlock, SkipableBlock
from pyVHDLParser.Blocks.Whitespace       import LinebreakBlock, WhitespaceBlock


@export
class StartBlock(Block):
	@classmethod
	def stateLibraryKeyword(cls, parserState: TokenToBlockParser):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(fromExistingToken=token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected whitespace after keyword LIBRARY.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: TokenToBlockParser):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =    IdentifierToken(fromExistingToken=token)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   LibraryNameBlock.stateLibraryName
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   LibraryNameBlock.stateLibraryName
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    block(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken)):
			return
		elif isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken)):
			parserState.NewToken =    BoundaryToken(fromExistingToken=token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise BlockParserException("Expected library name (identifier).", token)


@export
class LibraryNameBlock(Block):
	@classmethod
	def stateLibraryName(cls, parserState: TokenToBlockParser):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if token == ",":
				parserState.NewToken =  DelimiterToken(fromExistingToken=token)
				parserState.NewBlock =  cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
				_ =                     DelimiterBlock(parserState.NewBlock, parserState.NewToken)
				parserState.NextState = DelimiterBlock.stateDelimiter
				return
			elif token == ";":
				parserState.NewToken =  EndToken(fromExistingToken=token)
				parserState.NewBlock =  cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
				_ =                     EndBlock(parserState.NewBlock, parserState.NewToken)
				parserState.Pop()
				return
		elif isinstance(token, SpaceToken):
			#parserState.NewToken =    BoundaryToken(fromExistingToken=token)
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected ';' after library name.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: TokenToBlockParser):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if token == ",":
				parserState.NewToken =    DelimiterToken(fromExistingToken=token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
				_ =                       DelimiterBlock(parserState.NewBlock, parserState.NewToken)
				parserState.NextState =   DelimiterBlock.stateDelimiter
				return
			elif token == ";":
				parserState.NewToken =    EndToken(fromExistingToken=token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
				_ =                       EndBlock(parserState.NewBlock, parserState.NewToken)
				parserState.Pop()
				return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken)):
			return
		elif isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken)):
			parserState.NewToken =      BoundaryToken(fromExistingToken=token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected ';'.", token)


@export
class DelimiterBlock(SkipableBlock):
	@classmethod
	def stateDelimiter(cls, parserState: TokenToBlockParser):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =      IdentifierToken(fromExistingToken=token)
			parserState.NextState =     LibraryNameBlock.stateLibraryName
			parserState.TokenMarker =   parserState.NewToken
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =     LibraryNameBlock.stateLibraryName
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(fromExistingToken=token)
			# parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   parserState.NewToken
			parserState.NextState =     cls.stateWhitespace1
			return

		raise BlockParserException("Expected library name (identifier).", token)

	@classmethod
	def stateWhitespace1(cls, parserState: TokenToBlockParser):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =      IdentifierToken(fromExistingToken=token)
			parserState.NextState =     LibraryNameBlock.stateLibraryName
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken)):
			return
		elif isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken)):
			parserState.NewToken =      BoundaryToken(fromExistingToken=token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected library name (identifier).", token)


@export
class EndBlock(FinalBlock):
	pass
