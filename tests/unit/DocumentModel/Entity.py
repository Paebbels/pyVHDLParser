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
# Copyright 2017-2022 Patrick Lehmann - Boetzingen, Germany                                                            #
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
from textwrap import dedent
from unittest import TestCase

from pytest   import mark

from pyVHDLParser.DocumentModel import Document
from tests.unit.Common import Initializer


if __name__ == "__main__":  # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class Entity(TestCase):
	@mark.xfail(reason="Not working yet")
	def test_Entity(self):
		code = dedent("""\
			package p is
			end package;
			""")

		document = Document("Entity.vhdl")
		document.Parse(code)

		self.assertTrue(len(document.Architectures) == 0,   "Document contains unexpected architectures.")
		self.assertTrue(len(document.Configurations) == 0,  "Document contains unexpected configurations.")
		self.assertTrue(len(document.Contexts) == 0,        "Document contains unexpected contexts.")
		self.assertTrue(len(document.Entities) == 1,        "Document doesn't contain the expected entity.")
		self.assertTrue(len(document.Libraries) == 0,       "Document contains unexpected libraries.")
		self.assertTrue(len(document.PackageBodies) == 0,   "Document contains unexpected package bodies.")
		self.assertTrue(len(document.Packages) == 0,        "Document contains unexpected packages.")
		self.assertTrue(len(document.Uses) == 0,            "Document contains unexpected uses.")
