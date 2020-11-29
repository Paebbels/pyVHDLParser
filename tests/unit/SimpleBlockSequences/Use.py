from unittest                       import TestCase

from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import LinebreakBlock
from pyVHDLParser.Blocks.Reference  import Use

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


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
	code = "use lib0.pkg0.all, lib0 . pkg1 . all ;"
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
			(SpaceToken,           " "),
			(CharacterToken,       "."),
			(SpaceToken,           " "),
			(WordToken,            "pkg1"),
			(SpaceToken,           " "),
			(CharacterToken,       "."),
			(SpaceToken,           " "),
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
			(Use.ReferenceNameBlock,  " lib0 . pkg1 . all "), # lib0.pkg1.all
			(Use.EndBlock,            ";"),             # ;
			(EndOfDocumentBlock,      None)             #
		]
	)

class Use_MultipleLines_SinglePackage_All(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "use\nlib0\n.\npkg0\n.\nall\n;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "use"),
			(LinebreakToken,       "\n"),
			(WordToken,            "lib0"),
			(LinebreakToken,       "\n"),
			(CharacterToken,       "."),
			(LinebreakToken,       "\n"),
			(WordToken,            "pkg0"),
			(LinebreakToken,       "\n"),
			(CharacterToken,       "."),
			(LinebreakToken,       "\n"),
			(WordToken,            "all"),
			(LinebreakToken,       "\n"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),               #
			(Use.StartBlock,          "use"),          # use
			(LinebreakBlock,          "\n"),
			(Use.ReferenceNameBlock,  "lib0"), # lib0.pkg0.all
			(LinebreakBlock,          "\n"),
			(Use.ReferenceNameBlock,  "."), # lib0.pkg0.all
			(LinebreakBlock,          "\n"),
			(Use.ReferenceNameBlock,  "pkg0"), # lib0.pkg0.all
			(LinebreakBlock,          "\n"),
			(Use.ReferenceNameBlock,  "."), # lib0.pkg0.all
			(LinebreakBlock,          "\n"),
			(Use.ReferenceNameBlock,  "all\n"), # lib0.pkg0.all
			(Use.EndBlock,            ";"),             # ;
			(EndOfDocumentBlock,      None)             #
		]
	)
