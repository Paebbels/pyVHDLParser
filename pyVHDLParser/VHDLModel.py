# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python module:      An abstract VHDL language model
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
from enum               import Enum
from pathlib            import Path
from typing             import Any, List

from pydecor.decorators import export

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
	_path:           Path                   #: path to the document. ``None`` if virtual document.
	_contexts:       List['Context']        #: List of all contexts defined in a document.
	_configurations: List['Configuration']  #: List of all configurations defined in a document.
	_entities:       List['Entity']         #: List of all entities defined in a document.
	_architectures:  List['Architecture']   #: List of all architectures defined in a document.
	_packages:       List['Package']        #: List of all packages defined in a document.
	_packageBodies:  List['PackageBody']    #: List of all package bodies defined in a document.

	def __init__(self, path: Path):
		super().__init__()

		self._path =            path
		self._contexts =        []
		self._configurations =  []
		self._entities =        []
		self._architectures =   []
		self._packages =        []
		self._packageBodies =   []

	@property
	def Path(self) -> Path:
		return self._path

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
class Direction(Enum):
	To =      0
	DownTo =  1

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
	def __init__(self, name: str):
		super().__init__()
		NamedEntity.__init__(self, name)


@export
class Type(BaseType):
	pass


@export
class SubType(BaseType):
	_type: Type

	def __init__(self, name: str):
		super().__init__(name)

	@property
	def Type(self) -> Type:
		return self._type


@export
class ScalarType(BaseType):
	pass


@export
class NumericType:
	pass


@export
class DiscreteType:
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
class EnumeratedType(ScalarType, DiscreteType):
	_elements: List

	def __init__(self, name: str):
		super().__init__(name)

		self._elements = []

	@property
	def Elements(self) -> List:
		return self._elements


@export
class IntegerType(ScalarType, NumericType, DiscreteType):
	_leftBound:  'Expression'
	_rightBound: 'Expression'

	def __init__(self, name: str):
		super().__init__(name)


@export
class RealType(ScalarType, NumericType):
	_leftBound:  'Expression'
	_rightBound: 'Expression'

	def __init__(self, name: str):
		super().__init__(name)

# TODO: PhysicalType

@export
class ArrayType(CompositeType):
	_dimensions:  List['Range']
	_elementType: SubType

	def __init__(self, name: str):
		super().__init__(name)

		self._dimensions =  []

	@property
	def Dimensions(self):
		return self._dimensions

	@property
	def ElementType(self):
		return self._elementType


@export
class RecordTypeMember(ModelEntity):
	def __init__(self, name: str):
		super().__init__()

		self._name =        name
		self._subType =     None

	@property
	def Name(self):
		return self._name


@export
class RecordType(BaseType):
	_members: List[RecordTypeMember]

	def __init__(self, name: str):
		super().__init__(name)

		self._members =     []

	@property
	def Members(self):
		return self._members


@export
class Expression:
	pass


@export
class Literal:
	pass


@export
class IntegerLiteral:
	_value: int

	def __init__(self, value: int):
		self._value = value

	@property
	def Value(self):
		return self._value


@export
class FloatingPointLiteral:
	_value: float

	def __init__(self, value: float):
		self._value = value

	@property
	def Value(self):
		return self._value

# CharacterLiteral
# StringLiteral
# BitStringLiteral
# EnumerationLiteral
# PhysicalLiteral

@export
class UnaryExpression(Expression):
	_operand:  Expression

	def __init__(self):
		pass

	@property
	def Operand(self):
		return self._operand

@export
class FunctionCall(Expression):
	pass

@export
class QualifiedExpression(Expression):
	pass

@export
class BinaryExpression(Expression):
	_leftOperand:  Expression
	_rightOperand: Expression

	def __init__(self):
		pass

	@property
	def LeftOperand(self):
		return self._leftOperand

	@property
	def RightOperand(self):
		return self._rightOperand

# AddingExpression
# MultiplyingExpression
# LogicalExpression
# ShiftExpression

@export
class Range:
	_leftBound:  Any
	_rightBound: Any
	_direction:  Direction

	def __init__(self):
		pass


