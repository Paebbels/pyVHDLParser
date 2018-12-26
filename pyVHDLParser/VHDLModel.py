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
from enum import Enum


class ModelEntity:
	def __init__(self):
		self._parent = None

	@property
	def Parent(self):
		return self._parent


class NamedEntity:
	def __init__(self):
		self._name = None

	@property
	def Name(self):
		return self._name


class LabledEntity:
	def __init__(self):
		self._label = None

	@property
	def Label(self):
		return self._label


class Model(ModelEntity):
	def __init__(self):
		super().__init__()
		self._libraries = []
		self._documents = []

	@property
	def Libraries(self):
		return self._libraries

	@property
	def Documents(self):
		return self._documents


class Library(ModelEntity):
	def __init__(self):
		super().__init__()
		self._configurations =  []
		self._entities =        []
		self._packages =        []

	@property
	def Configurations(self):
		return self._configurations

	@property
	def Entities(self):
		return self._entities

	@property
	def Packages(self):
		return self._packages


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


class Modes(Enum):
	Default = 0
	In =      1
	Out =     2
	InOut =   3
	Buffer =  4
	Linkage = 5


class Class(Enum):
	Default =    0
	Constant =   1
	Variable =   2
	Signal =     3
	File =       4
	Type =       5
	Subprogram = 6


class InterfaceItem(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name = None

	@property
	def Name(self):
		return self._name

class GenericInterfaceItem(InterfaceItem):   pass
class PortInterfaceItem(InterfaceItem):      pass
class ParameterInterfaceItem(InterfaceItem): pass


class ConstantInterfaceItem(GenericInterfaceItem):
	def __init__(self):
		super().__init__()
		self._subType =           None
		self._defaultExpression = None

	@property
	def SubType(self):
		return self._subType

	@property
	def DefaultExpression(self):
		return self._defaultExpression


class PortSignalInterfaceItem(PortInterfaceItem):
	def __init__(self):
		super().__init__()
		self._subType =           None
		self._mode =              None
		self._defaultExpression = None

	@property
	def SubType(self):
		return self._subType

	@property
	def Mode(self):
		return self._mode

	@property
	def DefaultExpression(self):
		return self._defaultExpression


class ParameterVariableInterfaceItem(ParameterInterfaceItem):
	def __init__(self):
		super().__init__()
		self._subType =           None
		self._mode =              None
		self._defaultExpression = None

	@property
	def SubType(self):
		return self._subType

	@property
	def Mode(self):
		return self._mode

	@property
	def DefaultExpression(self):
		return self._defaultExpression


# class GenericItem(ModelEntity):
# 	def __init__(self):
# 		super().__init__()
# 		self._name = None
# 		self._subType = None
# 		self._init = None
#
#
# class PortItem(ModelEntity):
# 	def __init__(self):
# 		super().__init__()
# 		self._name =        None
# 		self._subType =     None
# 		self._init =        None
# 		self._mode =        None
# 		self._class =       None


class PrimaryUnit(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)


class SecondaryUnit(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)


class Context(PrimaryUnit):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)
		self._uses =            []

	@property
	def Uses(self):
		return self._uses


class Entity(PrimaryUnit):
	def __init__(self):
		super().__init__()
		self._libraryReferences = []
		self._uses =              []
		self._genericItems =      []
		self._portItems =         []
		self._declaredItems =     []
		self._bodyItems =         []

	@property
	def LibraryReferences(self):
		return self._libraryReferences

	@property
	def Uses(self):
		return self._uses

	@property
	def GenericItems(self):
		return self._genericItems

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


class Architecture(SecondaryUnit):
	def __init__(self):
		super().__init__()
		self._entity =            None
		self._libraryReferences = []
		self._uses =              []
		self._declaredItems =     []
		self._bodyItems =         []

	@property
	def Entity(self):
		return self._entity

	@property
	def LibraryReferences(self):
		return self._libraryReferences

	@property
	def Uses(self):
		return self._uses

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


class AssociationItem(ModelEntity):
	def __init__(self):
		super().__init__()
		self._formal = None
		self._actual = None

	@property
	def Formal(self):
		return self._formal

	@property
	def Actual(self):
		return self._actual


class GenericAssociationItem(InterfaceItem):   pass
class PortAssociationItem(InterfaceItem):      pass
class ParameterAssociationItem(InterfaceItem): pass


class Configuration(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()

		raise NotImplementedError()


class Instantiation(NamedEntity):
	def __init__(self):
		super().__init__()
		self._packageReference =    None
		self._genericAssociations = []


class Package(PrimaryUnit):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)
		self._libraryReferences = []
		self._uses =              []
		self._genericItems =      []
		self._declaredItems =     []

	@property
	def LibraryReferences(self):
		return self._libraryReferences

	@property
	def Uses(self):
		return self._uses

	@property
	def GenericItems(self):
		return self._genericItems

	@property
	def DeclaredItems(self):
		return self._declaredItems


