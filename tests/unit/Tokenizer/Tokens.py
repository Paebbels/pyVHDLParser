from unittest import TestCase

from pyVHDLParser.Token           import StartOfDocumentToken, WordToken, SpaceToken, LinebreakToken, IndentationToken, CharacterToken, CharacterLiteralToken, StringLiteralToken, BitStringLiteralToken, FusedCharacterToken, RealLiteralToken, IntegerLiteralToken, EndOfDocumentToken, ExtendedIdentifier, SingleLineCommentToken, MultiLineCommentToken
from pyVHDLParser.Token.Keywords  import EntityKeyword
from pyVHDLParser.Token.Parser    import Tokenizer, TokenizerException

from tests.unit.Common            import ExpectedDataMixin, ExpectedTokenStream, TokenSequence


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Sequence_1(TestCase, ExpectedDataMixin, TokenSequence):
#	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> ?<= ?>= <>"
	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> <> "
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
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
			(SpaceToken,          " "),    # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
			(EndOfDocumentToken, None)
		]
	)

class Sequence_2(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc   \\def\\ \t 'a' "abc" /* help */ -- foo\n """
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
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
			(SpaceToken,              " "),    # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
			(EndOfDocumentToken, None)
		]
	)

class Sequence_3(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc\n123\n456.789\n'Z'\n"Hallo"\n\\foo\\\n-- comment\n/* comment */\n;\n  \nabc\r\n123\r\n456.789\r\n'Z'\r\n"Hallo"\r\n\\foo\\\r\n-- comment\r\n/* comment */\r\n;\r\n  \r\n\tabc """
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
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
			(SpaceToken,              " "),
			(EndOfDocumentToken, None)
		]
	)

class Sequence_4(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc-- comment\n123-- comment\n456.789-- comment\n'Z'-- comment\n"Hallo"-- comment\n\\foo\\-- comment\n-- comment\n/* comment */-- comment\n;-- comment\n  -- comment\n """
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken,    None),
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
			(SpaceToken,              " "),    # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
			(EndOfDocumentToken,      None)
		]
	)

class Sequence_5(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc/* comment */123/* comment */456.789/* comment */'Z'/* comment */"Hallo"/* comment */\\foo\\/* comment */-- comment\n/* comment *//* comment */;/* comment */  /* comment */ """
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken,   None),
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
			(SpaceToken,              " "),    # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
			(EndOfDocumentToken,     None)
		]
	)

class Tokenizer_ExceptionInKeyword(TestCase, ExpectedDataMixin, TokenSequence):
	code = """keyword"""
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "keyword"),
			(EndOfDocumentToken,   None)
		]
	)

	def test_KeywordToWordTokenMissmatch(self) -> None:
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)
		tokenIterator = iter(tokenStream)
		token = next(tokenIterator)
		self.assertIsInstance(
			token, StartOfDocumentToken,
			msg="Token has not expected type.\n  Actual:   {actual}     pos={pos!s}\n  Expected: {expected}".format(
				actual=token.__class__.__qualname__,
				pos=token.Start,
				expected=StartOfDocumentToken.__qualname__
			)
		)

		token = next(tokenIterator)
		keywordToken = token
		self.assertIsInstance(
			token, WordToken,
			msg="Token has not expected type.\n  Actual:   {actual}     pos={pos!s}\n  Expected: {expected}".format(
				actual=token.__class__.__qualname__,
				pos=token.Start,
				expected=StartOfDocumentToken.__qualname__
			)
		)
		self.assertTrue(
			token == "keyword",
			msg="The token's value does not match.\n  Context:  {context}\n  Actual:   {actual}\n  Expected: {expected}".format(
				context="at {pos!s}".format(pos=token.Start),
				actual="'{token!r}' of {type}".format(token=token, type=token.__class__.__qualname__),
				expected="'{value}' of {type}".format(value="keyword", type=WordToken.__qualname__)
			)
		)

		token = next(tokenIterator)
		self.assertIsInstance(
			token, EndOfDocumentToken,
			msg="Token has not expected type.\n  Actual:   {actual}     pos={pos!s}\n  Expected: {expected}".format(
				actual=token.__class__.__qualname__,
				pos=token.Start,
				expected=EndOfDocumentToken.__qualname__
			)
		)

		with self.assertRaises(TokenizerException) as ex:
			_ = EntityKeyword(keywordToken)
		# TODO: check exception message
