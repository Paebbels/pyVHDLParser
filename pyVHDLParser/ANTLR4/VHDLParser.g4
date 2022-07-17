parser grammar VHDLParser;

options {
	tokenVocab = VHDLLexer;
}

// TODO: Context
// TODO: Protzected Type
// TODO: PSL
// TODO: VHDL-2019
// TODO: VHDL-AMS

rule_AbsolutePathname
	: TOK_DOT rule_PartialPathName
	;

// rule_AbstractLiteral
// handled by lexer

rule_AccessTypeDefinition
  : KW_ACCESS subtypeIndication=rule_SubtypeIndication
  ;

/*
across_aspect
  : identifier_list ( tolerance_aspect )? ( TOK_VAR_ASSIGN expression )? ACROSS
  ;
*/

rule_ActualDesignator
  : inertial=KW_INERTIAL? expression=rule_Expression
  | name=rule_Name
  | subtypeIndication=rule_SubtypeIndication
  | open=KW_OPEN
  ;

rule_ActualParameterPart
  : associationList=rule_AssociationList
  ;

rule_ActualPart
  : conversion=rule_Name TOK_LP actualDesignator=rule_ActualDesignator TOK_RP
  | actualDesignator=rule_ActualDesignator
  ;

// TODO: combine into expression
rule_AddingOperator
  : operator=OP_PLUS
  | operator=OP_MINUS
  | operator=OP_CONCAT
  ;

rule_Aggregate
  : TOK_LP elementAssociation+=rule_ElementAssociation ( TOK_COMMA elementAssociation+=rule_ElementAssociation )* TOK_RP
  ;

rule_AliasDeclaration
  : KW_ALIAS aliasDesignator=rule_AliasDesignator ( TOK_COLON aliasIndication=rule_AliasIndication )?
      KW_IS aliasTarget=rule_Name ( sig=rule_Signature )?
    TOK_SEMICOL
  ;

rule_AliasDesignator
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  | LIT_STRING
  ;

rule_AliasIndication
  : /* subnature_indication
  | */ subtypeIndication=rule_SubtypeIndication
  ;

rule_Allocator
  : KW_NEW (
      rule_QualifiedExpression
    | subtypeIndication=rule_SubtypeIndication
    )
  ;

rule_ArchitectureBody
  : KW_ARCHITECTURE LIT_IDENTIFIER KW_OF LIT_IDENTIFIER KW_IS
      rule_ArchitectureDeclarativePart
    KW_BEGIN
      rule_ArchitectureStatementPart
    KW_END KW_ARCHITECTURE? LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_ArchitectureDeclarativePart
  : rule_BlockDeclarativeItem*
  ;

rule_ArchitectureStatement
  : rule_BlockStatement
  | rule_ProcessStatement
  | rule_PostponedProcessStatement
  | rule_LabelWithColon? rule_ConcurrentProcedureCallStatement
  | rule_LabelWithColon? rule_ConcurrentAssertionStatement
  | rule_LabelWithColon? KW_POSTPONED? rule_ConcurrentSignalAssignmentStatement
  | rule_ComponentInstantiationStatement
  | rule_GenerateStatement
//  | concurrent_break_statement
//  | simultaneous_statement
  ;

// TODO: simplyfy?
rule_ArchitectureStatementPart
  : rule_ArchitectureStatement*
  ;

/*
array_nature_definition
  : unconstrained_nature_definition
  | constrained_nature_definition
  ;
*/

rule_ArrayTypeDefinition
  : rule_UnconstrainedArrayDefinition
  | rule_ConstrainedArrayDefinition
  ;

rule_Assertion
  : KW_ASSERT rule_Condition
    ( KW_REPORT rule_Expression )?
    ( KW_SEVERITY rule_Expression )?
  ;

rule_AssertionStatement
  : rule_LabelWithColon? rule_Assertion TOK_SEMICOL
  ;

rule_AssociationElement
  : ( rule_FormalPart TOK_RARROW )? rule_ActualPart
  ;

rule_AssociationList
  : rule_AssociationElement ( TOK_COMMA rule_AssociationElement )*
  ;

// TODO: why label_colon and why just name?
rule_AttributeDeclaration
  : KW_ATTRIBUTE rule_LabelWithColon rule_Name TOK_SEMICOL
  ;

/*
// Need to add several tokens here, for they are both, VHDLAMS reserved words
// and attribute names.
// (25.2.2004, e.f.)
attribute_designator
  : LIT_IDENTIFIER
  | RANGE
  | REVERSE_RANGE
  | ACROSS
  | THROUGH
  | REFERENCE
  | TOLERANCE
  ;
*/

rule_AttributeDesignator
  : LIT_IDENTIFIER
  ;

rule_AttributeSpecification
  : KW_ATTRIBUTE rule_AttributeDesignator
      KW_OF rule_EntitySpecification
      KW_IS rule_Expression
    TOK_SEMICOL
  ;

rule_BaseUnitDeclaration
  : LIT_IDENTIFIER TOK_SEMICOL
  ;

rule_BindingIndication
  : ( KW_USE rule_EntityAspect )?
      rule_GenericMapAspect?
      rule_PortMapAspect?
  ;

rule_BlockConfiguration
  : KW_FOR rule_BlockSpecification
      rule_UseClause*
      rule_ConfigurationItem*
    KW_END KW_FOR TOK_SEMICOL
  ;