@export
class InterfaceItem(ModelEntity):
	_name: str
	_mode: Modes

	def __init__(self, name: str, mode: Modes):
		super().__init__()

		self._name = name
		self._mode = mode

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Mode(self) -> Modes:
		return self._mode


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
	_defaultExpression: Expression

	def __init__(self, name: str, mode: Modes):
		super().__init__(name, mode)

	@property
	def SubType(self) -> SubType:
		return self._subType

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

	def __init__(self, name: str):
		super().__init__(name)

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
	_library: Library

	def __init__(self):
		super().__init__()
		self._library = None

	@property
	def Library(self) -> Library:
		return self._library


@export
class Use(ModelEntity):
	_library: Library
	_package: 'Package'
	_item:    str

	def __init__(self):
		super().__init__()

	@property
	def Library(self) -> Library:
		return self._library

	@property
	def Package(self) -> 'Package':
		return self._package

	@property
	def Item(self) -> str:
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
	_bodyItems:         List['ConcurrentStatement']

	def __init__(self, name: str):
		super().__init__(name)

		self._libraryReferences = []
		self._uses              = []
		self._genericItems      = []
		self._portItems         = []
		self._declaredItems     = []
		self._bodyItems         = []

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
	def BodyItems(self) -> List['ConcurrentStatement']:
		return self._bodyItems


@export
class Architecture(SecondaryUnit):
	_entity:            Entity
	_libraryReferences: List[Library]
	_uses:              List[Use]
	_declaredItems:     List   # FIXME: define liste element type e.g. via Union
	_bodyItems:         List['ConcurrentStatement']

	def __init__(self, name: str):
		super().__init__(name)

		self._libraryReferences = []
		self._uses =              []
		self._declaredItems =     []
		self._bodyItems =         []

	@property
	def Entity(self) -> Entity:
		return self._entity

	@property
	def LibraryReferences(self) -> List[Library]:
		return self._libraryReferences

	@property
	def Uses(self) -> List[Use]:
		return self._uses

	@property
	def DeclaredItems(self) -> List:   # FIXME: define liste element type e.g. via Union
		return self._declaredItems

	@property
	def BodyItems(self) -> List['ConcurrentStatement']:
		return self._bodyItems


@export
class AssociationItem(ModelEntity):
	_formal: str    # FIXME: defined type
	_actual: Expression

	def __init__(self):
		super().__init__()

	@property
	def Formal(self):    # FIXME: defined return type
		return self._formal

	@property
	def Actual(self) -> Expression:
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
	def __init__(self, name: str):
		super().__init__()
		NamedEntity.__init__(self, name)



@export
class Instantiation:
	pass


@export
class Package(PrimaryUnit):
	_libraryReferences: List[Library]
	_uses:              List[Use]
	_genericItems:      List[GenericInterfaceItem]
	_declaredItems:     List

	def __init__(self, name: str):
		super().__init__(name)

		self._libraryReferences = []
		self._uses =              []
		self._genericItems =      []
		self._declaredItems =     []

	@property
	def LibraryReferences(self) -> List[Library]:
		return self._libraryReferences

	@property
	def Uses(self) -> List[Use]:
		return self._uses

	@property
	def GenericItems(self) -> List[GenericInterfaceItem]:
		return self._genericItems

	@property
	def DeclaredItems(self) -> List:
		return self._declaredItems


@export
class PackageBody(SecondaryUnit):
	_package:           Package
	_libraryReferences: List[Library]
	_uses:              List[Use]
	_declaredItems:     List

	def __init__(self, name: str):
		super().__init__(name)

		self._libraryReferences = []
		self._uses =              []
		self._declaredItems =     []

	@property
	def Package(self) -> Package:
		return self._package

	@property
	def LibraryReferences(self) -> List[Library]:
		return self._libraryReferences

	@property
	def Uses(self) -> List[Use]:
		return self._uses

	@property
	def DeclaredItems(self) -> List:
		return self._declaredItems


@export
class PackageInstantiation(PrimaryUnit, Instantiation):
	_packageReference:    Package
	_genericAssociations: List[GenericAssociationItem]

	def __init__(self, name: str):
		super().__init__(name)
		Instantiation.__init__(self)

		self._genericAssociations = []

	@property
	def PackageReference(self) -> Package:
		return self._packageReference

	@property
	def GenericAssociations(self) -> List[GenericAssociationItem]:
		return self._genericAssociations


