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
from pyVHDLParser.Groups               import Group
from pyVHDLParser.Groups.Parser        import BlockToGroupParser
from pyVHDLParser.Token.Keywords       import SingleLineCommentKeyword
from pyVHDLParser.Token.Parser         import CharacterToken


# Type alias for type hinting
ParserState = BlockToGroupParser.BlockParserState


class CommentGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block
		if (isinstance(block, CharacterToken) and (block == "-")):
			parserState.NewToken =    SingleLineCommentKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class LibraryGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))


class UseGroup(Group):
	@classmethod
	def stateParse(cls, parserState: ParserState):
		block = parserState.Block

		raise NotImplementedError("State=Parse: {0!r}".format(block))
