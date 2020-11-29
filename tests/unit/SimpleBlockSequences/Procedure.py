from unittest                       import TestCase

from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import WhitespaceBlock
from pyVHDLParser.Blocks.Sequential import Package, Procedure

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class SimpleProcedureInPackage_OneLine_NoParameter(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package p is procedure p; end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "procedure"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
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
			(Procedure.NameBlock,  "procedure p;"),
			(WhitespaceBlock,          " "),            #
			(Package.EndBlock,     "end;"),         # end;
			(EndOfDocumentBlock,   None)            #
		]
	)
