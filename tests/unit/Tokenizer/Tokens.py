# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from unittest import TestCase

from pyVHDLParser.Token           import StartOfDocumentToken, WordToken, WhitespaceToken, LinebreakToken, IndentationToken, CharacterToken, CharacterLiteralToken, StringLiteralToken, BitStringLiteralToken, FusedCharacterToken, RealLiteralToken, IntegerLiteralToken, EndOfDocumentToken, ExtendedIdentifier, SingleLineCommentToken, MultiLineCommentToken
from pyVHDLParser.Token.Keywords  import EntityKeyword
from pyVHDLParser.Token.Parser    import Tokenizer, TokenizerException

from tests.unit.Common            import ExpectedDataMixin, ExpectedTokenStream, TokenSequence


if __name__ == "__main__":  # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Sequence_1(TestCase, ExpectedDataMixin, TokenSequence):
#	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> ?<= ?>= <>"
	code = "a bbb 1 23 3.4 45.6 5.67 67.89 .7 .89 ( ) < > = . , ; & / + - * << >> /= <= >= => := ** ?= ?/= ?< ?> <> "
	tokenStream = ExpectedTokenStream(
		[(StartOfDocumentToken, None),
         (WordToken,           "a"),
         (WhitespaceToken, " "),
         (WordToken,           "bbb"),
         (WhitespaceToken, " "),
         (IntegerLiteralToken, "1"),
         (WhitespaceToken, " "),
         (IntegerLiteralToken, "23"),
         (WhitespaceToken, " "),
         (RealLiteralToken,    "3.4"),
         (WhitespaceToken, " "),
         (RealLiteralToken,    "45.6"),
         (WhitespaceToken, " "),
         (RealLiteralToken,    "5.67"),
         (WhitespaceToken, " "),
         (RealLiteralToken,    "67.89"),
         (WhitespaceToken, " "),
         (RealLiteralToken,    ".7"),
         (WhitespaceToken, " "),
         (RealLiteralToken,    ".89"),
         (WhitespaceToken, " "),
         (CharacterToken,      "("),
         (WhitespaceToken, " "),
         (CharacterToken,      ")"),
         (WhitespaceToken, " "),
         (CharacterToken,      "<"),
         (WhitespaceToken, " "),
         (CharacterToken,      ">"),
         (WhitespaceToken, " "),
         (CharacterToken,      "="),
         (WhitespaceToken, " "),
         (CharacterToken,      "."),
         (WhitespaceToken, " "),
         (CharacterToken,      ","),
         (WhitespaceToken, " "),
         (CharacterToken,      ";"),
         (WhitespaceToken, " "),
         (CharacterToken,      "&"),
         (WhitespaceToken, " "),
         (CharacterToken,      "/"),
         (WhitespaceToken, " "),
         (CharacterToken,      "+"),
         (WhitespaceToken, " "),
         (CharacterToken,      "-"),
         (WhitespaceToken, " "),
         (CharacterToken,      "*"),
         (WhitespaceToken, " "),
         #			(CharacterToken,      "'"),
         #			(SpaceToken,          " "),
         (FusedCharacterToken, "<<"),
         (WhitespaceToken, " "),
         (FusedCharacterToken, ">>"),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "/="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "<="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, ">="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "=>"),
         (WhitespaceToken, " "),
         (FusedCharacterToken, ":="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "**"),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "?="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "?/="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "?<"),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "?>"),
         #			(SpaceToken,          " "),
         #			(FusedCharacterToken, "?<="),
         #			(SpaceToken,          " "),
         #			(FusedCharacterToken, "?>="),
         (WhitespaceToken, " "),
         (FusedCharacterToken, "<>"),
         (WhitespaceToken, " "),  # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
         (EndOfDocumentToken, None)
         ]
	)

