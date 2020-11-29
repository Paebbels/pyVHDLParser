from unittest                       import TestCase

from pyVHDLParser.Blocks.Reference  import Library
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
	code = "library lib0;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "library"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Library.StartBlock,        "library "),  # library
			(Library.LibraryNameBlock,  "lib0"),      # lib0
			(Library.EndBlock,          ";"),         # ;
			(EndOfDocumentBlock,        None)         #
		]
	)

class Library_OneLine_TripleLibrary(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "library lib0, lib1 , lib2 ;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "library"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       ","),
			(SpaceToken,           " "),
			(WordToken,            "lib1"),
			(SpaceToken,           " "),
			(CharacterToken,       ","),
			(SpaceToken,           " "),
			(WordToken,            "lib2"),
			(SpaceToken,           " "),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(Library.StartBlock,        "library "),  # library
			(Library.LibraryNameBlock,  "lib0"),      # lib0
			(Library.DelimiterBlock,    ","),         # ,
			(Library.LibraryNameBlock,  " lib1 "),    # lib1
			(Library.DelimiterBlock,    ","),         # ,
			(Library.LibraryNameBlock,  " lib2 "),    # lib1
			(Library.EndBlock,          ";"),         # ;
			(EndOfDocumentBlock,        None)         #
		]
	)
