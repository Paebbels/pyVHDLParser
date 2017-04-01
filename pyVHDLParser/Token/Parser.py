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
# Copyright 2007-2017 Patrick Lehmann - Dresden, Germany
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
from enum                     import Enum

from pyVHDLParser             import SourceCodePosition
from pyVHDLParser.Base        import ParserException
from pyVHDLParser.Token import StartOfDocumentToken, EndOfDocumentToken, IndentationToken, FusedCharacterToken, \
	LiteralToken, StringLiteralToken, ExtendedIdentifier, DirectiveToken
from pyVHDLParser.Token       import CharacterToken, SpaceToken, StringToken, SingleLineCommentToken, MultiLineCommentToken, LinebreakToken


class TokenizerException(ParserException):
	def __init__(self, message, position):
		super().__init__(message)
		self.Position = position

	def __str__(self):
		return "{0!s}: {1}".format(self.Position, self._message)


class Tokenizer:
	class TokenKind(Enum):
		SpaceChars =                      0
		AlphaChars =                      1
		NumberChars =                     2
		DelimiterChars =                  3
		PossibleSingleLineCommentStart =  4
		PossibleLinebreak =               5
		PossibleLiteral =            6
		PossibleStringLiteralStart =      7
		PossibleExtendedIdentifierStart =       8
		SingleLineComment =               9
		MultiLineComment =               10
		Linebreak =                      11
		Directive =                      12
		FuseableCharacter =              13
		OtherChars =                     14


	@classmethod
	def GetWordTokenizer(cls, iterable):
		previousToken = StartOfDocumentToken()
		tokenKind =     cls.TokenKind.OtherChars
		start =         SourceCodePosition(1, 1, 1)
		buffer =        ""
		absolute =      0
		column =        0
		row =           1

		__ALPHA_CHARACTERS__ =      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"
		__WHITESPACE_CHARACTERS__ = " \t"
		__FUSEABLE_CHARS__ =        "=<:/*>?"

		yield previousToken

		for char in iterable:
			absolute +=   1
			column +=     1

			# State: SpaceChars
			if (tokenKind is cls.TokenKind.SpaceChars):
				if (char in __WHITESPACE_CHARACTERS__):
					buffer += char
				else:
					end = SourceCodePosition(row, column - 1, absolute - 1)
					if isinstance(previousToken, (LinebreakToken, SingleLineCommentToken)):
						previousToken = IndentationToken(previousToken, buffer, start, end)
					else:
						previousToken = SpaceToken(previousToken, buffer, start, end)
					yield previousToken

					start =   SourceCodePosition(row, column, absolute)
					buffer =  char
					if (char in __ALPHA_CHARACTERS__):    tokenKind = cls.TokenKind.AlphaChars
					elif (char == "'"):                   tokenKind = cls.TokenKind.PossibleLiteral
					elif (char == "\""):                  tokenKind = cls.TokenKind.PossibleStringLiteralStart
					elif (char == "-"):                   tokenKind = cls.TokenKind.PossibleSingleLineCommentStart
					elif (char == "\r"):                  tokenKind = cls.TokenKind.PossibleLinebreak
					elif (char == "\n"):
						previousToken = LinebreakToken(previousToken, char, start, start)
						yield previousToken
						tokenKind = cls.TokenKind.OtherChars
					elif (char in __FUSEABLE_CHARS__):
						buffer =        char
						tokenKind =     cls.TokenKind.FuseableCharacter
					elif (char == "\\"):                   tokenKind = cls.TokenKind.PossibleExtendedIdentifierStart
					elif ((char == "`") and isinstance(previousToken, (SpaceToken, LinebreakToken))):
						tokenKind = cls.TokenKind.Directive
					else:
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
						tokenKind =     cls.TokenKind.OtherChars

			# State: AlphaChars
			elif (tokenKind is cls.TokenKind.AlphaChars):
				if (char in __ALPHA_CHARACTERS__):
					buffer += char
				else:
					previousToken = StringToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken

					start =   SourceCodePosition(row, column, absolute)
					buffer =  char
					if (char in __WHITESPACE_CHARACTERS__): tokenKind = cls.TokenKind.SpaceChars
					elif (char == "'"):                     tokenKind = cls.TokenKind.PossibleLiteral
					elif (char == "\""):                    tokenKind = cls.TokenKind.PossibleStringLiteralStart
					elif (char == "-"):                     tokenKind = cls.TokenKind.PossibleSingleLineCommentStart
					elif (char == "\r"):                    tokenKind = cls.TokenKind.PossibleLinebreak
					elif (char == "\n"):
						previousToken = LinebreakToken(previousToken, char, start, start)
						yield previousToken
						tokenKind = cls.TokenKind.OtherChars
					elif (char in __FUSEABLE_CHARS__):
						buffer =        char
						tokenKind =     cls.TokenKind.FuseableCharacter
					elif (char == "\\"):                     tokenKind = cls.TokenKind.PossibleExtendedIdentifierStart
					elif ((char == "`") and isinstance(previousToken, (SpaceToken, LinebreakToken))):
						tokenKind = cls.TokenKind.Directive
					else:
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
						tokenKind =     cls.TokenKind.OtherChars

			# State: PossibleSingleLineCommentStart
			elif (tokenKind is cls.TokenKind.PossibleSingleLineCommentStart):
				if (char == "-"):
					buffer =    "--"
					tokenKind = cls.TokenKind.SingleLineComment
				else:
					previousToken = CharacterToken(previousToken, "-", start)
					yield previousToken

					buffer =        char
					if (char in __WHITESPACE_CHARACTERS__): tokenKind = cls.TokenKind.SpaceChars
					elif (char in __ALPHA_CHARACTERS__):    tokenKind = cls.TokenKind.AlphaChars
					elif (char == "'"):                     tokenKind = cls.TokenKind.PossibleLiteral
					elif (char == "\""):                    tokenKind = cls.TokenKind.PossibleStringLiteralStart
					elif (char == "/r"):                    tokenKind = cls.TokenKind.PossibleLinebreak
					elif (char == "/n"):
						previousToken = LinebreakToken(previousToken, char, start, start)
						yield previousToken
						tokenKind =     cls.TokenKind.OtherChars
					elif (char in __FUSEABLE_CHARS__):
						buffer =        char
						tokenKind =     cls.TokenKind.FuseableCharacter
					elif (char == "\\"):                     tokenKind = cls.TokenKind.PossibleExtendedIdentifierStart
					elif ((char == "`") and isinstance(previousToken, (SpaceToken, LinebreakToken))):
						tokenKind =     cls.TokenKind.Directive
					else:
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
						tokenKind = cls.TokenKind.OtherChars

			# State: PossibleLinebreak
			elif (tokenKind is cls.TokenKind.PossibleLinebreak):
				end = SourceCodePosition(row, column, absolute)
				if (char == "\n"):
					tokenKind = cls.TokenKind.OtherChars
					if (buffer[:2] == "--"):
						buffer += char
						previousToken = SingleLineCommentToken(previousToken, buffer, start, end)
					else:
						previousToken = LinebreakToken(previousToken, "\r\n", start, end)
					buffer = "\r\n"
					yield previousToken
				else:
					previousToken = LinebreakToken(previousToken, "\r", start, end)
					yield previousToken

					start =   end
					buffer =  char
					if (char in __WHITESPACE_CHARACTERS__): tokenKind = cls.TokenKind.SpaceChars
					elif (char in __ALPHA_CHARACTERS__):    tokenKind = cls.TokenKind.AlphaChars
					elif (char == "'"):                     tokenKind = cls.TokenKind.PossibleLiteral
					elif (char == "\""):                    tokenKind = cls.TokenKind.PossibleStringLiteralStart
					elif (char == "-"):                     tokenKind = cls.TokenKind.PossibleSingleLineCommentStart
					elif (char == "/r"):                    tokenKind = cls.TokenKind.PossibleLinebreak
					elif (char == "/n"):
						previousToken = LinebreakToken(previousToken, char, start, start)
						yield previousToken
						tokenKind =     cls.TokenKind.OtherChars
					elif (char in __FUSEABLE_CHARS__):
						buffer =        char
						tokenKind =     cls.TokenKind.FuseableCharacter
					elif (char == "\\"):                     tokenKind = cls.TokenKind.PossibleExtendedIdentifierStart
					elif ((char == "`") and isinstance(previousToken, (SpaceToken, LinebreakToken))):
						tokenKind =     cls.TokenKind.Directive
					else:
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken
						tokenKind =     cls.TokenKind.OtherChars

			# State: PossibleLiteral
			elif (tokenKind is cls.TokenKind.PossibleLiteral):
				buffer += char
				if (len(buffer) == 2):
					if (buffer[1] == "'"):
						previousToken =   CharacterToken(previousToken, "'", start)
						yield previousToken
						previousToken =   CharacterToken(previousToken, "'", SourceCodePosition(row, column, absolute))
						yield previousToken
						tokenKind =       cls.TokenKind.OtherChars
					else:
						continue
				elif ((len(buffer) == 3) and (buffer[2] == "'")):
					previousToken =   LiteralToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind = cls.TokenKind.OtherChars
				else:
					previousToken =   CharacterToken(previousToken, "'", start)
					yield previousToken

					start.Column +=   1
					start.Absolute += 1
					buffer =          buffer[:2]
					if ((buffer[0] in __ALPHA_CHARACTERS__) and (buffer[1] in __ALPHA_CHARACTERS__)):
						tokenKind =     cls.TokenKind.AlphaChars
					elif ((buffer[0] in __WHITESPACE_CHARACTERS__) and (buffer[1] in __WHITESPACE_CHARACTERS__)):
						tokenKind =     cls.TokenKind.SpaceChars
					else:
						raise TokenizerException("Ambiguous syntax detected.", start)

			# State: PossibleStringLiteralStart
			elif (tokenKind is cls.TokenKind.PossibleStringLiteralStart):
				buffer += char
				if (char == "\""):
					previousToken = StringLiteralToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind = cls.TokenKind.OtherChars

			# State: PossibleExtendedIdentifierStart
			elif (tokenKind is cls.TokenKind.PossibleExtendedIdentifierStart):
				buffer += char
				if (char == "\\"):
					previousToken = ExtendedIdentifier(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind =     cls.TokenKind.OtherChars

			# State: Directive
			elif (tokenKind is cls.TokenKind.Directive):
				buffer += char
				if (char == "\r"):
					tokenKind =     cls.TokenKind.PossibleLinebreak
				elif (char == "\n"):
					previousToken = DirectiveToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind =     cls.TokenKind.OtherChars

			# State: SingleLineComment
			elif (tokenKind is cls.TokenKind.SingleLineComment):
				buffer += char
				if (char == "\r"):
					tokenKind =     cls.TokenKind.PossibleLinebreak
				elif (char == "\n"):
					previousToken = SingleLineCommentToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind =     cls.TokenKind.OtherChars

			# State: MultiLineComment
			elif (tokenKind is cls.TokenKind.MultiLineComment):
				buffer += char
				if (buffer[-2:] == "*/"):
					previousToken = MultiLineCommentToken(previousToken, buffer, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind =     cls.TokenKind.OtherChars

			# State: FuseableCharacter
			elif (tokenKind is cls.TokenKind.FuseableCharacter):
				fused = buffer + char
				if (fused in ("=>", "**", ":=", "/=", "<=", ">=", "<>", "??", "?=", "<<", ">>", "?/=", "?<=", "?>=")):
					previousToken = FusedCharacterToken(previousToken, fused, start, SourceCodePosition(row, column, absolute))
					yield previousToken
					tokenKind = cls.TokenKind.OtherChars
				elif (fused in ("?/", "?<", "?>")):
					buffer =    fused
				elif (fused == "/*"):
					buffer =    fused
					tokenKind = cls.TokenKind.MultiLineComment
				else:
					previousToken = CharacterToken(previousToken, buffer[0], start)
					yield previousToken
					if (len(buffer) == 2):
						previousToken = CharacterToken(previousToken, buffer[1], start)
						yield previousToken

					buffer = char
					if (char in __ALPHA_CHARACTERS__):        tokenKind = cls.TokenKind.AlphaChars
					elif (char in __WHITESPACE_CHARACTERS__): tokenKind = cls.TokenKind.SpaceChars
					elif (char == "'"):                       tokenKind = cls.TokenKind.PossibleLiteral
					elif (char == "\""):                      tokenKind = cls.TokenKind.PossibleStringLiteralStart
					elif (char == "-"):                       tokenKind = cls.TokenKind.PossibleSingleLineCommentStart
					elif (char == "\r"):                      tokenKind = cls.TokenKind.PossibleLinebreak
					elif (char == "\n"):
						previousToken = LinebreakToken(previousToken, char, start, start)
						yield previousToken
						tokenKind = cls.TokenKind.OtherChars
					elif (char in __FUSEABLE_CHARS__):        pass
					elif (char == "\\"):                       tokenKind = cls.TokenKind.PossibleExtendedIdentifierStart
					elif ((char == "`") and isinstance(previousToken, (SpaceToken, LinebreakToken))):
						tokenKind = cls.TokenKind.Directive
					else:
						previousToken = CharacterToken(previousToken, char, start)
						yield previousToken

			# State: OtherChars
			elif (tokenKind is cls.TokenKind.OtherChars):
				start =     SourceCodePosition(row, column, absolute)
				buffer =    char
				if (char in __ALPHA_CHARACTERS__):        tokenKind = cls.TokenKind.AlphaChars
				elif (char in __WHITESPACE_CHARACTERS__): tokenKind = cls.TokenKind.SpaceChars
				elif (char == "'"):                       tokenKind = cls.TokenKind.PossibleLiteral
				elif (char == "\""):                      tokenKind = cls.TokenKind.PossibleStringLiteralStart
				elif (char == "-"):                       tokenKind = cls.TokenKind.PossibleSingleLineCommentStart
				elif (char == "\r"):                      tokenKind = cls.TokenKind.PossibleLinebreak
				elif (char == "\n"):
					previousToken = LinebreakToken(previousToken, char, start, start)
					yield previousToken
					tokenKind = cls.TokenKind.OtherChars
				elif (char in __FUSEABLE_CHARS__):
					buffer =        char
					tokenKind =     cls.TokenKind.FuseableCharacter
				elif (char == "\\"):                       tokenKind = cls.TokenKind.PossibleExtendedIdentifierStart
				elif ((char == "`") and isinstance(previousToken, (SpaceToken, LinebreakToken))):
					tokenKind =     cls.TokenKind.Directive
				else:
					tokenKind =     cls.TokenKind.OtherChars
					previousToken = CharacterToken(previousToken, char, start)
					yield previousToken

			# State: unknown
			else:
				raise TokenizerException("Unknown state.", SourceCodePosition(row, column, absolute))

			if (char == "\n"):
				column =  0
				row +=    1
		# end for

		if (tokenKind is cls.TokenKind.MultiLineComment):
			raise TokenizerException("End of document before end of multi line comment.", SourceCodePosition(row, column, absolute))

		# End of document
		yield EndOfDocumentToken(previousToken, SourceCodePosition(row, column, absolute))
