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
from pyVHDLParser.Decorators  import Export
from pyVHDLParser.Token       import SpaceToken, IndentationToken
from pyVHDLParser.Blocks      import ParserState, SkipableBlock

__all__ = []
__api__ = __all__


@Export
class WhitespaceBlock(SkipableBlock):
	def __init__(self, previousBlock, startToken):
		super().__init__(previousBlock, startToken, startToken)

	def __str__(self):
		return "[{blockName: <50s}  {stream} at {start!s} .. {end!s}]".format(
			blockName=type(self).__name__,
			stream=" "*61,
			start=self.StartToken.Start,
			end=self.EndToken.End
		)


@Export
class LinebreakBlock(WhitespaceBlock):
	@classmethod
	def stateLinebreak(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken = IndentationToken(token)
			parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken)
			parserState.Pop()
			# print("  {GREEN}continue: {0!s}{NOCOLOR}".format(parserState, **Console.Foreground))
		else:
			parserState.Pop()
			if (parserState.TokenMarker is None):
				# print("  {DARK_GREEN}set marker: {GREEN}LinebreakBlock.stateLinebreak    {DARK_GREEN}marker {GREEN}{0!s}{NOCOLOR}".format(token, **Console.Foreground))
				parserState.TokenMarker = token
			# print("  {DARK_GREEN}re-issue:   {GREEN}{state!s: <20s}    {DARK_GREEN}token  {GREEN}{token}{NOCOLOR}".format(state=parserState, token=parserState.Token, **Console.Foreground))
			parserState.NextState(parserState)


@Export
class EmptyLineBlock(LinebreakBlock):
	pass


@Export
class IndentationBlock(WhitespaceBlock):
	__TABSIZE__ = 2

	def __str__(self):
		length = len(self.StartToken.Value)
		actual = sum([(self.__TABSIZE__ if (c == "\t") else 1) for c in self.StartToken.Value])

		return "[{blockName: <50s}  length={len: <53}  at {start!s} .. {end!s}]".format(
				blockName=type(self).__name__,
				len="{len} ({actual}) ".format(
					len=length,
					actual=actual
				),
				start=self.StartToken.Start,
				end=self.EndToken.End
			)
