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
from src.Token.Tokens         import EndOfDocumentToken
from src.Token.Keywords       import LinebreakToken, IndentationToken
from src.Token.Keywords       import ContextKeyword, LibraryKeyword, UseKeyword
from src.Token.Keywords       import ArchitectureKeyword, EntityKeyword, PackageKeyword, ConfigurationKeyword
from src.Token.Parser         import CharacterToken, SpaceToken, StringToken
from src.Blocks.Exception     import BlockParserException
from src.Blocks.Base          import Block
from src.Blocks.Common        import EmptyLineBlock, IndentationBlock
from src.Blocks.Comment       import SingleLineCommentBlock, MultiLineCommentBlock
from src.Blocks.Reference     import Context, Library, Use
from src.Blocks.Sequential    import Package
from src.Blocks.Structural    import Entity, Architecture, Configuration


class StartOfDocumentBlock(Block):
	def __init__(self, startToken):
		self._previousBlock =     None
		self._nextBlock =         None
		self.StartToken =         startToken
		self._endToken =          startToken
		self.MultiPart =          False

	def __len__(self):
		return 0

	def __str__(self):
		return "[StartOfDocumentBlock]"

	def RegisterStates(self):
		return [
			self.stateDocument
		]

	@classmethod
	def stateDocument(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected keywords: architecture, context, entity, library, package, use."
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
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
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
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
				raise BlockParserException(errorMessage, token)

			parserState.NewToken =      newToken
			parserState.TokenMarker =   newToken
			return
		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock =      EndOfDocumentBlock(token)
			raise StopIteration()
		else:  # tokenType
			raise BlockParserException(errorMessage, token)


class EndOfDocumentBlock(Block):
	def __init__(self, endToken):
		self._previousBlock =     None
		self._nextBlock =         None
		self.StartToken =         endToken
		self._endToken =          endToken
		self.MultiPart =          False

	def __len__(self):
		return 0

	def __str__(self):
		return "[EndOfDocumentBlock]"