rule_BlockDeclarativeItem
  : rule_SubprogramDeclaration
  | rule_SubprogramBody
  | rule_TypeDeclaration
  | rule_SubtypeDeclaration
  | rule_ConstantDeclaration
  | rule_SignalDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
  | rule_AliasDeclaration
  | rule_ComponentDeclaration
  | rule_AttributeDeclaration
  | rule_AttributeSpecification
  | rule_ConfigurationSpecification
  | rule_DisconnectionSpecification
//  | step_limit_specification
  | rule_UseClause
//  | group_template_declaration
//  | group_declaration
//  | nature_declaration
//  | subnature_declaration
//  | quantity_declaration
//  | terminal_declaration
  ;

rule_BlockDeclarativePart
  : rule_BlockDeclarativeItem*
  ;

rule_BlockHeader
  : ( rule_GenericClause ( rule_GenericMapAspect TOK_SEMICOL )? )?
    ( rule_PortClause    ( rule_PortMapAspect    TOK_SEMICOL )? )?
  ;

rule_BlockSpecification
  : LIT_IDENTIFIER ( TOK_LP rule_IndexSpecification TOK_RP )?
  | rule_Name
  ;

rule_BlockStatement
  : rule_LabelWithColon KW_BLOCK ( TOK_LP rule_Expression TOK_RP )? KW_IS?
      rule_BlockHeader
      rule_BlockDeclarativePart
    KW_BEGIN
      rule_BlockStatementPart
    KW_END KW_BLOCK LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_BlockStatementPart
  : rule_ArchitectureStatement*
  ;

/*
branch_quantity_declaration
  : QUANTITY ( across_aspect )?
    ( through_aspect )? terminal_aspect TOK_SEMICOL
  ;

break_element
  : ( break_selector_clause )? name ARROW expression
  ;

break_list
  : break_element ( TOK_COMMA break_element )*
  ;

break_selector_clause
  : FOR name USE
  ;

break_statement
  : ( label_colon )? BREAK ( break_list )? ( WHEN condition )? TOK_SEMICOL
  ;
*/

rule_CaseStatement
  : rule_LabelWithColon? KW_CASE rule_Expression KW_IS
      rule_CaseStatementAlternative+
    KW_END KW_CASE LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_CaseStatementAlternative
  : KW_WHEN rule_Choices TOK_RARROW
  		rule_SequenceOfStatements
  ;

rule_Choice
  : LIT_IDENTIFIER
  | rule_DiscreteRange
  | rule_SimpleExpression
  | KW_OTHERS
  ;

rule_Choices
  : choices+=rule_Choice ( TOK_BAR choices+=rule_Choice )*
  ;

rule_ComponentConfiguration
  : KW_FOR rule_ComponentSpecification
      ( rule_BindingIndication TOK_SEMICOL )?
      rule_BlockConfiguration?
    KW_END KW_FOR TOK_SEMICOL
  ;

rule_ComponentDeclaration
  : KW_COMPONENT LIT_IDENTIFIER KW_IS?
      rule_GenericClause?
      rule_PortClause?
    KW_END KW_COMPONENT LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_ComponentInstantiationStatement
  : rule_LabelWithColon rule_InstantiatedUnit
      rule_GenericMapAspect?
      rule_PortMapAspect?
    TOK_SEMICOL
  ;

rule_ComponentSpecification
  : rule_InstantiationList TOK_COLON rule_Name
  ;

/*
composite_nature_definition
  : array_nature_definition
  | record_nature_definition
  ;
*/

rule_CompositeTypeDefinition
  : rule_ArrayTypeDefinition
  | rule_RecordTypeDefinition
  ;

rule_ConcurrentAssertionStatement
  : rule_LabelWithColon? KW_POSTPONED? rule_Assertion TOK_SEMICOL
  ;

/*
concurrent_break_statement
  : ( label_colon )? BREAK ( break_list )? ( sensitivity_clause )?
    ( WHEN condition )? TOK_SEMICOL
  ;
*/

rule_ConcurrentProcedureCallStatement
  : rule_LabelWithColon? KW_POSTPONED? rule_ProcedureCall TOK_SEMICOL
  ;

rule_ConcurrentSignalAssignmentStatement
  : rule_LabelWithColon? KW_POSTPONED? (
      rule_ConditionalSignalAssignment
    | rule_SelectedSignalAssignment
    )
  ;

// TODO: combine into expression
rule_Condition
  : rule_Expression
  ;

rule_ConditionClause
  : KW_UNTIL rule_Condition
  ;

rule_ConditionalSignalAssignment
  : rule_Target TOK_SIG_ASSIGN rule_Opts rule_ConditionalWaveforms TOK_SEMICOL
  ;

rule_ConditionalWaveforms
  : rule_Waveform ( KW_WHEN rule_Condition ( KW_ELSE rule_ConditionalWaveforms )? )?
  ;

rule_ConfigurationDeclaration
  : KW_CONFIGURATION LIT_IDENTIFIER KW_OF rule_Name KW_IS
      rule_ConfigurationDeclarativePart
      rule_BlockConfiguration
    KW_END KW_CONFIGURATION? LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_ConfigurationDeclarativeItem
  : rule_UseClause
  | rule_AttributeSpecification
//  | group_declaration
  ;

rule_ConfigurationDeclarativePart
  : rule_ConfigurationDeclarativeItem*
  ;

rule_ConfigurationItem
  : rule_BlockConfiguration
  | rule_ComponentConfiguration
  ;

rule_ConfigurationSpecification
  : KW_FOR rule_ComponentSpecification rule_BindingIndication TOK_SEMICOL
  ;

