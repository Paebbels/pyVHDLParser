from unittest import TestCase

from pyVHDLParser.Token import StartOfDocumentToken, WordToken, SpaceToken, LinebreakToken, IndentationToken, CharacterToken, CharacterLiteralToken, StringLiteralToken, BitStringLiteralToken, FusedCharacterToken, RealLiteralToken, IntegerLiteralToken, EndOfDocumentToken, ExtendedIdentifier, SingleLineCommentToken, MultiLineCommentToken
from tests.unit import ExpectedDataMixin, ExpectedTokenStream, TokenSequence


class Sequence_1(TestCase, ExpectedDataMixin, TokenSequence):
#	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> ?<= ?>= <>"
	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> <>"
	tokenstream = ExpectedTokenStream(
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

class Sequence_2(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc   \def\ \t 'a' "abc" /* help */ -- foo\n"""
	tokenstream = ExpectedTokenStream(
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

class Sequence_3(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc\n123\n456.789\n'Z'\n"Hallo"\n\\foo\\\n-- comment\n/* comment */\n;\n  \nabc\r\n123\r\n456.789\r\n'Z'\r\n"Hallo"\r\n\\foo\\\r\n-- comment\r\n/* comment */\r\n;\r\n  \r\n\tabc """
	tokenstream = ExpectedTokenStream(
		tokenList=[
			(StartOfDocumentToken, None),
			(WordToken,               "abc"),
			(LinebreakToken,          None),
			(IntegerLiteralToken,     "123"),
			(LinebreakToken,          None),
			(RealLiteralToken,        "456.789"),
			(LinebreakToken,          None),
			(CharacterLiteralToken,   "Z"),
			(LinebreakToken,          None),
			(StringLiteralToken,      "Hallo"),
			(LinebreakToken,          None),
			(ExtendedIdentifier,      "\\foo\\"),
			(LinebreakToken,          None),
			(SingleLineCommentToken,  "-- comment\n"),
#			(LinebreakToken,          None),
			(MultiLineCommentToken,   "/* comment */"),
			(LinebreakToken,          None),
			(CharacterToken,          ";"),
			(LinebreakToken,          None),
			(IndentationToken,        "  "),
			(LinebreakToken,          None),
			(WordToken,               "abc"),
			(LinebreakToken,          None),
			(IntegerLiteralToken,     "123"),
			(LinebreakToken,          None),
			(RealLiteralToken,        "456.789"),
			(LinebreakToken,          None),
			(CharacterLiteralToken,   "Z"),
			(LinebreakToken,          None),
			(StringLiteralToken,      "Hallo"),
			(LinebreakToken,          None),
			(ExtendedIdentifier,      "\\foo\\"),
			(LinebreakToken,          None),
			(SingleLineCommentToken,  "-- comment\r\n"),
#			(LinebreakToken,          None),
			(MultiLineCommentToken,   "/* comment */"),
			(LinebreakToken,          None),
			(CharacterToken,          ";"),
			(LinebreakToken,          None),
			(IndentationToken,        "  "),
			(LinebreakToken,          None),
			(IndentationToken,        "\t"),
			(WordToken,               "abc"),
			(EndOfDocumentToken, None)
		]
	)

class Sequence_4(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc-- comment\n123-- comment\n456.789-- comment\n'Z'-- comment\n"Hallo"-- comment\n\\foo\\-- comment\n-- comment\n/* comment */-- comment\n;-- comment\n  -- comment\n"""
	tokenstream = ExpectedTokenStream(
		tokenList=[
			(StartOfDocumentToken,    None),
			(WordToken,               "abc"),
			(SingleLineCommentToken,  "-- comment\n"),
			(IntegerLiteralToken,     "123"),
			(SingleLineCommentToken,  "-- comment\n"),
			(RealLiteralToken,        "456.789"),
			(SingleLineCommentToken,  "-- comment\n"),
			(CharacterLiteralToken,   "Z"),
			(SingleLineCommentToken,  "-- comment\n"),
			(StringLiteralToken,      "Hallo"),
			(SingleLineCommentToken,  "-- comment\n"),
			(ExtendedIdentifier,      "\\foo\\"),
			(SingleLineCommentToken,  "-- comment\n"),
			(SingleLineCommentToken,  "-- comment\n"),
			(MultiLineCommentToken,   "/* comment */"),
			(SingleLineCommentToken,  "-- comment\n"),
			(CharacterToken,          ";"),
			(SingleLineCommentToken,  "-- comment\n"),
			(IndentationToken,        "  "),
			(SingleLineCommentToken,  "-- comment\n"),
			(EndOfDocumentToken,      None)
		]
	)

class Sequence_5(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc/* comment */123/* comment */456.789/* comment */'Z'/* comment */"Hallo"/* comment */\\foo\\/* comment */-- comment\n/* comment *//* comment */;/* comment */  /* comment */"""
	tokenstream = ExpectedTokenStream(
		tokenList=[
			(StartOfDocumentToken,   None),
			(WordToken,              "abc"),
			(MultiLineCommentToken,  "/* comment */"),
			(IntegerLiteralToken,    "123"),
			(MultiLineCommentToken,  "/* comment */"),
			(RealLiteralToken,       "456.789"),
			(MultiLineCommentToken,  "/* comment */"),
			(CharacterLiteralToken,  "Z"),
			(MultiLineCommentToken,  "/* comment */"),
			(StringLiteralToken,     "Hallo"),
			(MultiLineCommentToken,  "/* comment */"),
			(ExtendedIdentifier,     "\\foo\\"),
			(MultiLineCommentToken,  "/* comment */"),
			(SingleLineCommentToken, "-- comment\n"),
			(MultiLineCommentToken,  "/* comment */"),
			(MultiLineCommentToken,  "/* comment */"),
			(CharacterToken,         ";"),
			(MultiLineCommentToken,  "/* comment */"),
			(SpaceToken,             "  "),
			(MultiLineCommentToken,  "/* comment */"),
			(EndOfDocumentToken,     None)
		]
	)
