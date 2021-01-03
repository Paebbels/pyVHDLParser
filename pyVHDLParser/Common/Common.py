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
from enum                     import Enum

from pydecor.decorators       import export

__all__ = []
__api__ = __all__


@export
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

	def __eq__(self, other: 'VHDLVersion') -> bool:
		"""Return true if the internal value is equal to the second operand."""
		if ((self is VHDLVersion.Any) or (other is VHDLVersion.Any)):
			return True
		else:
			return (self.value == other.value)

	def __ne__(self, other: 'VHDLVersion') -> bool:
		"""Return true if the internal value is unequal to the second operand."""
		return self.value != other.value

	def __lt__(self, other: 'VHDLVersion') -> bool:
		"""Return true if the internal value is less than to the second operand."""
		return self.value <  other.value

	def __le__(self, other: 'VHDLVersion') -> bool:
		"""Return true if the internal value is less than or equal to the second operand."""
		return self.value <= other.value

	def __gt__(self, other: 'VHDLVersion') -> bool:
		"""Return true if the internal value is greater than to the second operand."""
		return self.value >  other.value

	def __ge__(self, other: 'VHDLVersion') -> bool:
		"""Return true if the internal value is greater than or equal to the second operand."""
		return self.value >= other.value


	def __str__(self) -> str:
		return "VHDL'" + str(self.value)[-2:]

	def __repr__(self) -> str:
		return str(self.value)

	@classmethod
	def Parse(cls, value) -> 'VHDLVersion':
		try:
			return cls.__VHDL_VERSION_MAPPINGS__[value]
		except KeyError:
			ValueError("Value '{0!s}' cannot be parsed to member of {1}.".format(value, cls.__name__))
