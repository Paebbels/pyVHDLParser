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
from pyVHDLParser.Functions import Console


class Counter:


	def __init__(self):
		self._history =   {}
		self._expected =  {}
		self._failing =   {}

	def AddType(self, type, count):
		self._expected[type] = count

	def Count(self, type):
		if type in self._history:
			self._history[type] += 1
		else:
			self._history[type] = 1

	def Check(self):
		good = True
		for key,expectedCount in self._expected.items():
			try:
				count = self._history[key]
			except KeyError:
				self._failing[key] = (0, expectedCount)
				continue

			if (count != expectedCount):
				good = False
				self._failing[key] = (count, expectedCount)
			self._history.pop(key)

		for key,value in self._history.items():
			self._failing[key] = (value, 0)

		return good

	def PrintReport(self):
		for key,(count,expectedCount) in self._failing.items():
			if (count == 0):
				print("      {DARK_GRAY}Missing {expectedCount} {type}{NOCOLOR}".format(expectedCount=expectedCount, type=key.__name__, **Console.Foreground))
			elif (expectedCount == 0):
				print("      {DARK_GRAY}Found {count} unexpected {type}{NOCOLOR}".format(count=count, type=key.__name__, **Console.Foreground))
			else:
				print("      {DARK_GRAY}Expected {expectedCount} of {type}; found {count}{NOCOLOR}".format(count=count, expectedCount=expectedCount, type=key.__name__, **Console.Foreground))
