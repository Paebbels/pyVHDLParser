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
from pathlib        import Path

from pyAttributes.ArgParseAttributes import CommandAttribute
from pyTooling.Graph import Graph, Vertex, Subgraph
from pyTooling.Graph.GraphML         import GraphMLDocument

from pyVHDLParser.Base         import ParserException
from pyVHDLParser.CLI.GraphML import GraphML
from pyVHDLParser.Token        import StartOfDocumentToken, EndOfDocumentToken, CharacterToken, SpaceToken, WordToken, LinebreakToken, CommentToken, IndentationToken
from pyVHDLParser.Token        import CharacterTranslation, SingleLineCommentToken
from pyVHDLParser.Token.Parser import Tokenizer

from pyVHDLParser.CLI              import FrontEndProtocol, FilenameAttribute, translate


class TokenStreamHandlers:
	# ----------------------------------------------------------------------------
	# create the sub-parser for the "token-stream" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("token-stream", help="Create a stream of token objects.", description="Create a stream of token objects.")
	@FilenameAttribute()
	def HandleTokenize(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if not file.exists():
			print(f"File '{file}' does not exist.")

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		tokenStream =   Tokenizer.GetVHDLTokenizer(content)
		tokenIterator = iter(tokenStream)
		firstToken =    next(tokenIterator)

		try:
			while next(tokenIterator):
				pass
		except StopIteration:
			pass

		if isinstance(firstToken, StartOfDocumentToken):
			print("{YELLOW}{token!r}{NOCOLOR}".format(token=firstToken, **self.Foreground))

		try:
			tokenIterator = firstToken.GetIterator(inclusiveStopToken=False)
			for token in tokenIterator:
				if isinstance(token, (LinebreakToken, SpaceToken, IndentationToken)):
					print("{DARK_GRAY}{token!r}{NOCOLOR}".format(token=token, **self.Foreground))
				elif isinstance(token, CommentToken):
					print("{DARK_GREEN}{token!r}{NOCOLOR}".format(token=token, **self.Foreground))
				elif isinstance(token, CharacterToken):
					print("{DARK_CYAN}{token!r}{NOCOLOR}".format(token=token, **self.Foreground))
				elif isinstance(token, WordToken):
					print("{WHITE}{token!r}{NOCOLOR}".format(token=token, **self.Foreground))
				else:
					print("{RED}{token!r}{NOCOLOR}".format(token=token, **self.Foreground))

			tokenIterator = token.GetIterator()
			lastToken = next(tokenIterator)
			if isinstance(lastToken, EndOfDocumentToken):
				print("{YELLOW}{token!r}{NOCOLOR}".format(token=lastToken, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		exporter = GraphML()
		exporter.AddTokenStream(firstToken)
		exporter.WriteDocument(Path.cwd() / "temp/TokenStream.graphml")

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "token-check" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("token-check", help="Check a stream of token objects.", description="Generates and checks a stream of token objects for correct double-pointers.")
	@FilenameAttribute()
	def HandleCheckTokenize(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if not file.exists():
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)

		try:
			tokenIterator = iter(vhdlTokenStream)
			firstToken = next(tokenIterator)

			try:
				while next(tokenIterator):
					pass
			except StopIteration:
				pass

			if not isinstance(firstToken, StartOfDocumentToken):
				print("{RED}First token is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstToken, **self.Foreground))
			if firstToken.NextToken is None:
				print("{RED}First token has an open end.{NOCOLOR}".format(**self.Foreground))

			tokenIterator = firstToken.GetIterator()
			lastToken =     None
			token =     firstToken

			for newToken in tokenIterator:
				if token.NextToken is None:
					print("{RED}Token has an open end.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Token:  {token}{NOCOLOR}".format(token=token, **self.Foreground))
				elif (token is not firstToken) and (lastToken.NextToken is not token):
					print("{RED}Last token is not connected to the current token.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **self.Foreground))
					print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **self.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
					print("{RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
					if lastToken.NextToken is None:
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token="--------", **self.Foreground))
					else:
						print(
							"{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken.NextToken, **self.Foreground))
					if token.PreviousToken is None:
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token="--------", **self.Foreground))
					else:
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken.PreviousToken,
						                                                    **self.Foreground))
				elif token.PreviousToken is not lastToken:
					print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **self.Foreground))
					print("{RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **self.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
					print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))

				lastToken = token
				token = newToken

				if isinstance(newToken, EndOfDocumentToken):
					print("{GREEN}No double-linking errors in token stream found.{NOCOLOR}".format(**self.Foreground))
					break
			else:
				print("{RED}No EndOfDocumentToken found.{NOCOLOR}".format(**self.Foreground))

			if not isinstance(token, EndOfDocumentToken):
				print(
					"{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
			elif token.PreviousToken is not lastToken:
				print("{RED}EndOfDocumentToken is not connected to lastToken.{NOCOLOR}".format(**self.Foreground))
				print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **self.Foreground))
				print("{RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **self.Foreground))
				print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
				print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()
