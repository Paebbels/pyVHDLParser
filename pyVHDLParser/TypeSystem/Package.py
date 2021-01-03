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
from pydecor.decorators               import export

__all__ = []
__api__ = __all__


@export
class Parameter:
	def __init__(self, name, subType):
		self._name = name
		self._subType = subType


@export
class SubProgramDeclaration:
	def __init__(self, name, parameters):
		self._name = name
		self._parameters = parameters


@export
class ProcedureDeclaration(SubProgramDeclaration):
	pass

@export
class FunctionDeclaration(SubProgramDeclaration):
	def __init__(self, name, parameters, returnType):
		super().__init__(name, parameters)
		self._returnType = returnType


@export
class SubProgram:
	def __init__(self, subprogramDeclaration):
		self._subprogramDeclaration = subprogramDeclaration


@export
class Procedure(SubProgram):
	def __init__(self, procedureDeclaration):
		super().__init__(procedureDeclaration)


@export
class Function(SubProgram):
	def __init__(self, functionDeclaration, function):
		super().__init__(functionDeclaration)
		self._function = function

	def Call(self, arguments):
		return self._function(arguments)


@export
class PackageDeclation:
	def __init__(self, name, publicMembers):
		self._name =            name
		self._publicMembers =   publicMembers

@export
class PackageBody:
	def __init__(self, declaration, privateMembers):
		self._declaration =     declaration
		self._privateMembers =  privateMembers

@export
class Package:
	def __init__(self, declaration, body):
		self._declaration =     declaration
		self._body =            body