class PackageBody(SecondaryUnit):
	def __init__(self):
		super().__init__()
		self._package =           None
		self._libraryReferences = []
		self._uses =              []
		self._declaredItems =     []

	@property
	def Package(self):
		return self._package

	@property
	def LibraryReferences(self):
		return self._libraryReferences

	@property
	def Uses(self):
		return self._uses

	@property
	def DeclaredItems(self):
		return self._declaredItems


class PackageInstantiation(PrimaryUnit, Instantiation):
	def __init__(self):
		super().__init__()
		Instantiation.__init__(self)
		self._packageReferences = None


class LibraryReference(ModelEntity):
	def __init__(self):
		super().__init__()
		self._library = None

	@property
	def Library(self):
		return self._library


class Use(ModelEntity):
	def __init__(self):
		super().__init__()
		self._library = None
		self._package = None
		self._item =    None

	@property
	def Library(self):
		return self._library

	@property
	def Package(self):
		return self._package

	@property
	def Item(self):
		return self._item


class Object(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)
		self._subType = None

	@property
	def SubType(self):
		return self._subType


class BaseConstant(Object): pass


class DeferredConstant(BaseConstant):
	def __init__(self):
		super().__init__()
		self._constantReference = None

	@property
	def ConstantReference(self):
		return self._constantReference


class Constant(BaseConstant):
	def __init__(self):
		super().__init__()
		self._defaultExpression = None

	@property
	def DefaultExpression(self):
		return self._defaultExpression


class Variable(Object):
	def __init__(self):
		super().__init__()
		self._defaultExpression = None

	@property
	def DefaultExpression(self):
		return self._defaultExpression


class Signal(Object):
	def __init__(self):
		super().__init__()
		self._defaultExpression = None

	@property
	def DefaultExpression(self):
		return self._defaultExpression


class BaseType(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)


class Type(BaseType): pass


class SubType(BaseType):
	def __init__(self):
		super().__init__()
		self._type = None
		
	@property
	def Type(self):
		return self._type


class ScalarType(BaseType):     pass
class CompositeType(BaseType):  pass
class ProtectedType(BaseType):  pass
class AccessType(BaseType):     pass
class FileType(BaseType):       pass


class EnumeratedType(ScalarType):
	def __init__(self):
		super().__init__()
		self._elements = []
		
	@property
	def Elements(self):
		return self._elements


class IntegerType(ScalarType):
	def __init__(self):
		super().__init__()
		self._leftBound = None
		self._rightBound = None


class RealType(ScalarType):
	def __init__(self):
		super().__init__()
		self._leftBound = None
		self._rightBound = None


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
		self._leftBound = None
		self._rightBound = None
		self._direction =  None


class SubProgramm(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)
		self._genericItems =    []
		self._parameterItems =  []
		self._declaredItems =   []
		self._bodyItems =       []

	@property
	def GenericItems(self):
		return self._genericItems

	@property
	def ParameterItems(self):
		return self._parameterItems

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


class Procedure(SubProgramm): pass


class Function(SubProgramm):
	def __init__(self):
		super().__init__()
		self._returnType =  None
		self._isPure =      True

	@property
	def ReturnType(self):
		return self._returnType

	@property
	def IsPure(self):
		return self._isPure


class SubprogramInstantiation(ModelEntity, Instantiation):
	def __init__(self):
		super().__init__()
		Instantiation.__init__(self)
		self._subprogramReference = None

class ProcedureInstantiation(SubprogramInstantiation):  pass
class FunctionInstantiation(SubprogramInstantiation):   pass


class Method:
	def __init__(self):
		super().__init__()
		self._protectedType = None


class ProcedureMethod(Procedure, Method):
	def __init__(self):
		super().__init__()
		Method.__init__(self)


class FunctionMethod(Function, Method):
	def __init__(self):
		super().__init__()
		Method.__init__(self)