rule_ConstantDeclaration
  : KW_CONSTANT rule_IdentifierList TOK_COLON subtypeIndication=rule_SubtypeIndication
    ( TOK_VAR_ASSIGN rule_Expression )? TOK_SEMICOL
  ;

rule_ConstrainedArrayDefinition
  : KW_ARRAY rule_IndexConstraint KW_OF subtypeIndication=rule_SubtypeIndication
  ;

/*
constrained_nature_definition
  : KW_ARRAY index_constraint KW_OF subnature_indication
  ;
*/

rule_Constraint
  : rule_RangeConstraint
  | rule_IndexConstraint
  ;

rule_ContextClause
  : rule_ContextItem*
  ;

rule_ContextItem
  : rule_LibraryClause
  | rule_UseClause
  ;

rule_DelayMechanism
  : KW_TRANSPORT
  | ( KW_REJECT rule_Expression )? KW_INERTIAL
  ;

rule_DesignFile
  : designUnits+=rule_DesignUnit*
    EOF
  ;

rule_DesignUnit
  : contextClause=rule_ContextClause
    libraryUnit=rule_LibraryUnit
  ;

rule_Designator
  : LIT_IDENTIFIER
  | LIT_STRING     // TODO: should be limited to operator names
  ;

rule_Direction
  : KW_TO
  | KW_DOWNTO
  ;

rule_DisconnectionSpecification
  : KW_DISCONNECT rule_GuardedSignalSpecification
      KW_AFTER rule_Expression
    TOK_SEMICOL
  ;

rule_DiscreteRange
  : rule_RangeDeclaration
  | subtypeIndication=rule_SubtypeIndication
  ;

rule_ElementAssociation
  : ( rule_Choices TOK_RARROW )? rule_Expression
  ;

rule_ElementDeclaration
  : rule_IdentifierList TOK_COLON rule_ElementSubtypeDefinition TOK_SEMICOL
  ;

/*
element_subnature_definition
  : subnature_indication
  ;
*/

rule_ElementSubtypeDefinition
  : subtypeIndication=rule_SubtypeIndication
  ;

rule_EntityAspect
  : KW_ENTITY rule_Name ( TOK_LP LIT_IDENTIFIER TOK_RP )?
  | KW_CONFIGURATION rule_Name
  | KW_OPEN
  ;

rule_EntityClass
  : KW_ENTITY
  | KW_ARCHITECTURE
  | KW_CONFIGURATION
  | KW_PROCEDURE
  | KW_FUNCTION
  | KW_PACKAGE
  | KW_TYPE
  | KW_SUBTYPE
  | KW_CONSTANT
  | KW_SIGNAL
  | KW_VARIABLE
  | KW_COMPONENT
  | KW_LABEL
//  | KW_LITERAL    // TODO: ???
  | KW_UNITS
//  | KW_GROUP
  | KW_FILE
//  | NATURE
//  | SUBNATURE
//  | QUANTITY
//  | TERMINAL
  ;

rule_EntityClassEntry
  : rule_EntityClass TOK_BOX?
  ;

rule_EntityClassEntryList
  : rule_EntityClassEntry ( TOK_COMMA rule_EntityClassEntry )*
  ;

rule_EntityDeclaration
  : KW_ENTITY entityName=LIT_IDENTIFIER KW_IS
      genericClause=rule_GenericClause?
    	portClause=rule_PortClause?
      declarativePart=rule_EntityDeclarativePart
    ( KW_BEGIN
      statementPart=rule_EntityStatementPart
    )?
    KW_END KW_ENTITY? entityName2=LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_EntityDeclarativeItem
  : rule_SubprogramDeclaration
  | rule_SubprogramBody
  | rule_TypeDeclaration
  | rule_SubtypeDeclaration
  | rule_ConstantDeclaration
  | rule_SignalDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
  | rule_AliasDeclaration
  | rule_AttributeDeclaration
  | rule_AttributeSpecification
  | rule_DisconnectionSpecification
//  | step_limit_specification
  | rule_UseClause
//  | group_template_declaration
//  | group_declaration
//  | nature_declaration
//  | subnature_declaration
//  | quantity_declaration
//  | terminal_declaration
  ;

rule_EntityDeclarativePart
  : rule_EntityDeclarativeItem*
  ;

rule_EntityDesignator
  : rule_EntityTag rule_Signature?
  ;

// rule_entity_header
// merged into rule_entity_declaration

rule_EntityNameList
  : rule_EntityDesignator ( TOK_COMMA rule_EntityDesignator )*
  | KW_OTHERS
  | KW_ALL
  ;

rule_EntitySpecification
  : rule_EntityNameList TOK_COLON rule_EntityClass
  ;

rule_EntityStatement
  : rule_ConcurrentAssertionStatement
  | rule_ProcessStatement
  | rule_PostponedProcessStatement
  | rule_ConcurrentProcedureCallStatement
  ;

rule_EntityStatementPart
  : rule_EntityStatement*
  ;

rule_EntityTag
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  | LIT_STRING
  ;

rule_EnumerationLiteral
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  ;

rule_EnumerationTypeDefinition
  : TOK_LP rule_EnumerationLiteral ( TOK_COMMA rule_EnumerationLiteral )* TOK_RP
  ;

rule_ExitStatement
  : rule_LabelWithColon? KW_EXIT LIT_IDENTIFIER? ( KW_WHEN rule_Condition )? TOK_SEMICOL
  ;

