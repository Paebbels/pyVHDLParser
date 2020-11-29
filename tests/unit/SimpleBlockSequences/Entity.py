from textwrap                       import dedent
from unittest                       import TestCase

from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken, IndentationToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import WhitespaceBlock, LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Structural import Entity
from pyVHDLParser.Blocks.List       import GenericList

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, BlockSequenceWithParserError, ExpectedTokenStream, ExpectedBlockStream, TokenLinking


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class SimpleEntity_OneLine_OnlyEnd(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
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
			(Entity.NameBlock,     "entity e is"),  # entity e is
			(WhitespaceBlock,      " "),            #
			(Entity.EndBlock,      "end;"),         # end;
			(EndOfDocumentBlock,   None)            #
		]
	)

class SimpleEntity_OneLine_EndWithKeyword(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end entity;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "entity"),  # entity
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Entity.NameBlock,     "entity e is"),  # entity e is
			(WhitespaceBlock,      " "),            #
			(Entity.EndBlock,      "end entity;"),  # end entity;
			(EndOfDocumentBlock,   None)            #
		],
	)


class SimpleEntity_OneLine_EndWithName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end e;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Entity.NameBlock,     "entity e is"),  # entity e is
			(WhitespaceBlock,      " "),            #
			(Entity.EndBlock,      "end e;"),       # end e;
			(EndOfDocumentBlock,   None)            #
		]
	)


class SimpleEntity_OneLine_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end entity e;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity e;"),  # end entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_NoName_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "entity is end entity e;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity is"),      # entity is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity e;"),  # end entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_NoIs_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "entity e end entity e;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e"),       # entity e
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity e;"),  # end entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_NoEnd_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "entity e is entity e;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "entity e;"),      # entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_EndWithKeywordAndName_WrongName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end entity a;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "e"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "entity"),  # entity
			(SpaceToken,           " "),       #
			(WordToken,            "a"),       # a
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_MultiLine_LongForm(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
		end entity e ;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       "\n"),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(CharacterToken,       ";"),
			(LinebreakToken,       "\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),
			(Entity.NameBlock,     "entity e is"),
			(LinebreakBlock,       "\n"),
			(Entity.EndBlock,      "end entity e ;"),
			(LinebreakBlock,       "\n"),
			(EndOfDocumentBlock,   None)
		]
	)


class SimpleEntity_AllLine_LongForm(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity\ne\nis\nend\nentity\ne\n;\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(LinebreakToken,       "\n"),
			(WordToken,            "e"),
			(LinebreakToken,       "\n"),
			(WordToken,            "is"),
			(LinebreakToken,       "\n"),
			(WordToken,            "end"),
			(LinebreakToken,       "\n"),
			(WordToken,            "entity"),
			(LinebreakToken,       "\n"),
			(WordToken,            "e"),
			(LinebreakToken,       "\n"),
			(CharacterToken,       ";"),
			(LinebreakToken,       "\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,  None),
			(Entity.NameBlock,      "entity"),
			(LinebreakBlock,        "\n"),
#			(IndentationBlock,      "\t"),
			(Entity.NameBlock,      "e"),
			(LinebreakBlock,        "\n"),
			(Entity.NameBlock,      "is"),
			(LinebreakBlock,        "\n"),
			(Entity.EndBlock,       "end\n"),
#			(LinebreakBlock,        "\n"),
			(Entity.EndBlock,       "entity\n"),
#			(LinebreakBlock,        "\n"),
			(Entity.EndBlock,       "e\n"),
#			(LinebreakBlock,        "\n"),
			(Entity.EndBlock,       ";"),
			(LinebreakBlock,        "\n"),
			(EndOfDocumentBlock,    None)
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
			generic (
				G : integer
			);
		end entity e;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
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
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Entity.NameBlock,        "entity e is"),
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
			(Entity.EndBlock,         "end entity e;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_NoGenericKeyword(TestCase, ExpectedDataMixin, TokenLinking, BlockSequenceWithParserError):
	code = dedent("""\
		entity e is
			(
				G : integer
			);
		end	entity e;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
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
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Entity.NameBlock,        "entity e is"),
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
			(Entity.EndBlock,         "end entity e;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_NoOpeningRoundBracket(TestCase, ExpectedDataMixin, TokenLinking):
	code = dedent("""\
		entity e is
			generic
				G : integer
			);
		end	entity e;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
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
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Entity.NameBlock,        "entity e is"),
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
			(Entity.EndBlock,         "end entity e;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_NoClosingRoundBracket(TestCase, ExpectedDataMixin, TokenLinking):
	code = dedent("""\
		entity e is
			generic (
				G : integer
			;
		end	entity e;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
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
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Entity.NameBlock,        "entity e is"),
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
			(Entity.EndBlock,         "end entity e;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_TypoInGeneric(TestCase, ExpectedDataMixin, TokenLinking, BlockSequenceWithParserError):
	code = dedent("""\
		entity e is
			gen (
				G : integer
			;
		end	entity e;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
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
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "a"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Entity.NameBlock,        "entity e is"),
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
			(Entity.EndBlock,         "end entity e;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)
