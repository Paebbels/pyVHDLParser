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
# Copyright 2007-2017 Patrick Lehmann - Dresden, Germany
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
# load dependencies
from pathlib import Path

import sys

import pyVHDLParser.Blocks.InterfaceObject
from pyVHDLParser.Base               import ParserException
from pyVHDLParser.Token              import StartOfDocumentToken, EndOfDocumentToken, CharacterToken, SpaceToken, StringToken, LinebreakToken, CommentToken, IndentationToken, Token
from pyVHDLParser.Token.Keywords     import BoundaryToken, EndToken, KeywordToken, DelimiterToken, IdentifierToken
from pyVHDLParser.Blocks             import CommentBlock, Block, StartOfDocumentBlock, EndOfDocumentBlock, MetaBlock
from pyVHDLParser.Blocks.Common      import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Structural  import Entity
from pyVHDLParser.Blocks.List        import GenericList, PortList
from pyVHDLParser.Functions          import Console, Exit



Console.init()

for block in MetaBlock.BLOCKS:
	try:
		block.__cls_init__()
	except AttributeError:
		pass

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

with file.open('r') as fileHandle:
	content = fileHandle.read()


# ==============================================================================
if (mode & 6 == 2):
	from pyVHDLParser.Token.Parser  import Tokenizer

	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)

	try:
		for vhdlToken in vhdlTokenStream:
			if isinstance(vhdlToken, (LinebreakToken, SpaceToken, IndentationToken)):
				print("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlToken, **Console.Foreground))
			elif isinstance(vhdlToken, CommentToken):
				print("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlToken, **Console.Foreground))
			elif isinstance(vhdlToken, CharacterToken):
				print("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlToken, **Console.Foreground))
			elif isinstance(vhdlToken, StringToken):
				print("{WHITE}{block}{NOCOLOR}".format(block=vhdlToken, **Console.Foreground))
			elif isinstance(vhdlToken, (StartOfDocumentToken, EndOfDocumentToken)):
				print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlToken, **Console.Foreground))
			else:
				print("{RED}{block}{NOCOLOR}".format(block=vhdlToken, **Console.Foreground))
	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))

	if (mode & 1 == 1):
		print("{RED}{line}{NOCOLOR}".format(line="=" * 160, **Console.Foreground))
		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)

		try:
			tokenIterator = iter(vhdlTokenStream)
			firstToken = next(tokenIterator)
			if (not isinstance(firstToken, StartOfDocumentToken)):
				print("{RED}First block is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstToken, **Console.Foreground))

			lastToken = None
			vhdlToken = firstToken

			for newToken in tokenIterator:
				if (vhdlToken.NextToken is None):
					print("{RED}Token has an open end.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Token:  {token}{NOCOLOR}".format(token=vhdlToken, **Console.Foreground))
				elif ((vhdlToken is not firstToken) and (lastToken.NextToken is not vhdlToken)):
					print("{RED}Last token is not connected to the current token.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=vhdlToken, **Console.Foreground))
					print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken, **Console.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
					print("{RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **Console.Foreground))
					if (lastToken.NextToken is None):
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token="--------", **Console.Foreground))
					else:
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken.NextToken, **Console.Foreground))
					if (vhdlToken.PreviousToken is None):
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token="--------", **Console.Foreground))
					else:
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken.PreviousToken, **Console.Foreground))
				elif (vhdlToken.PreviousToken is not lastToken):
					print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=vhdlToken, **Console.Foreground))
					print("{RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken, **Console.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
					print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **Console.Foreground))

				lastToken = vhdlToken
				vhdlToken = newToken

				if isinstance(newToken, EndOfDocumentToken):
					break
			else:
				print("{RED}No EndOfDocumentToken found.{NOCOLOR}".format(**Console.Foreground))

			if (not isinstance(vhdlToken, EndOfDocumentToken)):
				print("{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
			elif (vhdlToken.PreviousToken is not lastToken):
				print("{RED}EndOfDocumentToken is not connected to lastToken.{NOCOLOR}".format(**Console.Foreground))
				print("{RED}  Curr:   {token}{NOCOLOR}".format(token=vhdlToken, **Console.Foreground))
				print("{RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken, **Console.Foreground))
				print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
				print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **Console.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))