// TODO: combine into expression
rule_Expression
  : rule_Relation (: rule_LogicalOperator rule_Relation )*
  ;

// TODO: combine into expression
rule_Factor
  : rule_Primary ( : OP_POW rule_Primary )?
  | OP_ABS rule_Primary
  | OP_NOT rule_Primary
  ;

rule_FileDeclaration
  : KW_FILE rule_IdentifierList TOK_COLON subtypeIndication=rule_SubtypeIndication
    rule_FileOpenInformation? TOK_SEMICOL
  ;

rule_FileLogicalName
  : rule_Expression
  ;

rule_FileOpenInformation
  : ( KW_OPEN rule_Expression )? KW_IS rule_FileLogicalName
  ;

rule_FileTypeDefinition
  : KW_FILE KW_OF subtypeIndication=rule_SubtypeIndication
  ;

rule_FormalParameterList
  : rule_InterfaceList
  ;

rule_FormalPart
  : LIT_IDENTIFIER
  | LIT_IDENTIFIER TOK_LP rule_ExplicitRange  TOK_RP
  ;

/*
free_quantity_declaration
  : QUANTITY identifier_list TOK_COLON subtypeIndication=subtype_indication
    ( TOK_VAR_ASSIGN expression )? TOK_SEMICOL
  ;
*/

rule_GenerateStatement
  : rule_LabelWithColon
    rule_GenerationScheme KW_GENERATE
      ( rule_BlockDeclarativeItem*
    KW_BEGIN
    )?
      rule_ArchitectureStatement*
    KW_END KW_GENERATE LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_GenerationScheme
  : KW_FOR rule_ParameterSpecification
  | KW_IF rule_Condition
  ;

rule_GenericClause
  : KW_GENERIC TOK_LP generics=rule_GenericList TOK_RP TOK_SEMICOL
  ;

rule_GenericList
  : constants+=rule_InterfaceConstantDeclaration ( TOK_SEMICOL constants+=rule_InterfaceConstantDeclaration )*
  ;

rule_GenericMapAspect
  : KW_GENERIC KW_MAP TOK_LP
      rule_AssociationList
    TOK_RP
  ;

/*
group_constituent
  : name
  | LIT_CHARACTER
  ;

group_constituent_list
  : group_constituent ( TOK_COMMA group_constituent )*
  ;

group_declaration
  : GROUP label_colon name
    TOK_LP group_constituent_list TOK_RP TOK_SEMICOL
  ;

group_template_declaration
  : GROUP LIT_IDENTIFIER IS TOK_LP entity_class_entry_list TOK_RP TOK_SEMICOL
  ;
*/

rule_GuardedSignalSpecification
  : rule_SignalList TOK_COLON rule_Name
  ;

/*
identifier
  : BASIC_IDENTIFIER
  | EXTENDED_IDENTIFIER
  ;
*/

rule_IdentifierList
  : identifier+=LIT_IDENTIFIER ( TOK_COMMA identifier+=LIT_IDENTIFIER )*
  ;

rule_IfStatement
  : rule_LabelWithColon? KW_IF rule_Condition KW_THEN
      rule_SequenceOfStatements
    ( KW_ELSIF rule_Condition KW_THEN
      rule_SequenceOfStatements
    )*
    ( KW_ELSE
      rule_SequenceOfStatements
    )?
    KW_END KW_IF LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_IndexConstraint
  : TOK_LP rule_DiscreteRange ( TOK_COMMA rule_DiscreteRange )* TOK_RP
  ;

rule_IndexSpecification
  : rule_DiscreteRange
  | rule_Expression
  ;

rule_IndexSubtypeDefinition
  : rule_Name KW_RANGE TOK_BOX
  ;

rule_InstantiatedUnit
  : KW_COMPONENT? rule_Name
  | KW_ENTITY rule_Name ( TOK_LP LIT_IDENTIFIER TOK_RP )?
  | KW_CONFIGURATION rule_Name
  ;

rule_InstantiationList
  : LIT_IDENTIFIER ( TOK_COMMA LIT_IDENTIFIER )*
  | KW_OTHERS
  | KW_ALL
  ;

rule_InterfaceConstantDeclaration
  : KW_CONSTANT? constantNames=rule_IdentifierList TOK_COLON modeName=KW_IN? subtypeIndication=rule_SubtypeIndication
    ( TOK_VAR_ASSIGN defaultValue=rule_Expression )?
  ;

rule_InterfaceDeclaration
  : rule_InterfaceConstantDeclaration
  | rule_InterfaceSignalDeclaration
  | rule_InterfaceVariableDeclaration
  | rule_InterfaceFileDeclaration
//  | interface_terminal_declaration
//  | interface_quantity_declaration
  ;

rule_InterfaceElement
  : rule_InterfaceDeclaration
  ;

rule_InterfaceFileDeclaration
  : KW_FILE rule_IdentifierList TOK_COLON subtypeIndication=rule_SubtypeIndication
  ;

rule_InterfaceSignalList
  : rule_InterfaceSignalDeclaration ( TOK_SEMICOL rule_InterfaceSignalDeclaration )*
  ;

rule_InterfacePortList
  : rule_InterfacePortDeclaration ( TOK_SEMICOL rule_InterfacePortDeclaration )*
  ;

rule_InterfaceList
  : rule_InterfaceElement ( TOK_SEMICOL rule_InterfaceElement )*
  ;

/*
interface_quantity_declaration
  : QUANTITY identifier_list TOK_COLON ( IN | OUT )? subtypeIndication=subtype_indication
    ( TOK_VAR_ASSIGN expression )?
  ;
*/

