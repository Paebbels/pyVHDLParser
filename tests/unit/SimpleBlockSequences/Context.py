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
from unittest                       import TestCase

from pyVHDLParser.Blocks.Whitespace import WhitespaceBlock
from pyVHDLParser.Blocks.Reference  import Context, Use, Library
from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, WhitespaceToken, CharacterToken, EndOfDocumentToken, SingleLineCommentToken, MultiLineCommentToken, IndentationToken, LinebreakToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock, CommentBlock
from pyVHDLParser.Blocks.Whitespace import IndentationBlock, LinebreakBlock

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":  # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	_ = Initializer()

class Context_OneLine_SingleLibrary(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context ctx is use lib0.pkg0.all; end context;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "context"),
			(WhitespaceToken, " "),
			(WordToken,            "ctx"),
			(WhitespaceToken, " "),
			(WordToken,            "is"),
			(WhitespaceToken, " "),
			(WordToken,            "use"),
			(WhitespaceToken, " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ";"),
			(WhitespaceToken, " "),
			(WordToken,            "end"),
			(WhitespaceToken, " "),
			(WordToken,            "context"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(Context.DeclarationStartBlock,  "context"), #
			(WhitespaceBlock,                " "),
			(Context.DeclarationStartBlock,  "ctx"), #
			(WhitespaceBlock,                " "),
			(Context.DeclarationStartBlock,  "is"), #
			(WhitespaceBlock,                " "),
			(Use.StartBlock,                 "use "),           # use
			(Use.ReferenceNameBlock,         "lib0.pkg0.all"),  # lib0.pkg0.all
			(Use.EndBlock,                   ";"),              # ;
			(WhitespaceBlock,                " "),
			(Context.DeclarationEndBlock,    "end context;"),
			(EndOfDocumentBlock,             None)              #
		]
	)

class Context_SingleLibrary_Whitespaces(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context --test1\n ctx is use lib0.pkg0.all; end  --test\ncontext /**/;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "context"),
			(WhitespaceToken, " "),
			(SingleLineCommentToken, "--test1\n"),
			(IndentationToken, " "),
			(WordToken,            "ctx"),
			(WhitespaceToken, " "),
			(WordToken,            "is"),
			(WhitespaceToken, " "),
			(WordToken,            "use"),
			(WhitespaceToken, " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ";"),
			(WhitespaceToken, " "),
			(WordToken,            "end"),
			(WhitespaceToken, "  "),
			(SingleLineCommentToken, "--test\n"),
			(WordToken,            "context"),
			(WhitespaceToken, " "),
			(MultiLineCommentToken, "/**/"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),
			(Context.DeclarationStartBlock,  "context"),
			(WhitespaceBlock,                " "),
			(CommentBlock,                   "--test1\n"),
			(IndentationBlock,               " "),
			(Context.DeclarationStartBlock,  "ctx"),
			(WhitespaceBlock,                " "),
			(Context.DeclarationStartBlock,  "is"),
			(WhitespaceBlock,                " "),
			(Use.StartBlock,                 "use "),           # use
			(Use.ReferenceNameBlock,         "lib0.pkg0.all"),  # lib0.pkg0.all
			(Use.EndBlock,                   ";"),              # ;
			(WhitespaceBlock,                " "),
			(Context.DeclarationEndBlock,    "end  "),
			(CommentBlock,                   "--test\n"),
			(Context.DeclarationEndBlock,    "context "),
			(CommentBlock,                   "/**/"),
			(Context.DeclarationEndBlock,    ";"),
			(EndOfDocumentBlock,             None)              #
		]
	)

class Context_OneLine_Single_SimpleReference(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context ctx;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,             "context"),
			(WhitespaceToken,       " "),
			(WordToken,             "ctx"),
			(CharacterToken,        ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(Context.ReferenceStartBlock, "context"), #
			(WhitespaceBlock,             " "),
			(Context.ReferenceNameBlock,  "ctx"), #
			(Context.ReferenceEndBlock,   ";"), #
			(EndOfDocumentBlock,     None)              #
		]
	)


class Context_OneLine_Single_Reference(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context lib.ctx;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,             "context"),
			(WhitespaceToken,       " "),
			(WordToken,             "lib"),
			(CharacterToken,        "."),
			(WordToken,             "ctx"),
			(CharacterToken,        ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(Context.ReferenceStartBlock, "context"),
			(WhitespaceBlock,             " "),
			(Context.ReferenceNameBlock,  "lib.ctx"),
			(Context.ReferenceEndBlock,   ";"),
			(EndOfDocumentBlock,     None)
		]
	)


