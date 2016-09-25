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
from src.Base               import ParserException
from src.Model.VHDLModel    import Entity as EntityModel
from src.Token.Keywords     import EntityKeyword, IdentifierToken
from src.Blocks.Structural  import Entity as EntityBlock


class Entity(EntityModel):
	@classmethod
	def stateParse(cls, parserState, currentBlock, blockIterator):
		if currentBlock.MultiPart:
			tokenIterator = iter(MultiPartIterator(currentBlock, blockIterator, EntityBlock.NameBlock))
		else:
			tokenIterator = iter(currentBlock)

		firstToken = next(tokenIterator)
		if (not isinstance(firstToken, EntityKeyword)): raise ParserException()

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				newEntity = cls(token.Value)
				parserState.CurrentNode.AddEntity(newEntity)

			# if (not isinstance(token, EntityKeyword)): raise ParserException()

		# block = next(iterator)