rule_InterfacePortDeclaration
  : rule_IdentifierList TOK_COLON rule_SignalMode? subtypeIndication=rule_SubtypeIndication
    KW_BUS? ( TOK_VAR_ASSIGN rule_Expression )?
  ;

rule_InterfaceSignalDeclaration
  : KW_SIGNAL rule_IdentifierList TOK_COLON rule_SignalMode? subtypeIndication=rule_SubtypeIndication
    KW_BUS? ( TOK_VAR_ASSIGN rule_Expression )?
  ;

/*
interface_terminal_declaration
  : KW_TERMINAL identifier_list TOK_COLON subnature_indication
  ;
*/

rule_InterfaceVariableDeclaration
  : KW_VARIABLE? rule_IdentifierList TOK_COLON
    rule_SignalMode? subtypeIndication=rule_SubtypeIndication ( TOK_VAR_ASSIGN rule_Expression )?
  ;

rule_IterationScheme
  : KW_WHILE rule_Condition
  | KW_FOR rule_ParameterSpecification
  ;

rule_Label
  : LIT_IDENTIFIER
  ;

rule_LabelWithColon
  : LIT_IDENTIFIER TOK_COLON
  ;

rule_LibraryClause
  : KW_LIBRARY rule_LogicalNameList TOK_SEMICOL
  ;

// TODO: can it be merged?
rule_LibraryUnit
  : primaryUnit=rule_PrimaryUnit
  | secondaryUnit=rule_SecondaryUnit
  ;

rule_Literal
  : KW_NULL
  | LIT_BIT_STRING
  | LIT_STRING
  | rule_EnumerationLiteral
  | rule_NumericLiteral
  ;

rule_LogicalName
  : LIT_IDENTIFIER
  ;

rule_LogicalNameList
  : rule_LogicalName ( TOK_COMMA rule_LogicalName )*
  ;

// TODO: combine into expression
rule_LogicalOperator
  : OP_AND
  | OP_OR
  | OP_NAND
  | OP_NOR
  | OP_XOR
  | OP_XNOR
  ;

rule_LoopStatement
  : rule_LabelWithColon?
    rule_IterationScheme? KW_LOOP
      rule_SequenceOfStatements
    KW_END KW_LOOP LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_SignalMode
  : KW_IN
  | KW_OUT
  | KW_INOUT
  | KW_BUFFER
  | KW_LINKAGE
  ;

// TODO: combine into expression
rule_MultiplyingOperator
  : OP_MUL
  | OP_DIV
  | OP_MOD
  | OP_REM
  ;


// was
//   name
//     : simple_name
//     | operator_symbol
//     | selected_name
//     | indexed_name
//     | slice_name
//     | attribute_name
//     ;
// changed to avoid left-recursion to name (from selected_name, indexed_name,
// slice_name, and attribute_name, respectively)
// (2.2.2004, e.f.) + (12.07.2017, o.p.)
rule_Name
  : ( LIT_IDENTIFIER | LIT_STRING ) rule_NamePart*
  ;

rule_NamePart
  : rule_SelectedNamePart
  | rule_FunctionCallOrIndexedNamePart
  | rule_SliceNamePart
  | rule_AttributeNamePart
  ;

rule_SelectedName
  : LIT_IDENTIFIER ( TOK_DOT rule_Suffix )*
  ;

rule_SelectedNamePart
  : ( TOK_DOT rule_Suffix )+
  ;

rule_FunctionCallOrIndexedNamePart
  : TOK_LP rule_ActualParameterPart TOK_RP
  ;

rule_SliceNamePart
  : TOK_LP rule_DiscreteRange TOK_RP
  ;

rule_AttributeNamePart
  : rule_Signature? TOK_TICK rule_AttributeDesignator ( TOK_LP rule_Expression TOK_RP )?
  ;

/*
nature_declaration
  : NATURE LIT_IDENTIFIER IS nature_definition TOK_SEMICOL
  ;

nature_definition
  : scalar_nature_definition
  | composite_nature_definition
  ;

nature_element_declaration
  : identifier_list TOK_COLON element_subnature_definition
  ;
*/

rule_NextStatement
  : rule_LabelWithColon? KW_NEXT LIT_IDENTIFIER?
    ( KW_WHEN rule_Condition )?
    TOK_SEMICOL
  ;

rule_NumericLiteral
  : LIT_ABSTRACT
  | rule_PhysicalLiteral
  ;

rule_ObjectDeclaration
  : rule_ConstantDeclaration
  | rule_SignalDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
//  | terminal_declaration
//  | quantity_declaration
  ;

rule_Opts
  : KW_GUARDED? rule_DelayMechanism?
  ;

rule_PackageBody
  : KW_PACKAGE KW_BODY LIT_IDENTIFIER KW_IS
      rule_PackageBodyDeclarativePart
    KW_END ( KW_PACKAGE KW_BODY )? LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_PackageBodyDeclarativeItem
  : rule_SubprogramDeclaration
  | rule_SubprogramBody
  | rule_TypeDeclaration
  | rule_SubtypeDeclaration
  | rule_ConstantDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
  | rule_AliasDeclaration
  | rule_UseClause
//  | group_template_declaration
//  | group_declaration
  ;

rule_PackageBodyDeclarativePart
  : rule_PackageBodyDeclarativeItem*
  ;

