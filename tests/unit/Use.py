from unittest import TestCase

from pyVHDLParser.Blocks.Reference  import Use
from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock

from tests.unit                     import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class Use_OneLine_SinglePackage_All(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "use lib0.pkg0.all;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "use"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),               #
			(Use.StartBlock,          "use "),          # use
			(Use.ReferenceNameBlock,  "lib0.pkg0.all"), # lib0.pkg0.all
			(Use.EndBlock,            ";"),             # ;
			(EndOfDocumentBlock,      None)             #
		]
	)

class Use_OneLine_SinglePackage_Const0(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "use lib0.pkg0.const0;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "use"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "const0"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),               #
			(Use.StartBlock,          "use "),          # use
			(Use.ReferenceNameBlock,  "lib0.pkg0.const0"), # lib0.pkg0.all
			(Use.EndBlock,            ";"),             # ;
			(EndOfDocumentBlock,      None)             #
		]
	)

class Use_OneLine_DoublePackage_All(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "use lib0.pkg0.all, lib0.pkg1.all ;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "use"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ","),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg1"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(SpaceToken,           " "),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),               #
			(Use.StartBlock,          "use "),          # use
			(Use.ReferenceNameBlock,  "lib0.pkg0.all"), # lib0.pkg0.all
			(Use.DelimiterBlock,      ","),             # ,
			(Use.ReferenceNameBlock,  " lib0.pkg1.all "), # lib0.pkg1.all
			(Use.EndBlock,            ";"),             # ;
			(EndOfDocumentBlock,      None)             #
		]
	)
