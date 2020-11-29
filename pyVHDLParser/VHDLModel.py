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
# Copyright 2017-2020 Patrick Lehmann - Boetzingen, Germany
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
from typing                   import List

from pydecor.decorators       import export

__all__ = []
__api__ = __all__


@export
class ModelEntity:
	def __init__(self):
		self._parent = None

	@property
	def Parent(self) -> 'ModelEntity':
		return self._parent


@export
class NamedEntity:
	_name: str

	def __init__(self, name: str):
		self._name = name

	@property
	def Name(self) -> str:
		return self._name


@export
class LabledEntity:
	_label: str

	def __init__(self, label: str):
		self._label = label

	@property
	def Label(self) -> str:
		return self._label


@export
class Design(ModelEntity):
	_libraries:  List['Library']  #: List of all libraries defined for a design
	_documents:  List['Document'] #: List of all documents loaded for a design

	def __init__(self):
		super().__init__()

		self._libraries = []
		self._documents = []

	@property
	def Libraries(self) -> List['Library']:
		return self._libraries

	@property
	def Documents(self) -> List['Document']:
		return self._documents


@export
class Library(ModelEntity):
	_contexts:       List['Context']        #: List of all contexts defined in a library.
	_configurations: List['Configuration']  #: List of all configurations defined in a library.
	_entities:       List['Entity']         #: List of all entities defined in a library.
	_packages:       List['Package']        #: List of all packages defined in a library.

	def __init__(self):
		super().__init__()

		self._contexts =        []
		self._configurations =  []
		self._entities =        []
		self._packages =        []

	@property
	def Contexts(self) -> List['Context']:
		return self._contexts

	@property
	def Configurations(self) -> List['Configuration']:
		return self._configurations

	@property
	def Entities(self) -> List['Entity']:
		return self._entities

	@property
	def Packages(self) -> List['Package']:
		return self._packages


@export
class Document(ModelEntity):
	_contexts:       List['Context']        #: List of all contexts defined in a document.
	_configurations: List['Configuration']  #: List of all configurations defined in a document.
	_entities:       List['Entity']         #: List of all entities defined in a document.
	_architectures:  List['Architecture']   #: List of all architectures defined in a document.
	_packages:       List['Package']        #: List of all packages defined in a document.
	_packageBodies:  List['PackageBody']    #: List of all package bodies defined in a document.

	def __init__(self):
		super().__init__()

		self._contexts =        []
		self._configurations =  []
		self._entities =        []
		self._architectures =   []
		self._packages =        []
		self._packageBodies =   []

	@property
	def Contexts(self) -> List['Context']:
		return self._contexts

	@property
	def Configurations(self) -> List['Configuration']:
		return self._configurations

	@property
	def Entities(self) -> List['Entity']:
		return self._entities

	@property
	def Architectures(self) -> List['Architecture']:
		return self._architectures

	@property
	def Packages(self) -> List['Package']:
		return self._packages

	@property
	def PackageBodies(self) -> List['PackageBody']:
		return self._packageBodies


@export
class Modes(Enum):
	Default = 0
	In =      1
	Out =     2
	InOut =   3
	Buffer =  4
	Linkage = 5


@export
class Class(Enum):
	Default =    0
	Constant =   1
	Variable =   2
	Signal =     3
	File =       4
	Type =       5
	Subprogram = 6


@export
class BaseType(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)


@export
class Type(BaseType):
	pass

@export
class SubType(BaseType):
	def __init__(self):
		super().__init__()
		self._type = None

	@property
	def Type(self):
		return self._type


@export
class ScalarType(BaseType):
	pass

@export
class CompositeType(BaseType):
	pass

@export
class ProtectedType(BaseType):
	pass

@export
class AccessType(BaseType):
	pass

@export
class FileType(BaseType):
	pass

@export
class EnumeratedType(ScalarType):
	def __init__(self):
		super().__init__()
		self._elements = []

	@property
	def Elements(self):
		return self._elements


@export
class IntegerType(ScalarType):
	def __init__(self):
		super().__init__()
		self._leftBound = None
		self._rightBound = None