rule_PackageDeclaration
  : KW_PACKAGE LIT_IDENTIFIER KW_IS
      rule_PackageDeclarativePart
    KW_END KW_PACKAGE? LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_PackageDeclarativeItem
  : rule_SubprogramDeclaration
  | rule_SubprogramBody
  | rule_TypeDeclaration
  | rule_SubtypeDeclaration
  | rule_ConstantDeclaration
  | rule_SignalDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
  | rule_AliasDeclaration
  | rule_ComponentDeclaration
  | rule_AttributeDeclaration
  | rule_AttributeSpecification
  | rule_DisconnectionSpecification
  | rule_UseClause
//  | group_template_declaration
//  | group_declaration
//  | nature_declaration
//  | subnature_declaration
//  | terminal_declaration
  ;

rule_PackageDeclarativePart
  : rule_PackageDeclarativeItem*
  ;

// rule_PackageHeader

// rule_PackageInstantiationDeclaration

// rule_PackagePathName

rule_ParameterSpecification
  : LIT_IDENTIFIER KW_IN rule_DiscreteRange
  ;

rule_PartialPathName
	: ( rule_PathNameElement TOK_DOT )* rule_SimpleName
	;

rule_PathNameElement
	: rule_SimpleName
	| rule_Label
	;

rule_PhysicalLiteral
  : LIT_ABSTRACT (: LIT_IDENTIFIER)
  ;

rule_PhysicalTypeDefinition
  : rule_RangeConstraint KW_UNITS
      rule_BaseUnitDeclaration
      rule_SecondaryUnitDeclaration*
    KW_END KW_UNITS LIT_IDENTIFIER?
  ;

rule_PortClause
  : KW_PORT TOK_LP rule_PortList TOK_RP TOK_SEMICOL
  ;

rule_PortList
  : rule_InterfacePortList
  ;

rule_PortMapAspect
  : KW_PORT KW_MAP TOK_LP
      rule_AssociationList
    TOK_RP
  ;

// TODO: combine into expression ?
rule_Primary
  : rule_Literal
  | rule_QualifiedExpression
  | TOK_LP rule_Expression TOK_RP
  | rule_Allocator
  | rule_Aggregate
  | rule_Name
  ;

rule_PrimaryUnit
  : entity=rule_EntityDeclaration
  | configuration=rule_ConfigurationDeclaration
  | package=rule_PackageDeclaration         // TODO: context
  ;

/*
procedural_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | variable_declaration
  | alias_declaration
  | attribute_declaration
  | attribute_specification
  | use_clause
//  | group_template_declaration
//  | group_declaration
  ;

procedural_declarative_part
  : ( procedural_declarative_item )*
  ;

procedural_statement_part
  : ( sequential_statement )*
  ;
*/

rule_ProcedureCall
  : rule_SelectedName ( TOK_LP rule_ActualParameterPart TOK_RP )?
  ;

rule_ProcedureCallStatement
  : rule_LabelWithColon? rule_ProcedureCall TOK_SEMICOL
  ;

rule_ProcessDeclarativeItem
  : rule_SubprogramDeclaration
  | rule_SubprogramBody
  | rule_TypeDeclaration
  | rule_SubtypeDeclaration
  | rule_ConstantDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
  | rule_AliasDeclaration
  | rule_AttributeDeclaration
  | rule_AttributeSpecification
  | rule_UseClause
//  | group_template_declaration
//  | group_declaration
  ;

rule_ProcessDeclarativePart
  : rule_ProcessDeclarativeItem*
  ;

rule_ProcessStatement
  : rule_LabelWithColon? KW_PROCESS
      ( TOK_LP rule_SensitivityList TOK_RP )?
    KW_IS?
      rule_ProcessDeclarativePart
    KW_BEGIN
      rule_ProcessStatementPart
    KW_END KW_PROCESS LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_PostponedProcessStatement
  : rule_LabelWithColon? KW_POSTPONED? KW_PROCESS
      ( TOK_LP rule_SensitivityList TOK_RP )?
    KW_IS?
      rule_ProcessDeclarativePart
    KW_BEGIN
      rule_ProcessStatementPart
    KW_END KW_POSTPONED? KW_PROCESS LIT_IDENTIFIER? TOK_SEMICOL
  ;

rule_ProcessStatementPart
  : rule_SequentialStatement*
  ;

// TODO: combine into expression
rule_QualifiedExpression
  : subtypeIndication=rule_SubtypeIndication TOK_TICK  ( rule_Aggregate | TOK_LP rule_Expression TOK_RP )
  ;

/*
quantity_declaration
  : free_quantity_declaration
  | branch_quantity_declaration
  | source_quantity_declaration
  ;

quantity_list
  : name ( TOK_COMMA name )*
  | OTHERS
  | ALL
  ;

quantity_specification
  : quantity_list TOK_COLON name
  ;
*/

rule_RangeDeclaration
  : rule_ExplicitRange
  | rule_Name
  ;

// TODO: move to e
rule_ExplicitRange
  : rule_SimpleExpression ( rule_Direction rule_SimpleExpression )?
  ;

rule_RangeConstraint
  : KW_RANGE rule_RangeDeclaration
  ;

/*
record_nature_definition
  : RECORD ( nature_element_declaration )+
    END RECORD ( LIT_IDENTIFIER )?
  ;
*/

rule_RecordTypeDefinition
  : KW_RECORD rule_ElementDeclaration+
    KW_END KW_RECORD LIT_IDENTIFIER?
  ;

// TODO: combine into expression
rule_Relation
  : rule_ShiftExpression
    (: rule_RelationalOperator rule_ShiftExpression )?
  ;

