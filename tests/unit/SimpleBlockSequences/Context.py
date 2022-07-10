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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany                                                            #
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

from pyVHDLParser.Blocks.Common     import WhitespaceBlock
from pyVHDLParser.Blocks.Reference  import Use, Context
from pyVHDLParser.Token             import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock

from tests.unit.Common              import Initializer, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":  # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	i = Initializer()

class Library_OneLine_SingleLibrary(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "context ctx is use lib0.pkg0.all; end context;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "context"),
			(SpaceToken,           " "),
			(WordToken,            "ctx"),
			(SpaceToken,           " "),
			(WordToken,            "is"),
			(SpaceToken,           " "),
			(WordToken,            "use"),
			(SpaceToken,           " "),
			(WordToken,            "lib0"),
			(CharacterToken,       "."),
			(WordToken,            "pkg0"),
			(CharacterToken,       "."),
			(WordToken,            "all"),
			(CharacterToken,       ";"),
			(SpaceToken,           " "),
			(WordToken,            "end"),
			(SpaceToken,           " "),
			(WordToken,            "context"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock, None),                  #
			(Context.NameBlock,         "context ctx is"), #
			(WhitespaceBlock,           " "),
			(Use.StartBlock,            "use "),           # use
			(Use.ReferenceNameBlock,    "lib0.pkg0.all"),  # lib0.pkg0.all
			(Use.EndBlock,              ";"),              # ;
			(WhitespaceBlock,           " "),
			(Context.EndBlock,          "end context;"),
			(EndOfDocumentBlock,        None)              #
		]
	)
