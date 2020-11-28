from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock, CommentBlock
from pyVHDLParser.Blocks.Common import WhitespaceBlock, IndentationBlock, LinebreakBlock
from pyVHDLParser.Blocks.Structural import Architecture
from pyVHDLParser.Token import StartOfDocumentToken, WordToken, SpaceToken, CharacterToken, EndOfDocumentToken, \
	LinebreakToken, IndentationToken, MultiLineCommentToken, SingleLineCommentToken
from unittest   import TestCase
from tests.unit import Result, Initializer, ExpectedTokenStream, ExpectedBlockStream, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class SimpleAssertInArchitecture_OneLine_OnlyAssert(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin assert true; end;"
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
			(Architecture.EndBlock,   "end;"),
			(EndOfDocumentBlock,      None)
		]
	)