// TODO: combine into expression
rule_RelationalOperator
  : OP_EQ
  | OP_NE
  | OP_LT
  | OP_LE
  | OP_GT
  | OP_GE
  ;

rule_ReportStatement
  : rule_LabelWithColon? KW_REPORT rule_Expression
    ( KW_SEVERITY rule_Expression )?
    TOK_SEMICOL
  ;

rule_ReturnStatement
  : rule_LabelWithColon? KW_RETURN rule_Expression? TOK_SEMICOL
  ;

/*
scalar_nature_definition
  : name ACROSS name THROUGH name REFERENCE
  ;
*/

rule_ScalarTypeDefinition
  : rule_PhysicalTypeDefinition
  | rule_EnumerationTypeDefinition
  | rule_RangeConstraint
  ;

rule_SecondaryUnit
  : rule_ArchitectureBody
  | rule_PackageBody
  ;

rule_SecondaryUnitDeclaration
  : LIT_IDENTIFIER OP_EQ rule_PhysicalLiteral TOK_SEMICOL
  ;

rule_SelectedSignalAssignment
  : KW_WITH rule_Expression KW_SELECT rule_Target TOK_SIG_ASSIGN rule_Opts rule_SelectedWaveforms TOK_SEMICOL
  ;

rule_SelectedWaveforms
  : rule_Waveform KW_WHEN rule_Choices ( TOK_COMMA rule_Waveform KW_WHEN rule_Choices )*
  ;

rule_SensitivityClause
  : KW_ON rule_SensitivityList
  ;

rule_SensitivityList
  : rule_Name ( TOK_COMMA rule_Name )*
  ;

rule_SequenceOfStatements
  : rule_SequentialStatement*
  ;

rule_SequentialStatement
  : rule_WaitStatement
  | rule_AssertionStatement
  | rule_ReportStatement
  | rule_SignalAssignmentStatement
  | rule_VariableAssignmentStatement
  | rule_IfStatement
  | rule_CaseStatement
  | rule_LoopStatement
  | rule_NextStatement
  | rule_ExitStatement
  | rule_ReturnStatement
  | rule_LabelWithColon? KW_NULL TOK_SEMICOL
//  | break_statement
  | rule_ProcedureCallStatement
  ;

// TODO: combine into expression
rule_ShiftExpression
  : rule_SimpleExpression
    (: rule_ShiftOperator rule_SimpleExpression )?
  ;

// TODO: combine into expression
rule_ShiftOperator
  : OP_SLL
  | OP_SRL
  | OP_SLA
  | OP_SRA
  | OP_ROL
  | OP_ROR
  ;

rule_SignalAssignmentStatement
  : rule_LabelWithColon?
    rule_Target TOK_SIG_ASSIGN rule_DelayMechanism? rule_Waveform TOK_SEMICOL
  ;

rule_SignalDeclaration
  : KW_SIGNAL rule_IdentifierList TOK_COLON
    subtypeIndication=rule_SubtypeIndication rule_SignalKind? ( TOK_VAR_ASSIGN rule_Expression )? TOK_SEMICOL
  ;

rule_SignalKind
  : KW_REGISTER
  | KW_BUS
  ;

rule_SignalList
  : rule_Name ( TOK_COMMA rule_Name )*
  | KW_OTHERS
  | KW_ALL
  ;

rule_Signature
  : TOK_LB ( rule_Name ( TOK_COMMA rule_Name )* )? ( KW_RETURN rule_Name )? TOK_RB
  ;

// NOTE that sign is applied to first operand only (LRM does not permit
// `a op -b' - use `a op (-b)' instead).
// (3.2.2004, e.f.)
// TODO: combine into expression
rule_SimpleExpression
  : ( OP_PLUS | OP_MINUS )? rule_Term (: rule_AddingOperator rule_Term )*
  ;

rule_SimpleName
	: LIT_IDENTIFIER
	;

/*
rule_SimpleSimultaneousStatement
  : rule_LabelWithColon?
    rule_SimpleExpression TOK_SIG_ASSIGN rule_SimpleExpression ( tolerance_aspect )? TOK_SEMICOL
  ;

rule_SimultaneousAlternative
  : KW_WHEN rule_Choices TOK_RARROW simultaneous_statement_part
  ;

simultaneous_case_statement
  : rule_LabelWithColon? KW_CASE rule_Expression KW_USE
      rule_SimultaneousAlternative+
    KW_END KW_CASE LIT_IDENTIFIER? TOK_SEMICOL
  ;

simultaneous_if_statement
  : rule_LabelWithColon? KW_IF rule_Condition KW_USE
      simultaneous_statement_part
    ( KW_ELSIF rule_Condition KW_USE
      simultaneous_statement_part
    )*
    ( KW_ELSE
      simultaneous_statement_part
    )?
    KW_END KW_USE LIT_IDENTIFIER? TOK_SEMICOL
  ;

simultaneous_procedural_statement
  : ( label_colon )? KW_PROCEDURAL ( IS )?
    procedural_declarative_part KW_BEGIN
    procedural_statement_part
    KW_END KW_PROCEDURAL ( LIT_IDENTIFIER )? TOK_SEMICOL
  ;

simultaneous_statement
  : rule_SimpleSimultaneousStatement
  | simultaneous_if_statement
  | simultaneous_case_statement
//  | simultaneous_procedural_statement
  | rule_LabelWithColon? KW_NULL TOK_SEMICOL
  ;

simultaneous_statement_part
  : simultaneous_statement*
  ;
*/

