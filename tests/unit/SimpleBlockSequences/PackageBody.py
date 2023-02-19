# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from textwrap                       import dedent
from unittest                       import TestCase

from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken, IndentationToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common     import WhitespaceBlock, LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.List       import GenericList
from pyVHDLParser.Blocks.Sequential import PackageBody

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream, TokenLinking, BlockSequenceWithParserError


if __name__ == "__main__":  # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class SimplePackageBody_OneLine_OnlyEnd(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package body p is end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "body"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(PackageBody.NameBlock, "package body p is"), # package body p is
			(WhitespaceBlock,       " "),            #
			(PackageBody.EndBlock,  "end;"),         # end;
			(EndOfDocumentBlock,    None)            #
		]
	)

class SimplePackageBody_OneLine_EndWithKeyword(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package body p is end package body;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # package
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # e
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(PackageBody.NameBlock, "package body p is"),  # package p is
			(WhitespaceBlock,       " "),            #
			(PackageBody.EndBlock,  "end package body;"),  # end package;
			(EndOfDocumentBlock,    None)            #
		],
	)


class SimplePackageBody_OneLine_EndWithName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package body p is end p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),           #
			(PackageBody.NameBlock, "package body p is"),  # package body p is
			(WhitespaceBlock,       " "),            #
			(PackageBody.EndBlock,  "end p;"),       # end e;
			(EndOfDocumentBlock,    None)            #
		]
	)


class SimplePackageBody_OneLine_EndWithKeywordAndName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package body p is end package body p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(PackageBody.NameBlock, "package body p is"),    # package body p is
			(WhitespaceBlock,       " "),              #
			(PackageBody.EndBlock,  "end package body p;"),  # end package body p;
			(EndOfDocumentBlock,    None)              #
		]
	)


class SimplePackageBody_OneLine_NoName_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "package body is end package body p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(PackageBody.NameBlock, "package body is"),      # package body is
			(WhitespaceBlock,       " "),              #
			(PackageBody.EndBlock,  "end package body p;"),  # end package body p;
			(EndOfDocumentBlock,    None)              #
		]
	)


class SimplePackageBody_OneLine_NoIs_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "package body p end package body p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(PackageBody.NameBlock,  "package body p"),       # package body p
			(WhitespaceBlock,        " "),              #
			(PackageBody.EndBlock,   "end package body p;"),  # end package body p;
			(EndOfDocumentBlock,     None)              #
		]
	)


class SimplePackageBody_OneLine_NoEnd_EndWithKeywordAndName(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = "package body p is package body p;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(PackageBody.NameBlock, "package body p is"),    # package body p is
			(WhitespaceBlock,       " "),              #
			(PackageBody.EndBlock,  "package body p;"),      # package body p;
			(EndOfDocumentBlock,    None)              #
		]
	)


class SimplePackageBody_OneLine_EndWithKeywordAndName_WrongName(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "package body p is end package body a;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),      #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "p"),       # p
			(SpaceToken,           " "),       #
			(WordToken,            "is"),      # is
			(SpaceToken,           " "),       #
			(WordToken,            "end"),     # end
			(SpaceToken,           " "),       #
			(WordToken,            "package"), # package
			(SpaceToken,           " "),       #
			(WordToken,            "body"),    # body
			(SpaceToken,           " "),       #
			(WordToken,            "a"),       # a
			(CharacterToken,       ";"),       # ;
			(EndOfDocumentToken,   None)       #
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),             #
			(PackageBody.NameBlock, "package body p is"),    # package p is
			(WhitespaceBlock,       " "),              #
			(PackageBody.EndBlock,  "end package body a;"),  # end package a;
			(EndOfDocumentBlock,    None)              #
		]
	)


