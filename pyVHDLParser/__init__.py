# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
#            __     ___   _ ____  _     ____
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|
# |_|    |___/
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python package:     A streaming-based VHDL parser.
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
from pyVHDLParser.Decorators          import Export

__all__ = []
__api__ = __all__


@Export
class SourceCodePosition:
	"""Represent a position (row, column, absolute) in a source code file."""

	Row :       int = None    #: Row in the source code file
	Column :    int = None    #: Column (character) in the source code file's line
	Absolute :  int = None    #: Absolute character position regardless of linebreaks.

	def __init__(self, row : int, column : int, absolute : int):
		"""Initializes a SourceCodePosition object."""

		self.Row =       row
		self.Column =    column
		self.Absolute =  absolute

	def __repr__(self):
		return "{0}:{1}".format(self.Row, self.Column)

	def __str__(self):
		return "(line: {0: >3}, col: {1: >2})".format(self.Row, self.Column)


@Export
class StartOf:
	"""Base-class (mixin) for all StartOf*** classes."""

@Export
class StartOfDocument(StartOf):
	"""Base-class (mixin) for all StartOf***Document classes."""

@Export
class StartOfSnippet(StartOf):
	"""Base-class (mixin) for all StartOf***Snippet classes."""

@Export
class EndOf:
	"""Base-class (mixin) for all EndOf*** classes."""

@Export
class EndOfDocument(EndOf):
	"""Base-class (mixin) for all EndOf***Document classes."""

@Export
class EndOfSnippet(EndOf):
	"""Base-class (mixin) for all EndOf***Snippet classes."""
