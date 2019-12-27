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
from enum                     import Enum

from pyVHDLParser.Decorators  import Export

__all__ = []
__api__ = __all__


@Export
class VHDLVersion(Enum):
	Any =       0
	VHDL87 =    87
	VHDL93 =    93
	VHDL2002 =  2002
	VHDL2008 =  2008
	
	__VHDL_VERSION_MAPPINGS__ = {
		87:     VHDL87,
		93:     VHDL93,
		2:      VHDL2002,
		8:      VHDL2008,
		1987:   VHDL87,
		1993:   VHDL93,
		2002:   VHDL2002,
		2008:   VHDL2008,
		"87":   VHDL87,
		"93":   VHDL93,
		"02":   VHDL2002,
		"08":   VHDL2008,
		"1987": VHDL87,
		"1993": VHDL93,
		"2002": VHDL2002,
		"2008": VHDL2008
	}
	
	def __init__(self, *_):
		"""Patch the embedded MAP dictionary"""
		for k, v in self.__class__.__VHDL_VERSION_MAPPINGS__.items():
			if ((not isinstance(v, self.__class__)) and (v == self.value)):
				self.__class__.__VHDL_VERSION_MAPPINGS__[k] = self

	def __eq__(self, other):
		if ((self is VHDLVersion.Any) or (other is VHDLVersion.Any)):
			return True
		else:
			return (self.value == other.value)
	def __ne__(self, other):  return self.value != other.value
	def __lt__(self, other):  return self.value <  other.value
	def __le__(self, other):  return self.value <= other.value
	def __gt__(self, other):  return self.value >  other.value
	def __ge__(self, other):  return self.value >= other.value
	
	def __str__(self):
		return "VHDL'" + str(self.value)[-2:]
	
	def __repr__(self):
		return str(self.value)
	
	@classmethod
	def Parse(cls, value):
		try:
			return cls.__VHDL_VERSION_MAPPINGS__[value]
		except KeyError:
			ValueError("Value '{0!s}' cannot be parsed to member of {1}.".format(value, cls.__name__))
