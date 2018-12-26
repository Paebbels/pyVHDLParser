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
from pyVHDLParser.Common                import VHDLVersion, vhdlVersion
from pyVHDLParser.TypeSystem.Package    import Parameter, FunctionDeclaration, Function, PackageDeclation, PackageBody, Package
from pyVHDLParser.TypeSystem.TypeSystem import EnumerationType, ArrayType, Range, SubType, EnumerationSubType
from pyVHDLParser.TypeSystem.std        import Natural


Std_ULogic_Values = [
	"U",  # Uninitialized
  "X",  # Forcing  Unknown
  "0",  # Forcing  0
  "1",  # Forcing  1
  "Z",  # High Impedance
  "W",  # Weak     Unknown
  "L",  # Weak     0
  "H",  # Weak     1
  "-"   # Don't care
]

Std_ULogic =          EnumerationType("std_ulogic", Std_ULogic_Values)
Std_ULogic_U =        Std_ULogic.Attributes.Value("U")
Std_ULogic_Z =        Std_ULogic.Attributes.Value("Z")

Std_ULogic_Vector =   ArrayType("std_ulogic_vector", Range(Natural), Std_ULogic)

Func_Resolved_Decl =  FunctionDeclaration("resolved", [
	Parameter("s", Std_ULogic_Vector)
], Std_ULogic)

RESOLUTION_TABLE = (
	## ---------------------------------------------------------
  ## |  U    X    0    1    Z    W    L    H    -        |   |
  ## ---------------------------------------------------------
			('U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U'),  ## | U |
			('U', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'),  ## | X |
			('U', 'X', '0', 'X', '0', '0', '0', '0', 'X'),  ## | 0 |
			('U', 'X', 'X', '1', '1', '1', '1', '1', 'X'),  ## | 1 |
			('U', 'X', '0', '1', 'Z', 'W', 'L', 'H', 'X'),  ## | Z |
			('U', 'X', '0', '1', 'W', 'W', 'W', 'W', 'X'),  ## | W |
			('U', 'X', '0', '1', 'L', 'W', 'L', 'W', 'X'),  ## | L |
			('U', 'X', '0', '1', 'H', 'W', 'W', 'H', 'X'),  ## | H |
			('U', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X')   ## | - |
	)

def Resolution(arguments):
	sources = arguments[0]
	if sources.Attributes.Length == 1:
		return sources[sources.Attributes.Low]
	else:
		result = Std_ULogic_Z.Pos
		# result = Std_ULogic.Attributes.Pos(Std_ULogic_Z)
		for source in sources:
			idx2 =   source.Pos
			# idx2 =   Std_ULogic.Attributes.Pos(source)
			result = RESOLUTION_TABLE[result][idx2]
			
		return Std_Logic.Attributes.Val(result)
	

Func_Resolved =           Function(Func_Resolved_Decl, Resolution)

Std_Logic =               EnumerationSubType("std_logic", Std_ULogic, resolutionFunction=Func_Resolved)

if (vhdlVersion < VHDLVersion.VHDL2008):
	Std_Logic_Vector =      ArrayType("std_logic_vector", Range(Natural), Std_Logic)
else:
	pass
	# Std_Logic_Vector =      ArraySubType("std_logic_vector", Std_ULogic_Vector, resolutionFunction=Func_Resolved)



Std_Logic_1164_Decl =     PackageDeclation("std_logic_1164", [
	Std_ULogic,
	Std_ULogic_Vector,
	Func_Resolved_Decl,
	Std_Logic,
	Std_Logic_Vector
])
Std_Logic_1164_Body =     PackageBody(Std_Logic_1164_Decl, [
	Func_Resolved
])

Std_Logic_1164 =          Package(Std_Logic_1164_Decl, Std_Logic_1164_Body)
