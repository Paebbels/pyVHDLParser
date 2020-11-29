from textwrap                       import dedent
from unittest                       import TestCase

from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken, IndentationToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import WhitespaceBlock, LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.List       import GenericList
from pyVHDLParser.Blocks.Sequential import Package

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream, BlockSequenceWithParserError, TokenLinking


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class SimplePackage_OneLine_OnlyEnd(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package p is end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Package.NameBlock,    "package p is"), # package pis
			(WhitespaceBlock,      " "),            #
			(Package.EndBlock,     "end;"),         # end;
			(EndOfDocumentBlock,   None)            #
		]
	)

class SimplePackage_OneLine_EndWithKeyword(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package p is end package;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"),  # package
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Package.NameBlock,     "package p is"),  # package p is
			(WhitespaceBlock,      " "),            #
			(Package.EndBlock,      "end package;"),  # end package;
			(EndOfDocumentBlock,   None)            #
		],
	)


class SimplePackage_OneLine_EndWithName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package p is end p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Package.NameBlock,     "package p is"),  # package p is
			(WhitespaceBlock,      " "),            #
			(Package.EndBlock,      "end p;"),       # end e;
			(EndOfDocumentBlock,   None)            #
		]
	)


class SimplePackage_OneLine_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package p is end package p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package p is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package p;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_OneLine_NoName_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "package is end package p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package is"),      # package is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_OneLine_NoIs_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "package p end package p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p"),       # package p
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package p;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_OneLine_NoEnd_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "package p is package p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package p is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "package p;"),      # package p;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_OneLine_EndWithKeywordAndName_WrongName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package p is end package a;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"),  # package
			(SpaceToken,           " "),       #
			(WordToken,            "a"),       # a
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package p is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package a;"),  # end package a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_MultiLine_LongForm(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		package p is
		end package p ;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       "\n"),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(CharacterToken,       ";"),
			(LinebreakToken,       "\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),
			(Package.NameBlock,     "package p is"),
			(LinebreakBlock,       "\n"),
			(Package.EndBlock,      "end package p ;"),
			(LinebreakBlock,       "\n"),
			(EndOfDocumentBlock,   None)
		]
	)


class SimplePackage_AllLine_LongForm(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package\np\nis\nend\npackage\np\n;\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(LinebreakToken,       "\n"),
			(WordToken,            "p"),
			(LinebreakToken,       "\n"),
			(WordToken,            "is"),
			(LinebreakToken,       "\n"),
			(WordToken,            "end"),
			(LinebreakToken,       "\n"),
			(WordToken,            "package"),
			(LinebreakToken,       "\n"),
			(WordToken,            "p"),
			(LinebreakToken,       "\n"),
			(CharacterToken,       ";"),
			(LinebreakToken,       "\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,  None),
			(Package.NameBlock,      "package"),
			(LinebreakBlock,        "\n"),
#			(IndentationBlock,      "\t"),
			(Package.NameBlock,      "p"),
			(LinebreakBlock,        "\n"),
			(Package.NameBlock,      "is"),
			(LinebreakBlock,        "\n"),
			(Package.EndBlock,       "end\n"),
#			(LinebreakBlock,        "\n"),
			(Package.EndBlock,       "package\n"),
#			(LinebreakBlock,        "\n"),
			(Package.EndBlock,       "p\n"),
#			(LinebreakBlock,        "\n"),
			(Package.EndBlock,       ";"),
			(LinebreakBlock,        "\n"),
			(EndOfDocumentBlock,    None)
		]
	)


class SimplePackage_MultiLine_LongForm_WithSingleGeneric(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		package p is
			generic (
				G : integer
			);
		end package p;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "generic"),
			(SpaceToken,           " "),
			(CharacterToken,       "("),
			(LinebreakToken,       None),
			(IndentationToken,     "\t\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Package.NameBlock,        "package p is"),
			(LinebreakBlock,          "\n"),
			(IndentationBlock,        "\t"),
			(GenericList.OpenBlock,   "generic ("),
			(LinebreakBlock,          "\n"),
			(IndentationBlock,        "\t\t"),
			(GenericList.GenericListInterfaceConstantBlock, "G : integer"),
			(LinebreakBlock,          "\n"),
			(GenericList.GenericListInterfaceConstantBlock, "\t"),
			(GenericList.CloseBlock,  ");"),
			(LinebreakBlock,          "\n"),
			(Package.EndBlock,         "end package p;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimplePackage_MultiLine_LongForm_WithSingleGeneric_NoGenericKeyword(TestCase, ExpectedDataMixin, TokenLinking):
	code = dedent("""\
		package p is
			(
				G : integer
			);
		end	package p;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       "("),
			(LinebreakToken,       None),
			(IndentationToken,     "\t\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package e is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_MultiLine_LongForm_WithSingleGeneric_NoOpeningRoundBracket(TestCase, ExpectedDataMixin, TokenLinking):
	code = dedent("""\
		package p is
			generic
				G : integer
			);
		end	package p;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "generic"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package e is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_MultiLine_LongForm_WithSingleGeneric_NoClosingRoundBracket(TestCase, ExpectedDataMixin, TokenLinking):
	code = dedent("""\
		package p is
			generic (
				G : integer
			;
		end	package p;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "generic"),
			(SpaceToken,           " "),
			(CharacterToken,       "("),
			(LinebreakToken,       None),
			(IndentationToken,     "\t\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package e is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimplePackage_MultiLine_LongForm_WithSingleGeneric_TypoInGeneric(TestCase, ExpectedDataMixin, TokenLinking):
	code = dedent("""\
		package p is
			gen (
				G : integer
			;
		end	package e;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "gen"),
			(SpaceToken,           " "),
			(CharacterToken,       "("),
			(LinebreakToken,       None),
			(IndentationToken,     "\t\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Package.NameBlock,     "package p is"),    # package e is
			(WhitespaceBlock,      " "),              #
			(Package.EndBlock,      "end package p;"),  # end package a;
			(EndOfDocumentBlock,   None)              #
		]
	)
