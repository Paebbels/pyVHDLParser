# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from pyTooling.Decorators           import export

from pyVHDLParser.Token             import SpaceToken, LinebreakToken, CommentToken
from pyVHDLParser.Token.Keywords    import BoundaryToken
from pyVHDLParser.Blocks            import ParserState, CommentBlock, BlockParserException
from pyVHDLParser.Blocks.Common     import LinebreakBlock
from pyVHDLParser.Blocks.Expression import ExpressionBlockEndedBySemicolon
from pyVHDLParser.Blocks.Object     import ObjectDeclarationEndMarkerBlock, ObjectDeclarationBlock


@export
class VariableDeclarationEndMarkerBlock(ObjectDeclarationEndMarkerBlock):
	pass


@export
class VariableDeclarationDefaultExpressionBlock(ExpressionBlockEndedBySemicolon):
	END_BLOCK = VariableDeclarationEndMarkerBlock


@export
class VariableDeclarationBlock(ObjectDeclarationBlock):
	OBJECT_KIND =       "variable"
	EXPRESSION_BLOCK =  VariableDeclarationDefaultExpressionBlock
	END_BLOCK =         VariableDeclarationEndMarkerBlock

	@classmethod
	def stateVariableKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(fromExistingToken=token)
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected whitespace after keyword VARIABLE.", token)
