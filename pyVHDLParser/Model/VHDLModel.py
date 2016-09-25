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
# Copyright 2007-2016 Patrick Lehmann - Dresden, Germany
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
from enum import Enum


class ModelEntity:
	def __init__(self):
		self._parent = None


class LabledEntity:
	def __init__(self):
		self._label = None

class Model(ModelEntity):
	def __init__(self):
		super().__init__()
		self._libraries = []
		self._documents = []

class Library(ModelEntity):
	def __init__(self):
		super().__init__()
		self._entities =  []
		self._packages =  []

class Document(ModelEntity):
	def __init__(self):
		super().__init__()
		self._contexts =        []
		self._entities =        []
		self._architectures =   []
		self._packages =        []
		self._packageBodies =   []

	@property
	def Contexts(self):       return self._contexts
	@property
	def Entities(self):       return self._entities
	@property
	def Architectures(self):  return self._architectures
	@property
	def Packages(self):       return self._packages
	@property
	def PackageBodies(self):  return self._packageBodies


class Architecture(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =            None
		self._entity =          None
		self._uses =            []
		self._declaredItems =   []
		self._bodyItems =       []


class Context(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =            None
		self._uses =            []


class Entity(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =            None
		self._uses =            []
		self._genericItems =    []
		self._portItems =       []
		self._declaredItems =   []
		self._bodyItems =       []


class GenericItem(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name = None
		self._subType = None
		self._init = None


class PortItem(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =        None
		self._subType =     None
		self._init =        None
		self._mode =        None
		self._class =       None


class Modes(Enum):
	Default = 0
	In =      1
	Out =     2
	InOut =   3
	Buffer =  4


class Class(Enum):
	Default =  0
	Constant = 1
	Variable = 2
	Signal =   3


class Package(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =            None
		self._uses =            []
		self._genericItems =    []
		self._declaredItems =   []


class PackageBody(ModelEntity):
	def __init__(self):
		super().__init__()
		self._package =         None
		self._uses =            []
		self._declaredItems =   []


class Use(ModelEntity):
	def __init__(self):
		super().__init__()
		self._library = None
		self._package = None
		self._item =    None


class LibraryReference(ModelEntity):
	def __init__(self):
		super().__init__()
		self._library = None


class Constant(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =    None
		self._subType = None
		self._init =    None


class Variable(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =    None
		self._subType = None
		self._init =    None


class Signal(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =    None
		self._subType = None
		self._init =    None


class BaseType(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name = None


class Type(BaseType):
	def __init__(self):
		super().__init__()


class SubType(BaseType):
	def __init__(self):
		super().__init__()
		self._type = None


class ScalarType(BaseType):
	def __init__(self):
		super().__init__()


class CompositeType(BaseType):
	def __init__(self):
		super().__init__()


class ProtectedType(BaseType):
	def __init__(self):
		super().__init__()


class EnumeratedType(ScalarType):
	def __init__(self):
		super().__init__()
		self._elements = []


class IntegerType(ScalarType):
	def __init__(self):
		super().__init__()
		self._lowerBound = None
		self._upperBound = None


class RealType(ScalarType):
	def __init__(self):
		super().__init__()
		self._lowerBound = None
		self._upperBound = None


class ArrayType(CompositeType):
	def __init__(self):
		super().__init__()
		self._dimensions =  []
		self._baseType =    None


class RecordType(BaseType):
	def __init__(self):
		super().__init__()
		self._members =     []


class RecordTypeMember(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =        None
		self._subType =     None


class Range:
	def __init__(self):
		self._lowerBound = None
		self._upperBound = None
		self._direction =  None


class SubProgramm(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =            None
		self._genericItems =    []
		self._parameterItems =  []
		self._declaredItems =   []
		self._bodyItems =       []


class Procedure(SubProgramm):
	def __init__(self):
		super().__init__()


class Function(SubProgramm):
	def __init__(self):
		super().__init__()
		self._returnType =  None
		self._isPure =      True


class ProcedureMethod(Procedure):
	def __init__(self):
		super().__init__()
		self._protectedType = None


class FunctionMethod(Procedure):
	def __init__(self):
		super().__init__()
		self._protectedType = None


class Process(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		LabledEntity.__init__(self)
		self._parameterItems =  []
		self._declaredItems =   []
		self._bodyItems =       []


class Block(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		LabledEntity.__init__(self)
		self._portItems = []
		self._declaredItems = []
		self._bodyItems = []


class BaseGenerate(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		LabledEntity.__init__(self)
		self._declaredItems = []
		self._bodyItems = []


class IfGenerate(BaseGenerate):
	def __init__(self):
		super().__init__()
		self._condition = None


class ElsIfGenerate(IfGenerate):
	def __init__(self):
		super().__init__()
		self._condition = None
		self._ifGenerate = None


class ElseGenerate(BaseGenerate):
	def __init__(self):
		super().__init__()
		self._ifGenerate = None


class ForGenerate(BaseGenerate):
	def __init__(self):
		super().__init__()
		self._constantName =    None
		self._range =           None


# class CaseGenerate(BaseGenerate):
# 	def __init__(self):
# 		super().__init__()
# 		self._expression =      None
# 		self._cases =           []


class SignalAssignment(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		self._signal =      None
		self._waveform =    None


class VariableAssignment(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		self._variable =    None
		self._expression =  None


class ReportStatement(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		self._expression =  None
		self._severity =    None


class AssertStatement(ReportStatement):
	def __init__(self):
		super().__init__()
		self._condition =   None


class BaseBlockStatement(ModelEntity):
	def __init__(self):
		super().__init__()
		self._bodyItems = []


class IfStatement(BaseBlockStatement):
	def __init__(self):
		super().__init__()
		self._condition = None


class ElsIfStatement(IfStatement):
	def __init__(self):
		super().__init__()
		self._ifStatement = None


class ElseStatement(BaseBlockStatement):
	def __init__(self):
		super().__init__()
		self._ifStatement = None


class ForLoopStatement(BaseBlockStatement):
	def __init__(self):
		super().__init__()
		self._variableName =    None
		self._range =           None


class WhileLoopStatement(BaseBlockStatement):
	def __init__(self):
		super().__init__()
		self._condition = None


class LoopControlStatement(ModelEntity):
	def __init__(self):
		super().__init__()
		self._loop =      None
		self._condition = None


class ContinueStatement(LoopControlStatement):
	def __init__(self):
		super().__init__()


class ExitStatement(LoopControlStatement):
	def __init__(self):
		super().__init__()


class ReturnStatement(BaseBlockStatement):
	def __init__(self):
		super().__init__()
