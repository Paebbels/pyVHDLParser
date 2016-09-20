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
from src.Parser         import CharacterToken, SpaceToken, EndOfDocumentToken, ParserException
from src.VHDLKeywords   import *

class BlockGroup:
	def __init__(self, a, b, endToken):
		print("---- BlockGroup ----")

class Block:
	def __init__(self, previousBlock, startToken, endToken=None, multiPart=False):
		previousBlock.NextBlock = self
		self._previousBlock =     previousBlock
		self._nextBlock =         None
		self.StartToken =         startToken
		self._endToken =          endToken
		self.MultiPart =          multiPart

	def __len__(self):
		return self.EndToken.End.Absolute - self.StartToken.Start.Absolute + 1

	def __iter__(self):
		token = self.StartToken
		# print("start={0!s}  end={1!s}".format(self.StartToken, self.EndToken))
		while (token is not self.EndToken):
			yield token
			if (token.NextToken is None):
				raise ParserException("Token after {0} <- {1} <- {2} is None.".format(token, token.PreviousToken, token.PreviousToken.PreviousToken), token)
			token = token.NextToken

		yield self.EndToken

	def __repr__(self):
		buffer = ""
		for token in self:
			if isinstance(token, CharacterToken):
				buffer += repr(token)
			else:
				buffer += token.Value

		buffer = buffer.replace("\t", "\\t")
		buffer = buffer.replace("\n", "\\n")
		return buffer

	def __str__(self):
		return "[{blockName: <30s} '{stream!r: <60s}' at {start!s} .. {end!s}]".format(
			blockName=type(self).__name__,
			stream=self,
			start=self.StartToken.Start,
			end=self.EndToken.End
		)

	@property
	def PreviousBlock(self):
		return self._previousBlock
	@PreviousBlock.setter
	def PreviousBlock(self, value):
		self._previousBlock = value
		value.NextBlock = self

	@property
	def NextBlock(self):
		return self._nextBlock
	@NextBlock.setter
	def NextBlock(self, value):
		self._nextBlock = value

	@property
	def EndToken(self):
		return self._endToken
	@EndToken.setter
	def EndToken(self, value):
		self._endToken = value

	@property
	def Length(self):
		return len(self)


class StartOfDocumentBlock(Block):
	def __init__(self, startToken):
		self._previousBlock =     None
		self._nextBlock =         None
		self.StartToken =         startToken
		self._endToken =          startToken
		self.MultiPart =          False

	def __len__(self):
		return 0

	def __str__(self):
		return "[StartOfDocumentBlock]"

	def RegisterStates(self):
		return [
			self.stateDocument
		]

	@classmethod
	def stateDocument(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected keywords: architecture, context, entity, library, package, use."
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			keyword = token.Value.lower()
			if (keyword == "library"):
				newToken = LibraryKeyword(token)
				parserState.PushState =   LibraryBlock.stateLibraryKeyword
			elif (keyword == "use"):
				newToken = UseKeyword(token)
				parserState.PushState =   UseBlock.stateUseKeyword
			elif (keyword == "context"):
				newToken = ContextKeyword(token)
				parserState.PushState =   Context.NameBlock.stateContextKeyword
			elif (keyword == "entity"):
				newToken = EntityKeyword(token)
				parserState.PushState =   Entity.NameBlock.stateEntityKeyword
			elif (keyword == "architecture"):
				newToken = ArchitectureKeyword(token)
				parserState.PushState =   Architecture.NameBlock.stateArchitectureKeyword
			elif (keyword == "package"):
				newToken = PackageKeyword(token)
				parserState.PushState =   Package.NameBlock.statePackageKeyword
			else:
				raise ParserException(errorMessage, token)

			parserState.NewToken =      newToken
			parserState.TokenMarker =   newToken
			return
		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock =      EndOfDocumentBlock(token)
			raise StopIteration()
		else:  # tokenType
			raise ParserException(errorMessage, token)


class EndOfDocumentBlock(Block):
	def __init__(self, endToken):
		self._previousBlock =     None
		self._nextBlock =         None
		self.StartToken =         endToken
		self._endToken =          endToken
		self.MultiPart =          False

	def __len__(self):
		return 0

	def __str__(self):
		return "[EndOfDocumentBlock]"


class WhitespaceBlock(Block):
	pass

class EmptyLineBlock(WhitespaceBlock):
	def __str__(self):
		buffer = ""
		for token in self:
			buffer += token.Value
		buffer = buffer.replace("\t", "\\t").replace("\n", "\\n")
		return "[EmptyLineBlock: '{0}']".format(buffer)

	@classmethod
	def stateLinebreak(cls, parserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken = IndentationToken(token)
			parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
		else:
			parserState.Pop()
			if (parserState.TokenMarker is None):
				# print("  new marker: None -> {0!s}".format(token))
				parserState.TokenMarker = token
			# print("  re-issue: {0!s}".format(parserState))
			parserState.NextState(parserState)


class IndentationBlock(WhitespaceBlock):
	__TABSIZE__ = 2

	def __str__(self):
		buffer = ""
		for token in self:
			buffer += token.Value
		actual = sum([(self.__TABSIZE__ if (c=="\t") else 1) for c in buffer])
		return "[IndentationBlock: length={len} ({actual})]".format(len=len(self), actual=actual)


class CommentBlock(Block):
	pass

class SingleLineCommentBlock(CommentBlock):
	def RegisterStates(self):
		return [
			self.statePossibleCommentStart,
			self.stateConsumeComment
		]

	@classmethod
	def statePossibleCommentStart(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "-")):
			parserState.NewToken =    SingleLineCommentKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return

		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateConsumeComment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "\n")):
			parserState.NewBlock =    SingleLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.Token)
			parserState.NextState =   cls.stateLinebreak
			return
		else:
			pass	# consume everything until "\n"

	@classmethod
	def stateLinebreak(cls, parserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken = IndentationToken(token)
			parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			parserState.Pop()
		else:
			parserState.Pop()
			if (parserState.TokenMarker is None):
				# print("  new marker: None -> {0!s}".format(token))
				parserState.TokenMarker = token
			# print("  re-issue: {0!s}".format(parserState))
			parserState.NextState(parserState)


class MultiLineCommentBlock(CommentBlock):
	def RegisterStates(self):
		return [
			self.statePossibleCommentStart,
			self.stateConsumeComment,
			self.statePossibleCommentEnd
		]

	@classmethod
	def statePossibleCommentStart(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "*")):
			parserState.NewToken =    MultiLineCommentStartKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return

		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateConsumeComment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "*")):
			parserState.PushState =   cls.statePossibleCommentEnd
			parserState.TokenMarker = token
			return
		else:
			pass  # consume everything until "*/"

	@classmethod
	def statePossibleCommentEnd(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "/")):
			parserState.NewToken = MultiLineCommentEndKeyword(parserState.TokenMarker)
			parserState.Pop()
			parserState.NewBlock = MultiLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		else:
			parserState.Pop()


