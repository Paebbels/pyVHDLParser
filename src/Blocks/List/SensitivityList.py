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
from src.Token.Keywords       import LinebreakToken, BoundaryToken, IndentationToken, IdentifierToken, EndToken, DelimiterToken, AllKeyword, \
	OpeningRoundBracketToken, ClosingRoundBracketToken
from src.Token.Parser         import CharacterToken, SpaceToken, StringToken
from src.Blocks.Exception     import BlockParserException
from src.Blocks.Base          import Block
from src.Blocks.Common        import LinebreakBlock, IndentationBlock, WhitespaceBlock
from src.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock


class OpenBlock(Block):
	def RegisterStates(self):
		return [
			# self.stateProcessKeyword,
			# self.stateWhitespace1,
			self.stateOpeningParenthesis
		]

	# @classmethod
	# def stateProcessKeyword(cls, parserState):
	# 	token = parserState.Token
	# 	errorMessage = "Expected whitespace or '(' after keyword PROCESS."
	# 	if isinstance(token, CharacterToken):
	# 		if (token == "("):
	# 			parserState.NewToken =    BoundaryToken(token)
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
	# 			parserState.NextState =   CloseBlock.stateClosingParenthesis
	# 			parserState.PushState =   OpenBlock.stateOpeningParenthesis
	# 			parserState.Counter =     1
	# 			return
	# 		elif (token == "\n"):
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
	# 			parserState.NewToken =    LinebreakToken(token)
	# 			_ =                       LinebreakBlock(parserState.NewBlock, parserState.NewToken)
	# 			parserState.TokenMarker = None
	# 			parserState.NextState =   cls.stateWhitespace1
	# 			parserState.PushState =   LinebreakBlock.stateLinebreak
	# 			return
	# 		elif (token == "-"):
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
	# 			parserState.TokenMarker = None
	# 			parserState.NextState =   cls.stateWhitespace1
	# 			parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
	# 			parserState.TokenMarker = token
	# 			return
	# 		elif (token == "/"):
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
	# 			parserState.TokenMarker = None
	# 			parserState.NextState =   cls.stateWhitespace1
	# 			parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
	# 			parserState.TokenMarker = token
	# 			return
	# 	elif isinstance(token, SpaceToken):
	# 		parserState.NextState =     cls.stateWhitespace1
	# 		return
	#
	# 	raise BlockParserException(errorMessage, token)
	#
	# @classmethod
	# def stateWhitespace1(cls, parserState):
	# 	token = parserState.Token
	# 	errorMessage = "Expected  '(' after keyword PROCESS."
	# 	if isinstance(token, CharacterToken):
	# 		if (token == "("):
	# 			parserState.NewToken =    BoundaryToken(token)
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
	# 			parserState.NextState =   CloseBlock.stateClosingParenthesis
	# 			parserState.PushState =   OpenBlock.stateOpeningParenthesis
	# 			parserState.Counter =     1
	# 			return
	# 		elif (token == "\n"):
	# 			parserState.NewToken =    LinebreakToken(token)
	# 			if (not isinstance(parserState.LastBlock, MultiLineCommentBlock)):
	# 				parserState.NewBlock =  OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken, multiPart=True)
	# 				_ =                     LinebreakBlock(parserState.NewBlock, parserState.NewToken)
	# 			else:
	# 				parserState.NewBlock =  LinebreakBlock(parserState.LastBlock, parserState.NewToken)
	# 			parserState.TokenMarker = None
	# 			parserState.NextState =   cls.stateWhitespace1
	# 			parserState.PushState =   LinebreakBlock.stateLinebreak
	# 			return
	# 		elif (token == "-"):
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
	# 			parserState.TokenMarker = None
	# 			parserState.NextState =   cls.stateWhitespace1
	# 			parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
	# 			parserState.TokenMarker = token
	# 			return
	# 		elif (token == "/"):
	# 			parserState.NewBlock =    OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
	# 			parserState.TokenMarker = None
	# 			parserState.NextState =   cls.stateWhitespace1
	# 			parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
	# 			parserState.TokenMarker = token
	# 			return
	# 	elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
	# 		parserState.NewToken =      BoundaryToken(token)
	# 		parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
	# 		parserState.TokenMarker =   None
	# 		return
	#
	# 	raise BlockParserException(errorMessage, token)

	@classmethod
	def stateOpeningParenthesis(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected signal name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == ")"):
				# if (parserState.TokenMarker != token):
				# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
				parserState.Pop()
				parserState.TokenMarker = token
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
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			if (token <= "all"):
				parserState.NewToken =    AllKeyword(token)
				parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				parserState.NextState =   CloseBlock.stateAllKeyword
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState =   ItemBlock.stateItemRemainder

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
				parserState.NewToken =      OpeningRoundBracketToken(token)
				parserState.Counter += 1
			elif (token == ")"):
				parserState.Counter -= 1
				if (parserState.Counter == 0):
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
					parserState.NewToken =    BoundaryToken(token)
					_ =                       CloseBlock(parserState.NewBlock, parserState.NewToken, parserState.NewToken)
					parserState.Pop()
					parserState.TokenMarker = None
				else:
					parserState.NewToken =    ClosingRoundBracketToken(token)
			elif (token == ","):
				if (parserState.Counter == 1):
					parserState.NewToken =    DelimiterToken(token)
					parserState.NewBlock =    ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					_ =                       DelimiterBlock(parserState.NewBlock, parserState.NewToken)
					parserState.NextState =   DelimiterBlock.stateItemDelimiter
				else:
					raise BlockParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)


class DelimiterBlock(Block):
	def __init__(self, previousBlock, startToken):
		super().__init__(previousBlock, startToken, startToken)

	def RegisterStates(self):
		return [
			self.stateItemDelimiter
		]

	@classmethod
	def stateItemDelimiter(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected signal name (identifier)."

		if (isinstance(token, CharacterToken) and (token == "\n")):
			parserState.NewToken =      LinebreakToken(token)
			parserState.NewBlock =      LinebreakBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			parserState.NextState =     OpenBlock.stateOpeningParenthesis
			parserState.PushState =     LinebreakBlock.stateLinebreak
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
			self.stateAllKeyword,
			self.stateWhitespace1,
			self.stateClosingParenthesis,
			self.stateWhitespace2
		]

	@classmethod
	def stateAllKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace or ')' after keyword ALL."
		if isinstance(token, CharacterToken):
			if (token == ")"):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				parserState.NextState =   cls.stateClosingParenthesis
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.NewBlock, parserState.NewToken)
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
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected  '(' after keyword PROCESS."
		if isinstance(token, CharacterToken):
			if (token == ")"):
				parserState.NewToken =    BoundaryToken(token)
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				parserState.NextState =   CloseBlock.stateClosingParenthesis
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				# if (not isinstance(parserState.LastBlock, MultiLineCommentBlock)):
				# 	parserState.NewBlock =  LinebreakBlock(parserState.NewBlock, parserState.NewToken)
				# else:
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
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)

	@classmethod
	def stateClosingParenthesis(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';' or whitespace."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.PushState =   LinebreakBlock.stateLinebreak
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState = cls.stateWhitespace2
			return
		else:
			parserState.Pop()
			parserState.NextState(parserState)

		# raise BlockParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				# TODO: review this linebreak case
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
		elif (isinstance(token, SpaceToken) and isinstance(parserState.LastBlock, MultiLineCommentBlock)):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException(errorMessage, token)
