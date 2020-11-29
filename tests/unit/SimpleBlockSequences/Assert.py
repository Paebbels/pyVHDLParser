from unittest   import TestCase

from pyVHDLParser.Token             import StartOfDocumentToken, WordToken, SpaceToken, CharacterToken, EndOfDocumentToken, StringLiteralToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import WhitespaceBlock
from pyVHDLParser.Blocks.Reporting  import Assert
from pyVHDLParser.Blocks.Structural import Architecture

from tests.unit.Common              import Initializer, ExpectedTokenStream, ExpectedBlockStream, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequence


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class SimpleAssertInArchitecture_OneLine_OnlyAssert(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence):
	code = "architecture a of e is begin assert true report \"error\"; end;"
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
			(WordToken,            "assert"),
			(SpaceToken,           " "),
			(WordToken,            "true"),
			(SpaceToken,           " "),
			(WordToken,            "report"),
			(SpaceToken,           " "),
			(StringLiteralToken,   "error"),
			(CharacterToken,       ";"),
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
			(Assert.AssertBlock,      "assert true report \"error\";"),
			(Architecture.EndBlock,   "end;"),
			(EndOfDocumentBlock,      None)
		]
	)