class LibraryBlock(Block):
	def RegisterStates(self):
		return [
			self.stateLibraryKeyword,
			self.stateWhitespace1,
			self.stateLibraryName,
			self.stateWhitespace2
		]

	@classmethod
	def stateLibraryKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword LIBRARY."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
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
			parserState.NextState =     cls.stateWhitespace1
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected library name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateLibraryName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateLibraryName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';' after library name."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "-"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return

		raise ParserException(errorMessage, token)


class UseBlock(Block):
	def RegisterStates(self):
		return [
			self.stateUseKeyword,
			self.stateWhitespace1,
			self.stateLibraryName,
			self.stateDot1,
			self.statePackageName,
			self.stateDot2,
			self.stateObjectName,
			self.stateWhitespace2
		]

	@classmethod
	def stateUseKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword USE."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
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
			parserState.NextState =     cls.stateWhitespace1
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected library name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateLibraryName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateLibraryName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected dot after library name."
		if isinstance(token, CharacterToken):
			if (token == "."):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NextState =   cls.stateDot1
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateDot1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected package name after first dot."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.statePackageName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def statePackageName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected dot after package name."
		if isinstance(token, CharacterToken):
			if (token == "."):
				parserState.NewToken =    DelimiterToken(token)
				parserState.NextState =   cls.stateDot2
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateDot2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateDot2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected object name or ALL after second dot."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
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

		raise ParserException(errorMessage, token)

	@classmethod
	def stateObjectName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';' or whitespace."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected ';'."
		if isinstance(token, CharacterToken):
			if (token == ";"):
				parserState.NewToken =    EndToken(token)
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.Pop()
				return
			elif (token == "-"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    UseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return

		raise ParserException(errorMessage, token)


class Entity(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEntityKeyword,
				self.stateWhitespace1,
				self.stateEntityName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateEntityKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ENTITY."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected entity name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateEntityName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateEntityName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ENTITY."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after entity name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Entity.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Entity.EndBlock.stateEndKeyword
				elif (keyword == "constant"):
					newToken =              ConstantKeyword(token)
					parserState.PushState = ObjectDeclaration.ConstantBlock.stateConstantKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Entity.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Entity.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)


	class BeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			errorMessage = "Expected label or one of these keywords: process."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "process"):
					newToken =              ProcessKeyword(token)
					parserState.PushState = Process.OpenBlock.stateProcessKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Entity.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateEntityKeyword,
				self.stateWhitespace2,
				self.stateEntityName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', ENTITY keyword or entity name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "entity"):
					parserState.NewToken =    EntityKeyword(token)
					parserState.NextState =   cls.stateEntityKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateEntityName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateEntityKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or entity name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateEntityName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateEntityName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Entity.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class Component(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateComponentKeyword,
				self.stateWhitespace1,
				self.stateComponentName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateComponentKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword COMPONENT."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected component name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateComponentName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateComponentName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword COMPONENT."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after component name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Component.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Component.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Component.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Component.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)


	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateComponentKeyword,
				self.stateWhitespace2,
				self.stateComponentName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', COMPONENT keyword or component name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "component"):
					parserState.NewToken =    ComponentKeyword(token)
					parserState.NextState =   cls.stateComponentKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateComponentName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateComponentKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or component name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateComponentName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateComponentName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Component.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class GenericList(BlockGroup):
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
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.NextState =   GenericList.CloseBlock.stateClosingParenthesis
					parserState.PushState =   GenericList.OpenBlock.stateOpeningParenthesis
					parserState.Counter =     1
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected  '(' after keyword GENERIC."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.NextState =   GenericList.CloseBlock.stateClosingParenthesis
					parserState.PushState =   GenericList.OpenBlock.stateOpeningParenthesis
					parserState.Counter =     1
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

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
					# parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					# parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    GenericList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
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
				parserState.NextState =     GenericList.ItemBlock.stateItemRemainder

				# if (parserState.TokenMarker != token):
				# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token)
				return

			raise ParserException(errorMessage, token)

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
						parserState.NewBlock =  GenericList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.Pop()
						parserState.TokenMarker = parserState.NewToken
				elif (token == ";"):
					if (parserState.Counter == 1):
						parserState.NewToken =  DelimiterToken(token)
						parserState.NewBlock =  GenericList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.TokenMarker = parserState.NewToken
						parserState.NextState = GenericList.DelimiterBlock.stateItemDelimiter
					else:
						raise ParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)

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
			parserState.NewBlock =        GenericList.DelimiterBlock(parserState.LastBlock, parserState.TokenMarker, parserState.TokenMarker)

			if (isinstance(token, CharacterToken) and (token == "\n")):
				parserState.NextState =     GenericList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     GenericList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.TokenMarker =   parserState.NewToken
				parserState.NextState =     GenericList.ItemBlock.stateItemRemainder
				return

			raise ParserException(errorMessage, token)

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
					parserState.NewBlock =    GenericList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    GenericList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    GenericList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState = cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    GenericList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    GenericList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    GenericList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class PortList:
	class OpenBlock(Block):
		def RegisterStates(self):
			return [
				self.statePortKeyword,
				self.stateWhitespace1,
				self.stateOpeningParenthesis
			]

		@classmethod
		def statePortKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace or '(' after keyword PORT."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.NextState =   PortList.CloseBlock.stateClosingParenthesis
					parserState.PushState =   PortList.OpenBlock.stateOpeningParenthesis
					parserState.Counter =     1
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token

			errorMessage = "Expected  '(' after keyword PORT."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.NextState =   PortList.CloseBlock.stateClosingParenthesis
					parserState.PushState =   PortList.OpenBlock.stateOpeningParenthesis
					parserState.Counter =     1
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateOpeningParenthesis(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected port name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == ")"):
					# if (parserState.TokenMarker != token):
					# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
					parserState.Pop()
					parserState.TokenMarker = token
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					# parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					# parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    PortList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
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
				parserState.NextState =     PortList.ItemBlock.stateItemRemainder

				# if (parserState.TokenMarker != token):
				# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token)
				return

			raise ParserException(errorMessage, token)

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
						parserState.NewBlock =  PortList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.Pop()
						parserState.TokenMarker = parserState.NewToken
				elif (token == ";"):
					if (parserState.Counter == 1):
						parserState.NewToken =  DelimiterToken(token)
						parserState.NewBlock =  PortList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.TokenMarker = parserState.NewToken
						parserState.NextState = PortList.DelimiterBlock.stateItemDelimiter
					else:
						raise ParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)

	class DelimiterBlock(Block):
		def RegisterStates(self):
			return [
				self.stateItemDelimiter
			]

		@classmethod
		def stateItemDelimiter(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected port name (identifier)."

			# produce a new block for the last generated token (delimiter)
			parserState.NewBlock =        PortList.DelimiterBlock(parserState.LastBlock, parserState.TokenMarker, parserState.TokenMarker)

			if (isinstance(token, CharacterToken) and (token == "\n")):
				parserState.NextState =     PortList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     PortList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.TokenMarker =   parserState.NewToken
				parserState.NextState =     PortList.ItemBlock.stateItemRemainder
				return

			raise ParserException(errorMessage, token)

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
					parserState.NewBlock =    PortList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    PortList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    PortList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState = cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    PortList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    PortList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    PortList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class ParameterList:
	class OpenBlock(Block):
		def RegisterStates(self):
			return [
				self.stateParameterKeyword,
				self.stateWhitespace1,
				self.stateOpeningParenthesis
			]

		@classmethod
		def stateParameterKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace or '(' after keyword PARAMETER."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken = BoundaryToken(token)
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.NextState = ParameterList.CloseBlock.stateClosingParenthesis
					parserState.PushState = ParameterList.OpenBlock.stateOpeningParenthesis
					parserState.Counter = 1
					return
				elif (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState = cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token

			errorMessage = "Expected  '(' after keyword PARAMETER."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken = BoundaryToken(token)
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.NextState = ParameterList.CloseBlock.stateClosingParenthesis
					parserState.PushState = ParameterList.OpenBlock.stateOpeningParenthesis
					parserState.Counter = 1
					return
				elif (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateOpeningParenthesis(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected parameter name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == ")"):
					# if (parserState.TokenMarker != token):
					# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token.PreviousToken)
					parserState.Pop()
					parserState.TokenMarker = token
					return
				elif (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					# parserState.NewBlock =    ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					# parserState.NextState =   cls.stateWhitespace1
					parserState.PushState = EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ParameterList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken = IndentationToken(token)
				parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				parserState.NewToken = IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState = ParameterList.ItemBlock.stateItemRemainder

				# if (parserState.TokenMarker != token):
				# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token)
				return

			raise ParserException(errorMessage, token)

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
						parserState.NewToken = BoundaryToken(token)
						parserState.NewBlock = ParameterList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.Pop()
						parserState.TokenMarker = parserState.NewToken
				elif (token == ";"):
					if (parserState.Counter == 1):
						parserState.NewToken = DelimiterToken(token)
						parserState.NewBlock = ParameterList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.TokenMarker = parserState.NewToken
						parserState.NextState = ParameterList.DelimiterBlock.stateItemDelimiter
					else:
						raise ParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)

	class DelimiterBlock(Block):
		def RegisterStates(self):
			return [
				self.stateItemDelimiter
			]

		@classmethod
		def stateItemDelimiter(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected parameter name (identifier)."

			# produce a new block for the last generated token (delimiter)
			parserState.NewBlock = ParameterList.DelimiterBlock(parserState.LastBlock, parserState.TokenMarker, parserState.TokenMarker)

			if (isinstance(token, CharacterToken) and (token == "\n")):
				parserState.NextState = ParameterList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, SpaceToken):
				parserState.NextState = ParameterList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, StringToken):
				parserState.NewToken = IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState = ParameterList.ItemBlock.stateItemRemainder
				return

			raise ParserException(errorMessage, token)

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
					parserState.NewToken = EndToken(token)
					parserState.NewBlock = ParameterList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.PushState = EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock = ParameterList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ParameterList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace1
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState = cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken = EndToken(token)
					parserState.NewBlock = ParameterList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.PushState = EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock = ParameterList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ParameterList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class SensitivityList:
	class OpenBlock(Block):
		def RegisterStates(self):
			return [
				self.stateOpeningParenthesis
			]


		# TODO: move to PROCESS
		# @classmethod
		# def stateSensitivityKeyword(cls, parserState):
		# 	token = parserState.Token
		# 	errorMessage = "Expected whitespace or '(' after keyword SENSITIVITY."
		# 	if isinstance(token, CharacterToken):
		# 		if (token == "("):
		# 			parserState.NewToken = BoundaryToken(token)
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
		# 			parserState.NextState = SensitivityList.CloseBlock.stateClosingParenthesis
		# 			parserState.PushState = SensitivityList.OpenBlock.stateOpeningParenthesis
		# 			parserState.Counter = 1
		# 			return
		# 		elif (token == "\n"):
		# 			parserState.NewToken = LinebreakToken(token)
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
		# 			parserState.TokenMarker = None
		# 			parserState.NextState = cls.stateWhitespace1
		# 			parserState.PushState = EmptyLineBlock.stateLinebreak
		# 			return
		# 		elif (token == "-"):
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
		# 			parserState.TokenMarker = None
		# 			parserState.NextState = cls.stateWhitespace1
		# 			parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
		# 			parserState.TokenMarker = token
		# 			return
		# 		elif (token == "/"):
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
		# 			parserState.TokenMarker = None
		# 			parserState.NextState = cls.stateWhitespace1
		# 			parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
		# 			parserState.TokenMarker = token
		# 			return
		# 	elif isinstance(token, SpaceToken):
		# 		parserState.NextState = cls.stateWhitespace1
		# 		return
		#
		# 	raise ParserException(errorMessage, token)
		#
		# @classmethod
		# def stateWhitespace1(cls, parserState):
		# 	token = parserState.Token
		#
		# 	errorMessage = "Expected  '(' after keyword SENSITIVITY."
		# 	if isinstance(token, CharacterToken):
		# 		if (token == "("):
		# 			parserState.NewToken = BoundaryToken(token)
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
		# 			parserState.NextState = SensitivityList.CloseBlock.stateClosingParenthesis
		# 			parserState.PushState = SensitivityList.OpenBlock.stateOpeningParenthesis
		# 			parserState.Counter = 1
		# 			return
		# 		elif (token == "\n"):
		# 			parserState.NewToken = LinebreakToken(token)
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
		# 			parserState.TokenMarker = None
		# 			parserState.NextState = cls.stateWhitespace1
		# 			parserState.PushState = EmptyLineBlock.stateLinebreak
		# 			return
		# 		elif (token == "-"):
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
		# 			parserState.TokenMarker = None
		# 			parserState.NextState = cls.stateWhitespace1
		# 			parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
		# 			parserState.TokenMarker = token
		# 			return
		# 		elif (token == "/"):
		# 			parserState.NewBlock = SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
		# 			parserState.TokenMarker = None
		# 			parserState.NextState = cls.stateWhitespace1
		# 			parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
		# 			parserState.TokenMarker = token
		# 			return
		#
		# 	raise ParserException(errorMessage, token)

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
					# parserState.NewBlock =    SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					# parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    SensitivityList.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
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
				parserState.NextState =     SensitivityList.ItemBlock.stateItemRemainder

				# if (parserState.TokenMarker != token):
				# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.TokenMarker, token)
				return

			raise ParserException(errorMessage, token)

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
						parserState.NewToken =    BoundaryToken(token)
						parserState.NewBlock =    SensitivityList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.Pop()
						parserState.TokenMarker = parserState.NewToken
				elif (token == ","):
					if (parserState.Counter == 1):
						parserState.NewToken =    DelimiterToken(token)
						parserState.NewBlock =    SensitivityList.ItemBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
						parserState.TokenMarker = parserState.NewToken
						parserState.NextState =   SensitivityList.DelimiterBlock.stateItemDelimiter
					else:
						raise ParserException("Mismatch in opening and closing parenthesis: open={0}".format(parserState.Counter), token)

	class DelimiterBlock(Block):
		def RegisterStates(self):
			return [
				self.stateItemDelimiter
			]

		@classmethod
		def stateItemDelimiter(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected sensitivity name (identifier)."

			# produce a new block for the last generated token (delimiter)
			parserState.NewBlock = SensitivityList.DelimiterBlock(parserState.LastBlock, parserState.TokenMarker, parserState.TokenMarker)

			if (isinstance(token, CharacterToken) and (token == "\n")):
				parserState.NextState = SensitivityList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, SpaceToken):
				parserState.NextState = SensitivityList.OpenBlock.stateOpeningParenthesis
				return
			elif isinstance(token, StringToken):
				parserState.NewToken = IdentifierToken(token)
				parserState.TokenMarker = parserState.NewToken
				parserState.NextState = SensitivityList.ItemBlock.stateItemRemainder
				return

			raise ParserException(errorMessage, token)

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
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    SensitivityList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    SensitivityList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState = cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken = EndToken(token)
					parserState.NewBlock = SensitivityList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.PushState = EmptyLineBlock.stateLinebreak
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock = SensitivityList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = SensitivityList.CloseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class Architecture(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateArchitectureKeyword,
				self.stateWhitespace1,
				self.stateArchitectureName,
				self.stateWhitespace2,
				self.stateEntityName,
				self.stateWhitespace3,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateArchitectureKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ARCHITECTURE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected architecture name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateArchitectureName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateArchitectureName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ARCHITECTURE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after architecture name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "of")):
				parserState.NewToken =      OfKeyword(token)
				parserState.NextState =     cls.stateOfKeyword
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateOfKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword OF."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace3
					parserState.PushState = EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock = Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace3
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace3
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken = BoundaryToken(token)
				parserState.NextState = cls.stateWhitespace3
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected entity name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock = Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken = IdentifierToken(token)
				parserState.NextState = cls.stateEntityName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateEntityName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after entity name."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace4
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace4
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace4
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace4
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace4(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after entity name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Architecture.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: signal, constant, variable, shared, begin."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "signal"):
					newToken =              SignalKeyword(token)
					parserState.PushState = ObjectDeclaration.SignalBlock.stateSignalKeyword
				elif (keyword == "constant"):
					newToken =              ConstantKeyword(token)
					parserState.PushState = ObjectDeclaration.ConstantBlock.stateConstantKeyword
				elif (keyword == "variable"):
					newToken =              VariableKeyword(token)
					parserState.PushState = ObjectDeclaration.VariableBlock.stateVariableKeyword
				elif (keyword == "shared"):
					newToken =              SharedKeyword(token)
					parserState.PushState = ObjectDeclaration.SharedVariableBlock.stateSharedKeyword
				# elif (keyword == "end"):
				# 	newToken =              EndKeyword(token)
				# 	parserState.NextState = Architecture.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Architecture.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Architecture.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected label or one of these keywords: assert, process."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				return
			# 	parserState.NewToken = IndentationToken(token)
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			# 	return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "process"):
					newToken =                ProcessKeyword(token)
					parserState.PushState =   Process.OpenBlock.stateProcessKeyword
				elif (keyword == "assert"):
					newToken =                AssertKeyword(token)
					parserState.PushState =   AssertBlock.stateAssertKeyword
				elif (keyword == "end"):
					newToken =                EndKeyword(token)
					parserState.NextState =   Architecture.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateArchitectureKeyword,
				self.stateWhitespace2,
				self.stateArchitectureName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', ARCHITECTURE keyword or architecture name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "architecture"):
					parserState.NewToken =    ArchitectureKeyword(token)
					parserState.NextState =   cls.stateArchitectureKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateArchitectureName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateArchitectureKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or architecture name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateArchitectureName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateArchitectureName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Architecture.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class Package(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.statePackageKeyword,
				self.stateWhitespace1,
				self.statePackageName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def statePackageKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword PACKAGE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected package name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.statePackageName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePackageName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword PACKAGE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after package name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "constant"):
					newToken =              ConstantKeyword(token)
					parserState.PushState = ObjectDeclaration.ConstantBlock.stateConstantKeyword
				elif (keyword == "variable"):
					newToken =              VariableKeyword(token)
					parserState.PushState = ObjectDeclaration.VariableBlock.stateVariableKeyword
				elif (keyword == "shared"):
					newToken =              SharedKeyword(token)
					parserState.PushState = ObjectDeclaration.SharedVariableBlock.stateSharedKeyword
				elif (keyword == "procedure"):
					newToken =              ProcessKeyword(token)
					parserState.PushState = Procedure.NameBlock.stateProcesdureKeyword
				elif (keyword == "function"):
					newToken =              FunctionKeyword(token)
					parserState.PushState = Function.NameBlock.stateFunctionKeyword
				elif (keyword == "pure"):
					newToken =              PureKeyword(token)
					parserState.PushState = Function.NameBlock.statePureKeyword
				elif (keyword == "impure"):
					newToken =              ImpureKeyword(token)
					parserState.PushState = Function.NameBlock.stateImpureKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Package.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.statePackageKeyword,
				self.stateWhitespace2,
				self.statePackageName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', PACKAGE keyword or package name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "package"):
					parserState.NewToken =    PackageKeyword(token)
					parserState.NextState =   cls.statePackageKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.statePackageName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePackageKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or package name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.statePackageName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePackageName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class PackageBody(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.statePackageKeyword,
				self.stateWhitespace1,
				self.statePackageName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def statePackageKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword PACKAGE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected package name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.statePackageName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePackageName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword PACKAGE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after package name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Package.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "constant"):
					newToken = ConstantKeyword(token)
					parserState.PushState = ObjectDeclaration.ConstantBlock.stateConstantKeyword
				elif (keyword == "variable"):
					newToken = VariableKeyword(token)
					parserState.PushState = ObjectDeclaration.VariableBlock.stateVariableKeyword
				elif (keyword == "shared"):
					newToken = SharedKeyword(token)
					parserState.PushState = ObjectDeclaration.SharedVariableBlock.stateSharedKeyword
				elif (keyword == "procedure"):
					newToken = ProcessKeyword(token)
					parserState.PushState = Procedure.NameBlock.stateProcesdureKeyword
				elif (keyword == "function"):
					newToken = FunctionKeyword(token)
					parserState.PushState = Function.NameBlock.stateFunctionKeyword
				elif (keyword == "pure"):
					newToken = PureKeyword(token)
					parserState.PushState = Function.NameBlock.statePureKeyword
				elif (keyword == "impure"):
					newToken = ImpureKeyword(token)
					parserState.PushState = Function.NameBlock.stateImpureKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Package.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.statePackageKeyword,
				self.stateWhitespace2,
				self.statePackageName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', PACKAGE keyword or package name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "package"):
					parserState.NewToken =    PackageKeyword(token)
					parserState.NextState =   cls.statePackageKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.statePackageName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePackageKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or package name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.statePackageName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePackageName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Package.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class Block(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBlockKeyword,
				self.stateWhitespace1,
				self.stateBlockName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateBlockKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword BLOCK."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected block name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateBlockName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateBlockName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword BLOCK."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after block name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Block.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "constant"):
					newToken = ConstantKeyword(token)
					parserState.PushState =   ObjectDeclaration.ConstantBlock.stateConstantKeyword
				elif (keyword == "variable"):
					newToken = VariableKeyword(token)
					parserState.PushState =   ObjectDeclaration.VariableBlock.stateVariableKeyword
				elif (keyword == "begin"):
					parserState.NewToken =    BeginKeyword(token)
					parserState.NewBlock =    Block.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState =   Block.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken = newToken
				parserState.TokenMarker = newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block): pass

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateBlockKeyword,
				self.stateWhitespace2,
				self.stateBlockName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', BLOCK keyword or block name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "block"):
					parserState.NewToken =    BlockKeyword(token)
					parserState.NextState =   cls.stateBlockKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateBlockName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateBlockKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or block name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateBlockName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateBlockName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Block.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class Process(BlockGroup):
	class OpenBlock(Block):
		def RegisterStates(self):
			return [
				self.stateProcessKeyword,
				self.stateWhitespace1,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateProcessKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected '(' or whitespace after keyword PROCESS."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken =    BoundaryToken(token)

					# print(dir(Process.OpenBlock))
					print(Process.OpenBlock.__init__)
					print(Process.OpenBlock.__qualname__)
					print(Process.OpenBlock.__class__.__qualname__)

					a = Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					parserState.NewBlock =    a
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateDeclarativeRegion
					parserState.PushState =   SensitivityList.OpenBlock.stateOpeningParenthesis
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected '(' after PROCESS keyword."
			if isinstance(token, CharacterToken):
				if (token == "("):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NewBlock =    Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken.PreviousToken)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, is, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "constant"):
					newToken =              ConstantKeyword(token)
					parserState.PushState = ObjectDeclaration.ConstantBlock.stateConstantKeyword
				elif (keyword == "variable"):
					newToken =              VariableKeyword(token)
					parserState.PushState = ObjectDeclaration.VariableBlock.stateVariableKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Process.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Process.BeginBlock.stateBeginKeyword
					return
				elif (keyword == "is"):
					parserState.NewToken =  IsKeyword(token)
					parserState.NewBlock =  Process.OpenBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					# parserState.NextState = Process.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			errorMessage = "Expected label or one of these keywords: if, case, for, while, report, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "if"):
					newToken =                IfKeyword(token)
					parserState.PushState =   If.IfConditionBlock.stateIfKeyword
				elif (keyword == "case"):
					newToken =                CaseKeyword(token)
					parserState.PushState =   Case.CaseBlock.stateCaseKeyword
				elif (keyword == "for"):
					newToken =                ForKeyword(token)
					parserState.PushState =   ForLoop.RangeBlock.stateForKeyword
				elif (keyword == "while"):
					newToken =                WhileKeyword(token)
					parserState.PushState =   WhileLoop.ConditionBlock.stateWhileKeyword
				elif (keyword == "report"):
					newToken =                ReportKeyword(token)
					parserState.PushState =   ReportBlock.stateReportKeyword
				elif (keyword == "end"):
					newToken = EndKeyword(token)
					parserState.NextState =   Process.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken = newToken
				parserState.TokenMarker = newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateProcessKeyword,
				self.stateWhitespace2,
				self.stateProcessName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', PROCESS keyword or process name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "process"):
					parserState.NewToken =    ProcessKeyword(token)
					parserState.NextState =   cls.stateProcessKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateProcessName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateProcessKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or process name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateProcessName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateProcessName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Process.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class Configuration(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateConfigurationKeyword,
				self.stateWhitespace1,
				self.stateConfigurationName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateConfigurationKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CONFIGURATION."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected configuration name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateConfigurationName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateConfigurationName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CONFIGURATION."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after configuration name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Configuration.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Configuration.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Configuration.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Configuration.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateConfigurationKeyword,
				self.stateWhitespace2,
				self.stateConfigurationName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', CONFIGURATION keyword or configuration name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "configuration"):
					parserState.NewToken =    ConfigurationKeyword(token)
					parserState.NextState =   cls.stateConfigurationKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateConfigurationName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateConfigurationKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or configuration name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateConfigurationName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateConfigurationName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Configuration.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class Context(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateContextKeyword,
				self.stateWhitespace1,
				self.stateContextName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateContextKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CONTEXT."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected context name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateContextName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateContextName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CONTEXT."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after context name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Context.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "use"):
					newToken =              UseKeyword(token)
					parserState.PushState = UseBlock.stateUseKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Context.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateContextKeyword,
				self.stateWhitespace2,
				self.stateContextName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', CONTEXT keyword or context name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "context"):
					parserState.NewToken =    ContextKeyword(token)
					parserState.NextState =   cls.stateContextKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateContextName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateContextKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or context name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateContextName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateContextName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Context.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class ObjectDeclaration(BlockGroup):
	class SignalBlock(Block): pass

	class ConstantBlock(Block):
		def RegisterStates(self):
			return [
				self.stateConstantKeyword,
				self.stateWhitespace1,
				self.stateConstantName,
				self.stateWhitespace2,
				self.stateColon1,
				self.stateWhitespace3,
				self.statePossibleVariableAssignment,
				self.stateVariableAssignment
			]

		@classmethod
		def stateConstantKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CONSTANT."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected constant name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateConstantName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateConstantName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' after library name."
			if isinstance(token, CharacterToken):
				if (token == ":"):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NextState =   cls.stateColon1
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected constant name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == ":"):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NextState =   cls.stateColon1
					return
				elif (token == "-"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken = IdentifierToken(token)
				parserState.NextState = cls.stateColon1()
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateColon1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected typemark or whitespace after ':'."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace3
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace3
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace3
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace3
				return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateTypeMarkName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected constant name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken = IdentifierToken(token)
				parserState.NextState = cls.stateTypeMarkName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateTypeMarkName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ':=' or whitespace after type mark."
			if isinstance(token, CharacterToken):
				if (token == ":"):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NextState =   cls.statePossibleVariableAssignment
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace4
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace4(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ':=' after type mark."
			if isinstance(token, CharacterToken):
				if (token == ":"):
					parserState.NewToken =    BoundaryToken(token)
					parserState.NextState =   cls.statePossibleVariableAssignment
					return
				elif (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

		@classmethod
		def statePossibleVariableAssignment(cls, parserState):
			token = parserState.Token
			if (isinstance(token, CharacterToken) and (token == "=")):
				parserState.NewToken =      VariableAssignmentKeyword(parserState.TokenMarker)
				parserState.TokenMarker =   parserState.NewToken
				parserState.NextState =     cls.stateVariableAssignment
				return

			raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

		@classmethod
		def stateVariableAssignment(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ':=' or whitespace after type mark."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace5
					parserState.PushState = EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace5
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState = cls.stateWhitespace5
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState = cls.stateWhitespace5
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace5(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected expression after ':='."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock = ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NextState = cls.stateExpressionEnd
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateExpressionEnd(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ObjectDeclaration.ConstantBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

	class VariableBlock(Block): pass
	class SharedVariableBlock(Block): pass


class TypeBlock(Block): pass
class SubtypeBlock(Block): pass

class AttributeDeclarationBlock(Block): pass
class AttributeSpecificationBlock(Block): pass

class SignalAssignmentBlock(Block): pass
class VariableAssignmentBlock(Block): pass

class AssertStatementBlock(Block): pass
class ReportStatementBlock(Block): pass

class Instantiation(BlockGroup):
	class InstantiationBlock(Block): pass
	class InstantiationGenericMapBeginBlock(Block): pass
	class InstantiationGenericMapItemBlock(Block): pass
	class InstantiationGenericMapDelimiterBlock(Block): pass
	class InstantiationGenericMapEndBlock(Block): pass
	class InstantiationPortMapBeginBlock(Block): pass
	class InstantiationPortMapItemBlock(Block): pass
	class InstantiationPortMapDelimiterBlock(Block): pass
	class InstantiationPortMapEndBlock(Block): pass
	class InstantiationEndBlock(Block): pass

class PackageInstantiationBlock(Block): pass
class ProcedureInstantiationBlock(Block): pass
class FunctionInstantiationBlock(Block): pass

class Procedure(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateProcedureKeyword,
				self.stateWhitespace1,
				self.stateProcedureName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateProcedureKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword PROCEDURE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected procedure name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateProcedureName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateProcedureName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword PROCEDURE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after procedure name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Procedure.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Procedure.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Procedure.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Procedure.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			errorMessage = "Expected label or one of these keywords: if, case, for, while, return, report, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "if"):
					newToken =                IfKeyword(token)
					parserState.PushState =   If.IfConditionBlock.stateIfKeyword
				elif (keyword == "case"):
					newToken =                CaseKeyword(token)
					parserState.PushState =   Case.CaseBlock.stateCaseKeyword
				elif (keyword == "for"):
					newToken =                ForKeyword(token)
					parserState.PushState =   ForLoop.RangeBlock.stateForKeyword
				elif (keyword == "while"):
					newToken =                WhileKeyword(token)
					parserState.PushState =   WhileLoop.ConditionBlock.stateWhileKeyword
				elif (keyword == "return"):
					newToken =                ReturnKeyword(token)
					parserState.PushState =   ReturnBlock.stateReturnKeyword
				elif (keyword == "report"):
					newToken =                ReportKeyword(token)
					parserState.PushState =   ReportBlock.stateReportKeyword
				elif (keyword == "end"):
					newToken = EndKeyword(token)
					parserState.NextState =   Process.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken = newToken
				parserState.TokenMarker = newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateProcedureKeyword,
				self.stateWhitespace2,
				self.stateProcedureName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', PROCEDURE keyword or procedure name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "procedure"):
					parserState.NewToken =    ProcedureKeyword(token)
					parserState.NextState =   cls.stateProcedureKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateProcedureName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateProcedureKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or procedure name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateProcedureName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateProcedureName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Procedure.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class Function(BlockGroup):
	class NameBlock(Block):
		def RegisterStates(self):
			return [
				self.stateFunctionKeyword,
				self.stateWhitespace1,
				self.stateFunctionName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateFunctionKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword FUNCTION."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected function name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateFunctionName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateFunctionName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword FUNCTION."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after function name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Function.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Function.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Function.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Function.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			errorMessage = "Expected label or one of these keywords: if, case, for, while, return, report, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "if"):
					newToken =                IfKeyword(token)
					parserState.PushState =   If.IfConditionBlock.stateIfKeyword
				elif (keyword == "case"):
					newToken =                CaseKeyword(token)
					parserState.PushState =   Case.CaseBlock.stateCaseKeyword
				elif (keyword == "for"):
					newToken =                ForKeyword(token)
					parserState.PushState =   ForLoop.RangeBlock.stateForKeyword
				elif (keyword == "while"):
					newToken =                WhileKeyword(token)
					parserState.PushState =   WhileLoop.ConditionBlock.stateWhileKeyword
				elif (keyword == "return"):
					newToken =                ReturnKeyword(token)
					parserState.PushState =   ReturnBlock.stateReturnKeyword
				elif (keyword == "report"):
					newToken =                ReportKeyword(token)
					parserState.PushState =   ReportBlock.stateReportKeyword
				elif (keyword == "end"):
					newToken = EndKeyword(token)
					parserState.NextState =   Process.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken = newToken
				parserState.TokenMarker = newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateFunctionKeyword,
				self.stateWhitespace2,
				self.stateFunctionName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', FUNCTION keyword or function name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "function"):
					parserState.NewToken =    FunctionKeyword(token)
					parserState.NextState =   cls.stateFunctionKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateFunctionName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateFunctionKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or function name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateFunctionName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateFunctionName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Function.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class If(BlockGroup):
	class IfConditionBlock(Block):
		def RegisterStates(self):
			return [
				self.stateIfKeyword,
				self.stateWhitespace1,
				self.stateIfName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateIfKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword IF."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected if name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateIfName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateIfName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword IF."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after if name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      If.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = If.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ElsIfConditionBlock(Block):
		def RegisterStates(self):
			return [
				self.stateElsIfKeyword,
				self.stateWhitespace1,
				self.stateElsIfName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateElsIfKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ElsIf."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected elsIf name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    If.ElsIfBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.ElsIfBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateElsIfName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateElsIfName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ElsIf."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.ElsIfBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.ElsIfBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.ElsIfBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after elsIf name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      If.ElsIfBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = If.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ElseBlock(Block):
		def RegisterStates(self):
			return [
				self.stateElseKeyword,
				self.stateWhitespace1,
				self.stateElseName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateElseKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ELSE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected else name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateElseName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateElseName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword ELSE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after else name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      If.ElseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = If.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    If.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class Case(BlockGroup):
	class CaseBlock(Block):
		def RegisterStates(self):
			return [
				self.stateCaseKeyword,
				self.stateWhitespace1,
				self.stateCaseName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateCaseKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CASE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected case name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateCaseName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateCaseName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword CASE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after case name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      Case.NameBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = Case.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  Case.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = Case.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class CaseItemBlock(Block): pass
	class CaseOthersBlock(Block): pass
	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    Case.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class ContinueBlock(Block):
	def RegisterStates(self):
		return [
			self.stateContinueKeyword,
			self.stateWhitespace1,
			self.stateContinueName,
			self.stateWhitespace2,
			self.stateDeclarativeRegion
		]

	@classmethod
	def stateContinueKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword CONTINUE."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected continue name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateContinueName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateContinueName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword CONTINUE."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after continue name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      ContinueBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)


class BreakBlock(Block):
	def RegisterStates(self):
		return [
			self.stateBreakKeyword,
			self.stateWhitespace1,
			self.stateBreakName,
			self.stateWhitespace2,
			self.stateDeclarativeRegion
		]

	@classmethod
	def stateBreakKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword BREAK."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected break name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateBreakName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateBreakName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword BREAK."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after break name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      BreakBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)


class ReturnBlock(Block):
	def RegisterStates(self):
		return [
			self.stateReturnKeyword,
			self.stateWhitespace1,
			self.stateReturnName,
			self.stateWhitespace2,
			self.stateDeclarativeRegion
		]

	@classmethod
	def stateReturnKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword RETURN."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected return name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateReturnName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateReturnName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword RETURN."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after return name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      ReturnBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)


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

		raise ParserException(errorMessage, token)

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

		raise ParserException(errorMessage, token)

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

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after assert name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      AssertBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)


class ReportBlock(Block):
	def RegisterStates(self):
		return [
			self.stateReportKeyword,
			self.stateWhitespace1,
			self.stateReportName,
			self.stateWhitespace2,
			self.stateDeclarativeRegion
		]

	@classmethod
	def stateReportKeyword(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword REPORT."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace1
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NextState =     cls.stateWhitespace1
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace1(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected report name (identifier)."
		if isinstance(token, CharacterToken):
			if (token == "-"):
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, StringToken):
			parserState.NewToken =      IdentifierToken(token)
			parserState.NextState =     cls.stateReportName
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateReportName(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected whitespace after keyword REPORT."
		if isinstance(token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   EmptyLineBlock.stateLinebreak
				return
			elif (token == "-"):
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.NewBlock =    ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				parserState.TokenMarker = None
				parserState.NextState =   cls.stateWhitespace2
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NextState =     cls.stateWhitespace2
			return

		raise ParserException(errorMessage, token)

	@classmethod
	def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after report name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      ReportBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)


class ForLoop(BlockGroup):
	class RangeBlock(Block):
		def RegisterStates(self):
			return [
				self.stateForKeyword,
				self.stateWhitespace1,
				self.stateForName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateForKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword FOR."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected for name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateForName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateForName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword FOR."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after for name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      ForLoop.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = ForLoop.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ForLoopEndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class WhileLoop(BlockGroup):
	class ConditionBlock(Block):
		def RegisterStates(self):
			return [
				self.stateWhileKeyword,
				self.stateWhitespace1,
				self.stateWhileName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateWhileKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword WHILE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected while name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateWhileName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhileName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword WHILE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after while name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      WhileLoop.ConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = WhileLoop.EndBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class WhileLoopEndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    WhileLoop.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class IfGenerate(BlockGroup):
	class IfConditionBlock(Block):
		def RegisterStates(self):
			return [
				self.stateGenerateKeyword,
				self.stateWhitespace1,
				self.stateGenerateName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected generate name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after generate name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      IfGenerate.IfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = IfGenerate.EndGenerateBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  IfGenerate.IfGenerateBeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = IfGenerate.IfGenerateBeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class IfGenerateBeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected label or one of these keywords: assert, process."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				return
			# 	parserState.NewToken = IndentationToken(token)
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			# 	return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "process"):
					newToken =                ProcessKeyword(token)
					parserState.PushState =   Process.OpenBlock.stateProcessKeyword
				elif (keyword == "assert"):
					newToken =                AssertKeyword(token)
					parserState.PushState =   AssertBlock.stateAssertKeyword
				elif (keyword == "end"):
					newToken =                EndKeyword(token)
					parserState.NextState =   IfGenerate.EndGenerateBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ElsIfConditionBlock(Block):
		def RegisterStates(self):
			return [
				self.stateGenerateKeyword,
				self.stateWhitespace1,
				self.stateGenerateName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected generate name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after generate name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      IfGenerate.ElsIfConditionBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = IfGenerate.EndGenerateBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  IfGenerate.ElsIfGenerateBeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = IfGenerate.ElsIfGenerateBeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ElsIfGenerateBeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected label or one of these keywords: assert, process."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				return
			# 	parserState.NewToken = IndentationToken(token)
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			# 	return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "process"):
					newToken =                ProcessKeyword(token)
					parserState.PushState =   Process.OpenBlock.stateProcessKeyword
				elif (keyword == "assert"):
					newToken =                AssertKeyword(token)
					parserState.PushState =   AssertBlock.stateAssertKeyword
				elif (keyword == "end"):
					newToken =                EndKeyword(token)
					parserState.NextState =   IfGenerate.EndGenerateBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ElseGenerateBlock(Block):
		def RegisterStates(self):
			return [
				self.stateGenerateKeyword,
				self.stateWhitespace1,
				self.stateGenerateName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected generate name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after generate name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      IfGenerate.ElseGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = IfGenerate.EndGenerateBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  IfGenerate.ElseGenerateBeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = IfGenerate.ElseGenerateBeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class ElseGenerateBeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected label or one of these keywords: assert, process."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				return
			# 	parserState.NewToken = IndentationToken(token)
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			# 	return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "process"):
					newToken =                ProcessKeyword(token)
					parserState.PushState =   Process.OpenBlock.stateProcessKeyword
				elif (keyword == "assert"):
					newToken =                AssertKeyword(token)
					parserState.PushState =   AssertBlock.stateAssertKeyword
				elif (keyword == "end"):
					newToken =                EndKeyword(token)
					parserState.NextState =   IfGenerate.EndGenerateBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndGenerateBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    IfGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)

class CaseGenerate(BlockGroup):
	class CaseBlock(Block):
		def RegisterStates(self):
			return [
				self.stateGenerateKeyword,
				self.stateWhitespace1,
				self.stateGenerateName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected generate name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after generate name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      CaseGenerate.CaseBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = CaseGenerate.EndBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  CaseGenerate.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = CaseGenerate.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block): pass

	class EndBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    CaseGenerate.EndBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)


class ForGenerate(BlockGroup):
	class RangeBlock(Block):
		def RegisterStates(self):
			return [
				self.stateGenerateKeyword,
				self.stateWhitespace1,
				self.stateGenerateName,
				self.stateWhitespace2,
				self.stateDeclarativeRegion
			]

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected generate name (identifier)."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =      IdentifierToken(token)
				parserState.NextState =     cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected whitespace after keyword GENERATE."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected keyword IS after generate name."
			if isinstance(token, CharacterToken):
				if (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif (isinstance(token, StringToken) and (token <= "is")):
				parserState.NewToken =      IsKeyword(token)
				parserState.NewBlock =      ForGenerate.RangeBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
				parserState.NextState =     cls.stateDeclarativeRegion
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateDeclarativeRegion(cls, parserState):
			errorMessage = "Expected one of these keywords: generic, port, begin, end."
			token = parserState.Token
			if isinstance(parserState.Token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      IndentationToken(token)
				parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "generic"):
					newToken =              GenericKeyword(token)
					parserState.PushState = GenericList.OpenBlock.stateGenericKeyword
				elif (keyword == "port"):
					newToken =              PortKeyword(token)
					parserState.PushState = PortList.OpenBlock.statePortKeyword
				elif (keyword == "end"):
					newToken =              EndKeyword(token)
					parserState.NextState = ForGenerate.EndGenerateBlock.stateEndKeyword
				elif (keyword == "begin"):
					parserState.NewToken =  BeginKeyword(token)
					parserState.NewBlock =  ForGenerate.BeginBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.NextState = ForGenerate.BeginBlock.stateBeginKeyword
					return
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class BeginBlock(Block):
		def RegisterStates(self):
			return [
				self.stateBeginKeyword
			]

		@classmethod
		def stateBeginKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected label or one of these keywords: assert, process."
			if isinstance(token, CharacterToken):
				if (token == "\n"):
					parserState.NewToken = LinebreakToken(token)
					parserState.NewBlock = EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
					parserState.TokenMarker = parserState.NewToken
					return
				elif (token == "-"):
					parserState.PushState = SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.PushState = MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				return
			# 	parserState.NewToken = IndentationToken(token)
			# 	parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			# 	return
			elif isinstance(token, StringToken):
				keyword = token.Value.lower()
				if (keyword == "process"):
					newToken =                ProcessKeyword(token)
					parserState.PushState =   Process.OpenBlock.stateProcessKeyword
				elif (keyword == "assert"):
					newToken =                AssertKeyword(token)
					parserState.PushState =   AssertBlock.stateAssertKeyword
				elif (keyword == "end"):
					newToken =                EndKeyword(token)
					parserState.NextState =   ForGenerate.EndGenerateBlock.stateEndKeyword
				else:
					raise ParserException(errorMessage, token)

				parserState.NewToken =      newToken
				parserState.TokenMarker =   newToken
				return

			raise ParserException(errorMessage, token)

	class EndGenerateBlock(Block):
		def RegisterStates(self):
			return [
				self.stateEndKeyword,
				self.stateWhitespace1,
				self.stateGenerateKeyword,
				self.stateWhitespace2,
				self.stateGenerateName,
				self.stateWhitespace3
			]

		@classmethod
		def stateEndKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace1
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace1(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';', GENERATE keyword or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    LibraryBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				if (token <= "generate"):
					parserState.NewToken =    GenerateKeyword(token)
					parserState.NextState =   cls.stateGenerateKeyword
				else:
					parserState.NewToken =    IdentifierToken(token)
					parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateKeyword(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace1
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NewToken =      BoundaryToken(token)
				parserState.NextState =     cls.stateWhitespace2
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateWhitespace2(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or generate name."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, StringToken):
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.stateGenerateName
				return

			raise ParserException(errorMessage, token)

		@classmethod
		def stateGenerateName(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';' or whitespace."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "\n"):
					parserState.NewToken =    LinebreakToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   EmptyLineBlock.stateLinebreak
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.NextState =   cls.stateWhitespace2
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
			elif isinstance(token, SpaceToken):
				parserState.NextState =     cls.stateWhitespace3
				return

		@classmethod
		def stateWhitespace3(cls, parserState):
			token = parserState.Token
			errorMessage = "Expected ';'."
			if isinstance(token, CharacterToken):
				if (token == ";"):
					parserState.NewToken =    EndToken(token)
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
					parserState.Pop()
					return
				elif (token == "-"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return
				elif (token == "/"):
					parserState.NewBlock =    ForGenerate.EndGenerateBlock(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
					parserState.TokenMarker = None
					parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
					parserState.TokenMarker = token
					return

			raise ParserException(errorMessage, token)
