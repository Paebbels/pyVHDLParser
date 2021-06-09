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
from typing import Any


class ITestcase:
	code: str

	def skipTest(self, reason=None):
		pass

	def fail(self, msg: str = ""):
		pass

	def failIf(self, expr: bool, msg: str = ""):
		if expr:
			self.fail(msg=msg)

	def assertEqual(self, left: Any, right: Any, msg: str = ""):
		pass

	def assertIsInstance(self, obj: Any, typ, msg: str = ""):
		pass

	def assertIsNotInstance(self, obj: Any, typ, msg: str = ""):
		pass

	def assertTrue(self, obj: bool, msg: str = ""):
		pass

	def assertIsNone(self, obj: Any, msg: str = ""):
		pass

	def assertIsNotNone(self, obj: Any, msg: str = ""):
		pass
