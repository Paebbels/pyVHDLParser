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
from pyVHDLParser.Groups.Parser        import BlockToGroupParser
from pyVHDLParser.Groups               import BlockParserException, Group


# Type alias for type hinting
ParserState = BlockToGroupParser.BlockParserState


class StartOfDocumentGroup(Group):
	def __init__(self, startToken):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartToken =         startToken
		self.EndToken =           startToken
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartToken

	def __len__(self):
		return 0

	def __str__(self):
		return "[StartOfDocumentGroup]"

	@classmethod
	def stateDocument(cls, parserState: ParserState):
		token = parserState.Block

		errorMessage = "Expected keywords: architecture, context, entity, library, package, use."
		if isinstance(parserState.Block, CharacterToken):
			pass
			# if (token == "\n"):
			# 	parserState.NewBlock =    LinebreakToken(token)
			# 	parserState.NewGroup =    LinebreakGroup(parserState.LastGroup, parserState.NewBlock)
			# 	parserState.TokenMarker = parserState.NewBlock
			# 	return
			# elif (token == "-"):
			# 	parserState.PushState =   SingleLineCommentGroup.statePossibleCommentStart
			# 	parserState.TokenMarker = token
			# 	return
			# elif (token == "/"):
			# 	parserState.PushState =   MultiLineCommentGroup.statePossibleCommentStart
			# 	parserState.TokenMarker = token
			# 	return
		elif isinstance(token, SpaceToken):
			pass
			# parserState.NewBlock =      IndentationToken(token)
			# parserState.NewGroup =      IndentationGroup(parserState.LastGroup, parserState.NewBlock)
			# return
		elif isinstance(token, StringToken):
			pass
			# keyword = token.Value.lower()
			# if (keyword == "library"):
			# 	newToken = LibraryKeyword(token)
			# 	parserState.PushState =   Library.LibraryGroup.stateLibraryKeyword
			# elif (keyword == "use"):
			# 	newToken = UseKeyword(token)
			# 	parserState.PushState =   Use.UseGroup.stateUseKeyword
			# elif (keyword == "context"):
			# 	newToken = ContextKeyword(token)
			# 	parserState.PushState =   Context.NameGroup.stateContextKeyword
			# elif (keyword == "entity"):
			# 	newToken = EntityKeyword(token)
			# 	parserState.PushState =   Entity.NameGroup.stateEntityKeyword
			# elif (keyword == "architecture"):
			# 	newToken = ArchitectureKeyword(token)
			# 	parserState.PushState =   Architecture.NameGroup.stateArchitectureKeyword
			# elif (keyword == "package"):
			# 	newToken = PackageKeyword(token)
			# 	parserState.PushState =   Package.NameGroup.statePackageKeyword
			# else:
			# 	raise TokenParserException(errorMessage, token)
			#
			# parserState.NewBlock =      newToken
			# parserState.TokenMarker =   newToken
			# return
		elif isinstance(token, EndOfDocumentToken):
			parserState.NewGroup =      EndOfDocumentGroup(token)
			return
		else:  # tokenType
			raise BlockParserException(errorMessage, token)


class EndOfDocumentGroup(Group):
	def __init__(self, endToken):
		self._previousGroup =     None
		self.NextGroup =          None
		self.StartToken =         endToken
		self.EndToken =           endToken
		self.MultiPart =          False

	def __iter__(self):
		yield self.StartToken

	def __len__(self):
		return 0

	def __str__(self):
		return "[EndOfDocumentGroup]"