@export
class Object(ModelEntity, NamedEntity):
	_subType: SubType

	def __init__(self, name: str):
		super().__init__()
		NamedEntity.__init__(self, name)

	@property
	def SubType(self) -> SubType:
		return self._subType


@export
class BaseConstant(Object):
	pass


@export
class Constant(BaseConstant):
	_defaultExpression: Expression

	def __init__(self, name: str):
		super().__init__(name)

	@property
	def DefaultExpression(self) -> Expression:
		return self._defaultExpression


@export
class DeferredConstant(BaseConstant):
	_constantReference: Constant

	def __init__(self, name: str):
		super().__init__(name)

	@property
	def ConstantReference(self) -> Constant:
		return self._constantReference


@export
class Variable(Object):
	_defaultExpression: Expression

	def __init__(self, name: str):
		super().__init__(name)

	@property
	def DefaultExpression(self) -> Expression:
		return self._defaultExpression


@export
class Signal(Object):
	_defaultExpression: Expression

	def __init__(self, name: str):
		super().__init__(name)

	@property
	def DefaultExpression(self) -> Expression:
		return self._defaultExpression


@export
class SubProgramm(ModelEntity, NamedEntity):
	_genericItems:   List[GenericInterfaceItem]
	_parameterItems: List[ParameterInterfaceItem]
	_declaredItems:  List
	_bodyItems:      List['SequentialStatement']

	def __init__(self, name: str):
		super().__init__()
		NamedEntity.__init__(self, name)

		self._genericItems =    []
		self._parameterItems =  []
		self._declaredItems =   []
		self._bodyItems =       []

	@property
	def GenericItems(self) -> List[GenericInterfaceItem]:
		return self._genericItems

	@property
	def ParameterItems(self) -> List[ParameterInterfaceItem]:
		return self._parameterItems

	@property
	def DeclaredItems(self) -> List:
		return self._declaredItems

	@property
	def BodyItems(self) -> List['SequentialStatement']:
		return self._bodyItems


@export
class Procedure(SubProgramm):
	pass


@export
class Function(SubProgramm):
	_returnType: SubType
	_isPure:     bool    = True

	def __init__(self, name: str):
		super().__init__(name)

	@property
	def ReturnType(self) -> SubType:
		return self._returnType

	@property
	def IsPure(self) -> bool:
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
		self._protectedType = None


@export
class ProcedureMethod(Procedure, Method):
	def __init__(self, name: str):
		super().__init__(name)
		Method.__init__(self)


@export
class FunctionMethod(Function, Method):
	def __init__(self, name: str):
		super().__init__(name)
		Method.__init__(self)


@export
class Statement(ModelEntity, LabledEntity):
	def __init__(self, label: str = None):
		super().__init__()
		LabledEntity.__init__(self, label)


@export
class ConcurrentStatement(Statement):
	pass


@export
class SequentialStatement(Statement):
	pass


@export
class ProcessStatement(ConcurrentStatement):
	_parameterItems: List[Signal]
	_declaredItems:  List # TODO: create a union for (concurrent / sequential) DeclaredItems
	_bodyItems:      List[SequentialStatement]

	def __init__(self, label: str = None):
		super().__init__(label=label)

		self._parameterItems =  []
		self._declaredItems =   []
		self._bodyItems =       []

	@property
	def ParameterItems(self) -> List[Signal]:
		return self._parameterItems

	@property
	def DeclaredItems(self) -> List:
		return self._declaredItems

	@property
	def BodyItems(self) -> List[SequentialStatement]:
		return self._bodyItems


# TODO: could be unified with ProcessStatement if 'List[ConcurrentStatement]' becomes parametric to T
class BlockStatement:
	_declaredItems: List # TODO: create a union for (concurrent / sequential) DeclaredItems
	_bodyItems:     List[ConcurrentStatement]

	def __init__(self):
		self._declaredItems = []
		self._bodyItems =     []

	@property
	def DeclaredItems(self) -> List:
		return self._declaredItems

	@property
	def BodyItems(self) -> List[ConcurrentStatement]:
		return self._bodyItems


