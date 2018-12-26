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
# from pyVHDLParser.Blocks.Common        import IndentationBlock
# from pyVHDLParser.Blocks.Document      import CommentBlock
# from pyVHDLParser.Blocks.Parser        import TokenToBlockParser
# from pyVHDLParser.Token                import CharacterToken, SpaceToken
# from pyVHDLParser.Token.Keywords       import IndentationToken, SingleLineCommentKeyword, MultiLineCommentStartKeyword, MultiLineCommentEndKeyword


# Type alias for type hinting
# ParserState = TokenToBlockParser.TokenParserState

#
# class SingleLineCommentBlock(CommentBlock):
# 	@classmethod
# 	def statePossibleCommentStart(cls, parserState: ParserState):
# 		token = parserState.Token
# 		if (isinstance(token, CharacterToken) and (token == "-")):
# 			parserState.NewToken =    SingleLineCommentKeyword(parserState.TokenMarker)
# 			parserState.TokenMarker = parserState.NewToken
# 			parserState.NextState =   cls.stateConsumeComment
# 			return
#
# 		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))
#
# 	@classmethod
# 	def stateConsumeComment(cls, parserState: ParserState):
# 		token = parserState.Token
# 		if (isinstance(token, CharacterToken)and (token == "\n")):
# 			parserState.NewBlock =    SingleLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.Token)
# 			parserState.NextState =   cls.stateLinebreak
# 			return
# 		else:
# 			pass	# consume everything until "\n"
#
# 	@classmethod
# 	def stateLinebreak(cls, parserState: ParserState):
# 		token = parserState.Token
# 		if isinstance(token, SpaceToken):
# 			parserState.NewToken = IndentationToken(token)
# 			parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken)
# 			parserState.Pop()
# 		else:
# 			parserState.Pop()
# 			if (parserState.TokenMarker is None):
# 				# print("  new marker: None -> {0!s}".format(token))
# 				parserState.TokenMarker = token
# 				# print("  {DARK_GREEN}re-issue: {GREEN}{state!s}     {DARK_GREEN}token={GREEN}{token}{NOCOLOR}".format(state=parserState, token=parserState.Token, **Console.Foreground))
# 			parserState.NextState(parserState)
#
#
# class MultiLineCommentBlock(CommentBlock):
# 	@classmethod
# 	def statePossibleCommentStart(cls, parserState: ParserState):
# 		token = parserState.Token
# 		if (isinstance(token, CharacterToken) and (token == "*")):
# 			parserState.NewToken =    MultiLineCommentStartKeyword(parserState.TokenMarker)
# 			parserState.TokenMarker = parserState.NewToken
# 			parserState.NextState =   cls.stateConsumeComment
# 			return
# 		else:
# 			parserState.Pop()
# 			# print("  {DARK_GREEN}re-issue: {GREEN}{state!s}     {DARK_GREEN}token={GREEN}{token}{NOCOLOR}".format(state=parserState, token=parserState.Token, **Console.Foreground))
# 			parserState.NextState(parserState)
#
# 	@classmethod
# 	def stateConsumeComment(cls, parserState: ParserState):
# 		token = parserState.Token
# 		if (isinstance(token, CharacterToken) and (token == "*")):
# 			parserState.PushState =   cls.statePossibleCommentEnd
# 			parserState.TokenMarker = token
# 			return
# 		else:
# 			pass  # consume everything until "*/"
#
# 	@classmethod
# 	def statePossibleCommentEnd(cls, parserState: ParserState):
# 		token = parserState.Token
# 		if (isinstance(token, CharacterToken) and (token == "/")):
# 			parserState.NewToken = MultiLineCommentEndKeyword(parserState.TokenMarker)
# 			parserState.Pop()
# 			parserState.NewBlock = MultiLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
# 			parserState.Pop()
# 			return
# 		else:
# 			parserState.Pop()
# 			parserState.NextState(parserState)
