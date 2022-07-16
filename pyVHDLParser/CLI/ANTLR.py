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
from pathlib        import Path

from antlr4 import CommonTokenStream, InputStream
from pyAttributes.ArgParseAttributes import CommandAttribute

from ..ANTLR4.VHDLLexer import VHDLLexer
from ..ANTLR4.VHDLParser import VHDLParser


from . import FrontEndProtocol, FilenameAttribute


class ANTLRHandlers:
	# ----------------------------------------------------------------------------
	# create the sub-parser for the "token-stream" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("antlr", help="Create DOM from ANTLR4 grammar.", description="Create DOM from ANTLR4 grammar.")
	@FilenameAttribute()
	def HandleANTLR(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if not file.exists():
			print(f"File '{file}' does not exist.")

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		lexer = VHDLLexer(InputStream(content))
		stream = CommonTokenStream(lexer)
		parser = VHDLParser(stream)

		parserTree = parser.design_file()

		self.exit()
