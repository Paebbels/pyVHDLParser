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
from pathlib        import Path
from textwrap       import dedent

from pyAttributes.ArgParseAttributes import CommandAttribute

from ..Base         import ParserException
from ..Token        import StartOfDocumentToken, EndOfDocumentToken, CharacterToken, SpaceToken, WordToken, LinebreakToken, CommentToken, IndentationToken
from ..Token        import CharacterTranslation, SingleLineCommentToken
from ..Token.Parser import Tokenizer

from .              import FrontEndProtocol, FilenameAttribute, translate


class TokenStreamHandlers:
	# ----------------------------------------------------------------------------
	# create the sub-parser for the "token-stream" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("token-stream", help="Create a stream of token objects.", description="Create a stream of token objects.")
	@FilenameAttribute()
	def HandleTokenize(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

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

		nodeFormat="t_{line}_{id}"
		nodeID = 0
		line =   0
		node =   nodeFormat.format(line=line, id=nodeID)
		graphvizBuffer = dedent("""\
			digraph TokenStream {{
				graph [rankdir=LR splines=ortho]
			  node [shape=record];

		    {node} [style=filled, fillcolor=gold, label="{caption}|{{None|None|Next}}"];
			""").format(
			node=node,
			caption=firstToken.__class__.__qualname__
		)
		lline =      0
		sameRanked = [node]
		lineStarts = [node]

		tokenIterator = firstToken.GetIterator(inclusiveStopToken=False)
		for token in tokenIterator:
			nodeID += 1
			nnode=nodeFormat.format(line=line, id=nodeID)
			graphvizBuffer += dedent("""\
			  {lnode} -> {node};
			  {node} [style=filled, fillcolor={color}, label="{caption}|{{Prev|{content}|Next}}"];
			""").format(
				node=nnode,
				lnode=node,
				color=translate(token),
				caption=token.__class__.__qualname__,
				content=CharacterTranslation(str(token))
			)
			node = nnode
			if len(sameRanked) == 0:
				lineStarts.append(node)
			sameRanked.append(node)

			if isinstance(token, (LinebreakToken, SingleLineCommentToken)):
				# graphvizBuffer += dedent("""\
				#
				#   {{ rank=same {nodes} }}
				#
				# """).format(nodes=" ".join(sameRanked))

				sameRanked = []
				line += 1
			else:
				lline = line

		tokenIterator = token.GetIterator()
		lastToken = next(tokenIterator)

		graphvizBuffer += dedent("""\
		  t_{lline}_{lid} -> t_{line}_00;
		  t_{line}_00 [style=filled, fillcolor=gold, label="{caption}|{{Prev|None|None}}"];

		  {{ rank=same {nodes} }}
		}}
		""").format(
			line=line,
			lline=lline,
			lid=nodeID - 1,
			caption=lastToken.__class__.__qualname__,
			nodes=" ".join(lineStarts)
		)

		gvFile = file.with_suffix('.gv')
		with gvFile.open('w') as fileHandle:
			fileHandle.write(graphvizBuffer)

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "token-check" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("token-check", help="Check a stream of token objects.", description="Generates and checks a stream of token objects for correct double-pointers.")
	@FilenameAttribute()
	def HandleCheckTokenize(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if (not file.exists()):
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

			if (not isinstance(firstToken, StartOfDocumentToken)):
				print("{RED}First token is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstToken, **self.Foreground))
			if (firstToken.NextToken is None):
				print("{RED}First token has an open end.{NOCOLOR}".format(**self.Foreground))

			tokenIterator = firstToken.GetIterator()
			lastToken =     None
			token =     firstToken

			for newToken in tokenIterator:
				if (token.NextToken is None):
					print("{RED}Token has an open end.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Token:  {token}{NOCOLOR}".format(token=token, **self.Foreground))
				elif ((token is not firstToken) and (lastToken.NextToken is not token)):
					print("{RED}Last token is not connected to the current token.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **self.Foreground))
					print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **self.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
					print("{RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
					if (lastToken.NextToken is None):
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token="--------", **self.Foreground))
					else:
						print(
							"{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken.NextToken, **self.Foreground))
					if (token.PreviousToken is None):
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token="--------", **self.Foreground))
					else:
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken.PreviousToken,
						                                                    **self.Foreground))
				elif (token.PreviousToken is not lastToken):
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

			if (not isinstance(token, EndOfDocumentToken)):
				print(
					"{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
			elif (token.PreviousToken is not lastToken):
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
