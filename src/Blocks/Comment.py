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
from src.Token.Keywords       import IndentationToken, SingleLineCommentKeyword, MultiLineCommentStartKeyword, MultiLineCommentEndKeyword
from src.Token.Parser         import CharacterToken, SpaceToken, StringToken
from src.Blocks.Exception     import BlockParserException
from src.Blocks.Base          import Block
from src.Blocks.Common        import IndentationBlock


class CommentBlock(Block):
	pass

class SingleLineCommentBlock(CommentBlock):
	def RegisterStates(self):
		return [
			self.statePossibleCommentStart,
			self.stateConsumeComment
		]

	@classmethod
	def statePossibleCommentStart(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "-")):
			parserState.NewToken =    SingleLineCommentKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return

		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateConsumeComment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "\n")):
			parserState.NewBlock =    SingleLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.Token)
			parserState.NextState =   cls.stateLinebreak
			return
		else:
			pass	# consume everything until "\n"

	@classmethod
	def stateLinebreak(cls, parserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken = IndentationToken(token)
			parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken)
			parserState.Pop()
		else:
			parserState.Pop()
			if (parserState.TokenMarker is None):
				# print("  new marker: None -> {0!s}".format(token))
				parserState.TokenMarker = token
			# print("  re-issue: {0!s}".format(parserState))
			parserState.NextState(parserState)


class MultiLineCommentBlock(CommentBlock):
	def RegisterStates(self):
		return [
			self.statePossibleCommentStart,
			self.stateConsumeComment,
			self.statePossibleCommentEnd
		]

	@classmethod
	def statePossibleCommentStart(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "*")):
			parserState.NewToken =    MultiLineCommentStartKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return
		else:
			parserState.Pop()
			# if (parserState.TokenMarker is None):
				# print("  new marker: None -> {0!s}".format(token))
				# parserState.TokenMarker = token
			# print("  re-issue: {0!s}".format(parserState))
			parserState.NextState(parserState)
			
		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateConsumeComment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "*")):
			parserState.PushState =   cls.statePossibleCommentEnd
			parserState.TokenMarker = token
			return
		else:
			pass  # consume everything until "*/"

	@classmethod
	def statePossibleCommentEnd(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "/")):
			parserState.NewToken = MultiLineCommentEndKeyword(parserState.TokenMarker)
			parserState.Pop()
			parserState.NewBlock = MultiLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		else:
			parserState.Pop()
			parserState.NextState(parserState)
