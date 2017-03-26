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
from pyVHDLParser.Token                import EndOfDocumentToken, LinebreakToken, CommentToken, IndentationToken, SpaceToken
from pyVHDLParser.Token.Keywords       import ArchitectureKeyword, EntityKeyword, PackageKeyword
from pyVHDLParser.Token.Keywords       import ContextKeyword, LibraryKeyword, UseKeyword
from pyVHDLParser.Token.Parser         import StringToken
from pyVHDLParser.Blocks               import TokenParserException, Block, CommentBlock
from pyVHDLParser.Blocks.Common        import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Parser        import TokenToBlockParser
from pyVHDLParser.Blocks.Reference     import Context, Library, Use
from pyVHDLParser.Blocks.Sequential    import Package
from pyVHDLParser.Blocks.Structural    import Entity, Architecture


# Type alias for type hinting
ParserState = TokenToBlockParser.TokenParserState


class StartOfDocumentBlock(Block):
	def __init__(self, startToken):
		self._previousBlock =     None
		self.NextBlock =          None
		self.StartToken =         startToken
		self.EndToken =           startToken
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartToken

	def __len__(self):
		return 0

	def __str__(self):
		return "[StartOfDocumentBlock]"

	@classmethod
	def stateDocument(cls, parserState: ParserState):
		keywords = {
			# Keyword             Transition
			LibraryKeyword :      Library.LibraryBlock.stateLibraryKeyword,
			UseKeyword :          Use.UseBlock.stateUseKeyword,
		  ContextKeyword :      Context.NameBlock.stateContextKeyword,
		  EntityKeyword :       Entity.NameBlock.stateEntityKeyword,
		  ArchitectureKeyword : Architecture.NameBlock.stateArchitectureKeyword,
		  PackageKeyword :      Package.NameBlock.statePackageKeyword
		}

		token = parserState.Token
		if isinstance(token, SpaceToken):
			blockType =               IndentationBlock if isinstance(token, IndentationToken) else WhitespaceBlock
			parserState.NewBlock =    blockType(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, LinebreakToken):
			parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =    CommentBlock(parserState.LastBlock, token)
			parserState.TokenMarker = None
			return
		elif isinstance(token, StringToken):
			tokenValue = token.Value.lower()

			for keyword in keywords:
				if (tokenValue == keyword.__KEYWORD__):
					newToken =                keyword(token)
					parserState.PushState =   keywords[keyword]
					parserState.NewToken =    newToken
					parserState.TokenMarker = newToken
					return

		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock =    EndOfDocumentBlock(token)
			return

		raise TokenParserException(
			"Expected one of these keywords: {keywords}. Found: '{tokenValue}'.".format(
				keywords=", ".join(
					[kw.__KEYWORD__.upper() for kw in keywords]
				),
				tokenValue=token.Value
			), token)


class EndOfDocumentBlock(Block):
	def __init__(self, endToken):
		self._previousBlock =     None
		self.NextBlock =          None
		self.StartToken =         endToken
		self.EndToken =           endToken
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartToken

	def __len__(self):
		return 0

	def __str__(self):
		return "[EndOfDocumentBlock]"
