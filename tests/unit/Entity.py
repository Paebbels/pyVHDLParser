from textwrap import dedent
from unittest import TestCase

from pyVHDLParser.Token import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken, \
	LinebreakToken, IndentationToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock, BlockParserException
from pyVHDLParser.Blocks.Common     import WhitespaceBlock
from pyVHDLParser.Blocks.Structural import Entity

from tests.unit                     import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


def setUpModule():
	i = Initializer()

class SimpleEntity_OneLine_OnlyEnd(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Entity.NameBlock,     "entity e is"),  # entity e is
			(WhitespaceBlock,      " "),            #
			(Entity.EndBlock,      "end;"),         # end;
			(EndOfDocumentBlock,   None)            #
		]
	)

class SimpleEntity_OneLine_EndWithKeyword(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end entity;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Entity.NameBlock,     "entity e is"),  # entity e is
			(WhitespaceBlock,      " "),            #
			(Entity.EndBlock,      "end entity;"),  # end entity;
			(EndOfDocumentBlock,   None)            #
		],
	)


class SimpleEntity_OneLine_EndWithName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end e;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(Entity.NameBlock,     "entity e is"),  # entity e is
			(WhitespaceBlock,      " "),            #
			(Entity.EndBlock,      "end e;"),       # end e;
			(EndOfDocumentBlock,   None)            #
		]
	)


class SimpleEntity_OneLine_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end entity e;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity e;"),  # end entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_NoName_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity is end entity e;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity is"),      # entity is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity e;"),  # end entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_NoIs_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e end entity e;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e"),       # entity e
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity e;"),  # end entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_NoEnd_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is entity e;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "entity e;"),      # entity e;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_OneLine_EndWithKeywordAndName_WrongName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is end entity a;"
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
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
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_AllLine_LongForm(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity
		e
		is
		end
		entity
		e
		;
		""")
	tokenstream = ExpectedTokenStream(
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
			generic (
				G : integer
			);
		end	entity e;
		""")
	tokenstream = ExpectedTokenStream(
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
			(IndentationToken,     "\\t\\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\\t"),
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_NoGenericKeyword(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
			(
				G : integer
			);
		end	entity e;
		""")
	tokenstream = ExpectedTokenStream(
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
			(IndentationToken,     "\\t\\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\\t"),
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_NoOpeningRoundBracket(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
			generic
				G : integer
			);
		end	entity e;
		""")
	tokenstream = ExpectedTokenStream(
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
			(IndentationToken,     "\\t\\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\\t"),
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_NoClosingRoundBracket(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
			generic (
				G : integer
			;
		end	entity e;
		""")
	tokenstream = ExpectedTokenStream(
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
			(IndentationToken,     "\\t\\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\\t"),
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)


class SimpleEntity_MultiLine_LongForm_WithSingleGeneric_TypoInGeneric(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		entity e is
			gen (
				G : integer
			;
		end	entity e;
		""")
	tokenstream = ExpectedTokenStream(
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
			(IndentationToken,     "\\t\\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\\t"),
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
	blockstream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Entity.NameBlock,     "entity e is"),    # entity e is
			(WhitespaceBlock,      " "),              #
			(Entity.EndBlock,      "end entity a;"),  # end entity a;
			(EndOfDocumentBlock,   None)              #
		]
	)
