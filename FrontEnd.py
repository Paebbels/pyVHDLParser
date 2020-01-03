# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
#
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python frontend:    A streaming VHDL parser
#
# License:
# ==============================================================================
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
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
from argparse       import RawDescriptionHelpFormatter
from pathlib        import Path
from platform       import system as platform_system
from textwrap       import dedent, wrap

from pyAttributes                     import Attribute
from pyExceptions                     import ExceptionBase
from pyAttributes.ArgParseAttributes  import ArgParseMixin, SwitchArgumentAttribute
from pyAttributes.ArgParseAttributes  import CommandAttribute, ArgumentAttribute, DefaultAttribute
from pyAttributes.ArgParseAttributes  import CommonSwitchArgumentAttribute
from pyMetaClasses                    import Singleton
from pyTerminalUI                     import LineTerminal, Severity

import pyVHDLParser
from pyVHDLParser.Base                import ParserException
from pyVHDLParser.Blocks              import MetaBlock


__author__ =      "Patrick Lehmann"
__copyright__ =   "Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany\n" + \
                  "Copyright 2016-2017 Patrick Lehmann - Dresden, Germany"
__maintainer__ =  "Patrick Lehmann"
__email__ =       "Patrick.Lehmann@plc2.de"
__version__ =     "0.6.2"
__status__ =      "Alpha"
__license__ =     "Apache License 2.0"
__api__ = [
	'FilenameAttribute',
	'VHDLParser'
]
__all__ = __api__

def printImportError(ex):
	platform = platform_system()
	print("IMPORT ERROR: One or more Python packages are not available in your environment.")
	print("Missing package: '{0}'\n".format(ex.name))
	if (platform == "Windows"): print("Run: 'py.exe -3 -m pip install -r requirements.txt'\n")
	elif (platform == "Linux"): print("Run: 'python3 -m pip install -r requirements.txt'\n")
	exit(1)


class FilenameAttribute(Attribute):
	def __call__(self, func):
		self._AppendAttribute(func, ArgumentAttribute(metavar="filename", dest="Filename", type=str, help="The filename to parse."))
		return func

class WithTokensAttribute(Attribute):
	def __call__(self, func):
		self._AppendAttribute(func, SwitchArgumentAttribute("-T", "--with-tokens",  dest="withTokens",    help="Display tokens in between."))
		return func

class WithBlocksAttribute(Attribute):
	def __call__(self, func):
		self._AppendAttribute(func, SwitchArgumentAttribute("-B", "--with-blocks",  dest="withBlocks",    help="Display blocks in between."))
		return func


