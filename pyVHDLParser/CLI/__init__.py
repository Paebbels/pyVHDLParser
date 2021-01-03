# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python frontend:    A streaming VHDL parser
#
# License:
# ==============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
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
from typing                           import Protocol, Callable, Dict

from pyAttributes                     import Attribute
from pyAttributes.ArgParseAttributes  import ArgumentAttribute, SwitchArgumentAttribute

from pyVHDLParser.Token               import LinebreakToken, IndentationToken, CommentToken, StringLiteralToken
from pyVHDLParser.Token               import IntegerLiteralToken, WordToken, Token, SpaceToken, CharacterToken
from pyVHDLParser.Token.Keywords      import KeywordToken


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


class FrontEndProtocol(Protocol):
	# TerminalUI
	Foreground:    Dict
	WriteError:    Callable[[str], None]
	WriteWarning:  Callable[[str], None]
	WriteQuiet:    Callable[[str], None]
	WriteNormal:   Callable[[str], None]
	WriteVerbose:  Callable[[str], None]
	WriteDebug:    Callable[[str], None]
	exit:          Callable[[int], None]

	# Frontend
	PrintHeadline: Callable


TOKENTYPE_TO_COLOR_TRANSLATION = {
	LinebreakToken:       "black",
	IndentationToken:     "grey",
	SpaceToken:           "lightblue1",
	CharacterToken:       "darkorange",
	CommentToken:         "forestgreen",
	StringLiteralToken:   "chocolate1",
	IntegerLiteralToken:  "deepskyblue3",
	WordToken:            "aquamarine3",
	KeywordToken:         "dodgerblue4",
}


def translate(token: Token) -> str:
	if isinstance(token, Token):
		tokenCls = token.__class__
	else:
		tokenCls = token

	try:
		return TOKENTYPE_TO_COLOR_TRANSLATION[tokenCls]
	except KeyError:
		for key, color in TOKENTYPE_TO_COLOR_TRANSLATION.items():
			if issubclass(tokenCls, key):
				return color
		else:
			return "crimson"