# ==============================================================================
if (mode & 6 == 4):
	from pyVHDLParser.Token.Parser  import Tokenizer
	from pyVHDLParser.Blocks import TokenToBlockParser

	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
	vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream, debug=(mode & 1 == 1))

	try:
		for vhdlBlock in vhdlBlockStream:
			if isinstance(vhdlBlock, (LinebreakBlock, IndentationBlock)):
				print("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, CommentBlock):
				print("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (Entity.NameBlock, Entity.NameBlock, Entity.EndBlock)):
				print("{DARK_RED}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (GenericList.OpenBlock, GenericList.DelimiterBlock, GenericList.CloseBlock)):
				print("{DARK_BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (PortList.OpenBlock, PortList.DelimiterBlock, PortList.CloseBlock)):
				print("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			elif isinstance(vhdlBlock, (pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock)):
				print("{BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			else:
				print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))

	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))

if (mode & 6 == 6):
	from pyVHDLParser.Token.Parser  import Tokenizer
	from pyVHDLParser.Blocks import TokenToBlockParser

	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
	vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream, debug=(mode & 1 == 1))

	try:
		blockIterator = iter(vhdlBlockStream)
		firstBlock = next(blockIterator)
		if (not isinstance(firstBlock, StartOfDocumentBlock)):
			print("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=firstBlock, **Console.Foreground))
		elif (not isinstance(firstBlock.StartToken, StartOfDocumentToken)):
			print("{RED}First block is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstBlock.StartToken, **Console.Foreground))

		lastBlock : Block = firstBlock
		endBlock  : Block = None
		lastToken : Token = firstBlock.StartToken

		for vhdlBlock in blockIterator:
			if isinstance(vhdlBlock, EndOfDocumentBlock):
				endBlock = vhdlBlock
				break
			tokenIterator = iter(vhdlBlock)

			relTokenPosition = 0
			for token in tokenIterator:
				relTokenPosition += 1
				if (token.NextToken is None):
					print("{RED}Token({pos}) has an open end.{NOCOLOR}".format(pos=relTokenPosition, **Console.Foreground))
					print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
					print("{RED}  Token:  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif (lastToken.NextToken is not token):
					print("{RED}Last token is not connected to the current ({pos}) one.{NOCOLOR}".format(pos=relTokenPosition, **Console.Foreground))
					token11 = lastToken
					token21 = lastToken.NextToken
					token31 = "--------" if (lastToken.NextToken is None) else lastToken.NextToken.NextToken
					token41 = "--------" if (lastToken.NextToken.NextToken is None) else lastToken.NextToken.NextToken.NextToken
					token12 = "--------" if (token.PreviousToken.PreviousToken is None) else token.PreviousToken.PreviousToken.PreviousToken
					token22 = "--------" if (token.PreviousToken is None) else token.PreviousToken.PreviousToken
					token32 = token.PreviousToken
					token42 = token
					print("{RED} Block: {block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
					print("{RED} | Last:  {token1}{NOCOLOR} =?= {DARK_RED}Prev: {token2}{NOCOLOR}".format(token1=token11, token2=token12, **Console.Foreground))
					print("{DARK_RED} |  Next: {token1}{NOCOLOR} =?= {DARK_RED}Prev: {token2}{NOCOLOR}".format(token1=token21, token2=token22, **Console.Foreground))
					print("{DARK_RED} |  Next: {token1}{NOCOLOR} =?= {DARK_RED}Prev: {token2}{NOCOLOR}".format(token1=token31, token2=token32, **Console.Foreground))
					print("{DARK_RED} v  Next: {token1}{NOCOLOR} =?= {RED}Curr: {token2}{NOCOLOR}".format(token1=token41, token2=token42, **Console.Foreground))
				elif (token.PreviousToken is not lastToken):
					print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**Console.Foreground))
					print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))
					print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **Console.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=token, **Console.Foreground))
					print("{RED}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **Console.Foreground))

				lastToken = token

			lastBlock = vhdlBlock
		else:
			print("{RED}No EndOfDocumentBlock found.{NOCOLOR}".format(**Console.Foreground))

		if (not isinstance(endBlock, EndOfDocumentBlock)):
			print("{RED}Last block is not EndOfDocumentBlock: {block}{NOCOLOR}".format(block=endBlock, **Console.Foreground))
		elif (not isinstance(endBlock.StartToken, EndOfDocumentToken)):
			print("{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=endBlock.StartToken, **Console.Foreground))

	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))

