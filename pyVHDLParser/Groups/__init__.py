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
# Copyright 2007-2017 Patrick Lehmann - Dresden, Germany
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
from types                          import FunctionType

from pyVHDLParser.Base              import ParserException


class BlockParserException(ParserException):
	def __init__(self, message, token):
		super().__init__(message)
		self._token = token


class MetaGroup(type):
	"""Register all state*** methods in an array called '__STATES__'"""
	def __new__(cls, className, baseClasses, classMembers : dict):
		states = []
		for memberName, memberObject in classMembers.items():
			if (isinstance(memberObject, FunctionType) and (memberName[:5] == "state")):
				states.append(memberObject)

		classMembers['__STATES__'] = states
		return super().__new__(cls, className, baseClasses, classMembers)


class Group(metaclass=MetaGroup):
	__STATES__ = None

	def __init__(self, previousGroup, startBlock, endBlock=None):
		previousGroup.NextGroup = self
		self._previousGroup =     previousGroup
		self.NextGroup =          None
		self.StartBlock =         startBlock
		self.EndBlock =           startBlock if (endBlock is None) else endBlock

	def __len__(self):
		return self.EndBlock.End.Absolute - self.StartBlock.Start.Absolute + 1

	def __iter__(self):
		block = self.StartBlock
		# print("group={0}({1})  start={2!s}  end={3!s}".format(self.__class__.__name__, self.__class__.__module__, self.StartToken, self.EndToken))
		while (block is not self.EndBlock):
			yield block
			if (block.NextBlock is None):
				raise BlockParserException("Token after {0} <- {1} <- {2} is None.".format(block, block.PreviousToken, block.PreviousToken.PreviousToken), block)
			block = block.NextBlock

		yield self.EndBlock

	def __repr__(self):
		buffer = "undefined block content"
		# for block in self:
		# 	if isinstance(block, CharacterToken):
		# 		buffer += repr(block)
		# 	else:
		# 		buffer += block.Value

		buffer = buffer.replace("\t", "\\t")
		buffer = buffer.replace("\n", "\\n")
		return buffer

	def __str__(self):
		return "group ...."
		# return "[{groupName: <30s} {stream: <62s} at {start!s} .. {end!s}]".format(
		# 	groupName="{module}.{classname}".format(
		# 		module=self.__module__.rpartition(".")[2],
		# 		classname=self.__class__.__name__
		# 	),
		# 	stream="'" + repr(self) + "'",
		# 	start=self.StartBlock.StartToken.Start,
		# 	end=self.EndBlock.EndToken.End
		# )

	@property
	def PreviousGroup(self):
		return self._previousGroup
	@PreviousGroup.setter
	def PreviousGroup(self, value):
		self._previousGroup = value
		value.NextGroup = self

	@property
	def Length(self):
		return len(self)

	@property
	def States(self):
		return self.__STATES__
