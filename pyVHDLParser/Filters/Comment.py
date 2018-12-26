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
from pyVHDLParser.Blocks           import TokenParserException, CommentBlock
from pyVHDLParser.Blocks.Common    import IndentationBlock, LinebreakBlock, WhitespaceBlock
# from pyVHDLParser.Blocks.Document  import CommentBlock


def StripAndFuse(generator):
	iterator =  iter(generator)
	lastBlock = next(iterator)

	# don't filter the first block
	yield lastBlock

	for block in iterator:
		if isinstance(block, (IndentationBlock, CommentBlock, LinebreakBlock)):
			continue
		else:
			if (block.MultiPart == True):
				while True:
					nextBlock = next(iterator)
					if isinstance(nextBlock, (WhitespaceBlock, CommentBlock)):
						continue
					if (type(block) is not type(nextBlock)):
						raise TokenParserException("Error in multipart blocks. {0} <-> {1}".format(type(block), type(nextBlock)), None)   # TODO: review exception type

					nextBlock.StartToken.PreviousToken = block.EndToken
					block.EndToken = nextBlock.EndToken
					if (nextBlock.MultiPart == False):
						break

			block.PreviousBlock = lastBlock
			block.StartToken.PreviousToken = lastBlock.EndToken
			yield block
			lastBlock = block

def FastForward(generator):
	iterator =  iter(generator)
	# don't filter the first block
	yield next(iterator)

	for block in iterator:
		if isinstance(block, (IndentationBlock, CommentBlock, LinebreakBlock)):
			continue
		else:
			yield block