class Sequence_2(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc   \\def\\ \t 'a' ''' "abc" "\"\"" "foo\"\"" /* help */ -- foo\n """
	tokenStream = ExpectedTokenStream(
		[(StartOfDocumentToken, None),
         (WordToken,               "abc"),
         (WhitespaceToken, "   "),
         (ExtendedIdentifier,      "\\def\\"),
         (WhitespaceToken, " \t "),
         (CharacterLiteralToken,   "a"),
         (WhitespaceToken, " "),
         (CharacterLiteralToken,   "'"),
         (WhitespaceToken, " "),
         (StringLiteralToken,      "abc"),
         (WhitespaceToken, " "),
         (StringLiteralToken,      "\"\""),
         (WhitespaceToken, " "),
         (StringLiteralToken,      "foo\"\""),
         (WhitespaceToken, " "),
         (MultiLineCommentToken,   "/* help */"),
         (WhitespaceToken, " "),
         (SingleLineCommentToken,  "-- foo\n"),
         (WhitespaceToken, " "),  # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
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
			(WhitespaceToken, " "),
			(EndOfDocumentToken, None)
		]
	)

class Sequence_4(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc-- comment\n123-- comment\n456.789-- comment\n'Z'-- comment\n"Hallo"-- comment\n\\foo\\-- comment\n-- comment\n/* comment */-- comment\n;-- comment\n  -- comment\n """
	tokenStream = ExpectedTokenStream(
		[(StartOfDocumentToken,    None),
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
         (WhitespaceToken, " "),  # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
         (EndOfDocumentToken,      None)
         ]
	)

class Sequence_5(TestCase, ExpectedDataMixin, TokenSequence):
	code = """abc/* comment */123/* comment */456.789/* comment */'Z'/* comment */"Hallo"/* comment */\\foo\\/* comment */-- comment\n/* comment *//* comment */;/* comment */  /* comment */ """
	tokenStream = ExpectedTokenStream(
		[(StartOfDocumentToken,   None),
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
         (WhitespaceToken, "  "),
         (MultiLineCommentToken,  "/* comment */"),
         (WhitespaceToken, " "),  # FIXME: workaround until incomplete fused tokens are handled in Tokenizer
         (EndOfDocumentToken,     None)
         ]
	)


class Sequence_6(TestCase, ExpectedDataMixin, TokenSequence):
	code = """if Clk'event and Clk = '1' then     -- rising clock edge\nname'attr1'attr2\nsignal reg_catch1   : std_logic_vector(flags_src1'range);"""
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken,   None),
			(WordToken,               "if"),
			(WhitespaceToken,         " "),
			(WordToken,               "Clk"),
			(CharacterToken,          "'"),
			(WordToken,               "event"),
			(WhitespaceToken,         " "),
			(WordToken,               "and"),
			(WhitespaceToken,         " "),
			(WordToken,               "Clk"),
			(WhitespaceToken,         " "),
			(CharacterToken,          "="),
			(WhitespaceToken,         " "),
			(CharacterLiteralToken,   "1"),
			(WhitespaceToken,         " "),
			(WordToken,               "then"),
			(WhitespaceToken,         "     "),
			(SingleLineCommentToken,  "-- rising clock edge\n"),
			(WordToken,               "name"),
			(CharacterToken,          "'"),
			(WordToken,               "attr1"),
			(CharacterToken,          "'"),
			(WordToken,               "attr2"),
			(LinebreakToken,          None),
			(WordToken,               "signal"),
			(WhitespaceToken,         " "),
			(WordToken,               "reg_catch1"),
			(WhitespaceToken,         "   "),
			(CharacterToken,          ":"),
			(WhitespaceToken,         " "),
			(WordToken,               "std_logic_vector"),
			(CharacterToken,          "("),
			(WordToken,               "flags_src1"),
			(CharacterToken,          "'"),
			(WordToken,               "range"),
			(CharacterToken,          ")"),
			(CharacterToken,          ";"),
			(EndOfDocumentToken,     None)
		]
	)


class Sequence_7(TestCase, ExpectedDataMixin, TokenSequence):
	code = """constant BIT_STRING : UNSIGNED(0 downto 0) := UNSIGNED'(x\"0\");\nconstant LPAREN_CHAR : character := '(';\nfoo'('0')\nbar'('(')\ncharacter'(''')"""
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken,   None),
			(WordToken,               "constant"),
			(WhitespaceToken,         " "),
			(WordToken,               "BIT_STRING"),
			(WhitespaceToken,         " "),
			(CharacterToken,          ":"),
			(WhitespaceToken,         " "),
			(WordToken,               "UNSIGNED"),
			(CharacterToken,          "("),
			(IntegerLiteralToken,     "0"),
			(WhitespaceToken,         " "),
			(WordToken,               "downto"),
			(WhitespaceToken,         " "),
			(IntegerLiteralToken,     "0"),
			(CharacterToken,          ")"),
			(WhitespaceToken,         " "),
			(FusedCharacterToken,     ":="),
			(WhitespaceToken,         " "),
			(WordToken,               "UNSIGNED"),
			(CharacterToken,          "'"),
			(CharacterToken,          "("),
			(WordToken,               "x"),
			(StringLiteralToken,      "0"),
			(CharacterToken,          ")"),
			(CharacterToken,          ";"),
			(LinebreakToken,          None),
			(WordToken,               "constant"),
			(WhitespaceToken,         " "),
			(WordToken,               "LPAREN_CHAR"),
			(WhitespaceToken,         " "),
			(CharacterToken,          ":"),
			(WhitespaceToken,         " "),
			(WordToken,               "character"),
			(WhitespaceToken,         " "),
			(FusedCharacterToken,     ":="),
			(WhitespaceToken,         " "),
			(CharacterLiteralToken,   "("),
			(CharacterToken,          ";"),
			(LinebreakToken,          None),
			(WordToken,               "foo"),
			(CharacterToken,          "'"),
			(CharacterToken,          "("),
			(CharacterLiteralToken,   "0"),
			(CharacterToken,          ")"),
			(LinebreakToken,          None),
			(WordToken,               "bar"),
			(CharacterToken,          "'"),
			(CharacterToken,          "("),
			(CharacterLiteralToken,   "("),
			(CharacterToken,          ")"),
			(LinebreakToken,          None),
			(WordToken,               "character"),
			(CharacterToken,          "'"),
			(CharacterToken,          "("),
			(CharacterLiteralToken,   "'"),
			(CharacterToken,          ")"),
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
				context=f"at {token.Start!s}",
				actual=f"'{token!r}' of {token.__class__.__qualname__}",
				expected=f"'keyword' of {WordToken.__qualname__}"
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
			_ = EntityKeyword(fromExistingToken=keywordToken)
		# TODO: check exception message
