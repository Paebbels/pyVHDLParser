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
# Copyright 2007-2016 Patrick Lehmann - Dresden, Germany
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
from pyVHDLParser.Token.Keywords       import BoundaryToken, LinebreakToken, IdentifierToken, EndToken, DelimiterToken
from pyVHDLParser.Token.Parser         import CharacterToken, SpaceToken, StringToken
from pyVHDLParser.Blocks.Parser        import TokenToBlockParser
from pyVHDLParser.Blocks.Exception     import BlockParserException
from pyVHDLParser.Blocks.Base          import Block
from pyVHDLParser.Blocks.Common        import LinebreakBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock

# Type alias for type hinting
ParserState = TokenToBlockParser.TokenParserState


class LibraryBlock(Block):
	def RegisterStates(self):
		return [
			self.stateLibraryKeyword,
			self.stateWhitespace1
		]

	@classmethod
	def stateLibraryKeyword(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword LIBRARY."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      LibraryBlock(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected library name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NewBlock =      LibraryNameBlock(parserState.LastBlock, parserState.NewToken)
			parserState.NextState =     LibraryNameBlock.stateLibraryName
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)


class LibraryNameBlock(Block):
	def RegisterStates(self):
		return [
			self.stateLibraryName,
			self.stateWhitespace1
		]

	@classmethod
	def stateLibraryName(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected ';' after library name."
		if isinstance(token, CharacterToken):
			if (token == ","):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NewBlock =    LibraryDelimiterBlock(parserState.LastBlock, parserState.NewToken)
				parserState.NextState =   LibraryDelimiterBlock.stateDelimiter
				return
			elif (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    LibraryEndBlock(parserState.LastBlock, parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == ","):
				parserState.NewToken =      DelimiterToken(token)
				parserState.NewBlock =      LibraryDelimiterBlock(parserState.LastBlock, parserState.NewToken)
				parserState.NextState =     LibraryDelimiterBlock.stateDelimiter
				return
			elif (token == ";"):
				parserState.NewToken =      EndToken(token)
				parserState.NewBlock =      LibraryEndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)


class LibraryDelimiterBlock(Block):
	def RegisterStates(self):
		return [
			self.stateDelimiter,
			self.stateWhitespace1
		]

	@classmethod
	def stateDelimiter(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected library name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =      LinebreakToken(token)
				parserState.NewBlock =      LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker =   None
				parserState.PushState =     LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.TokenMarker =   None
				parserState.PushState =     SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
			elif (token == "/"):
				parserState.TokenMarker =   None
				parserState.PushState =     MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =        IdentifierToken(token)
			parserState.NewBlock =        LibraryNameBlock(parserState.LastBlock, parserState.NewToken)
			parserState.NextState =       LibraryNameBlock.stateLibraryName
			parserState.TokenMarker =     None
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =        BoundaryToken(token)
			parserState.NewBlock =        WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =     None
			parserState.NextState =       cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		errorMessage = "Expected library name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =      LinebreakToken(token)
				parserState.NewBlock =      LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker =   None
				parserState.PushState =     LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.TokenMarker =   None
				parserState.PushState =     SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
			elif (token == "/"):
				parserState.TokenMarker =   None
				parserState.PushState =     MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker =   token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =        IdentifierToken(token)
			parserState.NewBlock =        LibraryNameBlock(parserState.LastBlock, parserState.NewToken)
			parserState.NextState =       LibraryNameBlock.stateLibraryName
			parserState.TokenMarker =     None
			return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =        BoundaryToken(token)
			parserState.NewBlock =        WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =     None
			return

		raise BlockParserException(errorMessage, token)

class LibraryEndBlock(Block):
	pass
