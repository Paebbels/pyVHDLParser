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
from enum                     import Enum, unique

from pyVHDLParser.Decorators  import Export


@Export
class _Attributes:
	pass


@Export
class Type:
	def __init__(self, name):
		self._name =      name


@Export
class IntegerType(Type):
	class _Attributes(_Attributes):
		def __init__(self, integer):
			self._int = integer
		
		def Left(self):
			return -2**31
		
		def Right(self):
			return 2**31 - 1
		
		
	def __init__(self, name):
		super().__init__(name)
	

@Export
class RealType(Type):
	def __init__(self, name):
		super().__init__(name)


@Export
class EnumerationLiteral:
	def __init__(self, enum, name, pos):
		self._enum =  enum
		self.Name =   name
		self.Pos =    pos
	
	def __repr__(self):
		return "{enum!r}.{name}".format(enum=self._enum, name=self.Name)
	
	def __str__(self):
		return self.Name
	

@Export
class EnumerationType(Type):
	class _Attributes(_Attributes):
		def __init__(self, enum):
			self._enum = enum
		
		def Low(self):
			return self._enum._range.Left
		
		def High(self):
			return self._enum._range.Right
	
		def Pos(self, value):
			for pos,enumValue in enumerate(self._enum._enumeration):
				if (enumValue == value):
					return pos
		
		def Val(self, pos):
			return self._enum._enumeration[pos]
		
		def Value(self, str):
			for enumValue in self._enum._enumeration:
				if enumValue.Name == str:
					return enumValue
	
	
	def __init__(self, name, enumerationValues):
		super().__init__(name)
		self._enumeration =   tuple([EnumerationLiteral(self, value, pos) for pos,value in enumerate(enumerationValues)])
		self._range =         Range(self, Direction.To, self._enumeration[0], self._enumeration[-1])
		self.Attributes =     self._Attributes(self)
	
	def __repr__(self):
		return self._name
	
	def __str__(self):
		return self._name


@Export
class ArrayType(Type):
	def __init__(self, name, ranges, elementType):
		super().__init__(name)
		self._ranges =        ranges
		self._elementType =   elementType
		
	@property
	def IsConstrained(self):
		for range in self._ranges:
			if (not range.IsConstrained):
				return False
		return self._elementType.IsConstrained

@Export
class RecordMember:
	def __init__(self, name, elementType):
		self._name =          None
		self._elementType =   elementType
		
	@property
	def IsConstrained(self):
		return self._elementType.IsConstrained


@Export
class RecordType(Type):
	def __init__(self, name, members):
		super().__init__(name)
		self._members =       members
	
	@property
	def IsContrained(self):
		for member in self._members:
			if (not member.IsConstrained):
				return False
		return True
	

@Export
class SubType:
	class _Attributes(_Attributes):
		def __init__(self, subType):
			self._subType = subType
		
		def Low(self):
			raise NotImplementedError()
		
		def High(self):
			raise NotImplementedError()

	
	def __init__(self, name, subType, range=None, resolutionFunction=None):
		self._name =                name
		self._subType =             subType
		self._range =               range
		self._resolutionFunction =  resolutionFunction
		self.Attributes =           self._Attributes(self)
	
	@property
	def IsResolved(self):
		return (self._resolutionFunction is not None)
	
	@property
	def IsConstrained(self):
		return (self._range is not None)


@Export
class IntegerSubType(SubType):
	class _Attributes(SubType._Attributes):
		def Left(self):
			return self._subType._range.Left
		
		def Right(self):
			return self._subType._range.Right


@Export
class EnumerationSubType(SubType):
	class _Attributes(SubType._Attributes):
		def Low(self):
			return self._subType._range.Left
		
		def High(self):
			return self._subType._range.Right
		
		def Value(self, str):
			return self._subType._subType.Attributes.Value(str)


	def __init__(self, name, subType, range=None, resolutionFunction=None):
		if (range is None):
			range = subType._range
		super().__init__(name, subType, range, resolutionFunction)


@Export
@unique
class Direction(Enum):
	To =      0
	Downto =  1


@Export
class Range:
	def __init__(self, baseType, direction=None, left=None, right=None):
		self._baseType =  baseType
		
		if (direction is None):
			self.Direction = None
			self.Left =      None
			self.Right =     None
		else:
			self.Direction = direction
			self.Left =      left
			self.Right =     right
	
	@property
	def IsConstrained(self):
		return (self.Direction is not None)


@Export
class TypeInstance:
	pass

@Export
class Array(TypeInstance):
	def __init__(self, arrayType):
		self._arrayType = arrayType
	
	
