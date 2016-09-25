# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python functions:   A streaming VHDL parser
#
# Description:
# ------------------------------------
#		TODO:
#
# License:
# ==============================================================================
# Copyright 2007-2016 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
from pathlib import Path

import sys

from src.Base               import ParserException
from src.Filter.Comment     import StripAndFuse
from src.Functions          import Console, Exit
from src.Token.Tokens       import EndOfDocumentToken, DelimiterToken, StringToken, SpaceToken, CharacterToken
from src.Token.Keywords     import IndentationToken, LinebreakToken, BoundaryToken, EndToken, KeywordToken
from src.Token.Keywords     import SingleLineCommentKeyword, MultiLineCommentStartKeyword, MultiLineCommentEndKeyword
from src.Token.Parser       import Tokenizer, StartOfDocumentToken
from src.Blocks.Common      import LinebreakBlock, IndentationBlock
from src.Blocks.Comment     import CommentBlock
from src.Blocks.Document    import StartOfDocumentBlock, EndOfDocumentBlock
from src.Blocks.Structural  import Entity
from src.Blocks.List        import GenericList, PortList
from src.Blocks.Parser      import TokenToBlockParser


Console.init()

rootDirectory = Path(".")
vhdlDirectory = rootDirectory / "vhdl"

if (len(sys.argv) == 2):
	file = Path(sys.argv[1])
	mode = 255
elif (len(sys.argv) == 3):
	file = Path(sys.argv[1])
	mode = int(sys.argv[2])
	print("mode={0}".format(mode))
else:
	print("File name expected.")
	Exit.exit(-1)

if (not file.exists()):
	print("File '{0!s}' does not exist.".format(file))

content = None
with file.open('r') as fileHandle:
	content = fileHandle.read()


alphaCharacters = Tokenizer.__ALPHA_CHARS__ + "_" + Tokenizer.__NUMBER_CHARS__

# ==============================================================================
if (mode & 2 == 2):
	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters, numberCharacters="")
	vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream, debug=(mode & 1 == 1))

	try:
		for vhdlBlock in vhdlBlockStream:
			if isinstance(vhdlBlock, (LinebreakBlock, IndentationBlock)):
				print("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, CommentBlock):
				print("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (Entity.NameBlock, Entity.BeginBlock, Entity.EndBlock)):
				print("{DARK_RED}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (GenericList.OpenBlock, GenericList.DelimiterBlock, GenericList.CloseBlock)):
				print("{DARK_BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (PortList.OpenBlock, PortList.DelimiterBlock, PortList.CloseBlock)):
				print("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (GenericList.ItemBlock, PortList.ItemBlock)):
				print("{BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			else:
				print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
	except ParserException as ex:
		print("ERROR: " + str(ex))
	except NotImplementedError as ex:
		print("NotImplementedError: " + str(ex))


# ==============================================================================
if (mode & 4 == 4):
	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters, numberCharacters="")
	vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream, debug=(mode & 1 == 1))

	try:
		blockIterator = iter(vhdlBlockStream)
		firstBlock = next(blockIterator)
		if (not isinstance(firstBlock, StartOfDocumentBlock)):
			print("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=firstBlock, **Console.Foreground))
		elif (not isinstance(firstBlock.StartToken, StartOfDocumentToken)):
			print("{RED}First block is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstBlock.StartToken, **Console.Foreground))

		lastBlock = None
		lastToken = firstBlock.StartToken

		for vhdlBlock in blockIterator:
			if isinstance(vhdlBlock, EndOfDocumentBlock):
				lastBlock = vhdlBlock
				break
			tokenIterator = iter(vhdlBlock)

			for token in tokenIterator:
				if (token.NextToken is None):
					print("{RED}Token has an open end.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
					print("{RED}  Token:  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif (lastToken.NextToken is not token):
					print("{RED}Last token is not connected to the current one.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
					print("{RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **Console.Foreground))
					if (lastToken.NextToken is None):
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token="--------", **Console.Foreground))
					else:
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken.NextToken, **Console.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **Console.Foreground))
					print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **Console.Foreground))
					if (token.PreviousToken is None):
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token="--------", **Console.Foreground))
					else:
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken.PreviousToken, **Console.Foreground))
				elif (token.PreviousToken is not lastToken):
					print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
					print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **Console.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **Console.Foreground))
					print("{RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **Console.Foreground))

				lastToken = token
		else:
			print("{RED}No EndOfDocumentBlock found.{NOCOLOR}".format(**Console.Foreground))

		if (not isinstance(lastBlock, EndOfDocumentBlock)):
			print("{RED}Last block is not EndOfDocumentBlock: {block}{NOCOLOR}".format(block=lastBlock, **Console.Foreground))
		elif (not isinstance(lastBlock.StartToken, EndOfDocumentToken)):
			print("{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=lastBlock.StartToken, **Console.Foreground))

	except ParserException as ex:
		print("ERROR: " + str(ex))
	except NotImplementedError as ex:
		print("NotImplementedError: " + str(ex))

# ==============================================================================
if (mode & 8 == 8):
	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters, numberCharacters="")
	vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream, debug=(mode & 1 == 1))

	try:
		for vhdlBlock in vhdlBlockStream:
			print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			for token in vhdlBlock:
				if isinstance(token, (IndentationToken, LinebreakToken, BoundaryToken, DelimiterToken, EndToken)):
					print("{DARK_GRAY}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, (SingleLineCommentKeyword, MultiLineCommentStartKeyword, MultiLineCommentEndKeyword)):
					print("{DARK_GREEN}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, KeywordToken):
					print("{DARK_CYAN}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, (StringToken, SpaceToken, CharacterToken)):
					print("{DARK_RED}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				else:
					print("{YELLOW}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
	except ParserException as ex:
		print("ERROR: " + str(ex))
	except NotImplementedError as ex:
		print("NotImplementedError: " + str(ex))


# ==============================================================================
if (mode & 16 == 16):
	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters, numberCharacters="")
	vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream, debug=(mode & 1 == 1))
	strippedBlockStream = StripAndFuse(vhdlBlockStream)

	try:
		for vhdlBlock in strippedBlockStream:
			if isinstance(vhdlBlock, (LinebreakBlock, IndentationBlock)):
				print("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, CommentBlock):
				print("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (Entity.NameBlock, Entity.BeginBlock, Entity.EndBlock)):
				print("{DARK_RED}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (GenericList.OpenBlock, GenericList.DelimiterBlock, GenericList.CloseBlock)):
				print("{DARK_BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (PortList.OpenBlock, PortList.DelimiterBlock, PortList.CloseBlock)):
				print("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (GenericList.ItemBlock, PortList.ItemBlock)):
				print("{BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			else:
				print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
	except ParserException as ex:
		print("ERROR: " + str(ex))
	except NotImplementedError as ex:
		print("NotImplementedError: " + str(ex))
