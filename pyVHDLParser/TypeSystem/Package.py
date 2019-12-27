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
from pyVHDLParser.Decorators          import Export

__all__ = []
__api__ = __all__


@Export
class Parameter:
	def __init__(self, name, subType):
		self._name = name
		self._subType = subType


@Export
class SubProgramDeclaration:
	def __init__(self, name, parameters):
		self._name = name
		self._parameters = parameters


@Export
class ProcedureDeclaration(SubProgramDeclaration):
	pass

@Export
class FunctionDeclaration(SubProgramDeclaration):
	def __init__(self, name, parameters, returnType):
		super().__init__(name, parameters)
		self._returnType = returnType


@Export
class SubProgram:
	def __init__(self, subprogramDeclaration):
		self._subprogramDeclaration = subprogramDeclaration


@Export
class Procedure(SubProgram):
	def __init__(self, procedureDeclaration):
		super().__init__(procedureDeclaration)


@Export
class Function(SubProgram):
	def __init__(self, functionDeclaration, function):
		super().__init__(functionDeclaration)
		self._function = function
	
	def Call(self, arguments):
		return self._function(arguments)
	

@Export
class PackageDeclation:
	def __init__(self, name, publicMembers):
		self._name =            name
		self._publicMembers =   publicMembers

@Export
class PackageBody:
	def __init__(self, declaration, privateMembers):
		self._declaration =     declaration
		self._privateMembers =  privateMembers

@Export
class Package:
	def __init__(self, declaration, body):
		self._declaration =     declaration
		self._body =            body
