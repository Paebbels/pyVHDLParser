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
from pyVHDLParser.Token.Tokens         import EndOfDocumentToken
from pyVHDLParser.Token.Keywords       import LinebreakToken, IndentationToken
from pyVHDLParser.Token.Keywords       import ContextKeyword, LibraryKeyword, UseKeyword
from pyVHDLParser.Token.Keywords       import ArchitectureKeyword, EntityKeyword, PackageKeyword, ConfigurationKeyword
from pyVHDLParser.Token.Parser         import CharacterToken, SpaceToken, StringToken
from pyVHDLParser.Blocks.Parser        import TokenToBlockParser
from pyVHDLParser.Blocks               import TokenParserException, Block
from pyVHDLParser.Blocks.Common        import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock
from pyVHDLParser.Blocks.Reference     import Context, Library, Use
from pyVHDLParser.Blocks.Sequential    import Package
from pyVHDLParser.Blocks.Structural    import Entity, Architecture, Configuration

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
		token = parserState.Token
		errorMessage = "Expected keywords: architecture, context, entity, library, package, use."
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, parserState.NewToken)
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			keyword = token.Value.lower()
			if (keyword == "library"):
				newToken = LibraryKeyword(token)
				parserState.PushState =   Library.LibraryBlock.stateLibraryKeyword
			elif (keyword == "use"):
				newToken = UseKeyword(token)
				parserState.PushState =   Use.UseBlock.stateUseKeyword
			elif (keyword == "context"):
				newToken = ContextKeyword(token)
				parserState.PushState =   Context.NameBlock.stateContextKeyword
			elif (keyword == "entity"):
				newToken = EntityKeyword(token)
				parserState.PushState =   Entity.NameBlock.stateEntityKeyword
			elif (keyword == "architecture"):
				newToken = ArchitectureKeyword(token)
				parserState.PushState =   Architecture.NameBlock.stateArchitectureKeyword
			elif (keyword == "package"):
				newToken = PackageKeyword(token)
				parserState.PushState =   Package.NameBlock.statePackageKeyword
			else:
				raise TokenParserException(errorMessage, token)

			parserState.NewToken =      newToken
			parserState.TokenMarker =   newToken
			return
		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock =      EndOfDocumentBlock(token)
			return
		else:  # tokenType
			raise TokenParserException(errorMessage, token)


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
