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
from unittest                           import TestCase

from pyVHDLParser.Blocks.List           import PortList
from pyVHDLParser.Blocks.List.PortList  import PortListInterfaceSignalBlock
from pyVHDLParser.Token                 import WordToken, StartOfDocumentToken, SpaceToken, CharacterToken, EndOfDocumentToken
from pyVHDLParser.Blocks                import StartOfDocumentBlock, EndOfDocumentBlock
from pyVHDLParser.Blocks.Common         import WhitespaceBlock
from pyVHDLParser.Blocks.Structural     import Entity

from tests.unit.Common                  import Initializer, ExpectedDataMixin, LinkingTests, TokenLinking, TokenSequence, BlockSequence, ExpectedTokenStream, ExpectedBlockStream


if __name__ == "__main__":  # pragma: no cover
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
