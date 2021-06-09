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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
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
from pyVHDLParser.Token.Parser  import Tokenizer, TokenizerException
from pyVHDLParser.Token         import StartOfDocumentToken, EndOfDocumentToken, Token

from tests.Interfaces import ITestcase

class TokenizerChecks(ITestcase): #, ExpectedDataMixin):
	def check_TokenLinking(self) -> None:
		# test['name']
		tokenStream = Tokenizer.GetVHDLTokenizer(self.code)

		tokenIterator = iter(tokenStream)
		startToken =    next(tokenIterator)

		self.assertIsInstance(startToken, StartOfDocumentToken, msg="First token is not StartOfDocumentToken: {token}".format(token=startToken))
		self.assertIsNone(startToken.PreviousToken, msg="First token has no open start.")

		lastToken: Token = startToken
		endToken:  Token = None

		for token in tokenIterator:
			if isinstance(token, EndOfDocumentToken):
				endToken = token
				break

			self.assertEqual(lastToken.NextToken, token, msg="Last token is not connected to the current token: {token}".format(token=token))
			self.assertEqual(lastToken, token.PreviousToken, msg="Current token is not connected to lastToken: {token}".format(token=token))

			lastToken = token
		else:
			self.fail(msg="No EndOfDocumentToken found.")

		self.assertIsInstance(endToken, EndOfDocumentToken, msg="End token is not EndOfDocumentToken: {token}".format(token=endToken))
		self.assertEqual(lastToken.NextToken, endToken, msg="Last token is not connected to the end token: {token}".format(token=token))
		self.assertEqual(lastToken, endToken.PreviousToken, msg="End token is not connected to lastToken: {token}".format(token=token))
		self.assertIsNone(endToken.NextToken, msg="End token has no open end: {token}".format(token=endToken.NextToken))
