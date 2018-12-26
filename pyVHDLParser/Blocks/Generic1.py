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
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
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
# load dependencies
from pyVHDLParser.Token           import CharacterToken, SpaceToken, LinebreakToken, CommentToken, StringToken, MultiLineCommentToken, IndentationToken
from pyVHDLParser.Token           import SingleLineCommentToken, ExtendedIdentifier
from pyVHDLParser.Token.Keywords  import EndToken, BoundaryToken, LabelToken, IdentifierToken
from pyVHDLParser.Blocks          import FinalBlock, ParserState, CommentBlock, TokenParserException, Block
from pyVHDLParser.Blocks.Common   import LinebreakBlock, WhitespaceBlock


class EndBlock(FinalBlock):
	KEYWORD =             None
	KEYWORD_IS_OPTIONAL = False
	EXPECTED_NAME =       ""
	EXPECTED_NAME_KIND =  "keyword"  # keyword label

	@classmethod
	def stateEndKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if ((cls.KEYWORD_IS_OPTIONAL is True) and (token == ";")):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace1
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace1
			return

		raise TokenParserException("Expected ';' or whitespace.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if ((cls.KEYWORD_IS_OPTIONAL is True) and (token == ";")):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
		elif isinstance(token, StringToken):
			IS_SINGLE_KEYWORD = isinstance(cls.KEYWORD, tuple)
			KW = cls.KEYWORD[0] if IS_SINGLE_KEYWORD else cls.KEYWORD
			if (token <= KW.__KEYWORD__):
				parserState.NewToken =    KW(token)
				parserState.NextState =   cls.stateKeyword1
			elif (cls.EXPECTED_NAME_KIND == "label"):
				parserState.NewToken =    LabelToken(token)
				parserState.NextState =   cls.stateSimpleName
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateSimpleName
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

		if (cls.KEYWORD_IS_OPTIONAL is True):
			if (cls.EXPECTED_NAME_KIND == "label"):
				errorMessage = "Expected ';', {0} keyword or {1} label.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)
			else:
				errorMessage = "Expected ';', {0} keyword or {1} name.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)
		else:
			if (cls.EXPECTED_NAME_KIND == "label"):
				errorMessage = "Expected {0} keyword or {1} label.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)
			else:
				errorMessage = "Expected {0} keyword or {1} name.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)

		raise TokenParserException(errorMessage, token)

	@classmethod
	def stateKeyword1(cls, parserState: ParserState):
		IS_DOUBLE_KEYWORD = isinstance(cls.KEYWORD, tuple)
		nextState = cls.stateWhitespace2 if IS_DOUBLE_KEYWORD else cls.stateWhitespace3;
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if (not isinstance(cls.KEYWORD, tuple) and (token == ";")):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     nextState
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace3
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace3
			return

		raise TokenParserException("Expected ';' or whitespace.", token)

	@classmethod
	def stateWhitespace2(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if ((cls.KEYWORD_IS_OPTIONAL is True) and (not isinstance(cls.KEYWORD, tuple)) and (token == ";")):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
		elif (isinstance(token, StringToken) and (token <= cls.KEYWORD[1].__KEYWORD__)):
			parserState.NewToken =    cls.KEYWORD[1](token)
			parserState.NextState =   cls.stateKeyword2
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

		if (cls.KEYWORD_IS_OPTIONAL is True):
			if (cls.EXPECTED_NAME_KIND == "label"):
				errorMessage = "Expected ';', {0} keyword or {1} label.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)
			else:
				errorMessage = "Expected ';', {0} keyword or {1} name.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)
		else:
			if (cls.EXPECTED_NAME_KIND == "label"):
				errorMessage = "Expected {0} keyword or {1} label.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)
			else:
				errorMessage = "Expected {0} keyword or {1} name.".format(cls.EXPECTED_NAME.upper(), cls.EXPECTED_NAME)

		raise TokenParserException(errorMessage, token)

	@classmethod
	def stateKeyword2(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == ";")):
			parserState.NewToken =      EndToken(token)
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace3
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace3
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace3
			return

		raise TokenParserException("Expected ';' or whitespace.", token)

	@classmethod
	def stateWhitespace3(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =    IdentifierToken(token)
			parserState.NextState =   cls.stateSimpleName
			return
		elif isinstance(token, ExtendedIdentifier):
			parserState.NextState =   cls.stateSimpleName
			return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =  cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                     LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =  LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker = None
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise TokenParserException("Expected ';' or {0} name.".format(cls.EXPECTED_NAME), token)

	@classmethod
	def stateSimpleName(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =      EndToken(token)
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace4
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token, multiPart=True)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace4
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			parserState.NextState =     cls.stateWhitespace4
			return

		raise TokenParserException("Expected ';' or whitespace.", token)

	@classmethod
	def stateWhitespace4(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
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

		raise TokenParserException("Expected ';'.", token)


class BeginBlock(Block):
	END_BLOCK : EndBlock = None

	KEYWORDS = None

	@classmethod
	def stateStatementRegion(cls, parserState: ParserState):
		pass


class CloseBlock(Block):
	@classmethod
	def stateClosingParenthesis(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, SpaceToken):
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise TokenParserException("Expected ';' or whitespace.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == ";")):
			parserState.NewToken =    EndToken(token)
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		elif isinstance(token, LinebreakToken):
			# TODO: review this linebreak case
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker = token
			return
		elif (isinstance(token, IndentationToken) and isinstance(token.PreviousToken, (LinebreakToken, SingleLineCommentToken))):
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NewBlock =    WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker = None
			return

		raise TokenParserException("Expected ';'.", token)


class EndOfStatementBlock(Block):
	pass
