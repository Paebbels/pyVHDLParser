# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
#
# ==============================================================================
# Authors:          Patrick Lehmann
#
# Python Module:    TODO
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
from enum             import Enum

from pyVHDLParser.Base         import ParserException
from pyVHDLParser.Token.Tokens import CharacterToken, StartOfDocumentToken, SpaceToken, StringToken, NumberToken, EndOfDocumentToken, SourceCodePosition


class TokenizerException(ParserException):
	def __init__(self, message, position):
		super().__init__(message)
		self.Position = position

	def __str__(self):
		return "{0!s}: {1}".format(self.Position, self._message)


class Tokenizer:
	class TokenKind(Enum):
		SpaceChars =      0
		AlphaChars =      1
		NumberChars =     2
		DelimiterChars =  3
		OtherChars =      4

	__ALPHA_CHARS__ =   "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	__NUMBER_CHARS__ =  "0123456789"
	__SPACE_CHARS__ =   " \t"

	@classmethod
	def GetWordTokenizer(cls, iterable, alphaCharacters=__ALPHA_CHARS__, numberCharacters=__NUMBER_CHARS__, whiteSpaceCharacters=__SPACE_CHARS__):
		previousToken = StartOfDocumentToken()
		tokenKind =     cls.TokenKind.OtherChars
		start =         SourceCodePosition(1, 1, 1)
		buffer =        ""
		absolute =      0
		column =        0
		row =           1

		yield previousToken

		for char in iterable:
			absolute +=   1
			column +=     1

			# State: SpaceChars
			if (tokenKind is cls.TokenKind.SpaceChars):
				if (char in whiteSpaceCharacters):
					buffer += char
				else:
					previousToken = SpaceToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken

					start =   SourceCodePosition(row, column, absolute)
					buffer =  char
					if (char in alphaCharacters):       tokenKind = cls.TokenKind.AlphaChars
					elif (char in numberCharacters):    tokenKind = cls.TokenKind.NumberChars
					else:
						tokenKind = cls.TokenKind.OtherChars
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken

			# State: AlphaChars
			elif (tokenKind is cls.TokenKind.AlphaChars):
				if (char in alphaCharacters):
					buffer += char
				else:
					previousToken = StringToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken

					start =   SourceCodePosition(row, column, absolute)
					buffer =  char
					if (char in whiteSpaceCharacters):  tokenKind = cls.TokenKind.SpaceChars
					elif (char in numberCharacters):    tokenKind = cls.TokenKind.NumberChars
					else:
						tokenKind = cls.TokenKind.OtherChars
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken

			# State: NumberChars
			elif (tokenKind is cls.TokenKind.NumberChars):
				if (char in numberCharacters):
					buffer += char
				else:
					previousToken = NumberToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken

					start =   SourceCodePosition(row, column, absolute)
					buffer =  char
					if (char in whiteSpaceCharacters):  tokenKind = cls.TokenKind.SpaceChars
					elif (char in alphaCharacters):     tokenKind = cls.TokenKind.AlphaChars
					else:
						tokenKind = cls.TokenKind.OtherChars
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken

			# State: OtherChars
			elif (tokenKind is cls.TokenKind.OtherChars):
				start =     SourceCodePosition(row, column, absolute)
				buffer =    char
				if (char in whiteSpaceCharacters):    tokenKind =   cls.TokenKind.SpaceChars
				elif (char in alphaCharacters):       tokenKind =   cls.TokenKind.AlphaChars
				elif (char in numberCharacters):      tokenKind =   cls.TokenKind.NumberChars
				else:
					previousToken = CharacterToken(previousToken, char, start)
					yield previousToken

			# State: unknown
			else:
				raise TokenizerException("Unknown state.", SourceCodePosition(row, column, absolute))

			if (char == "\n"):
				column =  0
				row +=    1
		# end for

		# End of document
		yield EndOfDocumentToken(previousToken, SourceCodePosition(row, column, absolute))
