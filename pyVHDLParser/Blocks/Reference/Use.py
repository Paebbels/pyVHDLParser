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
from pyVHDLParser.Token.Keywords       import BoundaryToken, LinebreakToken, IdentifierToken, DelimiterToken, EndToken, AllKeyword
from pyVHDLParser.Token.Parser         import CharacterToken, SpaceToken, StringToken
from pyVHDLParser.Blocks.Exception     import BlockParserException
from pyVHDLParser.Blocks.Base          import Block
from pyVHDLParser.Blocks.Common        import LinebreakBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock


class UseBlock(Block):
	def RegisterStates(self):
		return [
			self.stateUseKeyword,
			self.stateWhitespace1
		]

	@classmethod
	def stateUseKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword USE."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      UseBlock(parserState.LastBlock, parserState.TokenMarker, parserState.NewToken)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
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
			parserState.TokenMarker =   parserState.NewToken
			parserState.NextState =     UseNameBlock.stateLibraryName
			return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)

class UseNameBlock(Block):
	def RegisterStates(self):
		return [
			self.stateLibraryName,
			self.stateWhitespace1,
			self.stateDot1,
			self.stateWhitespace2,
			self.statePackageName,
			self.stateWhitespace3,
			self.stateDot2,
			self.stateWhitespace4,
			self.stateObjectName,
			self.stateWhitespace5
		]

	@classmethod
	def stateLibraryName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected '.' after library name."
		if isinstance(token, CharacterToken):
			if (token == "."):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NextState =   cls.stateDot1
				return
			elif (token == "\n"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
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
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected '.'."
		if isinstance(token, CharacterToken):
			if (token == "."):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NextState =   cls.stateDot1
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

	@classmethod
	def stateDot1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected package name after '.'."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.statePackageName
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace2
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected package name (identifier)."
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
			parserState.NextState =     UseNameBlock.statePackageName
			return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def statePackageName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected '.' after package name."
		if isinstance(token, CharacterToken):
			if (token == "."):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NextState =   cls.stateDot2
				return
			elif (token == "\n"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace3
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace3
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace3
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace3
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace3(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected '.'."
		if isinstance(token, CharacterToken):
			if (token == "."):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NextState =   cls.stateDot2
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

	@classmethod
	def stateDot2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected object name after '.'."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.NewToken =    LinebreakToken(token)
				_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace4
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace4
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace4
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			if (token <= "all"):
				parserState.NewToken =    AllKeyword(token)
			else:
				parserState.NewToken =    IdentifierToken(token)
			parserState.NextState =     cls.stateObjectName
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace4
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace4(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected object name (identifier)."
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
			if (token <= "all"):
				parserState.NewToken =    AllKeyword(token)
			else:
				parserState.NewToken =    IdentifierToken(token)
			parserState.NewBlock =      UseNameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
			parserState.NextState =     UseNameBlock.stateObjectName
			return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateObjectName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ',', ';' or whitespace."
		if isinstance(token, CharacterToken):
			if (token == ","):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NewBlock =    UseDelimiterBlock(parserState.LastBlock, parserState.NewToken)
				parserState.NextState =   UseDelimiterBlock.stateDelimiter
				return
			elif (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    UseEndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace5
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace5
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace5
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace5
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace5(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == ","):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NewBlock =    UseDelimiterBlock(parserState.LastBlock, parserState.NewToken)
				parserState.NextState =   UseDelimiterBlock.stateDelimiter
				return
			elif (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    UseEndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
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


class UseDelimiterBlock(Block):
	def RegisterStates(self):
		return [
			self.stateDelimiter,
			self.stateWhitespace1
		]

	@classmethod
	def stateDelimiter(cls, parserState):
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
			parserState.NewBlock =        UseNameBlock(parserState.LastBlock, parserState.NewToken)
			parserState.NextState =       UseNameBlock.stateLibraryName
			parserState.TokenMarker =     parserState.NewToken
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =        BoundaryToken(token)
			parserState.NewBlock =        WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =     None
			parserState.NextState =       cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
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
			parserState.NewBlock =        UseNameBlock(parserState.LastBlock, parserState.NewToken)
			parserState.NextState =       UseNameBlock.stateLibraryName
			parserState.TokenMarker =     parserState.NewToken
			return
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =        BoundaryToken(token)
			parserState.NewBlock =        WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =     None
			return

		raise BlockParserException(errorMessage, token)

class UseEndBlock(Block):
	pass
