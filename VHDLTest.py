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
from colorama  import init

from src.Functions      import Console
from src.Parser         import Tokenizer, StartOfDocumentToken
from src.VHDLBlocks     import *
# from src.VHDLExamples   import CodeSnippet
from src.VHDLParser     import VHDL



Console.init()


content = """\
library ieee;
use     ieee.std_logic_1164.all;
  use   ieee.numeric_std.all;

entity myEntity is
	generic (
		INPUT_BITS  : positive := 8;
		OUTPUT_BITS : positive := 8
	);
	port (
		Clock  : in	 std_logic;
		Reset	 : in  std_logic;
		Input  : in  std_logic_vector(INPUT_BITS - 1 downto 0);
		Output : out std_logic_vector(OUTPUT_BITS - 1 downto 0)
	);
end entity;

architecture rtl of test is
--	subtype T_SLV is std_logic_vector(7 downto 0);
--  type T_STATE is (ST_IDLE, ST_FINISH);
--  type T_Record is record
--		Member1 : STD_LOGIC;
--		Member2 : BOOLEAN
--	end record;
	constant C_1 : positive;
--	signal   S_1 : std_logic := '0';
--	shared variable SV_1 : boolean;
begin

	process(Clock)
	begin
		if (Reset = '1') then
		end if;
	end process;
end architecture;

package pack is
	--function myFunc(foo : std_logic) return boolean;
	--procedure myProc(outp : out boolean; signal aaa : in std_logic);
	constant blabla : integer;
end package pack;

package body pack is
	function myFunc(foo : std_logic) return boolean is
	begin
	end function;

	procedure myProc(outp : out boolean; signal aaa : in std_logic) is
	begin
	end procedure;

	constant blabla : integer := 15;
end package body pack;
""".replace("\r\n", "\n") # make it universal newline compatible

# content = CodeSnippet["Comments"].replace("\r\n", "\n").replace("TABULATOR", "\t") # make it universal newline compatible
# content = CodeSnippet["Libraries"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["Uses"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["EntityEndings"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["ArchitectureEndings"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["GenericLists"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["PortLists"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["Constants"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["Processes"].replace("\r\n", "\n") # make it universal newline compatible
# content = CodeSnippet["Test1"].replace("\r\n", "\n") # make it universal newline compatible


def StripAndFuse(generator):
	iterator =  iter(generator)
	lastBlock = next(iterator)
	yield lastBlock

	for block in iterator:
		if isinstance(block, (IndentationBlock, CommentBlock, EmptyLineBlock)):
			continue
		else:
			if (block.MultiPart == True):
				while True:
					nextBlock = next(iterator)
					if isinstance(nextBlock, (IndentationBlock, CommentBlock, EmptyLineBlock)):
						continue
					if (type(block) is not type(nextBlock)):
						raise ParserException("Error in multipart blocks. {0} <-> {1}".format(type(block), type(nextBlock)))

					nextBlock.StartToken.PreviousToken = block.EndToken
					block.EndToken = nextBlock.EndToken
					if (nextBlock.MultiPart == False):
						break

			block.PreviousBlock = lastBlock
			block.StartToken.PreviousToken = lastBlock.EndToken
			yield block
			lastBlock = block


# ==============================================================================
print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
alphaCharacters = Tokenizer.__ALPHA_CHARS__ + "_" + Tokenizer.__NUMBER_CHARS__
wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters, numberCharacters="")
vhdlBlockStream = VHDL.TransformTokensToBlocks(wordTokenStream, debug= True)

try:
	for vhdlBlock in vhdlBlockStream:
		if isinstance(vhdlBlock, (EmptyLineBlock, IndentationBlock)):
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
print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
alphaCharacters = Tokenizer.__ALPHA_CHARS__ + "_" + Tokenizer.__NUMBER_CHARS__
wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters, numberCharacters="")
vhdlBlockStream = VHDL.TransformTokensToBlocks(wordTokenStream, debug=not True)

try:
	blockIterator = iter(vhdlBlockStream)
	firstBlock = next(blockIterator)
	if (not isinstance(firstBlock, StartOfDocumentBlock)):
		print("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=firstBlock, **Console.Foreground))
	elif (not isinstance(firstBlock.StartToken, StartOfDocumentToken)):
		print("{RED}First block is not StartOfDocumentBlock: {token}{NOCOLOR}".format(token=firstBlock.StartToken, **Console.Foreground))

	lastBlock = None
	lastToken = firstBlock.StartToken

	print("{YELLOW}{block}{NOCOLOR}".format(block=firstBlock, **Console.Foreground))
	print("{YELLOW}  {token}{NOCOLOR}".format(token=lastToken, **Console.Foreground))

	for vhdlBlock in blockIterator:
		print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **Console.Foreground))

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
	else:
		print("{RED}No EndOfDocumentBlock found.{NOCOLOR}".format(**Console.Foreground))

	if (not isinstance(lastBlock, EndOfDocumentBlock)):
		print("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=lastBlock, **Console.Foreground))
	elif (not isinstance(lastBlock.StartToken, EndOfDocumentToken)):
		print("{RED}First block is not StartOfDocumentBlock: {token}{NOCOLOR}".format(token=lastBlock.StartToken, **Console.Foreground))

except ParserException as ex:
	print("ERROR: " + str(ex))
except NotImplementedError as ex:
	print("NotImplementedError: " + str(ex))


# ==============================================================================
print("{RED}{line}{NOCOLOR}".format(line="="*160, **Console.Foreground))
wordTokenStream = Tokenizer.GetWordTokenizer(content, alphaCharacters=alphaCharacters)
vhdlBlockStream = VHDL.TransformTokensToBlocks(wordTokenStream)
strippedBlockStream = StripAndFuse(vhdlBlockStream)

try:
	for vhdlBlock in strippedBlockStream:
		if isinstance(vhdlBlock, (EmptyLineBlock, IndentationBlock)):
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
