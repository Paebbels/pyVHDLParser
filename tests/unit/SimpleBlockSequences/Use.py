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

from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, WhitespaceToken, CharacterToken, EndOfDocumentToken, LinebreakToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Whitespace     import LinebreakBlock
from pyVHDLParser.Blocks.Reference  import Use

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":  # pragma: no cover
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
			(WhitespaceToken, " "),
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
			(WhitespaceToken, " "),
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
			(WhitespaceToken, " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ","),
			(WhitespaceToken, " "),
			(WordToken,            "lib0"),
			(WhitespaceToken, " "),
			(CharacterToken,       "."),
			(WhitespaceToken, " "),
			(WordToken,            "pkg1"),
			(WhitespaceToken, " "),
			(CharacterToken,       "."),
			(WhitespaceToken, " "),
			(WordToken,            "all"),
			(WhitespaceToken, " "),
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