@export
class RealType(ScalarType):
	def __init__(self):
		super().__init__()
		self._leftBound = None
		self._rightBound = None


@export
class ArrayType(CompositeType):
	def __init__(self):
		super().__init__()
		self._dimensions =  []
		self._baseType =    None


@export
class RecordType(BaseType):
	def __init__(self):
		super().__init__()
		self._members =     []


@export
class RecordTypeMember(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name =        None
		self._subType =     None


@export
class Expression:
	pass

@export
class Range:
	def __init__(self):
		self._leftBound = None
		self._rightBound = None
		self._direction =  None


@export
class InterfaceItem(ModelEntity):
	def __init__(self):
		super().__init__()
		self._name = None

	@property
	def Name(self):
		return self._name


@export
class GenericInterfaceItem(InterfaceItem):
	pass

@export
class PortInterfaceItem(InterfaceItem):
	pass

@export
class ParameterInterfaceItem(InterfaceItem):
	pass

@export
class GenericConstantInterfaceItem(GenericInterfaceItem):
	_subtype:           SubType   # FIXME: add documentation
	_defaultExpression: Expression   # FIXME: add documentation

	@property
	def SubType(self) -> SubType:
		return self._subType

	@property
	def DefaultExpression(self) -> Expression:
		return self._defaultExpression

@export
class GenericTypeInterfaceItem(GenericInterfaceItem):
	pass

@export
class GenericSubprogramInterfaceItem(GenericInterfaceItem):
	pass

@export
class GenericPackageInterfaceItem(GenericInterfaceItem):
	pass


@export
class PortSignalInterfaceItem(PortInterfaceItem):
	_subType:           SubType
	_mode:              Modes
	_defaultExpression: Expression

	def __init__(self):
		super().__init__()

	@property
	def SubType(self) -> SubType:
		return self._subType

	@property
	def Mode(self) -> Modes:
		return self._mode

	@property
	def DefaultExpression(self) -> Expression:
		return self._defaultExpression


@export
class ParameterConstantInterfaceItem(ParameterInterfaceItem):
	pass


@export
class ParameterVariableInterfaceItem(ParameterInterfaceItem):
	_subType:           SubType
	_mode:              Modes
	_defaultExpression: Expression

	def __init__(self):
		super().__init__()

	@property
	def SubType(self):
		return self._subType

	@property
	def Mode(self):
		return self._mode

	@property
	def DefaultExpression(self):
		return self._defaultExpression


@export
class ParameterSignalInterfaceItem(ParameterInterfaceItem):
	pass


@export
class ParameterFileInterfaceItem(ParameterInterfaceItem):
	pass

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


@export
class LibraryReference(ModelEntity):
	def __init__(self):
		super().__init__()
		self._library = None

	@property
	def Library(self):
		return self._library


@export
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


@export
class PrimaryUnit(ModelEntity, NamedEntity):
	def __init__(self, name: str):
		super().__init__()
		NamedEntity.__init__(self, name)


@export
class SecondaryUnit(ModelEntity, NamedEntity):
	def __init__(self, name: str):
		super().__init__()
		NamedEntity.__init__(self, name)


@export
class Context(PrimaryUnit):
	_uses: List[Use]

	def __init__(self, name):
		super().__init__(name)

		self._uses = []

	@property
	def Uses(self) -> List[Use]:
		return self._uses


@export
class Entity(PrimaryUnit):
	_libraryReferences: List[LibraryReference]
	_uses:              List[Use]
	_genericItems:      List[GenericInterfaceItem]
	_portItems:         List[PortInterfaceItem]
	_declaredItems:     List   # FIXME: define liste element type e.g. via Union
	_bodyItems:         List   # FIXME: define liste element type e.g. via Union

	def __init__(self, name):
		super().__init__(name)

	@property
	def LibraryReferences(self) -> List[LibraryReference]:
		return self._libraryReferences

	@property
	def Uses(self) -> List[Use]:
		return self._uses

	@property
	def GenericItems(self) -> List[GenericInterfaceItem]:
		return self._genericItems

	@property
	def PortItems(self) -> List[PortInterfaceItem]:
		return self._portItems

	@property
	def DeclaredItems(self) -> List:   # FIXME: define liste element type e.g. via Union
		return self._declaredItems

	@property
	def BodyItems(self) -> List:    # FIXME: define liste element type e.g. via Union
		return self._bodyItems


@export
class Architecture(SecondaryUnit):
	_entity:            Entity
	_libraryReferences: List[LibraryReference]
	_uses:              List[Use]
	_declaredItems:     List   # FIXME: define liste element type e.g. via Union
	_bodyItems:         List   # FIXME: define liste element type e.g. via Union

	def __init__(self, name):
		super().__init__(name)

		self._libraryReferences = []
		self._uses =              []
		self._declaredItems =     []
		self._bodyItems =         []

	@property
	def Entity(self) -> Entity:
		return self._entity

	@property
	def LibraryReferences(self) -> List[LibraryReference]:
		return self._libraryReferences

	@property
	def Uses(self) -> List[Use]:
		return self._uses

	@property
	def DeclaredItems(self) -> List:   # FIXME: define liste element type e.g. via Union
		return self._declaredItems

	@property
	def BodyItems(self) -> List:   # FIXME: define liste element type e.g. via Union
		return self._bodyItems


@export
class AssociationItem(ModelEntity):
	_formal: str    # FIXME: defined type
	_actual: str    # FIXME: defined type

	def __init__(self):
		super().__init__()

	@property
	def Formal(self):    # FIXME: defined return type
		return self._formal

	@property
	def Actual(self):    # FIXME: defined return type
		return self._actual


@export
class GenericAssociationItem(InterfaceItem):
	pass

@export
class PortAssociationItem(InterfaceItem):
	pass

@export
class ParameterAssociationItem(InterfaceItem):
	pass

@export
class Configuration(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()

		raise NotImplementedError()


@export
class Instantiation(NamedEntity):
	def __init__(self):
		super().__init__()
		self._packageReference =    None
		self._genericAssociations = []


@export
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


@export
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


@export
class PackageInstantiation(PrimaryUnit, Instantiation):
	def __init__(self):
		super().__init__()
		Instantiation.__init__(self)
		self._packageReferences = None


@export
class Object(ModelEntity, NamedEntity):
	def __init__(self):
		super().__init__()
		NamedEntity.__init__(self)
		self._subType = None

	@property
	def SubType(self):
		return self._subType


@export
class BaseConstant(Object):
	pass

@export
class DeferredConstant(BaseConstant):
	def __init__(self):
		super().__init__()
		self._constantReference = None

	@property
	def ConstantReference(self):
		return self._constantReference


@export
class Constant(BaseConstant):
	def __init__(self):
		super().__init__()
		self._defaultExpression = None

	@property
	def DefaultExpression(self):
		return self._defaultExpression


@export
class Variable(Object):
	def __init__(self):
		super().__init__()
		self._defaultExpression = None

	@property
	def DefaultExpression(self):
		return self._defaultExpression


@export
class Signal(Object):
	def __init__(self):
		super().__init__()
		self._defaultExpression = None

	@property
	def DefaultExpression(self):
		return self._defaultExpression


@export
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


@export
class Procedure(SubProgramm):
	pass

@export
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


@export
class SubprogramInstantiation(ModelEntity, Instantiation):
	def __init__(self):
		super().__init__()
		Instantiation.__init__(self)
		self._subprogramReference = None

@export
class ProcedureInstantiation(SubprogramInstantiation):
	pass

@export
class FunctionInstantiation(SubprogramInstantiation):
	pass

@export
class Method:
	def __init__(self):
		super().__init__()
		self._protectedType = None


@export
class ProcedureMethod(Procedure, Method):
	def __init__(self):
		super().__init__()
		Method.__init__(self)


@export
class FunctionMethod(Function, Method):
	def __init__(self):
		super().__init__()
		Method.__init__(self)


@export
class Statement(ModelEntity, LabledEntity):
	def __init__(self):
		super().__init__()
		LabledEntity.__init__(self)


@export
class ConcurrentStatement(Statement):
	pass

@export
class SequentialStatement(Statement):
	pass

@export
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


@export
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


@export
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


@export
class IfGenerateStatement(GenerateStatement):
	def __init__(self):
		super().__init__()
		self._ifBranch =      None
		self._elsifBranches = []
		self._elseBranch =    None


@export
class BaseConditional:
	def __init__(self):
		super().__init__()
		self._condition = None

	@property
	def Condition(self):
		return self._condition


@export
class BaseBranch:
	pass

@export
class BaseConditionalBranch(BaseBranch, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)


@export
class BaseIfBranch(BaseConditionalBranch):
	pass

@export
class BaseElsifBranch(BaseConditionalBranch):
	pass

@export
class BaseElseBranch(BaseBranch):
	pass

@export
class GenerateBranch(ModelEntity):
	pass

@export
class IfGenerateBranch(GenerateBranch, BaseIfBranch):
	def __init__(self):
		super().__init__()
		BaseIfBranch.__init__(self)


@export
class ElsifGenerateBranch(GenerateBranch, BaseElsifBranch):
	def __init__(self):
		super().__init__()
		BaseElsifBranch.__init__(self)


@export
class ElseGenerateBranch(GenerateBranch, BaseElseBranch):
	def __init__(self):
		super().__init__()
		BaseElseBranch.__init__(self)


@export
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

@export
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


@export
class SignalAssignment(Assignment):
	pass

@export
class VariableAssignment(Assignment):
	pass

@export
class ConcurrentSignalAssignment(ConcurrentStatement, SignalAssignment):
	def __init__(self):
		super().__init__()
		SignalAssignment.__init__(self)


@export
class SequentialSignalAssignment(SequentialStatement, SignalAssignment):
	def __init__(self):
		super().__init__()
		SignalAssignment.__init__(self)


@export
class SequentialVariableAssignment(SequentialStatement, VariableAssignment):
	def __init__(self):
		super().__init__()
		VariableAssignment.__init__(self)



@export
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


@export
class AssertStatement(ReportStatement):
	def __init__(self):
		super().__init__()
		self._condition = None

	@property
	def Condition(self):
		return self._condition


@export
class ConcurrentAssertStatement(ConcurrentStatement, AssertStatement):
	def __init__(self):
		super().__init__()
		AssertStatement.__init__(self)


@export
class SequentialReportStatement(SequentialStatement, ReportStatement):
	def __init__(self):
		super().__init__()
		ReportStatement.__init__(self)


@export
class SequentialAssertStatement(SequentialStatement, AssertStatement):
	def __init__(self):
		super().__init__()
		AssertStatement.__init__(self)


@export
class CompoundStatement(SequentialStatement):
	def __init__(self):
		super().__init__()
		self._bodyItems = []

	@property
	def BodyItems(self):
		return self._bodyItems


@export
class IfStatement(CompoundStatement):
	def __init__(self):
		super().__init__()
		self._ifBranch =      None
		self._elsifBranches = []
		self._elseBranch =    None


@export
class Branch(ModelEntity):
	pass

@export
class IfBranch(Branch, BaseIfBranch):
	def __init__(self):
		super().__init__()
		BaseIfBranch.__init__(self)


@export
class ElsifBranch(Branch, BaseElsifBranch):
	def __init__(self):
		super().__init__()
		BaseElsifBranch.__init__(self)


@export
class ElseBranch(Branch, BaseElseBranch):
	def __init__(self):
		super().__init__()
		BaseElseBranch.__init__(self)


@export
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


@export
class WhileLoopStatement(CompoundStatement, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)


@export
class LoopControlStatement(ModelEntity, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)
		self._loopReference = None

	@property
	def LoopReference(self):
		return self._loopReference


@export
class NextStatement(LoopControlStatement):
	pass

@export
class ExitStatement(LoopControlStatement):
	pass

@export
class ReturnStatement(SequentialStatement):
	pass
