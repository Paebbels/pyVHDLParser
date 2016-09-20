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
from src.Token.Keywords       import *
from src.Token.Parser         import *
from src.Blocks.Exception     import BlockParserException
from src.Blocks.Base          import Block
from src.Blocks.Common        import EmptyLineBlock
from src.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock


class AssertBlock(Block):
	def RegisterStates(self):
		return [
			self.stateAssertKeyword,
			self.stateWhitespace1,
			self.stateAssertName,
			self.stateWhitespace2,
			self.stateDeclarativeRegion
		]

	@classmethod
	def stateAssertKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword ASSERT."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected assert name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateAssertName
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateAssertName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword ASSERT."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after assert name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise BlockParserException(errorMessage, token)

