# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python frontend:    A streaming VHDL parser
#
# License:
# ==============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
from pathlib import Path

from pyAttributes.ArgParseAttributes import CommandAttribute

from ..Base                   import ParserException
from ..DocumentModel          import Document

from .                        import FrontEndProtocol, FilenameAttribute


class CodeDOMHandlers:
	# ----------------------------------------------------------------------------
	# create the sub-parser for the "DOM" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("CodeDOM", help="Create a CodeDOM.", description="Create a code document object model (CodeDOM).")
	@FilenameAttribute()
	def HandleCodeDOM(self : FrontEndProtocol, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file)) # raise error

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		try:
			document = Document(file)
			document.Parse()
			document.Print(0)

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()
