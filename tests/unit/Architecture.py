from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common import WhitespaceBlock
from pyVHDLParser.Blocks.Structural import Entity
from pyVHDLParser.Token import StartOfDocumentToken, WordToken, SpaceToken, CharacterToken, EndOfDocumentToken
from unittest   import TestCase
from tests.unit import Result, Initializer, Struct1, Struct2, Struct3, LinkingTests, TokenSequence, BlockSequence


class SimpleArchitecture_OneLine_OnlyEnd(TestCase, Struct3, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is begin end;"
	tokenstream = Struct1(
		tokenList=[
			(StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(SpaceToken,           " "),
			(WordToken,            "b"),
			(SpaceToken,           " "),
			(WordToken,            "of"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "begin"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockstream = Struct2(
		blockList=[
			(StartOfDocumentBlock, None),
			(Entity.NameBlock,     "architecture a of e is"),
			(WhitespaceBlock,      " "),
			(Entity.BeginBlock,    "begin"),
			(WhitespaceBlock,      " "),
			(Entity.EndBlock,      "end;"),
			(EndOfDocumentBlock,   None)
		]
	)

	def test_TokenSequence(self) -> None:
		super().test_TokenSequence()

def setUpModule():
	Initializer()
