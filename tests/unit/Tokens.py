from unittest import TestCase

from pyVHDLParser.Token import StartOfDocumentToken, WordToken, SpaceToken, LinebreakToken, IndentationToken, CharacterToken, CharacterLiteralToken, StringLiteralToken, BitStringLiteralToken, FusedCharacterToken, RealLiteralToken, IntegerLiteralToken, EndOfDocumentToken, ExtendedIdentifier, SingleLineCommentToken, MultiLineCommentToken
from tests.unit import Struct3, Struct1, TokenSequence


class Sequence_1(TestCase, Struct3, TokenSequence):
#	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> ?<= ?>= <>"
	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> <>"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
			(WordToken,           "a"),
			(SpaceToken,          " "),
			(WordToken,           "bbb"),
			(SpaceToken,          " "),
			(IntegerLiteralToken, "1"),
			(SpaceToken,          " "),
			(IntegerLiteralToken, "23"),
			(SpaceToken,          " "),
			(RealLiteralToken,    "3.4"),
			(SpaceToken,          " "),
			(RealLiteralToken,    "45.6"),
			(SpaceToken,          " "),
			(RealLiteralToken,    "5.67"),
			(SpaceToken,          " "),
			(RealLiteralToken,    "67.89"),
			(SpaceToken,          " "),
			(RealLiteralToken,    ".7"),
			(SpaceToken,          " "),
			(RealLiteralToken,    ".89"),
			(SpaceToken,          " "),
			(CharacterToken,      "("),
			(SpaceToken,          " "),
			(CharacterToken,      ")"),
			(SpaceToken,          " "),
			(CharacterToken,      "<"),
			(SpaceToken,          " "),
			(CharacterToken,      ">"),
			(SpaceToken,          " "),
			(CharacterToken,      "="),
			(SpaceToken,          " "),
			(CharacterToken,      "."),
			(SpaceToken,          " "),
			(CharacterToken,      ","),
			(SpaceToken,          " "),
			(CharacterToken,      ";"),
			(SpaceToken,          " "),
			(CharacterToken,      "&"),
			(SpaceToken,          " "),
			(CharacterToken,      "/"),
			(SpaceToken,          " "),
			(CharacterToken,      "+"),
			(SpaceToken,          " "),
			(CharacterToken,      "-"),
			(SpaceToken,          " "),
			(CharacterToken,      "*"),
			(SpaceToken,          " "),
#			(CharacterToken,      "'"),
#			(SpaceToken,          " "),
			(FusedCharacterToken, "<<"),
			(SpaceToken,          " "),
			(FusedCharacterToken, ">>"),
			(SpaceToken,          " "),
			(FusedCharacterToken, "/="),
			(SpaceToken,          " "),
			(FusedCharacterToken, "<="),
			(SpaceToken,          " "),
			(FusedCharacterToken, ">="),
			(SpaceToken,          " "),
			(FusedCharacterToken, "=>"),
			(SpaceToken,          " "),
			(FusedCharacterToken, ":="),
			(SpaceToken,          " "),
			(FusedCharacterToken, "**"),
			(SpaceToken,          " "),
			(FusedCharacterToken, "?="),
			(SpaceToken,          " "),
			(FusedCharacterToken, "?/="),
			(SpaceToken,          " "),
			(FusedCharacterToken, "?<"),
			(SpaceToken,          " "),
			(FusedCharacterToken, "?>"),
#			(SpaceToken,          " "),
#			(FusedCharacterToken, "?<="),
#			(SpaceToken,          " "),
#			(FusedCharacterToken, "?>="),
			(SpaceToken,          " "),
			(FusedCharacterToken, "<>"),
			(EndOfDocumentToken, None)
		]
	)

class Sequence_2(TestCase, Struct3, TokenSequence):
	code = """abc   \def\ \t 'a' "abc" /* help */ -- foo\n"""
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
			(WordToken,               "abc"),
			(SpaceToken,              "   "),
			(ExtendedIdentifier,      "\\def\\"),
			(SpaceToken,              " \t "),
			(CharacterLiteralToken,   "a"),
			(SpaceToken,              " "),
			(StringLiteralToken,      "abc"),
			(SpaceToken,              " "),
			(MultiLineCommentToken,   "/* help */"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- foo\n"),
			(EndOfDocumentToken, None)
		]
	)
