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
from pathlib import Path

from pyAttributes.ArgParseAttributes import CommandAttribute

from .GraphML import GraphML
from ..Base                   import ParserException
from ..Token                  import CharacterToken, SpaceToken, WordToken, LinebreakToken, CommentToken, IndentationToken
from ..Token.Parser           import Tokenizer
from ..Token.Keywords         import BoundaryToken, EndToken, KeywordToken, DelimiterToken
from ..Blocks                 import TokenToBlockParser
from ..Groups import BlockToGroupParser, StartOfDocumentGroup

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

		if not file.exists():
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		tokenStream = Tokenizer.GetVHDLTokenizer(content)
		blockStream = TokenToBlockParser(tokenStream)()
		groupStream = BlockToGroupParser(blockStream)()

		groupIterator = iter(groupStream)
		firstGroup = next(groupIterator)

		try:
			while next(groupIterator):
				pass
		except StopIteration:
			pass

		if isinstance(firstGroup, StartOfDocumentGroup):
			print("{YELLOW}{group!r}{NOCOLOR}".format(block=firstGroup, **self.Foreground))
			print("  {YELLOW}{block!r}{NOCOLOR}".format(block=firstGroup.StartBlock, **self.Foreground))
			print("    {YELLOW}{token!r}{NOCOLOR}".format(token=firstGroup.StartBlock.StartToken, **self.Foreground))

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
				blockStream = [block for block in TokenToBlockParser(tokenStream)()]
			except ParserException as ex:
				print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
			except NotImplementedError as ex:
				print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		else:
			tokenStream = Tokenizer.GetVHDLTokenizer(content)
			blockStream = TokenToBlockParser(tokenStream)()

		self.WriteVerbose("Transforming blocks to groups...")
		groupStream = BlockToGroupParser(blockStream)()

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

		exporter = GraphML()
		tokenStreamSubgraph = exporter.AddTokenStream(firstBlock.StartToken)
		blockStreamSubgraph = exporter.AddBlockStream(firstBlock, tokenStreamSubgraph)
		blockStreamSubgraph = exporter.AddGroupStream(firstBlock, blockStreamSubgraph)
		exporter.WriteDocument(Path.cwd() / "temp/BlockStream.graphml")

		self.exit()
