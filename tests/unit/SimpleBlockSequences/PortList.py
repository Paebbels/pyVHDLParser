from unittest                           import TestCase

from pyVHDLParser.Blocks.List           import PortList
from pyVHDLParser.Blocks.List.PortList  import PortListInterfaceSignalBlock
from pyVHDLParser.Token                 import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks                import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common         import WhitespaceBlock
from pyVHDLParser.Blocks.Structural     import Entity

from tests.unit.Common                  import Initializer, ExpectedDataMixin, LinkingTests, TokenLinking, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class SimplePortList_OneLine_SinglePort(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "entity e is port (port1 : bit); end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "port"),
			(SpaceToken,           " "),
			(CharacterToken,       "("),
			(WordToken,            "port1"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "bit"),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,          None),           #
			(Entity.NameBlock,              "entity e is"),  # entity e is
			(WhitespaceBlock,               " "),            #
			(PortList.OpenBlock,            "port ("),       # port (
			(PortListInterfaceSignalBlock,  "port1 : bit"),  # port1 : bit
			(PortList.CloseBlock,           ");"),           # );
			(WhitespaceBlock,               " "),            #
			(Entity.EndBlock,               "end;"),         # end;
			(EndOfDocumentBlock,            None)            #
		]
	)

class SimplePortList_OneLine_DoublePort(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequence):
	code = "entity e is port (port1 : bit; port2 : boolean ); end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "entity"),
			(SpaceToken,           " "),
			(WordToken,            "e"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "port"),
			(SpaceToken,           " "),
			(CharacterToken,       "("),
			(WordToken,            "port1"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "bit"),
			(CharacterToken,       ";"),
			(SpaceToken,           " "),
			(WordToken,            "port2"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "boolean"),
			(SpaceToken,           " "),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,          None),               #
			(Entity.NameBlock,              "entity e is"),      # entity e is
			(WhitespaceBlock,               " "),                #
			(PortList.OpenBlock,            "port ("),           # port (
			(PortListInterfaceSignalBlock,  "port1 : bit"),      # port1 : bit
			(PortList.DelimiterBlock,       ";"),                # ;
			(PortListInterfaceSignalBlock,  "port2 : boolean "), # port2 : boolean
			(PortList.CloseBlock,           ");"),               # );
			(WhitespaceBlock,               " "),                #
			(Entity.EndBlock,               "end;"),             # end;
			(EndOfDocumentBlock,            None)                #
		]
	)