class SimplePackageBody_MultiLine_LongForm(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = dedent("""\
		package body p is
		end package body p ;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "body"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       "\n"),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "body"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(CharacterToken,       ";"),
			(LinebreakToken,       "\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),
			(PackageBody.NameBlock, "package body p is"),
			(LinebreakBlock,        "\n"),
			(PackageBody.EndBlock,  "end package body p ;"),
			(LinebreakBlock,        "\n"),
			(EndOfDocumentBlock,    None)
		]
	)


class SimplePackageBody_AllLine_LongForm(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence):
	code = "package\nbody\np\nis\nend\npackage\nbody\np\n;\n"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(LinebreakToken,       "\n"),
			(WordToken,            "body"),
			(LinebreakToken,       "\n"),
			(WordToken,            "p"),
			(LinebreakToken,       "\n"),
			(WordToken,            "is"),
			(LinebreakToken,       "\n"),
			(WordToken,            "end"),
			(LinebreakToken,       "\n"),
			(WordToken,            "package"),
			(LinebreakToken,       "\n"),
			(WordToken,            "body"),
			(LinebreakToken,       "\n"),
			(WordToken,            "p"),
			(LinebreakToken,       "\n"),
			(CharacterToken,       ";"),
			(LinebreakToken,       "\n"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,  None),
			(PackageBody.NameBlock, "package"),
			(LinebreakBlock,        "\n"),
			(PackageBody.NameBlock, "body"),
			(LinebreakBlock,        "\n"),
#			(IndentationBlock,      "\t"),
			(PackageBody.NameBlock, "p"),
			(LinebreakBlock,        "\n"),
			(PackageBody.NameBlock, "is"),
			(LinebreakBlock,        "\n"),
			(PackageBody.EndBlock,  "end\n"),
#			(LinebreakBlock,        "\n"),
			(PackageBody.EndBlock,  "package\n"),
#			(LinebreakBlock,        "\n"),
			(PackageBody.EndBlock,  "body\n"),
#			(LinebreakBlock,        "\n"),
			(PackageBody.EndBlock,  "p\n"),
#			(LinebreakBlock,        "\n"),
			(PackageBody.EndBlock,  ";"),
			(LinebreakBlock,        "\n"),
			(EndOfDocumentBlock,    None)
		]
	)


class SimplePackageBody_MultiLine_LongForm_WithSingleGeneric(TestCase, ExpectedDataMixin, TokenLinking, TokenSequence, BlockSequenceWithParserError):
	code = dedent("""\
		package body p is
			generic (
				G : integer
			);
		end package body p;
		""")
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "body"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(WordToken,            "generic"),
			(SpaceToken,           " "),
			(CharacterToken,       "("),
			(LinebreakToken,       None),
			(IndentationToken,     "\t\t"),
			(WordToken,            "G"),
			(SpaceToken,           " "),
			(CharacterToken,       ":"),
			(SpaceToken,           " "),
			(WordToken,            "integer"),
			(LinebreakToken,       None),
			(IndentationToken,     "\t"),
			(CharacterToken,       ")"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "package"),
			(SpaceToken,           " "),
			(WordToken,            "body"),
			(SpaceToken,           " "),
			(WordToken,            "p"),
			(CharacterToken,       ";"),
			(LinebreakToken,       None),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(PackageBody.NameBlock,   "package body p is"),
			(LinebreakBlock,          "\n"),
			(IndentationBlock,        "\t"),
			(GenericList.OpenBlock,   "generic ("),
			(LinebreakBlock,          "\n"),
			(IndentationBlock,        "\t\t"),
			(GenericList.GenericListInterfaceConstantBlock, "G : integer"),
			(LinebreakBlock,          "\n"),
			(GenericList.GenericListInterfaceConstantBlock, "\t"),
			(GenericList.CloseBlock,  ");"),
			(LinebreakBlock,          "\n"),
			(PackageBody.EndBlock,    "end package body p;"),
			(LinebreakBlock,          "\n"),
			(EndOfDocumentBlock,      None)
		]
	)
