from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock, CommentBlock
from pyVHDLParser.Blocks.Common import WhitespaceBlock, IndentationBlock, LinebreakBlock
from pyVHDLParser.Blocks.Structural import Architecture
from pyVHDLParser.Token import StartOfDocumentToken, WordToken, SpaceToken, CharacterToken, EndOfDocumentToken, \
	LinebreakToken, IndentationToken, MultiLineCommentToken, SingleLineCommentToken
from unittest   import TestCase
from tests.unit import Result, Initializer, Struct1, Struct2, Struct3, LinkingTests, TokenSequence, BlockSequence


def setUpModule():
	Initializer()


class SimpleArchitecture_OneLine_OnlyEnd(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end;"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end;"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimpleArchitecture_OneLine_WithKeyword(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end architecture;"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end architecture;"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_OneLine_WithName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end a;"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end a;"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_OneLine_WithKeywordAndName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end architecture a;"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end architecture a;"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_MultiLine_WithKeywordAndName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture\na\nof\ne\nis\nbegin\nend\narchitecture\na\n;\n"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture"),
			(LinebreakBlock,          "\\n"),
#			(IndentationBlock,        "\\t"),
			(Architecture.NameBlock,  "a"),
			(LinebreakBlock,          "\\n"),
			(Architecture.NameBlock,  "of"),
			(LinebreakBlock,          "\\n"),
			(Architecture.NameBlock,  "e"),
			(LinebreakBlock,          "\\n"),
			(Architecture.NameBlock,  "is"),
			(LinebreakBlock,          "\\n"),
			(Architecture.BeginBlock, "begin"),
			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   "end\\n"),
#			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   "architecture\\n"),
#			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   "a\\n"),
#			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   ";"),
			(LinebreakBlock,          "\\n"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_MultiLineIndented_WithKeywordAndName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "\tarchitecture\n\ta\n\tof\n\te\n\tis\n\tbegin\n\tend\n\tarchitecture\n\ta\n\t;\n"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(IndentationBlock,        "\\t"),
			(Architecture.NameBlock,  "architecture"),
			(LinebreakBlock,          "\\n"),
#			(IndentationBlock,        "\\t"),
			(Architecture.NameBlock,  "\\ta"),
			(LinebreakBlock,          "\\n"),
			(Architecture.NameBlock,  "\\tof"),
			(LinebreakBlock,          "\\n"),
			(Architecture.NameBlock,  "\\te"),
			(LinebreakBlock,          "\\n"),
			(Architecture.NameBlock,  "\\tis"),
			(LinebreakBlock,          "\\n"),
			(IndentationBlock,        "\\t"),
			(Architecture.BeginBlock, "begin"),
			(LinebreakBlock,          "\\n"),
			(IndentationBlock,        "\\t"),
			(Architecture.EndBlock,   "end\\n"),
#			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   "\\tarchitecture\\n"),
#			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   "\\ta\\n"),
#			(LinebreakBlock,          "\\n"),
			(Architecture.EndBlock,   "\\t;"),
			(LinebreakBlock,          "\\n"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_MultilineComments_WithKeywordAndName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture/* comment */a/* comment */of/* comment */e/* comment */is/* comment */begin/* comment */end/* comment */architecture/* comment */a/* comment */;/* comment */"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
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

class SimpleArchitecture_SingleLineComments_WithKeywordAndName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture-- comment\na-- comment\nof-- comment\ne-- comment\nis-- comment\nbegin-- comment\nend-- comment\narchitecture-- comment\na-- comment\n;-- comment\n"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "a"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "of"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "e"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "is"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.BeginBlock, "begin"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   "end"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   "architecture"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   "a"),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   ";"),
			(CommentBlock,            "-- comment\\n"),
			(EndOfDocumentBlock,      None)
		]
	)

class SimpleArchitecture_SpacePlusSingleLineComments_WithKeywordAndName(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture -- comment\na -- comment\nof -- comment\ne -- comment\nis -- comment\nbegin -- comment\nend -- comment\narchitecture -- comment\na -- comment\n; -- comment\n"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
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
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "a "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "of "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "e "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.NameBlock,  "is"),
			(WhitespaceBlock,         " "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   "end "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   "architecture "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   "a "),
			(CommentBlock,            "-- comment\\n"),
			(Architecture.EndBlock,   ";"),
			(WhitespaceBlock,         " "),
			(CommentBlock,            "-- comment\\n"),
			(EndOfDocumentBlock,      None)
		]
	)
