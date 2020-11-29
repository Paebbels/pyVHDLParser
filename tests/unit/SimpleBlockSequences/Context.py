from unittest                       import TestCase

from pyVHDLParser.Blocks.Common     import WhitespaceBlock
from pyVHDLParser.Blocks.Reference  import Use, Context
from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class Library_OneLine_SingleLibrary(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context ctx is use lib0.pkg0.all; end context;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "context"),
			(SpaceToken,           " "),
			(WordToken,            "ctx"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "use"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ";"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "context"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(Context.NameBlock,         "context ctx is"), #
			(WhitespaceBlock,           " "),
			(Use.StartBlock,            "use "),           # use
			(Use.ReferenceNameBlock,    "lib0.pkg0.all"),  # lib0.pkg0.all
			(Use.EndBlock,              ";"),              # ;
			(WhitespaceBlock,           " "),
			(Context.EndBlock,          "end context;"),
			(EndOfDocumentBlock,        None)              #
		]
	)