# ==============================================================================
	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
	vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream, debug=(mode & 1 == 1))

	try:
		for vhdlBlock in vhdlBlockStream:
			print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
			for token in vhdlBlock:
				if isinstance(token, (IndentationToken, LinebreakToken, BoundaryToken, DelimiterToken, EndToken)):
					print("{DARK_GRAY}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, (CommentToken)):
					print("{DARK_GREEN}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, KeywordToken):
					print("{DARK_CYAN}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, (StringToken, CharacterToken)):
					print("{DARK_GREEN}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				elif isinstance(token, (IdentifierToken)):
					print("{GREEN}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))
				else:
					print("{RED}  {token}{NOCOLOR}".format(token=token, **Console.Foreground))

	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))


# ==============================================================================
if (mode & 8 == 8):
	from pyVHDLParser.Token.Parser  import Tokenizer
	from pyVHDLParser.Blocks        import TokenToBlockParser
	from pyVHDLParser.Groups import BlockToGroupParser, StartOfDocumentGroup, EndOfDocumentGroup, Group

	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
	try:
		vhdlTokenStream = [token for token in Tokenizer.GetVHDLTokenizer(content)]
		vhdlBlockStream = [block for block in TokenToBlockParser.Transform(vhdlTokenStream)]
	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))

	vhdlGroupStream = BlockToGroupParser.Transform(vhdlBlockStream, debug=(mode & 1 == 1))

	try:
		for vhdlGroup in vhdlGroupStream:
			print("{CYAN}{block}{NOCOLOR}".format(block=vhdlGroup, **Console.Foreground))
			for block in vhdlGroup:
				if isinstance(block, (IndentationToken, LinebreakToken, BoundaryToken, DelimiterToken, EndToken)):
					print("{DARK_GRAY}  {block}{NOCOLOR}".format(block=block, **Console.Foreground))
				elif isinstance(block, (CommentToken)):
					print("{DARK_GREEN}  {block}{NOCOLOR}".format(block=block, **Console.Foreground))
				elif isinstance(block, KeywordToken):
					print("{DARK_CYAN}  {block}{NOCOLOR}".format(block=block, **Console.Foreground))
				elif isinstance(block, (StringToken, SpaceToken, CharacterToken)):
					print("{DARK_GREEN}  {block}{NOCOLOR}".format(block=block, **Console.Foreground))
				else:
					print("{YELLOW}  {block}{NOCOLOR}".format(block=block, **Console.Foreground))

	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))

# ==============================================================================
if (mode & 16 == 16):
	from pyVHDLParser.Token.Parser  import Tokenizer
	from pyVHDLParser.Blocks        import TokenToBlockParser
	from pyVHDLParser.Groups        import BlockToGroupParser, StartOfDocumentGroup, EndOfDocumentGroup, Group

	print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))

	vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
	vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream)
	vhdlGroupStream = BlockToGroupParser.Transform(vhdlBlockStream)
	groups =          [group for group in vhdlGroupStream]
	firstGroup =      groups[0]
	lastGroup =       groups[-1]

	if (not isinstance(firstGroup, StartOfDocumentGroup)):
		raise GroupParserException("Expected group is not a StartOfDocumentGroup.", firstGroup)
	elif (not isinstance(lastGroup, EndOfDocumentGroup)):
		raise GroupParserException("Expected group is not an EndOfDocumentGroup.", lastGroup)

	# def _CategoryIterator(categories):


	def validate(group : Group):
		innerGroup = group.InnerGroup
		while innerGroup is not None:
			validate(innerGroup)

			# if group registered?
			if innerGroup.__class__ in group._subGroups:
				if innerGroup not in group._subGroups[innerGroup.__class__]:
					print("innerGroup '{0}' is not listed in _subGroups of '{1}'.".format(innerGroup, group))
			else:
				print("innerGroup '{0}' is not supported in group '{1}'".format(innerGroup, group))

			innerGroup = innerGroup.NextGroup


	validate(firstGroup)








# 	wordTokenStream = Tokenizer.GetWordTokenizer(content)
# 	vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream, debug=(mode & 1 == 1))
# 	strippedBlockStream = StripAndFuse(vhdlBlockStream)
#
# 	try:
# 		for vhdlBlock in strippedBlockStream:
# 			if isinstance(vhdlBlock, (LinebreakBlock, IndentationBlock)):
# 				print("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
# 			elif isinstance(vhdlBlock, CommentBlock):
# 				print("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
# 			elif isinstance(vhdlBlock, (Entity.NameBlock, Entity.ConcurrentBeginBlock, Entity.EndBlock)):
# 				print("{DARK_RED}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
# 			elif isinstance(vhdlBlock, (GenericList.OpenBlock, GenericList.DelimiterBlock, GenericList.CloseBlock)):
# 				print("{DARK_BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
# 			elif isinstance(vhdlBlock, (PortList.OpenBlock, PortList.DelimiterBlock, PortList.CloseBlock)):
# 				print("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
# 			elif isinstance(vhdlBlock, (GenericList.ItemBlock, PortList.ItemBlock)):
# 				print("{BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
# 			else:
# 				print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))
#
# 	except ParserException as ex:
# 		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
# 	except NotImplementedError as ex:
# 		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))


if (mode & 32 == 32):
	from pyVHDLParser.DocumentModel import Document, GroupParserException, GroupParserException

	try:
		document = Document(file)
		document.Parse()
		document.Print(0)

	except ParserException as ex:
		print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
	except NotImplementedError as ex:
		print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
