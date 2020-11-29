from unittest                       import TestCase

from pyVHDLParser.Token             import StartOfDocumentToken, WordToken, SpaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken, IndentationToken, MultiLineCommentToken, SingleLineCommentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock, CommentBlock
from pyVHDLParser.Blocks.Common     import WhitespaceBlock, IndentationBlock, LinebreakBlock
from pyVHDLParser.Blocks.Structural import Architecture

from tests.unit.Common              import Result, Initializer, ExpectedTokenStream, ExpectedBlockStream, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class SimpleArchitecture_OneLine_OnlyEnd(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(SpaceToken,           " "),
			(WordToken,            "of"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "begin"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end;"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimpleArchitecture_OneLine_EndWithKeyword(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end architecture;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(SpaceToken,           " "),
			(WordToken,            "of"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "begin"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "architecture"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end architecture;"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_OneLine_EndWithName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end a;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(SpaceToken,           " "),
			(WordToken,            "of"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "begin"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end a;"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_OneLine_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end architecture a;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(SpaceToken,           " "),
			(WordToken,            "of"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "begin"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "architecture"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end architecture a;"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_MultiLine_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture\na\nof\ne\nis\nbegin\nend\narchitecture\na\n;\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(LinebreakToken,       None),
			(WordToken,            "a"),
			(LinebreakToken,       None),
			(WordToken,            "of"),
			(LinebreakToken,       None),
			(WordToken,            "e"),
			(LinebreakToken,       None),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(WordToken,            "begin"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(LinebreakToken,       None),
			(WordToken,            "architecture"),
			(LinebreakToken,       None),
			(WordToken,            "a"),
			(LinebreakToken,       None),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture"),
			(LinebreakBlock,          "\n"),
#			(IndentationBlock,        "\t"),
			(Architecture.NameBlock,  "a"),
			(LinebreakBlock,          "\n"),
			(Architecture.NameBlock,  "of"),
			(LinebreakBlock,          "\n"),
			(Architecture.NameBlock,  "e"),
			(LinebreakBlock,          "\n"),
			(Architecture.NameBlock,  "is"),
			(LinebreakBlock,          "\n"),
			(Architecture.BeginBlock, "begin"),
			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   "end\n"),
#			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   "architecture\n"),
#			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   "a\n"),
#			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   ";"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_MultiLineIndented_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "\tarchitecture\n\ta\n\tof\n\te\n\tis\n\tbegin\n\tend\n\tarchitecture\n\ta\n\t;\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(IndentationToken,     "\t"),
			(WordToken,            "architecture"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "a"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "of"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "e"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "begin"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "end"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "architecture"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "a"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(IndentationBlock,        "\t"),
			(Architecture.NameBlock,  "architecture"),
			(LinebreakBlock,          "\n"),
#			(IndentationBlock,        "\t"),
			(Architecture.NameBlock,  "\ta"),
			(LinebreakBlock,          "\n"),
			(Architecture.NameBlock,  "\tof"),
			(LinebreakBlock,          "\n"),
			(Architecture.NameBlock,  "\te"),
			(LinebreakBlock,          "\n"),
			(Architecture.NameBlock,  "\tis"),
			(LinebreakBlock,          "\n"),
			(IndentationBlock,        "\t"),
			(Architecture.BeginBlock, "begin"),
			(LinebreakBlock,          "\n"),
			(IndentationBlock,        "\t"),
			(Architecture.EndBlock,   "end\n"),
#			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   "\tarchitecture\n"),
#			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   "\ta\n"),
#			(LinebreakBlock,          "\n"),
			(Architecture.EndBlock,   "\t;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_MultilineComments_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture/* comment */a/* comment */of/* comment */e/* comment */is/* comment */begin/* comment */end/* comment */architecture/* comment */a/* comment */;/* comment */"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,             "architecture"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "a"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "of"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "e"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "is"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "begin"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "end"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "architecture"),
			(MultiLineCommentToken, "/* comment */"),
			(WordToken,            "a"),
			(MultiLineCommentToken, "/* comment */"),
			(CharacterToken,       ";"),
			(MultiLineCommentToken, "/* comment */"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture"),
			(CommentBlock,            "/* comment */"),
			(Architecture.NameBlock,  "a"),
			(CommentBlock,            "/* comment */"),
			(Architecture.NameBlock,  "of"),
			(CommentBlock,            "/* comment */"),
			(Architecture.NameBlock,  "e"),
			(CommentBlock,            "/* comment */"),
			(Architecture.NameBlock,  "is"),
			(CommentBlock,            "/* comment */"),
			(Architecture.BeginBlock, "begin"),
			(CommentBlock,            "/* comment */"),
			(Architecture.EndBlock,   "end"),
			(CommentBlock,            "/* comment */"),
			(Architecture.EndBlock,   "architecture"),
			(CommentBlock,            "/* comment */"),
			(Architecture.EndBlock,   "a"),
			(CommentBlock,            "/* comment */"),
			(Architecture.EndBlock,   ";"),
			(CommentBlock,            "/* comment */"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_SingleLineComments_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture-- comment\na-- comment\nof-- comment\ne-- comment\nis-- comment\nbegin-- comment\nend-- comment\narchitecture-- comment\na-- comment\n;-- comment\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,               "architecture"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,               "a"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,               "of"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,               "e"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "is"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "begin"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "end"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "architecture"),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "a"),
			(SingleLineCommentToken,  "-- comment\n"),
			(CharacterToken,         ";"),
			(SingleLineCommentToken,  "-- comment\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "a"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "of"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "e"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "is"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.BeginBlock, "begin"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   "end"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   "architecture"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   "a"),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   ";"),
			(CommentBlock,            "-- comment\n"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_SpacePlusSingleLineComments_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture -- comment\na -- comment\nof -- comment\ne -- comment\nis -- comment\nbegin -- comment\nend -- comment\narchitecture -- comment\na -- comment\n; -- comment\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,               "architecture"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,               "a"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,               "of"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,               "e"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "is"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "begin"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "end"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "architecture"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(WordToken,              "a"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(CharacterToken,         ";"),
			(SpaceToken,              " "),
			(SingleLineCommentToken,  "-- comment\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "a "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "of "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "e "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.NameBlock,  "is"),
			(WhitespaceBlock,         " "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   "end "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   "architecture "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   "a "),
			(CommentBlock,            "-- comment\n"),
			(Architecture.EndBlock,   ";"),
			(WhitespaceBlock,         " "),
			(CommentBlock,            "-- comment\n"),
			(EndOfDocumentBlock,      None)
		]
	)
