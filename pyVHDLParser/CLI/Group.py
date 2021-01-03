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
from ..Token                  import CharacterToken, SpaceToken, WordToken, LinebreakToken, CommentToken, IndentationToken
from ..Token.Parser           import Tokenizer
from ..Token.Keywords         import BoundaryToken, EndToken, KeywordToken, DelimiterToken
from ..Blocks                 import TokenToBlockParser
from ..Groups                 import BlockToGroupParser

from .                        import FrontEndProtocol, WithTokensAttribute, WithBlocksAttribute, FilenameAttribute


class GroupStreamHandlers:
	# ----------------------------------------------------------------------------
	# create the sub-parser for the "groupstreaming" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("group-stream", help="Create a stream of group objects.", description="Create a stream of group objects.")
	@WithTokensAttribute()
	@WithBlocksAttribute()
	@FilenameAttribute()
	def HandleGroupStreaming(self : FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		buffered = True
		if buffered:
			self.WriteVerbose("Reading and buffering tokens...")
			try:
				tokenStream = [token for token in Tokenizer.GetVHDLTokenizer(content)]
			except ParserException as ex:
				self.WriteError("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
			except NotImplementedError as ex:
				print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

			self.WriteVerbose("Reading and buffering blocks...")
			try:
				blockStream = [block for block in TokenToBlockParser.Transform(tokenStream)]
			except ParserException as ex:
				print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
			except NotImplementedError as ex:
				print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		else:
			tokenStream = Tokenizer.GetVHDLTokenizer(content)
			blockStream = TokenToBlockParser.Transform(tokenStream)

		self.WriteVerbose("Transforming blocks to groups...")
		groupStream = BlockToGroupParser.Transform(blockStream)

		try:
			for group in groupStream:
				print("{CYAN}{group}{NOCOLOR}".format(group=group, **self.Foreground))
				for block in group:
					if isinstance(block, (IndentationToken, LinebreakToken, BoundaryToken, DelimiterToken, EndToken)):
						print("{DARK_GRAY}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					elif isinstance(block, (CommentToken)):
						print("{DARK_GREEN}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					elif isinstance(block, KeywordToken):
						print("{DARK_CYAN}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					elif isinstance(block, (WordToken, SpaceToken, CharacterToken)):
						print("{DARK_GREEN}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					else:
						print("{YELLOW}  {block}{NOCOLOR}".format(block=block, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()
