from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock, BlockParserException
from pyVHDLParser.Blocks.Common     import WhitespaceBlock
from pyVHDLParser.Blocks.Structural import Entity

from tests.unit import StreamingTests, Result, Initializer


TESTCASES = [
	{ 'name': "Simple:Entity: one line; only end",
		'code': "entity e is end;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),           #
				(Entity.NameBlock,     "entity e is"),  # entity e is
				(WhitespaceBlock,      " "),            #
				(Entity.EndBlock,      "end;"),         # end;
				(EndOfDocumentBlock,   None)            #
			],
		  'result': Result.Pass
	  }
	},{
		'name': "Simple:Entity: one line; ends with keyword",
		'code': "entity e is end entity;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(SpaceToken,           " "),       #
				(WordToken,            "entity"),  # entity
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),           #
				(Entity.NameBlock,     "entity e is"),  # entity e is
				(WhitespaceBlock,      " "),            #
				(Entity.EndBlock,      "end entity;"),  # end entity;
				(EndOfDocumentBlock,   None)            #
			],
		  'result': Result.Pass
		}
	},{
		'name': "Simple:Entity: one line; ends with name",
		'code': "entity e is end e;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),           #
				(Entity.NameBlock,     "entity e is"),  # entity e is
				(WhitespaceBlock,      " "),            #
				(Entity.EndBlock,      "end e;"),       # end e;
				(EndOfDocumentBlock,   None)            #
			],
		  'result': Result.Pass
		}
	},{
		'name': "Simple:Entity: one line; ends with keyword and name",
		'code': "entity e is end entity e;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(SpaceToken,           " "),       #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),             #
				(Entity.NameBlock,     "entity e is"),    # entity e is
				(WhitespaceBlock,      " "),              #
				(Entity.EndBlock,      "end entity e;"),  # end entity e;
				(EndOfDocumentBlock,   None)              #
			],
		  'result': Result.Pass
		}
	},{
		'name': "Simple:Entity: one line; no name; ends with keyword and name",
		'code': "entity is end entity e;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(SpaceToken,           " "),       #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),             #
				(Entity.NameBlock,     "entity is"),      # entity is
				(WhitespaceBlock,      " "),              #
				(Entity.EndBlock,      "end entity e;"),  # end entity e;
				(EndOfDocumentBlock,   None)              #
			],
		  'result':     Result.Fail,
		  'Exception':  BlockParserException
		}
	},{
		'name': "Simple:Entity: one line; no is; ends with keyword and name",
		'code': "entity e end entity e;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(SpaceToken,           " "),       #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),             #
				(Entity.NameBlock,     "entity e"),       # entity e
				(WhitespaceBlock,      " "),              #
				(Entity.EndBlock,      "end entity e;"),  # end entity e;
				(EndOfDocumentBlock,   None)              #
			],
		  'result':     Result.Fail,
		  'Exception':  BlockParserException
		}
	},{
		'name': "Simple:Entity: one line; no end; ends with keyword and name",
		'code': "entity e is entity e;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),             #
				(Entity.NameBlock,     "entity e is"),    # entity e is
				(WhitespaceBlock,      " "),              #
				(Entity.EndBlock,      "entity e;"),      # entity e;
				(EndOfDocumentBlock,   None)              #
			],
		  'result':     Result.Fail,
		  'Exception':  BlockParserException
		}
	},{
		'name': "Simple:Entity: one line; ends with keyword and name; but wrong name",
		'code': "entity e is end entity a;",
		'tokenstream': {
			'tokens': [
				(StartOfDocumentToken, None),      #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "e"),       # e
				(SpaceToken,           " "),       #
				(WordToken,            "is"),      # is
				(SpaceToken,           " "),       #
				(WordToken,            "end"),     # end
				(SpaceToken,           " "),       #
				(WordToken,            "entity"),  # entity
				(SpaceToken,           " "),       #
				(WordToken,            "a"),       # a
				(CharacterToken,       ";"),       # ;
				(EndOfDocumentToken,   None)       #
			],
			'result': Result.Pass
		},
	  'blockstream': {
			'blocks': [
				(StartOfDocumentBlock, None),             #
				(Entity.NameBlock,     "entity e is"),    # entity e is
				(WhitespaceBlock,      " "),              #
				(Entity.EndBlock,      "end entity a;"),  # end entity a;
				(EndOfDocumentBlock,   None)              #
			],
		  'result':     Result.Pass
		}
	}
]

def setUpModule():
	i = Initializer()


class SimpleEntities(StreamingTests):
	_TESTCASES = TESTCASES

	def setUp(self):
		pass
