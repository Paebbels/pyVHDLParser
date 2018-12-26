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
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
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
from pyVHDLParser.Base              import ParserException
from pyVHDLParser.Blocks import StartOfDocumentBlock, EndOfDocumentBlock, ParserState
from pyVHDLParser.Filters.Comment   import StripAndFuse
from pyVHDLParser.Functions         import Console
from pyVHDLParser.Token             import StartOfDocumentToken, EndOfDocumentToken
from pyVHDLParser.Token.Parser      import Tokenizer
from .                              import EntityTest, GenericListTest, ArchitectureTest, ProcessTest
from .                              import LibraryTest, UseTest, PackageTest, PackageBodyTest
from .                              import PortListTest


class TestSuite:
	__NAME__ =      "BlockParserTestSuite"
	__TESTCASES__ = [
		LibraryTest.TestCase,
		UseTest.TestCase,
		PackageTest.TestCase,
		PackageBodyTest.TestCase,
		EntityTest.TestCase,
		GenericListTest.TestCase,
		PortListTest.TestCase,
		ArchitectureTest.TestCase,
		ProcessTest.TestCase
	]
	
	__ALPHA_CHARACTERS__ = Tokenizer.__ALPHA_CHARS__ + "_" + Tokenizer.__NUMBER_CHARS__

	def __init__(self, vhdlDirectory):
		self._vhdlDirectory = vhdlDirectory

	def RunTests(self):
		runExpectedBlocks =           True
		runExpectedBlocksAfterStrip = True
		runConnectivity =             True
		
		for testCase in self.__TESTCASES__:
			print("  Testcase: {DARK_CYAN}{name}.{NOCOLOR}".format(name=testCase.__NAME__, **Console.Foreground))
		
			file = self._vhdlDirectory / testCase.__FILENAME__
		
			if (not file.exists()):
				print("    {RED}File '{0!s}' does not exist.{NOCOLOR}".format(file, **Console.Foreground))
				continue
		
			with file.open('r') as fileHandle:
				content = fileHandle.read()
			
			if runExpectedBlocks:
				self._RunExpectedBlocks(testCase, content)
			
			if runExpectedBlocksAfterStrip:
				self._RunExpectedBlocksAfterStrip(testCase, content)
			
			if runConnectivity:
				self._RunConnectivityCheck(testCase, content)
		
			print("  Testcase: {DARK_CYAN}{name} COMPLETED.{NOCOLOR}".format(name=testCase.__NAME__, **Console.Foreground))
			
			
	def _RunExpectedBlocks(self, testCase, content):
		# History check
		counter =         testCase.GetExpectedBlocks()
		wordTokenStream = Tokenizer.GetVHDLTokenizer(content, alphaCharacters=self.__ALPHA_CHARACTERS__, numberCharacters="")
		vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream)

		try:
			for vhdlBlock in vhdlBlockStream:
				counter.Count(vhdlBlock.__class__)

			if counter.Check():
				print("    Expected blocks check - {GREEN}PASSED{NOCOLOR}".format(**Console.Foreground))
			else:
				print("    Expected blocks check - {RED}FAILED{NOCOLOR}".format(**Console.Foreground))
				counter.PrintReport()

		except ParserException as ex:     print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
		except NotImplementedError as ex: print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
		
	def _RunExpectedBlocksAfterStrip(self, testCase, content):
		# History check
		
		counter =             testCase.GetExpectedBlocksAfterStrip()
		wordTokenStream =     Tokenizer.GetVHDLTokenizer(content, alphaCharacters=self.__ALPHA_CHARACTERS__, numberCharacters="")
		vhdlBlockStream =     TokenToBlockParser.Transform(wordTokenStream)
		strippedBlockStream = StripAndFuse(vhdlBlockStream)

		try:
			for vhdlBlock in strippedBlockStream:
				counter.Count(vhdlBlock.__class__)

			if counter.Check():
				print("    Expected blocks after strip check - {GREEN}PASSED{NOCOLOR}".format(**Console.Foreground))
			else:
				print("    Expected blocks after strip check - {RED}FAILED{NOCOLOR}".format(**Console.Foreground))
				counter.PrintReport()
		
		
		except ParserException as ex:     print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
		except NotImplementedError as ex: print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
		
	def _RunConnectivityCheck(self, testCase, content):
		# Connectivity check
		wordTokenStream = Tokenizer.GetVHDLTokenizer(content, alphaCharacters=self.__ALPHA_CHARACTERS__, numberCharacters="")
		vhdlBlockStream = TokenToBlockParser.Transform(wordTokenStream)

		try:
			blockIterator = iter(vhdlBlockStream)
			firstBlock =    next(blockIterator)
			if (not isinstance(firstBlock, StartOfDocumentBlock)):              print("{RED}First block is not StartOfDocumentBlock: {block}{NOCOLOR}".format(block=firstBlock, **Console.Foreground))
			elif (not isinstance(firstBlock.StartToken, StartOfDocumentToken)): print("{RED}First token is not StartOfDocumentToken: {token}{NOCOLOR}".format(token=firstBlock.StartToken, **Console.Foreground))

			lastBlock = None
			lastToken = firstBlock.StartToken
			for vhdlBlock in blockIterator:
				if isinstance(vhdlBlock, EndOfDocumentBlock):
					lastBlock = vhdlBlock
					break
				tokenIterator = iter(vhdlBlock)

				for token in tokenIterator:
					if (token.NextToken is None):                 print("{RED}Token has an open end.{NOCOLOR}".format(**Console.Foreground))
					elif (lastToken.NextToken is not token):      print("{RED}Last token is not connected to the current one.{NOCOLOR}".format(**Console.Foreground))
					elif (token.PreviousToken is not lastToken):  print("{RED}Current token is not connected to lastToken.{NOCOLOR}".format(**Console.Foreground))
					lastToken = token
			else:
				print("{RED}No EndOfDocumentBlock found.{NOCOLOR}".format(**Console.Foreground))

			if (not isinstance(lastBlock, EndOfDocumentBlock)):              print("{RED}Last block is not EndOfDocumentBlock: {block}{NOCOLOR}".format(block=lastBlock, **Console.Foreground))
			elif (not isinstance(lastBlock.StartToken, EndOfDocumentToken)): print("{RED}Last block is not EndOfDocumentToken: {token}{NOCOLOR}".format(token=lastBlock.StartToken, **Console.Foreground))

		except ParserException as ex:     print("{RED}ERROR: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
		except NotImplementedError as ex: print("{RED}NotImplementedError: {0!s}{NOCOLOR}".format(ex, **Console.Foreground))