/*
source_aspect
  : KW_SPECTRUM simple_expression TOK_COMMA simple_expression
  | KW_NOISE simple_expression
  ;

source_quantity_declaration
  : QUANTITY identifier_list TOK_COLON subtypeIndication=subtype_indication source_aspect TOK_SEMICOL
  ;

step_limit_specification
  : LIMIT quantity_specification WITH expression TOK_SEMICOL
  ;

subnature_declaration
  : SUBNATURE LIT_IDENTIFIER IS subnature_indication TOK_SEMICOL
  ;

subnature_indication
  : name ( index_constraint )?
    ( TOLERANCE expression ACROSS expression THROUGH )?
  ;
*/

rule_SubprogramBody
  : rule_SubprogramSpecification KW_IS
      rule_SubprogramDeclarativePart
    KW_BEGIN
      rule_SubprogramStatementPart
    KW_END rule_SubprogramKind? rule_Designator? TOK_SEMICOL
  ;

rule_SubprogramDeclaration
  : rule_SubprogramSpecification TOK_SEMICOL
  ;

rule_SubprogramDeclarativeItem
  : rule_SubprogramDeclaration
  | rule_SubprogramBody
  | rule_TypeDeclaration
  | rule_SubtypeDeclaration
  | rule_ConstantDeclaration
  | rule_VariableDeclaration
  | rule_FileDeclaration
  | rule_AliasDeclaration
  | rule_AttributeDeclaration
  | rule_AttributeSpecification
  | rule_UseClause
//  | group_template_declaration
//  | group_declaration
  ;

rule_SubprogramDeclarativePart
  : rule_SubprogramDeclarativeItem*
  ;

rule_SubprogramKind
  : KW_PROCEDURE
  | KW_FUNCTION
  ;

rule_SubprogramSpecification
  : rule_ProcedureSpecification
  | rule_FunctionSpecification
  ;

rule_ProcedureSpecification
  : KW_PROCEDURE rule_Designator ( TOK_LP rule_FormalParameterList TOK_RP )?
  ;

rule_FunctionSpecification
  : ( KW_PURE | KW_IMPURE )? KW_FUNCTION rule_Designator
    ( TOK_LP rule_FormalParameterList TOK_RP )? KW_RETURN subtypeIndication=rule_SubtypeIndication
  ;

rule_SubprogramStatementPart
  : rule_SequentialStatement*
  ;

rule_SubtypeDeclaration
  : KW_SUBTYPE LIT_IDENTIFIER KW_IS subtypeIndication=rule_SubtypeIndication TOK_SEMICOL
  ;

rule_SubtypeIndication
  : rule_SelectedName rule_SelectedName? rule_Constraint? /* ( tolerance_aspect )? */
  ;

rule_Suffix
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  | LIT_STRING
  | KW_ALL
  ;

rule_Target
  : rule_Name
  | rule_Aggregate
  ;

// TODO: combine into expression
rule_Term
  : rule_Factor (: rule_MultiplyingOperator rule_Factor )*
  ;

/*
terminal_aspect
  : name ( TO name )?
  ;

terminal_declaration
  : TERMINAL identifier_list TOK_COLON subnature_indication TOK_SEMICOL
  ;

through_aspect
  : identifier_list ( tolerance_aspect )? ( TOK_VAR_ASSIGN expression )? THROUGH
  ;
*/

rule_TimeoutClause
  : KW_FOR rule_Expression
  ;

/*
tolerance_aspect
  : TOLERANCE expression
  ;
*/

rule_TypeDeclaration
  : KW_TYPE LIT_IDENTIFIER ( KW_IS rule_TypeDefinition )? TOK_SEMICOL
  ;

rule_TypeDefinition
  : rule_ScalarTypeDefinition
  | rule_CompositeTypeDefinition
  | rule_AccessTypeDefinition
  | rule_FileTypeDefinition
  ;

rule_UnconstrainedArrayDefinition
  : KW_ARRAY TOK_LP rule_IndexSubtypeDefinition ( TOK_COMMA rule_IndexSubtypeDefinition )*
    TOK_RP KW_OF subtypeIndication=rule_SubtypeIndication
  ;

/*
unconstrained_nature_definition
  : KW_ARRAY TOK_LP index_subtype_definition ( TOK_COMMA index_subtype_definition )*
    TOK_RP OF subnature_indication
  ;
*/

rule_UseClause
  : KW_USE rule_SelectedName ( TOK_COMMA rule_SelectedName )* TOK_SEMICOL
  ;

rule_VariableAssignmentStatement
  : rule_LabelWithColon? rule_Target TOK_VAR_ASSIGN rule_Expression TOK_SEMICOL
  ;

rule_VariableDeclaration
  : KW_SHARED? KW_VARIABLE rule_IdentifierList TOK_COLON
    subtypeIndication=rule_SubtypeIndication ( TOK_VAR_ASSIGN rule_Expression )? TOK_SEMICOL
  ;

rule_WaitStatement
  : rule_LabelWithColon? KW_WAIT
      rule_SensitivityClause?
      rule_ConditionClause?
      rule_TimeoutClause?
    TOK_SEMICOL
  ;

rule_Waveform
  : rule_WaveformElement ( TOK_COMMA rule_WaveformElement )*
  | KW_UNAFFECTED
  ;

rule_WaveformElement
  : rule_Expression ( KW_AFTER rule_Expression )?
  ;