class VHDLParser(LineTerminal, ArgParseMixin):
	HeadLine =                "pyVHDLParser - Test Application"

	# load platform information (Windows, Linux, Darwin, ...)
	__PLATFORM =              platform_system()


	def __init__(self, debug, verbose, quiet, sphinx=False):
		super().__init__(verbose, debug, quiet)

		Singleton.Register(LineTerminal, self)

		for block in MetaBlock.BLOCKS:
			try:
				block.__cls_init__()
			except AttributeError:
				pass

		# Call the constructor of the ArgParseMixin
		# --------------------------------------------------------------------------
		textWidth = min(self.Width, 160)
		description = dedent("""\
			Test application to test pyVHDLParser capabilities.
			""")
		epilog = "\n".join(wrap(dedent("""\
		  pyVHDLParser is a streaming parser to read and understand VHDL code equipped with comments for documentation extraction.
		  """), textWidth, replace_whitespace=False))


		class HelpFormatter(RawDescriptionHelpFormatter):
			def __init__(self, *args, **kwargs):
				kwargs['max_help_position'] = 25
				kwargs['width'] =             textWidth
				super().__init__(*args, **kwargs)

		ArgParseMixin.__init__(self, description=description, epilog=epilog, formatter_class=HelpFormatter, add_help=False)
		if sphinx: return


	# class properties
	# ============================================================================
	@property
	def Platform(self):           return self.__PLATFORM

	# ============================================================================
	# Common commands
	# ============================================================================
	# common arguments valid for all commands
	# ----------------------------------------------------------------------------
	@CommonSwitchArgumentAttribute("-d", "--debug",   dest="debug",   help="Enable debug mode.")
	@CommonSwitchArgumentAttribute("-v", "--verbose", dest="verbose", help="Print out detailed messages.")
	@CommonSwitchArgumentAttribute("-q", "--quiet",   dest="quiet",   help="Reduce messages to a minimum.")
	def Run(self):
		ArgParseMixin.Run(self)

	def PrintHeadline(self):
		self.WriteNormal("{HEADLINE}{line}{NOCOLOR}".format(line="="*80, **self.Foreground))
		self.WriteNormal("{HEADLINE}{headline: ^80s}{NOCOLOR}".format(headline=self.HeadLine, **self.Foreground))
		self.WriteNormal("{HEADLINE}{line}{NOCOLOR}".format(line="="*80, **self.Foreground))

	# ----------------------------------------------------------------------------
	# fallback handler if no command was recognized
	# ----------------------------------------------------------------------------
	@DefaultAttribute()
	def HandleDefault(self, _):
		self.PrintHeadline()
		self.MainParser.print_help()

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "help" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("help", help="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args):
		self.PrintHeadline()
		if (args.Command is None):
			self.MainParser.print_help()
			self.exit()
		elif (args.Command == "help"):
			print("This is a recursion ...")
		else:
			self.SubParsers[args.Command].print_help()
		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "info" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("info", help="Display tool and version information.")
	def HandleInfo(self, args):
		self.PrintHeadline()

		copyrights = __copyright__.split("\n", 1)
		self.WriteNormal("Copyright:  {0}".format(copyrights[0]))
		self.WriteNormal("            {0}".format(copyrights[1]))
		self.WriteNormal("License:    {0}".format(__license__))

		authors = __author__.split(", ")
		self.WriteNormal("Authors:    {0}".format(authors[0]))

		for author in authors[1:]:
			self.WriteNormal("            {0}".format(author))
		self.WriteNormal("Version:    {0}".format(__version__))
		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "tokenize" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("tokenize", help="Create a stream of token objects.", description=dedent("""\
		Create a stream of token objects.
		"""))
	@FilenameAttribute()
	def HandleTokenize(self, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		from pyVHDLParser.Base import ParserException
		from pyVHDLParser.Token import StartOfDocumentToken, EndOfDocumentToken, CharacterToken, SpaceToken, StringToken, LinebreakToken, CommentToken, IndentationToken
		from pyVHDLParser.Token.Parser import Tokenizer

		print("{RED}{line}{NOCOLOR}".format(line="=" * 160, **self.Foreground))
		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)

		try:
			for vhdlToken in vhdlTokenStream:
				if isinstance(vhdlToken, (LinebreakToken, SpaceToken, IndentationToken)):
					print("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlToken, **self.Foreground))
				elif isinstance(vhdlToken, CommentToken):
					print("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlToken, **self.Foreground))
				elif isinstance(vhdlToken, CharacterToken):
					print("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlToken, **self.Foreground))
				elif isinstance(vhdlToken, StringToken):
					print("{WHITE}{block}{NOCOLOR}".format(block=vhdlToken, **self.Foreground))
				elif isinstance(vhdlToken, (StartOfDocumentToken, EndOfDocumentToken)):
					print("{YELLOW}{block}{NOCOLOR}".format(block=vhdlToken, **self.Foreground))
				else:
					print("{RED}{block}{NOCOLOR}".format(block=vhdlToken, **self.Foreground))
		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "check-tokenize" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("check-tokenize", help="Check a stream of token objects.", description=dedent("""\
		Generates and checks a stream of token objects for correct double-pointers.
		"""))
	@FilenameAttribute()
	def HandleCheckTokenize(self, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		from pyVHDLParser.Base import ParserException
		from pyVHDLParser.Token import StartOfDocumentToken, EndOfDocumentToken
		from pyVHDLParser.Token.Parser import Tokenizer

		print("{RED}{line}{NOCOLOR}".format(line="=" * 160, **self.Foreground))
		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)

		try:
			tokenIterator = iter(vhdlTokenStream)
			firstToken = next(tokenIterator)
			if (not isinstance(firstToken, StartOfDocumentToken)):
				print("{RED}First block is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstToken, **self.Foreground))

			lastToken = None
			vhdlToken = firstToken

			for newToken in tokenIterator:
				if (vhdlToken.NextToken is None):
					print("{RED}Token has an open end.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Token:  {token}{NOCOLOR}".format(token=vhdlToken, **self.Foreground))
				elif ((vhdlToken is not firstToken) and (lastToken.NextToken is not vhdlToken)):
					print("{RED}Last token is not connected to the current token.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=vhdlToken, **self.Foreground))
					print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken, **self.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
					print("{RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
					if (lastToken.NextToken is None):
						print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token="--------", **self.Foreground))
					else:
						print(
							"{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken.NextToken, **self.Foreground))
					if (vhdlToken.PreviousToken is None):
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token="--------", **self.Foreground))
					else:
						print("{DARK_RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken.PreviousToken,
						                                                    **self.Foreground))
				elif (vhdlToken.PreviousToken is not lastToken):
					print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**self.Foreground))
					print("{RED}  Curr:   {token}{NOCOLOR}".format(token=vhdlToken, **self.Foreground))
					print("{RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken, **self.Foreground))
					print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
					print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))

				lastToken = vhdlToken
				vhdlToken = newToken

				if isinstance(newToken, EndOfDocumentToken):
					print("{GREEN}No double-linking errors in token stream found.{NOCOLOR}".format(**self.Foreground))
					break
			else:
				print("{RED}No EndOfDocumentToken found.{NOCOLOR}".format(**self.Foreground))

			if (not isinstance(vhdlToken, EndOfDocumentToken)):
				print(
					"{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
			elif (vhdlToken.PreviousToken is not lastToken):
				print("{RED}EndOfDocumentToken is not connected to lastToken.{NOCOLOR}".format(**self.Foreground))
				print("{RED}  Curr:   {token}{NOCOLOR}".format(token=vhdlToken, **self.Foreground))
				print("{RED}    Prev: {token}{NOCOLOR}".format(token=vhdlToken.PreviousToken, **self.Foreground))
				print("{RED}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
				print("{DARK_RED}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "blockstreaming" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("blockstreaming", help="Create a stream of block objects.", description=dedent("""\
		Create a stream of block objects.
		"""))
	@WithTokensAttribute()
	@FilenameAttribute()
	def HandleBlockStreaming(self, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		from pyVHDLParser.Token.Parser      import Tokenizer
		from pyVHDLParser.Blocks            import TokenToBlockParser
		from pyVHDLParser.Base              import ParserException
		from pyVHDLParser.Blocks            import CommentBlock
		from pyVHDLParser.Blocks.Common     import LinebreakBlock, IndentationBlock
		from pyVHDLParser.Blocks.Structural import Entity
		from pyVHDLParser.Blocks.List       import GenericList, PortList

		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
		vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream, debug=self.Verbose)

		try:
			for vhdlBlock in vhdlBlockStream:
				if isinstance(vhdlBlock, (LinebreakBlock, IndentationBlock)):
					self.WriteNormal("{DARK_GRAY}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
				elif isinstance(vhdlBlock, CommentBlock):
					self.WriteNormal("{DARK_GREEN}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
				elif isinstance(vhdlBlock, (Entity.NameBlock, Entity.NameBlock, Entity.EndBlock)):
					self.WriteNormal("{DARK_RED}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
				elif isinstance(vhdlBlock, (GenericList.OpenBlock, GenericList.DelimiterBlock, GenericList.CloseBlock)):
					self.WriteNormal("{DARK_BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
				elif isinstance(vhdlBlock, (PortList.OpenBlock, PortList.DelimiterBlock, PortList.CloseBlock)):
					self.WriteNormal("{DARK_CYAN}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
				elif isinstance(vhdlBlock, (pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock,
				                            pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock)):
					self.WriteNormal("{BLUE}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
				else:
					self.WriteNormal("{YELLOW}{block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))

				for token in vhdlBlock:
					self.WriteVerbose(str(token))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "check-blockstreaming" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("check-blockstreaming", help="Check a stream of block objects.", description=dedent("""\
		Check a stream of block objects.
		"""))
	@WithTokensAttribute()
	@FilenameAttribute()
	def HandleCheckBlockStreaming(self, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		from pyVHDLParser.Base         import ParserException
		from pyVHDLParser.Token        import StartOfDocumentToken, EndOfDocumentToken, Token
		from pyVHDLParser.Token.Parser import Tokenizer
		from pyVHDLParser.Blocks       import Block, StartOfDocumentBlock, EndOfDocumentBlock
		from pyVHDLParser.Blocks       import TokenToBlockParser


		vhdlTokenStream = Tokenizer.GetVHDLTokenizer(content)
		vhdlBlockStream = TokenToBlockParser.Transform(vhdlTokenStream, debug=True)

		try:
			blockIterator = iter(vhdlBlockStream)
			firstBlock = next(blockIterator)
			self.WriteVerbose(str(firstBlock))

			if (not isinstance(firstBlock, StartOfDocumentBlock)):
				self.WriteError("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=firstBlock, **self.Foreground))
				self.WriteError("{YELLOW}  Block:  {block}{NOCOLOR}".format(block=firstBlock, **self.Foreground))
			startToken = firstBlock.StartToken
			self.WriteDebug(str(startToken))
			if (not isinstance(startToken, StartOfDocumentToken)):
				self.WriteError("{RED}First token is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=startToken, **self.Foreground))
				self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=startToken, **self.Foreground))

			lastBlock : Block = firstBlock
			endBlock :  Block = None
			lastToken : Token = startToken

			for vhdlBlock in blockIterator:
				self.WriteVerbose(str(vhdlBlock))

				if isinstance(vhdlBlock, EndOfDocumentBlock):
					self.WriteDebug("{GREEN}Found EndOfDocumentBlock...{NOCOLOR}".format(**self.Foreground))
					endBlock = vhdlBlock
					break

				tokenIterator = iter(vhdlBlock)

				for token in tokenIterator:
					self.WriteDebug(str(token))

					if (token.NextToken is None):
						self.WriteError("{RED}Token has an open end (NextToken).{NOCOLOR}".format(**self.Foreground))
						self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=token, **self.Foreground))
					elif (lastToken.NextToken is not token):
						self.WriteError("{RED}Last token is not connected to the current token.{NOCOLOR}".format(**self.Foreground))
						self.WriteError("{YELLOW}  Last:   {token!s}{NOCOLOR}".format(token=lastToken, **self.Foreground))
						self.WriteError("{YELLOW}    Next: {token!s}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
						self.WriteError("")
						self.WriteError("{YELLOW}  Cur.:   {token!s}{NOCOLOR}".format(token=token, **self.Foreground))
						self.WriteError("")

					if (token.PreviousToken is None):
						self.WriteError("{RED}Token has an open end (PreviousToken).{NOCOLOR}".format(**self.Foreground))
						self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=token, **self.Foreground))
					elif (token.PreviousToken is not lastToken):
						print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**self.Foreground))
						# print("{RED}  Block:  {block}{NOCOLOR}".format(block=vhdlBlock, **self.Foreground))
						print("{YELLOW}  Cur.:   {token}{NOCOLOR}".format(token=token, **self.Foreground))
						print("{YELLOW}    Prev: {token}{NOCOLOR}".format(token=token.PreviousToken, **self.Foreground))
						self.WriteError("")
						print("{YELLOW}  Last:   {token}{NOCOLOR}".format(token=lastToken, **self.Foreground))
						print("{YELLOW}    Next: {token}{NOCOLOR}".format(token=lastToken.NextToken, **self.Foreground))
						self.WriteError("")

					lastToken = token

				lastBlock = vhdlBlock
			else:
				self.WriteError("{RED}No EndOfDocumentBlock found.{NOCOLOR}".format(**self.Foreground))

			if (not isinstance(endBlock, EndOfDocumentBlock)):
				self.WriteError("{RED}Last block is not EndOfDocumentBlock: {block}{NOCOLOR}".format(block=endBlock, **self.Foreground))
				self.WriteError("{YELLOW}  Block:  {block}{NOCOLOR}".format(block=firstBlock, **self.Foreground))
			elif (not isinstance(endBlock.EndToken, EndOfDocumentToken)):
				self.WriteError("{RED}Last token is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=endBlock.EndToken, **self.Foreground))
				self.WriteError("{YELLOW}  Token:  {token}{NOCOLOR}".format(token=endBlock.EndToken, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.WriteNormal("")
		self.WriteNormal("{CYAN}All checks are done.{NOCOLOR}".format(**self.Foreground))
		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "groupstreaming" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("groupstreaming", help="Create a stream of group objects.", description=dedent("""\
		Create a stream of group objects.
		"""))
	@WithTokensAttribute()
	@WithBlocksAttribute()
	@FilenameAttribute()
	def HandleGroupStreaming(self, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()


		from pyVHDLParser.Base import ParserException
		from pyVHDLParser.Token import CharacterToken, SpaceToken, StringToken, LinebreakToken, CommentToken, IndentationToken
		from pyVHDLParser.Token.Keywords import BoundaryToken, EndToken, KeywordToken, DelimiterToken
		from pyVHDLParser.Token.Parser import Tokenizer
		from pyVHDLParser.Blocks import TokenToBlockParser
		from pyVHDLParser.Groups import BlockToGroupParser

		print("{RED}{line}{NOCOLOR}".format(line="=" * 160, **self.Foreground))
		try:
			vhdlTokenStream = [token for token in Tokenizer.GetVHDLTokenizer(content)]
			vhdlBlockStream = [block for block in TokenToBlockParser.Transform(vhdlTokenStream)]
		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		vhdlGroupStream = BlockToGroupParser.Transform(vhdlBlockStream, debug=True)

		try:
			for vhdlGroup in vhdlGroupStream:
				print("{CYAN}{block}{NOCOLOR}".format(block=vhdlGroup, **self.Foreground))
				for block in vhdlGroup:
					if isinstance(block, (IndentationToken, LinebreakToken, BoundaryToken, DelimiterToken, EndToken)):
						print("{DARK_GRAY}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					elif isinstance(block, (CommentToken)):
						print("{DARK_GREEN}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					elif isinstance(block, KeywordToken):
						print("{DARK_CYAN}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					elif isinstance(block, (StringToken, SpaceToken, CharacterToken)):
						print("{DARK_GREEN}  {block}{NOCOLOR}".format(block=block, **self.Foreground))
					else:
						print("{YELLOW}  {block}{NOCOLOR}".format(block=block, **self.Foreground))

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "DOM" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("CodeDOM", help="Create a CodeDOM.", description=dedent("""\
		Create a code document object model (CodeDOM).
		"""))
	@FilenameAttribute()
	def HandleCodeDOM(self, args):
		self.PrintHeadline()

		file =         Path(args.Filename)

		if (not file.exists()):
			print("File '{0!s}' does not exist.".format(file))

		with file.open('r') as fileHandle:
			content = fileHandle.read()

		from pyVHDLParser.DocumentModel import Document, DOMParserException, DOMParserException

		try:
			document = Document(file)
			document.Parse()
			document.Print(0)

		except ParserException as ex:
			print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **self.Foreground))
		except NotImplementedError as ex:
			print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **self.Foreground))

		self.exit()


# main program
def main(): # mccabe:disable=MC0001
	"""This is the entry point for pyVHDLParser written as a function.

	1. It extracts common flags from the script's arguments list, before :py:class:`~argparse.ArgumentParser` is fully loaded.
	2. It creates an instance of VHDLParser and hands over to a class based execution.
	   All is wrapped in a big ``try..except`` block to catch every unhandled exception.
	3. Shutdown the script and return its exit code.
	"""
	from sys import argv as sys_argv

	debug =   "-d"        in sys_argv
	verbose = "-v"        in sys_argv
	quiet =   "-q"        in sys_argv

	try:
		# handover to a class instance
		vhdlParser = VHDLParser(debug, verbose, quiet)
		vhdlParser.Run()
		vhdlParser.exit()

	# except (CommonException, ConfigurationException) as ex:
	# 	print("{RED}ERROR:{NOCOLOR} {message}".format(message=ex.message, **Init.Foreground))
	# 	cause = ex.__cause__
	# 	if isinstance(cause, FileNotFoundError):
	# 		print("{YELLOW}  FileNotFound:{NOCOLOR} '{cause}'".format(cause=str(cause), **Init.Foreground))
	# 	elif isinstance(cause, NotADirectoryError):
	# 		print("{YELLOW}  NotADirectory:{NOCOLOR} '{cause}'".format(cause=str(cause), **Init.Foreground))
	# 	elif isinstance(cause, ParserException):
	# 		print("{YELLOW}  ParserException:{NOCOLOR} {cause}".format(cause=str(cause), **Init.Foreground))
	# 		cause = cause.__cause__
	# 		if (cause is not None):
	# 			print("{YELLOW}    {name}:{NOCOLOR} {cause}".format(name=cause.__class__.__name__, cause= str(cause), **Init.Foreground))
	#
	# 	if (not (verbose or debug)):
	# 		print()
	# 		print("{CYAN}  Use '-v' for verbose or '-d' for debug to print out extended messages.{NOCOLOR}".format(**Init.Foreground))
	# 	LineTerminal.exit(1)

	except ExceptionBase as ex:                 LineTerminal.printExceptionBase(ex)
	except NotImplementedError as ex:           LineTerminal.printNotImplementedError(ex)
	#except ImportError as ex:                   printImportError(ex)
	except Exception as ex:                     LineTerminal.printException(ex)

# entry point
if __name__ == "__main__":
	LineTerminal.versionCheck((3,5,0))
	main()
