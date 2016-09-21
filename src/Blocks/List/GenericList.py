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
from src.Token.Keywords       import LinebreakToken, BoundaryToken, IndentationToken, IdentifierToken, EndToken, DelimiterToken
from src.Token.Parser         import CharacterToken, SpaceToken, StringToken
from src.Blocks.Exception     import BlockParserException
from src.Blocks.Base          import Block
from src.Blocks.Common        import LinebreakBlock, IndentationBlock
from src.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock


class OpenBlock(Block):
	def RegisterStates(self):
		return [
			self.stateGenericKeyword,
			self.stateWhitespace1,
			self.stateOpeningParenthesis
		]

	@classmethod
	def stateGenericKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace or '(' after keyword GENERIC."
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =   CloseBlock.stateClosingParenthesis
				parserState.PushState =   OpenBlock.stateOpeningParenthesis
				parserState.Counter =     1
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
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
		errorMessage = "Expected  '(' after keyword GENERIC."
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =   CloseBlock.stateClosingParenthesis
				parserState.PushState =   OpenBlock.stateOpeningParenthesis
				parserState.Counter =     1
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateOpeningParenthesis(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected generic name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == ")"):
				# if (parserState.TokenMarker != token):
				# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
				parserState.Pop()
				parserState.TokenMarker = token
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				# parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				# parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   LinebreakBlock.stateLinebreak
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.TokenMarker =   parserState.NewToken
			parserState.NextState =     ItemBlock.stateItemRemainder

			# if (parserState.TokenMarker != token):
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token)
			return

		raise BlockParserException(errorMessage, token)

class ItemBlock(Block):
	def RegisterStates(self):
		return [
			self.stateItemRemainder
		]

	@classmethod
	def stateItemRemainder(cls, parserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if (token == "("):
				parserState.Counter += 1
			elif (token == ")"):
				parserState.Counter -= 1
				if (parserState.Counter == 0):
					parserState.NewToken =  BoundaryToken(token)
					parserState.NewBlock =  ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					parserState.Pop()
					parserState.TokenMarker = parserState.NewToken
			elif (token == ";"):
				if (parserState.Counter == 1):
					parserState.NewToken =  DelimiterToken(token)
					parserState.NewBlock =  ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					parserState.TokenMarker = parserState.NewToken
					parserState.NextState = DelimiterBlock.stateItemDelimiter
				else:
					raise BlockParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)

class DelimiterBlock(Block):
	def RegisterStates(self):
		return [
			self.stateItemDelimiter
		]

	@classmethod
	def stateItemDelimiter(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected generic name (identifier)."

		# produce a new block for the last generated token (delimiter)
		parserState.NewBlock =        DelimiterBlock(parserState.LastBlock, parserState.TokenMarker, parserState.TokenMarker)

		if (isinstance(token, CharacterToken) and (token == "\n")):
			parserState.NextState =     OpenBlock.stateOpeningParenthesis
			return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     OpenBlock.stateOpeningParenthesis
			return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.TokenMarker =   parserState.NewToken
			parserState.NextState =     ItemBlock.stateItemRemainder
			return

		raise BlockParserException(errorMessage, token)

class CloseBlock(Block):
	def RegisterStates(self):
		return [
			self.stateClosingParenthesis,
			self.stateWhitespace1
		]

	@classmethod
	def stateClosingParenthesis(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';' or whitespace."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.PushState =   LinebreakBlock.stateLinebreak
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState = cls.stateWhitespace1
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.PushState =   LinebreakBlock.stateLinebreak
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return

		raise BlockParserException(errorMessage, token)