class Statement(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		LabledEntity.__init__(self)


class ConcurrentStatement(Statement):	pass
class SequentialStatement(Statement):	pass


class ProcessStatement(ConcurrentStatement):
	def __init__(self):
		super().__init__()
		self._parameterItems =  []
		self._declaredItems =   []
		self._bodyItems =       []

	@property
	def ParameterItems(self):
		return self._parameterItems

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


class ConcurrentBlockStatement(ConcurrentStatement):
	def __init__(self):
		super().__init__()
		self._portItems = []
		self._declaredItems = []
		self._bodyItems = []

	@property
	def PortItems(self):
		return self._portItems

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


class GenerateStatement(ConcurrentStatement):
	def __init__(self):
		super().__init__()
		self._declaredItems = []
		self._bodyItems =     []

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


class IfGenerateStatement(GenerateStatement):
	def __init__(self):
		super().__init__()
		self._ifBranch =      None
		self._elsifBranches = []
		self._elseBranch =    None


class BaseConditional:
	def __init__(self):
		super().__init__()
		self._condition = None

	@property
	def Condition(self):
		return self._condition


class BaseBranch: pass

class BaseConditionalBranch(BaseBranch, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)


class BaseIfBranch(BaseConditionalBranch):                  pass
class BaseElsifBranch(BaseConditionalBranch):               pass
class BaseElseBranch(BaseBranch):                           pass

class GenerateBranch(ModelEntity):                          pass


class IfGenerateBranch(GenerateBranch, BaseIfBranch):
	def __init__(self):
		super().__init__()
		BaseIfBranch.__init__(self)


class ElsifGenerateBranch(GenerateBranch, BaseElsifBranch):
	def __init__(self):
		super().__init__()
		BaseElsifBranch.__init__(self)


class ElseGenerateBranch(GenerateBranch, BaseElseBranch):
	def __init__(self):
		super().__init__()
		BaseElseBranch.__init__(self)


class ForGenerateStatement(GenerateStatement):
	def __init__(self):
		super().__init__()
		self._loopIndex = None
		self._range =     None

	@property
	def LoopIndex(self):
		return self._loopIndex

	@property
	def Range(self):
		return self._range


# class CaseGenerate(GenerateStatement):
# 	def __init__(self):
# 		super().__init__()
# 		self._expression =      None
# 		self._cases =           []

class Assignment:
	def __init__(self):
		super().__init__()
		self._target =      None
		self._expression =  None

	@property
	def Target(self):
		return self._target

	@property
	def Expression(self):
		return self._expression


class SignalAssignment(Assignment):    pass
class VariableAssignment(Assignment):  pass


class ConcurrentSignalAssignment(ConcurrentStatement, SignalAssignment):
	def __init__(self):
		super().__init__()
		SignalAssignment.__init__(self)


class SequentialSignalAssignment(SequentialStatement, SignalAssignment):
	def __init__(self):
		super().__init__()
		SignalAssignment.__init__(self)


class SequentialVariableAssignment(SequentialStatement, VariableAssignment):
	def __init__(self):
		super().__init__()
		VariableAssignment.__init__(self)



class ReportStatement:
	def __init__(self):
		super().__init__()
		self._message =   None
		self._severity =  None

	@property
	def Message(self):
		return self._message

	@property
	def Severity(self):
		return self._severity


class AssertStatement(ReportStatement):
	def __init__(self):
		super().__init__()
		self._condition = None

	@property
	def Condition(self):
		return self._condition


class ConcurrentAssertStatement(ConcurrentStatement, AssertStatement):
	def __init__(self):
		super().__init__()
		AssertStatement.__init__(self)


class SequentialReportStatement(SequentialStatement, ReportStatement):
	def __init__(self):
		super().__init__()
		ReportStatement.__init__(self)


class SequentialAssertStatement(SequentialStatement, AssertStatement):
	def __init__(self):
		super().__init__()
		AssertStatement.__init__(self)



class CompoundStatement(SequentialStatement):
	def __init__(self):
		super().__init__()
		self._bodyItems = []

	@property
	def BodyItems(self):
		return self._bodyItems


class IfStatement(CompoundStatement):
	def __init__(self):
		super().__init__()
		self._ifBranch =      None
		self._elsifBranches = []
		self._elseBranch =    None


class Branch(ModelEntity):  pass

class IfBranch(Branch, BaseIfBranch):
	def __init__(self):
		super().__init__()
		BaseIfBranch.__init__(self)


class ElsifBranch(Branch, BaseElsifBranch):
	def __init__(self):
		super().__init__()
		BaseElsifBranch.__init__(self)


class ElseBranch(Branch, BaseElseBranch):
	def __init__(self):
		super().__init__()
		BaseElseBranch.__init__(self)


class ForLoopStatement(CompoundStatement):
	def __init__(self):
		super().__init__()
		self._loopIndex = None
		self._range =     None

	@property
	def LoopIndex(self):
		return self._loopIndex

	@property
	def Range(self):
		return self._range


class WhileLoopStatement(CompoundStatement, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)


class LoopControlStatement(ModelEntity, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)
		self._loopReference = None

	@property
	def LoopReference(self):
		return self._loopReference


class NextStatement(LoopControlStatement):  pass
class ExitStatement(LoopControlStatement):  pass
class ReturnStatement(SequentialStatement): pass
