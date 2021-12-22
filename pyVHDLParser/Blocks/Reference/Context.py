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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany                                                            #
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

from pyVHDLParser.Token               import CommentToken, SpaceToken, LinebreakToken, MultiLineCommentToken, IndentationToken, SingleLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords      import WordToken, BoundaryToken, IdentifierToken, IsKeyword, UseKeyword, EndKeyword, ContextKeyword, LibraryKeyword
from pyVHDLParser.Blocks              import Block, CommentBlock, BlockParserException, ParserState
from pyVHDLParser.Blocks.Common       import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic      import EndBlock as EndBlockBase


@export
class NameBlock(Block):
	KEYWORDS = None

	@classmethod
	def __cls_init__(cls):
		from pyVHDLParser.Blocks.Reference     import Use, Library

		cls.KEYWORDS = {
			# Keyword       Transition
			UseKeyword:     Use.StartBlock.stateUseKeyword,
			LibraryKeyword: Library.StartBlock.stateLibraryKeyword
		}
	@classmethod
	def stateContextKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected whitespace after keyword CONTEXT.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateContextName
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =     cls.stateContextName
			return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                       LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected context name (identifier).", token)

	@classmethod
	def stateContextName(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace2
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                     LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         block(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace2
			return

		raise BlockParserException("Expected whitespace after context name (identifier).", token)

	@classmethod
	def stateWhitespace2(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, WordToken) and (token <= "is")):
			parserState.NewToken =      IsKeyword(token)
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.NextState =     cls.stateDeclarativeRegion
			return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                       LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected keyword IS after context name.", token)

	@classmethod
	def stateDeclarativeRegion(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			blockType =                 IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =      blockType(parserState.LastBlock, token)
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                     LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =      block(parserState.LastBlock, token)
			parserState.TokenMarker =   None
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

			if (tokenValue == "end"):
				parserState.NewToken =    EndKeyword(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   EndBlock.stateEndKeyword
				return

		raise BlockParserException(
			"Expected one of these keywords: END, {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in cls.KEYWORDS]
				),
				tokenValue=token.Value
			), token)


@export
class EndBlock(EndBlockBase):
	KEYWORD =       ContextKeyword
	EXPECTED_NAME = KEYWORD.__KEYWORD__