@export
class ConcurrentBlockStatement(ConcurrentStatement, BlockStatement):
	_portItems:     List[PortInterfaceItem]

	def __init__(self, label: str = None):
		super().__init__(label=label)
		BlockStatement.__init__(self)

		self._portItems =     []

	@property
	def PortItems(self) -> List[PortInterfaceItem]:
		return self._portItems


@export
class BaseConditional:
	_condition: Expression

	def __init__(self):
		super().__init__()

	@property
	def Condition(self) -> Expression:
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
class GenerateStatement(ConcurrentStatement):
	def __init__(self, label: str = None):
		super().__init__(label=label)

		self._declaredItems = []
		self._bodyItems = []

	@property
	def DeclaredItems(self):
		return self._declaredItems

	@property
	def BodyItems(self):
		return self._bodyItems


@export
class IfGenerateStatement(GenerateStatement):
	_ifBranch: IfGenerateBranch
	_elsifBranch: List['ElsifGenerateBranch']
	_elseBranch: ElseGenerateBranch

	def __init__(self, label: str = None):
		super().__init__(label=label)

		self._elsifBranches = []


@export
class ForGenerateStatement(GenerateStatement):
	_loopIndex: Constant
	_range:     Range

	def __init__(self, label: str = None):
		super().__init__(label=label)

	@property
	def LoopIndex(self) -> Constant:
		return self._loopIndex

	@property
	def Range(self) -> Range:
		return self._range

# TODO: CaseGenerateStatement
# class CaseGenerateStatement(GenerateStatement):
# 	def __init__(self):
# 		super().__init__()
# 		self._expression =      None
# 		self._cases =           []

@export
class Assignment:
	_target:     Object
	_expression: Expression

	def __init__(self):
		super().__init__()

	@property
	def Target(self) -> Object:
		return self._target

	@property
	def Expression(self) -> Expression:
		return self._expression


@export
class SignalAssignment(Assignment):
	pass


@export
class VariableAssignment(Assignment):
	pass


@export
class ConcurrentSignalAssignment(ConcurrentStatement, SignalAssignment):
	def __init__(self, label: str = None):
		super().__init__(label=label)

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
	_message:  Expression
	_severity: Expression

	def __init__(self):
		super().__init__()

	@property
	def Message(self) -> Expression:
		return self._message

	@property
	def Severity(self) -> Expression:
		return self._severity


@export
class AssertStatement(ReportStatement):
	_condition: Expression

	def __init__(self):
		super().__init__()

	@property
	def Condition(self) -> Expression:
		return self._condition


@export
class ConcurrentAssertStatement(ConcurrentStatement, AssertStatement):
	def __init__(self, label: str = None):
		super().__init__(label=label)
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
class CompoundStatement(SequentialStatement):
	_bodyItems: List[SequentialStatement]

	def __init__(self):
		super().__init__()

		self._bodyItems = []

	@property
	def BodyItems(self) -> List[SequentialStatement]:
		return self._bodyItems


@export
class IfStatement(CompoundStatement):
	_ifBranch: IfBranch
	_elsifBranches: List['ElsifBranch']
	_elseBranch: ElseBranch

	def __init__(self):
		super().__init__()

		self._elsifBranches = []

	@property
	def IfBranch(self) -> IfBranch:
		return self._ifBranch

	@property
	def ElsIfBranches(self) -> List['ElsifBranch']:
		return self._elsifBranches

	@property
	def ElseBranch(self) -> ElseBranch:
		return self._elseBranch


@export
class LoopStatement(CompoundStatement):
	pass


@export
class ForLoopStatement(LoopStatement):
	_loopIndex: Constant
	_range:     Range

	def __init__(self):
		super().__init__()

	@property
	def LoopIndex(self) -> Constant:
		return self._loopIndex

	@property
	def Range(self) -> Range:
		return self._range


@export
class WhileLoopStatement(LoopStatement, BaseConditional):
	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)


@export
class LoopControlStatement(ModelEntity, BaseConditional):
	_loopReference: LoopStatement

	def __init__(self):
		super().__init__()
		BaseConditional.__init__(self)

	@property
	def LoopReference(self) -> LoopStatement:
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