class Context_OneLine_Multiple_References(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context lib.ctx,ctx2,xil_defaultlib.ctx3;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,             "context"),
			(WhitespaceToken,       " "),
			(WordToken,             "lib"),
			(CharacterToken,        "."),
			(WordToken,             "ctx"),
			(CharacterToken,        ","),
			(WordToken,             "ctx2"),
			(CharacterToken,        ","),
			(WordToken,             "xil_defaultlib"),
			(CharacterToken,        "."),
			(WordToken,             "ctx3"),
			(CharacterToken,        ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),
			(Context.ReferenceStartBlock, "context"),
			(WhitespaceBlock,             " "),
			(Context.ReferenceNameBlock,  "lib.ctx"),
			(Context.DelimiterBlock,      ","),
			(Context.ReferenceNameBlock,  "ctx2"),
			(Context.DelimiterBlock,      ","),
			(Context.ReferenceNameBlock,  "xil_defaultlib.ctx3"),
			(Context.ReferenceEndBlock,  ";"),
			(EndOfDocumentBlock,     None)
		]
	)

class Context_OneLine_Multiple_References2(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context lib.ctx,ctx2,ctx3;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,             "context"),
			(WhitespaceToken,       " "),
			(WordToken,             "lib"),
			(CharacterToken,        "."),
			(WordToken,             "ctx"),
			(CharacterToken,        ","),
			(WordToken,             "ctx2"),
			(CharacterToken,        ","),
			(WordToken,             "ctx3"),
			(CharacterToken,        ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(Context.ReferenceStartBlock, "context"),
			(WhitespaceBlock,             " "),
			(Context.ReferenceNameBlock,  "lib.ctx"),
			(Context.DelimiterBlock,      ","),
			(Context.ReferenceNameBlock,  "ctx2"),
			(Context.DelimiterBlock,      ","),
			(Context.ReferenceNameBlock,  "ctx3"),
			(Context.ReferenceEndBlock,  ";"),
			(EndOfDocumentBlock,     None)
		]
	)


class Context_Multiline_Multiple_Libraries_And_Contexts(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = """
context ctx_name is
   library ieee;
   use ieee.numeric_std.all;

   -- Include another context
   library xil_defaultlib;
   context xil_defaultlib.my_ctx;
end context;
"""
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(LinebreakToken,        None),
			(WordToken,             "context"),
			(WhitespaceToken,       " "),
			(WordToken,             "ctx_name"),
			(WhitespaceToken,       " "),
			(WordToken,             "is"),
			(LinebreakToken,        None),
			(IndentationToken,      "   "),
			(WordToken,             "library"),
			(WhitespaceToken,       " "),
			(WordToken,             "ieee"),
			(CharacterToken,        ";"),
			(LinebreakToken,        None),
			(IndentationToken,      "   "),
			(WordToken,             "use"),
			(WhitespaceToken,       " "),
			(WordToken,             "ieee"),
			(CharacterToken,        "."),
			(WordToken,             "numeric_std"),
			(CharacterToken,        "."),
			(WordToken,             "all"),
			(CharacterToken,        ";"),
			(LinebreakToken,        None),
			(LinebreakToken,        None),
			(IndentationToken,      "   "),
			(SingleLineCommentToken, "-- Include another context\n"),
			(IndentationToken,      "   "),
			(WordToken,             "library"),
			(WhitespaceToken,       " "),
			(WordToken,             "xil_defaultlib"),
			(CharacterToken,        ";"),
			(LinebreakToken,        None),
			(IndentationToken,      "   "),
			(WordToken,             "context"),
			(WhitespaceToken,       " "),
			(WordToken,             "xil_defaultlib"),
			(CharacterToken,        "."),
			(WordToken,             "my_ctx"),
			(CharacterToken,        ";"),
			(LinebreakToken,        None),
			(WordToken,             "end"),
			(WhitespaceToken,       " "),
			(WordToken,             "context"),
			(CharacterToken,        ";"),
			(LinebreakToken,        None),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(LinebreakBlock,               None),
			(Context.DeclarationStartBlock, "context"),
			(WhitespaceBlock,               " "),
			(Context.DeclarationStartBlock, "ctx_name"),
			(WhitespaceBlock,               " "),
			(Context.DeclarationStartBlock, "is"),
			(LinebreakBlock,               None),
			(IndentationBlock,             "   "),
			(Library.StartBlock,           "library "),
			(Library.LibraryNameBlock,     "ieee"),
			(Library.EndBlock,             ";"),
			(LinebreakBlock,               None),
			(IndentationBlock,             "   "),
			(Use.StartBlock,               "use "),
			(Use.ReferenceNameBlock,       "ieee.numeric_std.all"),
			(Use.EndBlock,                 ";"),
			(LinebreakBlock,               None),
			(LinebreakBlock,               None),
			(IndentationBlock,             "   "),
			(CommentBlock,                 "-- Include another context\n"),
			(IndentationBlock,             "   "),
			(Library.StartBlock,           "library "),
			(Library.LibraryNameBlock,     "xil_defaultlib"),
			(Library.EndBlock,             ";"),
			(LinebreakBlock,               None),
			(IndentationBlock,             "   "),
			(Context.ReferenceStartBlock,  "context"),
			(WhitespaceBlock,              " "),
			(Context.ReferenceNameBlock,   "xil_defaultlib.my_ctx"),
			(Context.ReferenceEndBlock,    ";"),
			(LinebreakBlock,               None),
			(Context.DeclarationEndBlock,  "end context;"), #
			(LinebreakBlock,               None),
			(EndOfDocumentBlock,     None)              #
		]
	)
