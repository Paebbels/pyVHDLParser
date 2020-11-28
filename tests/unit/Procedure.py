from pyVHDLParser.Blocks.Sequential import Package, Procedure
from textwrap import dedent
from unittest import TestCase

from pyVHDLParser.Blocks.List     import GenericList
from pyVHDLParser.Token           import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken, IndentationToken
from pyVHDLParser.Blocks          import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common   import WhitespaceBlock, LinebreakBlock, IndentationBlock

from tests.unit                   import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class SimpleprocedureInPackage_OneLine_NoParameter(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
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
			(Package.EndBlock,     "end;"),         # end;
			(EndOfDocumentBlock,   None)            #
		]
	)
