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

from pyVHDLParser.Token             import StartOfDocumentToken, WordToken, WhitespaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks            import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Whitespace     import WhitespaceBlock
from pyVHDLParser.Blocks.Object     import Signal
from pyVHDLParser.Blocks.Structural import Architecture

from tests.unit.Common              import Initializer, ExpectedTokenStream, ExpectedBlockStream, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence


if __name__ == "__main__":  # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class SimpleSignalInArchitecture_OneLine_OnlyDeclaration(TestCase, ExpectedDataMixin, LinkingTests, TokenSequence, BlockSequence):
	code = "architecture a of e is signal s : bit; begin end;"
	tokenStream = ExpectedTokenStream(
		[ (StartOfDocumentToken, None),
			(WordToken,            "architecture"),
			(WhitespaceToken, " "),
			(WordToken,            "a"),
			(WhitespaceToken, " "),
			(WordToken,            "of"),
			(WhitespaceToken, " "),
			(WordToken,            "e"),
			(WhitespaceToken, " "),
			(WordToken,            "is"),
			(WhitespaceToken, " "),
			(WordToken,            "signal"),
			(WhitespaceToken, " "),
			(WordToken,            "s"),
			(WhitespaceToken, " "),
			(CharacterToken,       ":"),
			(WhitespaceToken, " "),
			(WordToken,            "bit"),
			(CharacterToken,       ";"),
			(WhitespaceToken, " "),
			(WordToken,            "begin"),
			(WhitespaceToken, " "),
			(WordToken,            "end"),
			(CharacterToken,       ";"),
			(EndOfDocumentToken,   None)
		]
	)
	blockStream = ExpectedBlockStream(
		[ (StartOfDocumentBlock,    None),
			(Architecture.NameBlock,  "architecture a of e is"),
			(WhitespaceBlock,         " "),
			(Signal.SignalDeclarationBlock,           "signal s : bit"),
			(Signal.SignalDeclarationEndMarkerBlock,  ";"),
			(WhitespaceBlock,         " "),
			(Architecture.BeginBlock, "begin"),
			(WhitespaceBlock,         " "),
			(Architecture.EndBlock,   "end;"),
			(EndOfDocumentBlock,      None)
		]
	)
