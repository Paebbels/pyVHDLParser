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
from pyVHDLParser.Common import VHDLVersion, vhdlVersion
from pyVHDLParser.TypeSystem.Package import PackageDeclation, PackageBody, Package
from pyVHDLParser.TypeSystem.TypeSystem import EnumerationType, ArrayType, IntegerType, RealType, Direction, SubType, Range, IntegerSubType


Boolean_Values = [
  "FALSE", #
	"TRUE"   #
]

Boolean =               EnumerationType("boolean", Boolean_Values)


UniversatInteger =      IntegerType("universat_integer")
Integer =               IntegerSubType("integer",  UniversatInteger, Range(UniversatInteger, Direction.To, -2**31, 2*31))
Natural =               IntegerSubType("natural",  Integer, Range(UniversatInteger, Direction.To, 0, Integer.Attributes.Right))
Positive =              IntegerSubType("positive", Integer, Range(UniversatInteger, Direction.To, 1, Integer.Attributes.Right))

UniversatReal =         RealType("universat_real")
Real =                  IntegerSubType("real", UniversatReal, Range(UniversatReal, Direction.To, -10.0, 10.0))


if (vhdlVersion < VHDLVersion.VHDL2008):
	Std_Decl = PackageDeclation("std", [
		Boolean,
		Integer,
		Positive,
		Natural
	])
	Std_Body = PackageBody(Std_Decl, [])
	
elif (vhdlVersion >= VHDLVersion.VHDL2008):
	Boolean_Vector =      ArrayType("boolean_vector", Range(Natural), Boolean)
	Integer_Vector =      ArrayType("integer_vector", Range(Natural), Integer)


	Std_Decl =              PackageDeclation("std", [
		Boolean,
		Boolean_Vector,
		Integer,
		Positive,
		Natural
	])
	Std_Body =              PackageBody(Std_Decl, [])



Std =                   Package(Std_Decl, Std_Body)

