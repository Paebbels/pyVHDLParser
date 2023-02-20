// ================================================================================================================== //
//            __     ___   _ ____  _     ____                                                                         //
//  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                //
// | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                               //
// | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                  //
// | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                  //
// |_|    |___/                                                                                                       //
// ================================================================================================================== //
// Authors:                                                                                                           //
//   Patrick Lehmann                                                                                                  //
//                                                                                                                    //
// License:                                                                                                           //
// ================================================================================================================== //
// Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                          //
// Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                             //
//                                                                                                                    //
// Licensed under the Apache License, Version 2.0 (the "License");                                                    //
// you may not use this file except in compliance with the License.                                                   //
// You may obtain a copy of the License at                                                                            //
//                                                                                                                    //
//   http://www.apache.org/licenses/LICENSE-2.0                                                                       //
//                                                                                                                    //
// Unless required by applicable law or agreed to in writing, software                                                //
// distributed under the License is distributed on an "AS IS" BASIS,                                                  //
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                           //
// See the License for the specific language governing permissions and                                                //
// limitations under the License.                                                                                     //
// ================================================================================================================== //
//
parser grammar VHDLParser;

options {
	tokenVocab = VHDLLexer;
}

// TODO: PSL
// TODO: VHDL-AMS

rule_AbsolutePathname
	: TOK_DOT rule_PartialPathname
	;

// rule_AbstractLiteral
// handled by lexer

rule_AccessIncompleteTypeDefinition
	: KW_ACCESS rule_IncompleteSubtypeIndication
	;

rule_AccessTypeDefinition
	: KW_ACCESS subtypeIndication=rule_SubtypeIndication
	;

/*
// VHDL-AMS
across_aspect
	: identifier_list ( tolerance_aspect )? ( TOK_VAR_ASSIGN expression )? ACROSS
	;
*/

rule_ActualDesignator
	: inertial=KW_INERTIAL? expression=rule_Expression /*rule_ConditionalExpression*/
	| name=rule_Name
	| subtypeIndication=rule_SubtypeIndication
	| open=KW_OPEN
	;

rule_ActualPart
	: actualDesignator=rule_ActualDesignator
	| conversion=rule_Name TOK_LP actualDesignator=rule_ActualDesignator TOK_RP
	;

// rule_AddingOperator
// optimized into rule_SimpleExpression

rule_Aggregate
	: TOK_LP element+=rule_ElementAssociation ( TOK_COMMA element+=rule_ElementAssociation )* TOK_RP
	;

rule_AliasDeclaration
	: KW_ALIAS aliasDesignator=rule_AliasDesignator ( TOK_COLON aliasIndication=rule_AliasIndication )?
			KW_IS aliasTarget=rule_Name ( signature=rule_Signature )?
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
			subtypeIndication=rule_SubtypeIndication
		| qualifiedExpression=rule_QualifiedExpression
		)
	;

rule_Architecture
	: KW_ARCHITECTURE name=LIT_IDENTIFIER KW_OF entityName=LIT_IDENTIFIER KW_IS
			declarativeItems+=rule_BlockDeclarativeItem*
		KW_BEGIN
			statements+=rule_ConcurrentStatement*
		KW_END KW_ARCHITECTURE? name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

// rule_ArchitectureDeclarativePart
// moved into rule_Architecture

rule_ArchitectureStatement
	: blockStatement=rule_BlockStatement
	| processStatement=rule_ProcessStatement
	| postponedProcessStatement=rule_PostponedProcessStatement
	| ( label=LIT_IDENTIFIER TOK_COLON )? procedureCallStatement=rule_ConcurrentProcedureCallStatement
	| ( label=LIT_IDENTIFIER TOK_COLON )? assertionStatement=rule_ConcurrentAssertionStatement
	| ( label=LIT_IDENTIFIER TOK_COLON )? postponed=KW_POSTPONED? signalAssignmentStatement=rule_ConcurrentSignalAssignmentStatement
	| instantiationStatement=rule_ComponentInstantiationStatement
	| generateStatement=rule_GenerateStatement
//  | concurrent_break_statement
//  | simultaneous_statement
	;

// rule_ArchitectureStatementPart
// moved into rule_Architecture

rule_ArrayConstraint
	: rule_IndexConstraint rule_ElementConstraint?
	| TOK_LP KW_OPEN TOK_RP rule_ElementConstraint?
	;

// rule_ArrayElementConstraint
// moved into rule_ArrayConstraint

// rule_ArrayElementResolution
// moved into rule_ElementResolution

rule_ArrayIncompleteTypeDefinition
	: KW_ARRAY TOK_LP rule_ArrayIndexIncompleteTypeList TOK_RP
		KW_OF rule_IncompleteSubtypeIndication
	;

// TODO: report incomplete type vs. unspecified type
rule_ArrayIndexIncompleteType
	: rule_IndexSubtypeDefinition
	| rule_IndexConstraint
	| rule_UnspecifiedTypeIndication
	;

rule_ArrayIndexIncompleteTypeList
	: rule_ArrayIndexIncompleteType ( TOK_COMMA rule_ArrayIndexIncompleteType )*
	;

rule_ArrayModeViewIndication
	: KW_VIEW TOK_LP rule_Name TOK_RP ( KW_OF rule_SubtypeIndication )?
	;

/*
rule_AMS_ArrayNatureDefinition
	: rule_AMS_UnconstrainedNatureDefinition
	| rule_AMS_ConstrainedNatureDefinition
	;
*/

// rule_ArrayTypeDefinition
// moved into rule_CompositeTypeDefinition

rule_Assertion
	: KW_ASSERT assertCondition=rule_Expression
		( KW_REPORT reportExpression=rule_Expression )?
		( KW_SEVERITY severityExpression=rule_Expression )?
	;

rule_AssertionStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
	 		assertion=rule_Assertion
	 	TOK_SEMICOL
	;

rule_AssociationElement
	: ( formal=rule_FormalPart TOK_RARROW )? actual=rule_ActualPart
	;

rule_AssociationList
	: element+=rule_AssociationElement ( TOK_COMMA element+=rule_AssociationElement )*
	;

rule_AttributeDeclaration
	: KW_ATTRIBUTE label=LIT_IDENTIFIER TOK_COLON name=rule_Name TOK_SEMICOL
	;

// TODO: report bug to WG
rule_AttributeDesignator
	: KW_RANGE
	| KW_RECORD
	| KW_SIGNAL
	| KW_SUBTYPE
	| LIT_IDENTIFIER
	;

// rule_AttributeName
// moved into rule_Name

rule_AttributeSpecification
	: KW_ATTRIBUTE designator=LIT_IDENTIFIER
			KW_OF entitySpecification=rule_EntitySpecification
			KW_IS expression=rule_ConditionalExpression
		TOK_SEMICOL
	;

// rule_Base
// handled by lexer

// rule_BaseSpecifier
// handled by lexer

// rule_BasedInteger
// handled by lexer

// rule_BasedLiteral
// handled by lexer

// rule_BasicCharacter
// handled by lexer

// rule_BasicGraphicCharacter
// handled by lexer

// rule_BasicIdentifier
// handled by lexer

rule_BindingIndication
	: ( KW_USE entityAspect=rule_EntityAspect )?
			genericMapAspect=rule_GenericMapAspect?
			portMapAspect=rule_PortMapAspect?
	;

// rule_BitStringLiteral
// handled by lexer

// rule_BitValue
// handled by lexer

rule_BlockConfiguration
	: KW_FOR blockSpecification=rule_BlockSpecification
			useClauses+=rule_UseClause*
			configurationItems+=rule_ConfigurationItem*
		KW_END KW_FOR TOK_SEMICOL
	;

rule_BlockDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramBody
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageBody
	| rule_PackageInstantiationDeclaration
	| rule_TypeDeclaration
	| rule_SubtypeDeclaration
	| rule_ModeViewDeclaration
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
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
//  | rule_PSL_PropertyDeclaration
//  | rule_PSL_SequenceDeclaration
//  | rule_PSL_ClockDeclaration
//  | rule_AMS_NatureDeclaration
//  | rule_AMS_SubnatureDeclaration
//  | rule_AMS_QuantityDeclaration
//  | rule_AMS_TerminalDeclaration
	;

// rule_BlockDeclarativePart
// moved into rule_BlockStatement, rule_GenerateStatement

// rule_BlockHeader
// moved into rule_BlockStatement

// TODO: why /architecture/_name
rule_BlockSpecification
	: name=rule_Name
	| label=LIT_IDENTIFIER ( TOK_LP rule_GenerateSpecification TOK_RP )?
	;

rule_BlockStatement
	: label=LIT_IDENTIFIER TOK_COLON KW_BLOCK ( TOK_LP guardExpression=rule_Expression TOK_RP )? KW_IS?
			( genericClause=rule_GenericClause
				( genericMapAspect=rule_GenericMapAspect TOK_SEMICOL )?
			)?
			( portClause=rule_PortClause
				( portMapAspect=rule_PortMapAspect TOK_SEMICOL )?
			)?
			blockDeclarativeItem+=rule_BlockDeclarativeItem*
		KW_BEGIN
			blockStatements+=rule_ConcurrentStatement*
		KW_END KW_BLOCK label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

// TODO: report copy/replace error to WG
// rule_BlockStatementPart
// moved into rule_BlockStatement

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

rule_CaseGenerateAlternative
	: KW_WHEN ( alternativeLabel=LIT_IDENTIFIER TOK_COLON )? rule_Choices TOK_RARROW
			rule_GenerateStatementBody
	;

rule_CaseGenerateStatement
	: label=LIT_IDENTIFIER TOK_COLON
		KW_CASE expression=rule_Expression KW_GENERATE
			alternatives+=rule_CaseGenerateAlternative+
		KW_END KW_GENERATE label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

// TODO: needs a copy for variant with ?
rule_CaseStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
		KW_CASE expression=rule_Expression KW_IS
			alternatives+=rule_CaseStatementAlternative+
		KW_END KW_CASE label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_CaseStatementAlternative
	: KW_WHEN rule_Choices TOK_RARROW
			statements+=rule_SequentialStatement*
	;

rule_Choice
	: rule_Expression
	| rule_DiscreteRange
//	| LIT_IDENTIFIER
	| KW_OTHERS
	;

rule_Choices
	: choices+=rule_Choice ( TOK_BAR choices+=rule_Choice )*
	;

rule_ComponentConfiguration
	: KW_FOR componentSpecification=rule_ComponentSpecification
			( bindingIndication=rule_BindingIndication TOK_SEMICOL )?
// ( verificationUnitBindingIndications+=rule_VerificationUnitBindingIndication TOK_SEMICOL )*
			blockConfiguration=rule_BlockConfiguration?
		KW_END KW_FOR TOK_SEMICOL
	;

rule_ComponentDeclaration
	: KW_COMPONENT name=LIT_IDENTIFIER KW_IS?
			genericClause=rule_GenericClause?
			portClause=rule_PortClause?
		KW_END KW_COMPONENT? name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_ComponentInstantiationStatement
	: label=LIT_IDENTIFIER TOK_COLON instantiatedUnit=rule_InstantiatedUnit
			genericMapAspect=rule_GenericMapAspect?
			portMapAspect=rule_PortMapAspect?
		TOK_SEMICOL
	;

rule_ComponentSpecification
	: instantiationList=rule_InstantiationList TOK_COLON rule_Name
	;

/*
composite_nature_definition
	: array_nature_definition
	| record_nature_definition
	;
*/

rule_CompositeTypeDefinition
	: constrainedArrayDefinition=rule_ConstrainedArrayDefinition
	| unboundedArrayDefinition=rule_UnboundArrayDefinition
	| recordTypeDefinition=rule_RecordTypeDefinition
	;


rule_CompoundConfigurationSpecification
	: KW_FOR rule_ComponentSpecification rule_BindingIndication TOK_SEMICOL		// TODO: semicolon?
//			( verificationUnitBindingIndications+=rule_VerificationUnitBindingIndication TOK_SEMICOL )+
		KW_END KW_FOR TOK_SEMICOL
	;

rule_ConcurrentAssertionStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
			postponed=KW_POSTPONED?
			rule_Assertion
		TOK_SEMICOL
	;

/*
concurrent_break_statement
	: ( label_colon )? BREAK ( break_list )? ( sensitivity_clause )?
		( WHEN condition )? TOK_SEMICOL
	;
*/

rule_ConcurrentConditionalSignalAssignment
	: rule_Target TOK_SIG_ASSIGN
			guarded=KW_GUARDED?
			delayMechanism=rule_DelayMechanism?
			conditionalWaveforms=rule_ConditionalWaveforms
		TOK_SEMICOL
	;

rule_ConcurrentProcedureCallStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
			postponed=KW_POSTPONED?
			procedureCall=rule_ProcedureCall
		TOK_SEMICOL
	;

// TODO handle ?
rule_ConcurrentSelectedSignalAssignment
	: KW_WITH expression=rule_Expression KW_SELECT
			target=rule_Target TOK_SIG_ASSIGN
			guarded=KW_GUARDED?
			delayMechanism=rule_DelayMechanism?
			selectedWaveforms=rule_SelectedWaveforms
		TOK_SEMICOL
	;

rule_ConcurrentSignalAssignmentStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
		postponed=KW_POSTPONED?
		( rule_ConcurrentSimpleSignalAssignment
		| rule_ConcurrentConditionalSignalAssignment
		| rule_ConcurrentSelectedSignalAssignment
		)
	;

rule_ConcurrentSimpleSignalAssignment
	: target=rule_Target TOK_SIG_ASSIGN
			guarded=KW_GUARDED?
			delayMechanism=rule_DelayMechanism?
			waveform=rule_Waveform
		TOK_SEMICOL
	;

rule_ConcurrentStatement
	: blockStatement=rule_BlockStatement
	| processStatement=rule_ProcessStatement
	| postponedProcessStatement=rule_PostponedProcessStatement
	| ( label=LIT_IDENTIFIER TOK_COLON )? procedureCallStatement=rule_ConcurrentProcedureCallStatement
	| ( label=LIT_IDENTIFIER TOK_COLON )? assertionStatement=rule_ConcurrentAssertionStatement
	| ( label=LIT_IDENTIFIER TOK_COLON )? postponed=KW_POSTPONED? signalAssignmentStatement=rule_ConcurrentSignalAssignmentStatement
	| instantiationStatement=rule_ComponentInstantiationStatement
	| generateStatement=rule_GenerateStatement
//  | concurrent_break_statement
//  | simultaneous_statement
	;

// rule_Condition
// replaced by condition=rule_Expression

rule_ConditionClause
	: KW_UNTIL condition=rule_Expression
	;

// rule_ConditionOperator
// handled by lexer

rule_ConditionalExpression
	: left=rule_Expression
		( KW_WHEN condition=rule_Expression KW_ELSE right=rule_Expression )?
	;

rule_ConditionalOrUnaffectedExpression
	: left=rule_ExpressionOrUnaffected
		( KW_WHEN condition=rule_Expression KW_ELSE right=rule_ExpressionOrUnaffected )?
		( KW_WHEN finalCondition=rule_Expression )?
	;

rule_ConditionalSignalAssignment
	: target=rule_Target TOK_SIG_ASSIGN
			delayMechanism=rule_DelayMechanism?
			conditionalWaveforms=rule_ConditionalWaveforms
		TOK_SEMICOL
	;

rule_ConditionalWaveforms
	: waveform=rule_Waveform KW_WHEN condition=rule_Expression
		( KW_ELSE waveforms+=rule_Waveform KW_WHEN conditions+=rule_Expression )*
		( KW_ELSE lastCondition=rule_Expression)?
	;

rule_ConfigurationDeclaration
	: KW_CONFIGURATION name=LIT_IDENTIFIER KW_OF entityName=rule_Name KW_IS
			configurationDeclarativeItem+=rule_ConfigurationDeclarativeItem*
//			( verificationUnitBindingIndications+=rule_VerificationUnitBindingIndication TOK_SEMICOL )*
			blockConfiguration=rule_BlockConfiguration
		KW_END KW_CONFIGURATION? name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_ConfigurationDeclarativeItem
	: rule_UseClause
	| rule_AttributeSpecification
  | rule_GroupDeclaration
	;

// rule_ConfigurationDeclarativePart
// moved into rule_ConfigurationDeclaration

rule_ConfigurationItem
	: rule_BlockConfiguration
	| rule_ComponentConfiguration
	;

rule_ConfigurationSpecification
	: rule_SimpleConfigurationSpecification
	| rule_CompoundConfigurationSpecification
	;

rule_ConstantDeclaration
	: KW_CONSTANT name=rule_IdentifierList TOK_COLON subtypeIndication=rule_SubtypeIndication
		( TOK_VAR_ASSIGN expression=rule_ConditionalExpression )? TOK_SEMICOL
	;

rule_ConstrainedArrayDefinition
	: KW_ARRAY rule_IndexConstraint
			KW_OF subtypeIndication=rule_SubtypeIndication
	;

/*
constrained_nature_definition
	: KW_ARRAY index_constraint KW_OF subnature_indication
	;
*/

rule_Constraint
	: rule_SimpleRange                // FIXME: added for testing
	| rule_RangeConstraint
	| rule_ArrayConstraint
	| rule_RecordConstraint
	;

// rule_ContextClause
// moved into rule_DesignUnit

rule_ContextDeclaration
	: KW_CONTEXT name=LIT_IDENTIFIER KW_IS
			contextItems+=rule_ContextItem*
		KW_END KW_CONTEXT? name2=LIT_IDENTIFIER TOK_SEMICOL
	;

rule_ContextItem
	: libraryClause=rule_LibraryClause
	| useClause=rule_UseClause
	| contextReference=rule_ContextReference
	;

rule_ContextReference
	: KW_CONTEXT names+=rule_SelectedName2 ( TOK_COLON names+=rule_SelectedName2 )* TOK_SEMICOL
	;

// rule_DecimalLiteral
// handled by lexer

rule_DelayMechanism
	: KW_TRANSPORT
	| ( KW_REJECT expression=rule_Expression )? KW_INERTIAL
	;

// Entrypoint rule
rule_DesignFile
	: designUnits+=rule_DesignUnit+
		EOF
	;

rule_DesignUnit
	: contextItems+=rule_ContextItem*
		libraryUnit=rule_LibraryUnit
	;

rule_Designator
	: LIT_IDENTIFIER
	| LIT_STRING
	;

// TODO: merge into rules?
rule_Direction
	: direction=( KW_TO | KW_DOWNTO )
	;

rule_DisconnectionSpecification
	: KW_DISCONNECT guardedSignalSpecification=rule_GuardedSignalSpecification
			KW_AFTER expression=rule_Expression
		TOK_SEMICOL
	;

rule_DiscreteRange
	: subtypeIndication=rule_SubtypeIndication
	| range=rule_Range
	;

rule_DiscreteIncompleteTypeDefinition
	: TOK_LP TOK_BOX TOK_RP
	;

rule_ElementArrayModeViewIndication
	: KW_VIEW TOK_LP name=rule_Name TOK_RP
	;

rule_ElementAssociation
	: ( choices=rule_Choices TOK_RARROW )? expression=rule_Expression
	;

rule_ElementConstraint
	: arrayConstraint=rule_ArrayConstraint
	| recordConstraint=rule_RecordConstraint
	;

rule_ElementDeclaration
	: identifierList=rule_IdentifierList TOK_COLON subtypeIndication=rule_SubtypeIndication TOK_SEMICOL
	;

rule_ElementModeIndication
	: rule_Mode
	| rule_ElementModeViewIndication
	;

rule_ElementModeViewIndication
	: rule_ElementArrayModeViewIndication
	| rule_ElementRecordModeViewIndication
	;

rule_ElementRecordModeViewIndication
	: KW_VIEW name=rule_Name
	;

rule_ElementResolution
	: rule_ResolutionIndication
	| rule_RecordResolution
	;

/*
element_subnature_definition
	: subnature_indication
	;
*/

// rule_ElementSubtypeDefinition
// moved into rule_ElementDeclaration

rule_EntityAspect
	: KW_ENTITY entityName=rule_Name ( TOK_LP architectureName=LIT_IDENTIFIER TOK_RP )?
	| KW_CONFIGURATION configurationName=rule_Name
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
  | KW_GROUP
	| KW_FILE
//  | KW_PROPERTY
//  | KW_SEQUENCE
  | KW_VIEW
//  | NATURE
//  | SUBNATURE
//  | QUANTITY
//  | TERMINAL
	;


rule_EntityClassEntry
	: rule_EntityClass TOK_BOX?
	;

// rule_EntityClassEntryList
// moved into rule_GroupTemplateDeclaration

rule_EntityDeclaration
	: KW_ENTITY name=LIT_IDENTIFIER KW_IS
			genericClause=rule_GenericClause?
			portClause=rule_PortClause?
			declarations=rule_EntityDeclarativeItem*
		( KW_BEGIN
			statements=rule_EntityStatement*
		)?
		KW_END KW_ENTITY? name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_EntityDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramBody
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageBody
	| rule_PackageInstantiationDeclaration
	| rule_TypeDeclaration
	| rule_SubtypeDeclaration
	| rule_ModeViewDeclaration
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
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
//  | nature_declaration
//  | subnature_declaration
//  | quantity_declaration
//  | terminal_declaration
	;

// rule_EntityDeclarativePart
// moved into rule_EntityDeclaration

rule_EntityDesignator
	: entityTag=rule_EntityTag signature=rule_Signature?
	;

// rule_entity_header
// moved into rule_EntityDeclaration

rule_EntityNameList
	: entityDesignators+=rule_EntityDesignator ( TOK_COMMA entityDesignators+=rule_EntityDesignator )*
	| KW_OTHERS
	| KW_ALL
	;

rule_EntitySpecification
	: entityNameList=rule_EntityNameList TOK_COLON entityClass=rule_EntityClass
	;

rule_EntityStatement
	: rule_ConcurrentAssertionStatement
	| rule_ConcurrentProcedureCallStatement
	| rule_ProcessStatement
	| rule_PostponedProcessStatement
	;

// rule_EntityStatementPart
// moved into rule_EntityDeclaration

rule_EntityTag
	: LIT_IDENTIFIER    // rule_SimpleName
	| LIT_CHARACTER
	| LIT_STRING
	;

rule_EnumerationLiteral
	: LIT_IDENTIFIER
	| LIT_CHARACTER
	;

rule_EnumerationTypeDefinition
	: TOK_LP enumerationLiterals+=rule_EnumerationLiteral ( TOK_COMMA enumerationLiterals+=rule_EnumerationLiteral )* TOK_RP
	;

rule_ExitStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
			KW_EXIT referencedLabel=LIT_IDENTIFIER?
			( KW_WHEN condition=rule_Expression )?
		TOK_SEMICOL
	;

// rule_Exponent
// handled by lexer

rule_Expression
	: rule_Primary                                                                                                                                                 #primaryOp
	|	operator=OP_CONDITION right=rule_Expression                                                                                                                  #unaryOp
	| operator=( OP_ABS | OP_NOT | OP_AND | OP_OR | OP_NAND | OP_NOR | OP_XOR | OP_XNOR | OP_PLUS | OP_MINUS ) right=rule_Expression                               #unaryOp
	| <assoc=right> left=rule_Expression	operator=OP_POW right=rule_Expression                                                                                    #binaryOp
	| left=rule_Expression operator=( OP_MUL | OP_DIV | OP_MOD | OP_REM ) right=rule_Expression                                                                    #binaryOp
	| left=rule_Expression operator=( OP_PLUS | OP_MINUS | OP_CONCAT ) right=rule_Expression                                                                       #binaryOp
	| left=rule_Expression operator=( OP_SLL | OP_SRL | OP_SLA | OP_SRA | OP_ROL | OP_ROR ) right=rule_Expression                                                  #binaryOp
	| left=rule_Expression operator=( OP_EQ | OP_NE | OP_LT | TOK_SIG_ASSIGN | OP_GT | OP_GE | OP_IEQ | OP_INE | OP_ILT | OP_ILE | OP_IGT | OP_IGE ) right=rule_Expression  #binaryOp
	| left=rule_Expression operator=( OP_AND | OP_OR | OP_NAND | OP_NOR | OP_XOR | OP_XNOR ) right=rule_Expression                                                 #binaryOp
	;

rule_ExpressionOrUnaffected
	: rule_Expression
	| KW_UNAFFECTED
	;

// rule_ExtendedDigit
// handled by lexer

// rule_ExtendedIdentifier
// handled by lexer

rule_ExternalName
	: rule_ExternalConstantName
	| rule_ExternalSignalName
	| rule_ExternalVariableName
	;

rule_ExternalConstantName
	: TOK_DLA KW_CONSTANT rule_ExternalPathname TOK_COLON rule_InterfaceTypeIndication TOK_DRA
	;

rule_ExternalSignalName
	: TOK_DLA KW_SIGNAL rule_ExternalPathname TOK_COLON rule_InterfaceTypeIndication TOK_DRA
	;

rule_ExternalVariableName
	: TOK_DLA KW_VARIABLE rule_ExternalPathname TOK_COLON rule_InterfaceTypeIndication TOK_DRA
	;

rule_ExternalPathname
	: rule_PackagePathname
	| rule_AbsolutePathname
	| rule_RelativePathname
	;

// rule_Factor
// moved into rule_Expression

rule_FileDeclaration
	: KW_FILE identifierList=rule_IdentifierList TOK_COLON
			subtypeIndication=rule_SubtypeIndication
			rule_FileOpenInformation?
		TOK_SEMICOL
	;

// TODO: report false italic on **_incomplete_**
rule_FileIncompleteTypeDefinition
	: KW_FILE KW_OF rule_IncompleteTypeMark
	;

// rule_FileLogicalName
// moved into rule_FileOpenInformation

rule_FileOpenInformation
	: ( KW_OPEN openKindExpression=rule_Expression )?
		KW_IS fileNameExpression=rule_Expression
	;

rule_FileTypeDefinition
	: KW_FILE KW_OF rule_Name
	;

rule_FloatingIncompleteTypeDefinition
	: KW_RANGE TOK_BOX TOK_DOT TOK_BOX
	;

// TODO: merge?
rule_FloatingTypeDefinition
	: rule_RangeConstraint
	;

rule_ForGenerateStatement
	: label=LIT_IDENTIFIER TOK_COLON
			KW_FOR rule_ParameterSpecification KW_GENERATE
				( declaredItems+=rule_BlockDeclarativeItem*
			KW_BEGIN )?
				statements+=rule_ConcurrentStatement*      // TODO: rename to rule_ConcurrentStatement
			KW_END KW_GENERATE label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

// rule_ForceMode
// moved into rule_SelectedForceAssignment, rule_SimpleForceAssignment, rule_SimpleReleaseAssignment

// TODO: merge
rule_FormalDesignator
	: rule_Name signature=rule_Signature?
	;

// TODO: merge
rule_FormalParameterList
	: rule_InterfaceList
	;

rule_FormalPart
	: rule_FormalDesignator
	| ( rule_Name | rule_Name ) TOK_LP rule_FormalDesignator  TOK_RP
	;

rule_FullTypeDeclaration
	: KW_TYPE name=LIT_IDENTIFIER KW_IS rule_TypeDefinition TOK_SEMICOL
	;

rule_FunctionCall
	: name=rule_Name
			genericMapAspect=rule_GenericMapAspect
			parameterMapAspect=rule_ParameterMapAspect
	;

rule_FunctionSpecification
	: ( KW_PURE | KW_IMPURE )?
		KW_FUNCTION rule_Designator
// TODO: insert subprogram_header
		( KW_PARAMETER? TOK_LP rule_FormalParameterList TOK_RP )?
		KW_RETURN ( returnIdentifier=LIT_IDENTIFIER KW_OF )? rule_Name
	;

/*
free_quantity_declaration
	: QUANTITY identifier_list TOK_COLON subtypeIndication=subtype_indication
		( TOK_VAR_ASSIGN expression )? TOK_SEMICOL
	;
*/

rule_GenerateSpecification
	: rule_DiscreteRange
	| rule_Expression
	| LIT_IDENTIFIER
	;

rule_GenerateStatement
	: rule_ForGenerateStatement
	| rule_IfGenerateStatement
	| rule_CaseGenerateStatement
	;

// TODO: merge?
rule_GenerateStatementBody
	: ( declaredItems+=rule_BlockDeclarativeItem*
			KW_BEGIN
		)?
			statements+=rule_ConcurrentStatement*      // TODO: rename to rule_ConcurrentStatement
		( KW_END label=LIT_IDENTIFIER? TOK_SEMICOL )?
	;

rule_GenericClause
	: KW_GENERIC TOK_LP
			elements+=rule_InterfaceElement ( TOK_SEMICOL elements+=rule_InterfaceElement )* TOK_SEMICOL?
		TOK_RP TOK_SEMICOL
	;

// rule_GenericList
// moved into ???

rule_GenericMapAspect
	: KW_GENERIC KW_MAP TOK_LP
			associationList=rule_AssociationList
		TOK_RP
	;

// rule_GraphicCharacter
// handled by lexer


rule_GroupConstituent
	: rule_Name
	| LIT_CHARACTER
	;

// rule_GroupConstituentList
// moved into rule_GroupDeclaration

rule_GroupDeclaration
	: KW_GROUP name=LIT_IDENTIFIER TOK_COLON rule_Name
			TOK_LP constituents+=rule_GroupConstituent ( TOK_COMMA constituents+=rule_GroupConstituent )* TOK_RP
		TOK_SEMICOL
	;

rule_GroupTemplateDeclaration
	: KW_GROUP name=LIT_IDENTIFIER KW_IS
			TOK_LP entityClasses+=rule_EntityClassEntry ( TOK_COMMA entityClasses+=rule_EntityClassEntry )* TOK_RP
		TOK_SEMICOL
	;

rule_GuardedSignalSpecification
	: rule_SignalList TOK_COLON rule_Name
	;

// rule_Identifier
// handled by lexer

rule_IdentifierList
	: identifiers+=LIT_IDENTIFIER ( TOK_COMMA identifiers+=LIT_IDENTIFIER )*
	;

rule_IfGenerateStatement
	: label=LIT_IDENTIFIER TOK_COLON
		KW_IF ( ifAlternativeLabel=LIT_IDENTIFIER TOK_COLON )? ifCondition=rule_Expression KW_GENERATE
			ifBody=rule_GenerateStatementBody
		( KW_ELSIF ( elsifAlternativeLabel+=LIT_IDENTIFIER TOK_COLON )? elsifCondition+=rule_Expression KW_GENERATE
			elsifBody+=rule_GenerateStatementBody
		)*
		( KW_ELSE ( elseAlternativeLabel+=LIT_IDENTIFIER TOK_COLON )? KW_GENERATE
			elseBody=rule_GenerateStatementBody
		)?
		KW_END KW_GENERATE label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_IfStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_IF condition=rule_Expression KW_THEN
			thenStatements+=rule_SequentialStatement*
		( KW_ELSIF condition=rule_Expression KW_THEN
			elseifStatements+=rule_SequentialStatement*
		)*
		( KW_ELSE
			elseStatements+=rule_SequentialStatement*
		)?
		KW_END KW_IF label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_IncompleteSubtypeIndication
	: rule_SubtypeIndication
	| rule_UnspecifiedTypeIndication
	;

rule_IncompleteTypeDeclaration
	: KW_TYPE name=LIT_IDENTIFIER TOK_SEMICOL
	;

rule_IncompleteTypeDefinition
	: rule_PrivateIncompleteTypeDefinition
	| rule_ScalarIncompleteTypeDefinition
	| rule_DiscreteIncompleteTypeDefinition
	| rule_IntegerIncompleteTypeDefinition
	| rule_PhysicalIncompleteTypeDefinition
	| rule_FloatingIncompleteTypeDefinition
	| rule_ArrayIncompleteTypeDefinition
	| rule_AccessIncompleteTypeDefinition
	| rule_FileIncompleteTypeDefinition
	;

rule_IncompleteTypeMark
	: rule_Name
	| rule_UnspecifiedTypeIndication
	;

rule_IndexConstraint
	: TOK_LP ranges+=rule_DiscreteRange ( TOK_COMMA ranges+=rule_DiscreteRange )* TOK_RP
	;

// rule_IndexedName
// moed into rule_Name

//rule_IndexSpecification
//	: range=rule_DiscreteRange
//	| expression=rule_Expression
//	;

rule_IndexSubtypeDefinition
	: typeMark=rule_Name KW_RANGE TOK_BOX
	;

rule_InstantiatedUnit
	: component=KW_COMPONENT? componentName=rule_Name
	| KW_ENTITY entityName=rule_Name ( TOK_LP architectureName=LIT_IDENTIFIER TOK_RP )?
	| KW_CONFIGURATION configurationName=rule_Name
	;

rule_InstantiationList
	: componentNames+=LIT_IDENTIFIER ( TOK_COMMA componentNames+=LIT_IDENTIFIER )*
	| others=KW_OTHERS
	| all=KW_ALL
	;

// rule_Integer
// handled by lexer

rule_IntegerIncompleteTypeDefinition
	: KW_RANGE TOK_BOX
	;

rule_IntegerTypeDefinition
	: rule_RangeConstraint
	;

rule_InterfaceConstantDeclaration
	: KW_CONSTANT? constantNames=rule_IdentifierList TOK_COLON modeName=KW_IN? subtypeIndication=rule_SubtypeIndication
		( TOK_VAR_ASSIGN defaultValue=rule_Expression )?
	;

rule_InterfaceDeclaration
	: rule_InterfaceConstantDeclaration
//	| rule_InterfaceSignalDeclaration       -> directly used in rule_PortClause
	| rule_InterfaceVariableDeclaration
	| rule_InterfaceFileDeclaration
	| rule_InterfaceTypeDeclaration
	| rule_InterfaceSubprogramDeclaration
	| rule_InterfacePackageDeclaration
//  | interface_terminal_declaration
//  | interface_quantity_declaration
	;

// TODO: optimize this
rule_InterfaceElement
	: rule_InterfaceDeclaration
	;

rule_InterfaceFileDeclaration
	: KW_FILE names=rule_IdentifierList TOK_COLON subtypeIndication=rule_SubtypeIndication
	;

rule_InterfaceFunctionSpecification
	: ( KW_PURE | KW_IMPURE )? KW_FUNCTION rule_Designator
		( KW_PARAMETER? TOK_LP rule_FormalParameterList TOK_RP )?
		KW_RETURN rule_Name
	;

rule_InterfaceList
	: interfaceElements+=rule_InterfaceElement ( TOK_SEMICOL interfaceElements+=rule_InterfaceElement )* TOK_SEMICOL?
	;

// rule_InterfaceObjectDeclaration
// moved into rule_InterfaceDeclaration

rule_InterfacePackageDeclaration
	: KW_PACKAGE name=LIT_IDENTIFIER KW_IS
			KW_NEW rule_Name rule_InterfacePackageGenericMapAspect
	;

rule_InterfacePackageGenericMapAspect
	: rule_GenericMapAspect
	| KW_GENERIC KW_MAP TOK_LP ( TOK_BOX | KW_DEFAULT ) TOK_RP
	;

rule_InterfaceProcedureSpecification
	: KW_PROCEDURE name=LIT_IDENTIFIER
		( KW_PARAMETER? TOK_LP rule_FormalParameterList TOK_RP )?
	;

/*
interface_quantity_declaration
	: QUANTITY identifier_list TOK_COLON ( IN | OUT )? subtypeIndication=subtype_indication
		( TOK_VAR_ASSIGN expression )?
	;
*/

rule_InterfaceSignalDeclaration
	: KW_SIGNAL? rule_IdentifierList TOK_COLON modeName=rule_ModeIndication
	;

// rule_InterfaceSignalList
// merged into rule_InterfaceDeclaration, but directly used in rule_PortClause

rule_InterfaceSubprogramDeclaration
	: rule_InterfaceSubprogramSpecification ( KW_IS rule_InterfaceSubprogramDefault )?
	;

rule_InterfaceSubprogramDefault
	: rule_Name
	| TOK_BOX
	;

rule_InterfaceSubprogramSpecification
	: rule_InterfaceFunctionSpecification
	| rule_InterfaceProcedureSpecification
	;

rule_InterfaceTypeDeclaration
	: KW_TYPE name=LIT_IDENTIFIER ( KW_IS rule_IncompleteTypeDefinition )?
	;

rule_InterfaceTypeIndication
	: rule_SubtypeIndication
	| rule_UnspecifiedTypeIndication
	;

/*
interface_terminal_declaration
	: KW_TERMINAL identifier_list TOK_COLON subnature_indication
	;
*/

rule_InterfaceVariableDeclaration
	: KW_VARIABLE? names=rule_IdentifierList TOK_COLON
		modeName=rule_Mode? interfaceTypeIndication=rule_InterfaceTypeIndication ( TOK_VAR_ASSIGN expression=rule_ConditionalExpression )?
	;

rule_IterationScheme
	: KW_WHILE condition=rule_Expression
	| KW_FOR parameterSpecification=rule_ParameterSpecification
	;

// rule_Label
// moved into rules

// rule_Letter
// handled by lexer

// rule_LetterOrDigit
// handled by lexer

rule_LibraryClause
	: KW_LIBRARY names+=LIT_IDENTIFIER ( TOK_COMMA names+=LIT_IDENTIFIER )* TOK_SEMICOL
	;

rule_LibraryUnit
	: entity=rule_EntityDeclaration
	| configuration=rule_ConfigurationDeclaration
	| package=rule_PackageDeclaration
	| packageInstance=rule_PackageInstantiationDeclaration
	| context=rule_ContextDeclaration
	| architecture=rule_Architecture
	| packageBody=rule_PackageBody
//	| verificationUnit=rule_VerificationUnit
	;

rule_Literal
	: rule_NumericLiteral
	| rule_EnumerationLiteral
	| LIT_STRING
	| LIT_BIT_STRING
	| KW_NULL
	;

// rule_LogicalExpression
// moved into rule_Expression

// rule_LogicalName
// moved into many rules

// rule_LogicalNameList
// moved into many rules

// rule_LogicalOperator
// moved into rule_LogicalExpression

rule_LoopStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
		scheme=rule_IterationScheme? KW_LOOP
			statements+=rule_SequentialStatement*
		KW_END KW_LOOP label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

// rule_MiscellaneousOperator
// moved into ???

rule_Mode
	: name=( KW_IN	| KW_OUT | KW_INOUT	| KW_BUFFER	| KW_LINKAGE )
	;

rule_ModeIndication
	: rule_SimpleModeIndication
	| rule_ArrayModeViewIndication
	| rule_RecordModeViewIndication
	;

rule_ModeViewDeclaration
	: KW_VIEW name=LIT_IDENTIFIER KW_OF rule_SubtypeIndication KW_IS
			rule_ModeViewElementDefinition*
		KW_END KW_VIEW name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_ModeViewElementDefinition
	: rule_RecordElementList TOK_COLON rule_ElementModeIndication TOK_SEMICOL
	;

// rule_ModeViewIndication
// moved into rule_ModeIndication

// rule_MultiplyingOperator
// moved into rule_Term

rule_Name
	: LIT_IDENTIFIER                                                                                                                        #rule_SimpleName
	| LIT_STRING                                                                                                                            #rule_Operator
	| LIT_CHARACTER                                                                                                                         #rule_Char
	| prefix=rule_Name TOK_DOT rule_Suffix                                                                                                  #rule_SelectedName    // prefix.suffix
	| prefix=rule_Name TOK_LP expressions+=rule_Expression ( TOK_COMMA expressions+=rule_Expression )* TOK_RP                               #rule_IndexedName     // prefix ( expr , expr )             prefix -> name | functionCall
	| prefix=rule_Name TOK_LP rule_DiscreteRange TOK_RP                                                                                     #rule_SliceName       // prefix ( left direction right )
	| prefix=rule_Name signature=rule_Signature? TOK_TICK designator=rule_AttributeDesignator ( TOK_LP expression=rule_Expression TOK_RP )? #rule_AttributeName   // prefix ' id
	| rule_ExternalName                                                                                                                     #rule_External
	;

rule_NextStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_NEXT referencedLabel=LIT_IDENTIFIER?
			( KW_WHEN condition=rule_Expression )?
		TOK_SEMICOL
	;

rule_NullStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_NULL TOK_SEMICOL
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

rule_NumericLiteral
	: LIT_ABSTRACT
	| rule_PhysicalLiteral
	;

// rule_ObjectDeclaration
// unused rule

rule_PackageBody
	: KW_PACKAGE KW_BODY name=LIT_IDENTIFIER KW_IS
			declarativeItem+=rule_PackageBodyDeclarativeItem*
		KW_END ( KW_PACKAGE KW_BODY )? name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_PackageBodyDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramBody
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageBody
	| rule_PackageInstantiationDeclaration
	| rule_TypeDeclaration
	| rule_SubtypeDeclaration
	| rule_ConstantDeclaration
	| rule_VariableDeclaration
	| rule_FileDeclaration
	| rule_AliasDeclaration
	| rule_AttributeDeclaration
	| rule_AttributeSpecification
	| rule_UseClause
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
	;

// rule_PackageBodyDeclarativePart
// moved into rule_PackageBody

rule_PackageDeclaration
	: KW_PACKAGE name=LIT_IDENTIFIER KW_IS
			genericClause=rule_GenericClause?
			declarativeItems+=rule_PackageDeclarativeItem*
		KW_END KW_PACKAGE? name2=LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_PackageDeclarativeItem
	: subprogramDeclaration=rule_SubprogramDeclaration
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageInstantiationDeclaration
	| typeDeclaration=rule_TypeDeclaration
	| subtypeDeclaration=rule_SubtypeDeclaration
	| constantDeclaration=rule_ConstantDeclaration
	| signalDeclaration=rule_SignalDeclaration
	| variableDeclaration=rule_VariableDeclaration         // TODO: isn't it only shared variables?
	| fileDeclaration=rule_FileDeclaration
	| aliasDeclaration=rule_AliasDeclaration
	| componentDeclaration=rule_ComponentDeclaration
	| attributeDeclaration=rule_AttributeDeclaration
	| attributeSpecification=rule_AttributeSpecification
	| disconnectionSpecification=rule_DisconnectionSpecification
	| useClause=rule_UseClause
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
//  | nature_declaration
//  | subnature_declaration
//  | terminal_declaration
	;

// rule_PackageDeclarativePart
// moved into rule_PackageDeclaration

// rule_PackageHeader
// moved into rule_PackageDeclaration

rule_PackageInstantiationDeclaration
	: KW_PACKAGE name=LIT_IDENTIFIER KW_IS
			KW_NEW rule_Name
			( genericMasAspect=rule_GenericMapAspect )?
		TOK_SEMICOL
	;

// TODO: why * for /package/SimpleName
rule_PackagePathname
	: TOK_AT libraryName=LIT_IDENTIFIER TOK_DOT ( packageName=LIT_IDENTIFIER TOK_DOT )* objectName=LIT_IDENTIFIER
	;

rule_ParameterMapAspect
	: ( KW_PARAMETER KW_MAP )? TOK_LP rule_AssociationList TOK_RP
	;

rule_ParameterSpecification
	: LIT_IDENTIFIER KW_IN rule_DiscreteRange
	;

rule_PartialPathname
	: ( rule_PathnameElement TOK_DOT )* LIT_IDENTIFIER
	;

rule_PathnameElement
	: nameOrLabel=LIT_IDENTIFIER
	;

rule_PhysicalIncompleteTypeDefinition
	: KW_UNITS TOK_BOX
	;

rule_PhysicalLiteral
	: LIT_ABSTRACT? rule_Name
	;

rule_PhysicalTypeDefinition
	: rangeConstraint=rule_RangeConstraint KW_UNITS
			primaryUnit=LIT_IDENTIFIER TOK_SEMICOL
			secondaryUnits+=rule_SecondaryUnitDeclaration*
		KW_END KW_UNITS name2=LIT_IDENTIFIER?
	;

rule_PlainReturnStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_RETURN
			( KW_WHEN condition=rule_Expression )?
		TOK_SEMICOL
	;

rule_PortClause
	: KW_PORT TOK_LP
			ports+=rule_InterfaceSignalDeclaration ( TOK_SEMICOL ports+=rule_InterfaceSignalDeclaration )* TOK_SEMICOL?
		TOK_RP TOK_SEMICOL
	;

// rule_PortList
// moved into rule_PortClause

rule_PortMapAspect
	: KW_PORT KW_MAP TOK_LP
			associationList=rule_AssociationList
		TOK_RP
	;

// rule_Prefix
// merged into rule_Name

rule_Primary
	: rule_Name
	| rule_Literal
	| rule_Aggregate
	| rule_FunctionCall
	| rule_QualifiedExpression
	| rule_TypeConversion
	| rule_Allocator
	| TOK_LP expression=rule_Expression TOK_RP
	;

// rule_PrimaryUnitDeclaration
// moved into rule_PhysicalTypeDefinition

rule_PrivateVariableDeclaration
	: KW_PRIVATE rule_VariableDeclaration
	;

rule_PrivateIncompleteTypeDefinition
	: KW_PRIVATE
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
  | group_template_declaration
  | group_declaration
	;

procedural_declarative_part
	: ( procedural_declarative_item )*
	;

procedural_statement_part
	: ( sequential_statement )*
	;
*/

rule_ProcedureCall
	: rule_Name
			genericMapAspect=rule_GenericMapAspect?
			parameterMapAspect=rule_ParameterMapAspect?
	;

rule_ProcedureCallStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? rule_ProcedureCall TOK_SEMICOL
	;

rule_ProcedureSpecification
	: KW_PROCEDURE name=LIT_IDENTIFIER
		// TODO: subprogram header
		( KW_PARAMETER? TOK_LP rule_FormalParameterList TOK_RP )?
	;

rule_ProcessDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramBody
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageBody
	| rule_PackageInstantiationDeclaration
	| rule_TypeDeclaration
	| rule_SubtypeDeclaration
	| rule_ConstantDeclaration
	| rule_VariableDeclaration
	| rule_FileDeclaration
	| rule_AliasDeclaration
	| rule_AttributeDeclaration
	| rule_AttributeSpecification
	| rule_UseClause
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
	;

// rule_ProcessDeclarativePart
// moved into rule_ProcessStatement, rule_PostponedProcessStatement

rule_ProcessSensitivityList
	: rule_SensitivityList
	| KW_ALL
	;

rule_ProcessStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_PROCESS
			( TOK_LP rule_ProcessSensitivityList TOK_RP )?
		KW_IS?
			declaredItems+=rule_ProcessDeclarativeItem*
		KW_BEGIN
			statements+=rule_SequentialStatement*
		KW_END KW_PROCESS LIT_IDENTIFIER? TOK_SEMICOL
	;

rule_PostponedProcessStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_POSTPONED KW_PROCESS
			( TOK_LP rule_SensitivityList TOK_RP )?
		KW_IS?
			declaredItems+=rule_ProcessDeclarativeItem*
		KW_BEGIN
			statements+=rule_SequentialStatement*
		KW_END KW_POSTPONED? KW_PROCESS LIT_IDENTIFIER? TOK_SEMICOL
	;

// rule_ProcessStatementPart
// moved into rule_ProcessStatement, rule_PostponedProcessStatement

// TODO: where the semicolon?
rule_ProtectedTypeBody
	: KW_PROTECTED KW_BODY
			declaredItems+=rule_ProtectedTypeBodyDeclarativeItem*
		KW_END KW_PROTECTED KW_BODY name2=LIT_IDENTIFIER?
	;

// TODO: same as rule_ProcessDeclarativeItem
rule_ProtectedTypeBodyDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramBody
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageBody
	| rule_PackageInstantiationDeclaration
	| rule_TypeDeclaration
	| rule_SubtypeDeclaration
	| rule_ConstantDeclaration
	| rule_VariableDeclaration
	| rule_FileDeclaration
	| rule_AliasDeclaration
	| rule_AttributeDeclaration
	| rule_AttributeSpecification
	| rule_UseClause
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
	;

// rule_ProtectedTypeBodyDeclarativePart
// moved into rule_ProtectedTypeBody

rule_ProtectedTypeDeclaration
	: KW_PROTECTED
			// TODO: protected type header
			declaredItems+=rule_ProtectedTypeDeclarativeItem*
		KW_END KW_PROTECTED name2=LIT_IDENTIFIER?
	;

// TODO: same as
rule_ProtectedTypeDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramInstantiationDeclaration
	| rule_PrivateVariableDeclaration
	| rule_AliasDeclaration
	| rule_AttributeSpecification
	| rule_UseClause
	;

// rule_ProtectedTypeDeclarativePart
// moved into rule_ProtectedType

rule_ProtectedTypeDefinition
	: rule_ProtectedTypeDeclaration
	| rule_ProtectedTypeBody
	;

rule_ProtectedTypeInstantiationDefinition
	: KW_NEW rule_Name
			genericMapAspect=rule_GenericMapAspect?
	;

// TODO: combine into expression
rule_QualifiedExpression
	: typeMark=rule_Name TOK_TICK  (
		| TOK_LP expression=rule_Expression TOK_RP
		|	aggregate=rule_Aggregate
		)
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

rule_Range
	: rule_Name
	| rule_SimpleRange
	| rule_Expression
	;

rule_RangeConstraint
	: KW_RANGE rule_Range
	;

/*
record_nature_definition
	: RECORD ( nature_element_declaration )+
		END RECORD ( LIT_IDENTIFIER )?
	;
*/

rule_RecordConstraint
	: TOK_LP rule_RecordElementConstraint ( TOK_COMMA rule_RecordElementConstraint )* TOK_RP
	;

rule_RecordElementConstraint
	: LIT_IDENTIFIER rule_ElementConstraint
	;

rule_RecordElementList
	: elements+=LIT_IDENTIFIER ( TOK_COMMA elements+=LIT_IDENTIFIER )*
	;

rule_RecordElementResolution
	: LIT_IDENTIFIER rule_ResolutionIndication
	;

rule_RecordResolution
	: rule_RecordElementResolution ( TOK_COMMA rule_RecordElementResolution )*
	;

rule_RecordTypeDefinition
	: KW_RECORD
			elements+=rule_ElementDeclaration*
		KW_END KW_RECORD name2=LIT_IDENTIFIER?
	;

rule_RecordModeViewIndication
	: KW_VIEW rule_Name
		( KW_OF rule_SubtypeIndication )?
	;

// rule_Relation
// moved into rule_Expression

rule_RelativePathname
	: ( TOK_CIRCUMFLEX TOK_DOT )* rule_PartialPathname
	;

rule_ReportStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
			KW_REPORT reportExpression=rule_Expression
			( KW_SEVERITY severityExpression=rule_Expression )?
		TOK_SEMICOL
	;

rule_ResolutionIndication
	: rule_Name
	| TOK_LP rule_ElementResolution TOK_RP
	;

rule_ReturnStatement
	: rule_PlainReturnStatement
	| rule_ValueReturnStatement
	;
// ( label=LIT_IDENTIFIER TOK_COLON )? KW_RETURN expression=rule_Expression? TOK_SEMICOL

rule_ScalarIncompleteTypeDefinition
	: TOK_BOX
	;

/*
scalar_nature_definition
	: name ACROSS name THROUGH name REFERENCE
	;
*/

rule_ScalarTypeDefinition
	: rule_EnumerationTypeDefinition
	| rule_IntegerTypeDefinition
	| rule_FloatingTypeDefinition
	| rule_PhysicalTypeDefinition
	;

rule_SecondaryUnitDeclaration
	: name=LIT_IDENTIFIER OP_EQ value=LIT_ABSTRACT? unit=LIT_IDENTIFIER TOK_SEMICOL
	;

rule_SelectedExpressions
	: ( rule_Expression KW_WHEN rule_Choices TOK_COMMA )*
		rule_Expression KW_WHEN rule_Choices
	;

rule_SelectedForceAssignment
	: KW_WITH rule_Expression KW_SELECT TOK_QUESTION?
			rule_Target TOK_SIG_ASSIGN KW_FORCE forceMode=( KW_IN | KW_OUT ) rule_SelectedExpressions TOK_SEMICOL
	;

rule_SelectedName2
	: names+=LIT_IDENTIFIER ( TOK_DOT names+=LIT_IDENTIFIER )+
	| names+=LIT_IDENTIFIER ( TOK_DOT names+=LIT_IDENTIFIER )* TOK_DOT KW_ALL
	;

rule_SelectedSignalAssignment
	: rule_SelectedWaveformAssignment
	| rule_SelectedForceAssignment
	;

rule_SelectedVariableAssignment
	: KW_WITH expression=rule_Expression KW_SELECT TOK_QUESTION?
			target=rule_Target TOK_VAR_ASSIGN rule_SelectedExpressions
		TOK_SEMICOL
	;

rule_SelectedWaveformAssignment
	: KW_WITH expression=rule_Expression KW_SELECT TOK_QUESTION?
			target=rule_Target TOK_SIG_ASSIGN rule_DelayMechanism waveform=rule_SelectedWaveforms
		TOK_SEMICOL
	;

rule_SelectedWaveforms
	: ( rule_Waveform KW_WHEN rule_Choices TOK_COMMA )*
		rule_Waveform KW_WHEN rule_Choices
	;

rule_SensitivityClause
	: KW_ON sensitivityList=rule_SensitivityList
	;

// TODO: merge?
rule_SensitivityList
	: name+=rule_Name ( TOK_COMMA name+=rule_Name )*
	;

// rule_SequenceOfStatements
// moved into ???

rule_SequentialBlockStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
		KW_BLOCK KW_IS?
			declaredItems+=rule_ProcessDeclarativeItem*
		KW_BEGIN
			statements+=rule_SequentialStatement*
		KW_END KW_BLOCK? label2=LIT_IDENTIFIER? TOK_SEMICOL
	;

// rule_SequentialBlockDeclarativePart
// moved into rule_SequentialBlockStatement

// rule_SequentialBlockStatementPart
// moved into rule_SequentialBlockStatement

rule_SequentialStatement
	: rule_WaitStatement
	| rule_AssertionStatement
	| rule_ReportStatement
	| rule_SignalAssignmentStatement
	| rule_VariableAssignmentStatement
	| rule_ProcedureCallStatement
	| rule_IfStatement
	| rule_CaseStatement
	| rule_LoopStatement
	| rule_NextStatement
	| rule_ExitStatement
	| rule_ReturnStatement
	| rule_NullStatement
	| rule_SequentialBlockStatement
//  | break_statement

	;

// rule_ShiftExpression
// moved into rule_Expression

// rule_ShiftOperator
// moved into rule_ShiftExpression

// rule_Sign
// handled by lexer

rule_SignalAssignmentStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? (
				rule_SimpleSignalAssignment
			| rule_ConditionalSignalAssignment
			| rule_SelectedSignalAssignment
		)
	;

rule_SignalDeclaration
	: KW_SIGNAL names=rule_IdentifierList TOK_COLON
		subtypeIndication=rule_SubtypeIndication signalKind=( KW_REGISTER | KW_BUS )? ( TOK_VAR_ASSIGN expression=rule_Expression )? TOK_SEMICOL
	;

// rule_SignalKind
// moved into rule_SignalDeclaration

rule_SignalList
	: names+=rule_Name ( TOK_COMMA names+=rule_Name )*
	| others=KW_OTHERS
	| all=KW_ALL
	;

rule_Signature
	: TOK_LB
			( names+=rule_Name ( TOK_COMMA names+=rule_Name )* )?
			( KW_RETURN returnName=rule_Name )?
		TOK_RB
	;

// TODO: double semicol
rule_SimpleConfigurationSpecification
	: KW_FOR rule_ComponentSpecification rule_BindingIndication TOK_SEMICOL
		( KW_END KW_FOR TOK_SEMICOL )?
	;

// rule_SimpleExpression
// moved into rule_Expression

rule_SimpleForceAssignment
	: rule_Target TOK_SIG_ASSIGN KW_FORCE forceMode=( KW_IN | KW_OUT ) rule_ConditionalOrUnaffectedExpression TOK_SEMICOL
	;

rule_SimpleModeIndication
	: rule_Mode? rule_InterfaceTypeIndication KW_BUS?
		( TOK_VAR_ASSIGN rule_ConditionalExpression )?
	;

// rule_SimpleName
// moved to many rules

rule_SimpleRange
	: leftBound=rule_Expression direction=rule_Direction rightBound=rule_Expression
	;

rule_SimpleReleaseAssignment
	: rule_Target TOK_SIG_ASSIGN forceMode=( KW_IN | KW_OUT ) TOK_SEMICOL
	;

rule_SimpleSignalAssignment
	: rule_SimpleWaveformAssignment
	| rule_SimpleForceAssignment
	| rule_SimpleReleaseAssignment
	;

rule_SimpleWaveformAssignment
	: rule_Target TOK_SIG_ASSIGN rule_DelayMechanism? rule_Waveform TOK_SEMICOL
	;

rule_SimpleVariableAssignment
	: rule_Target TOK_VAR_ASSIGN rule_ConditionalOrUnaffectedExpression TOK_SEMICOL
	;

// rule_SliceName
// moved into rule_Name

// rule_StringLiteral
// handled by lexer

/*
rule_SimpleSimultaneousStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
		rule_SimpleExpression TOK_SIG_ASSIGN rule_SimpleExpression ( tolerance_aspect )? TOK_SEMICOL
	;

rule_SimultaneousAlternative
	: KW_WHEN rule_Choices TOK_RARROW simultaneous_statement_part
	;

simultaneous_case_statement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_CASE expression=rule_Expression KW_USE
			rule_SimultaneousAlternative+
		KW_END KW_CASE LIT_IDENTIFIER? TOK_SEMICOL
	;

simultaneous_if_statement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_IF condition=rule_Expression KW_USE
			simultaneous_statement_part
		( KW_ELSIF condition=rule_Expression KW_USE
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
	| ( label=LIT_IDENTIFIER TOK_COLON )? KW_NULL TOK_SEMICOL
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
			declaredItems+=rule_SubprogramDeclarativeItem*
		KW_BEGIN
			statements+=rule_SequentialStatement*
		KW_END rule_SubprogramKind? rule_Designator? TOK_SEMICOL
	;

rule_SubprogramDeclaration
	: rule_SubprogramSpecification TOK_SEMICOL
	;

rule_SubprogramDeclarativeItem
	: rule_SubprogramDeclaration
	| rule_SubprogramBody
	| rule_SubprogramInstantiationDeclaration
	| rule_PackageDeclaration
	| rule_PackageBody
	| rule_PackageInstantiationDeclaration
	| rule_TypeDeclaration
	| rule_SubtypeDeclaration
	| rule_ConstantDeclaration
	| rule_VariableDeclaration
	| rule_FileDeclaration
	| rule_AliasDeclaration
	| rule_AttributeDeclaration
	| rule_AttributeSpecification
	| rule_UseClause
  | rule_GroupTemplateDeclaration
  | rule_GroupDeclaration
	;

// rule_SubprogramDeclarativePart
// moved into rule_SubprogramBody

// rule_SubprogramHeader
// moved into rule_SubprogramSpecification

rule_SubprogramInstantiationDeclaration
	: rule_SubprogramKind name=LIT_IDENTIFIER KW_IS
			KW_NEW rule_Name rule_Signature?
				genericMapAspect=rule_GenericMapAspect?
		TOK_SEMICOL
	;

rule_SubprogramKind
	: KW_PROCEDURE
	| KW_FUNCTION
	;

rule_SubprogramSpecification
	: rule_ProcedureSpecification
	| rule_FunctionSpecification
	;

// rule_SubprogramStatementPart
// moved into rule_SubprogramBody

rule_SubtypeDeclaration
	: KW_SUBTYPE name=LIT_IDENTIFIER KW_IS subtypeIndication=rule_SubtypeIndication TOK_SEMICOL
	;

rule_SubtypeIndication
	: rule_ResolutionIndication? rule_Name rule_Constraint? /* ( tolerance_aspect )? */
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

// TODO: combine into expression? Sven?
// rule_Term
// moved into rule_Expression

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
	: KW_FOR expression=rule_Expression
	;

/*
tolerance_aspect
	: TOLERANCE expression
	;
*/

// rule_ToolDirective
// handled by lexer

rule_TypeConversion
	: rule_Name TOK_LP rule_Expression TOK_RP
	;

rule_TypeDeclaration
	: rule_FullTypeDeclaration
	| rule_IncompleteTypeDeclaration
	;

rule_TypeDefinition
	: rule_ScalarTypeDefinition
	| rule_CompositeTypeDefinition
	| rule_AccessTypeDefinition
	| rule_FileTypeDefinition
	| rule_ProtectedTypeDefinition
	| rule_ProtectedTypeInstantiationDefinition
	;

// rule_TypeMark
// moved into multiple rules

// rule_UnaryExpression
// moved into rule_Expression

// rule_UnaryMiscellaneousOperator
// unused rule

rule_UnboundArrayDefinition
	: KW_ARRAY TOK_LP rule_IndexSubtypeDefinition ( TOK_COMMA rule_IndexSubtypeDefinition )* TOK_RP
			KW_OF subtypeIndication=rule_SubtypeIndication
	;

rule_UnspecifiedTypeIndication
	: KW_TYPE KW_IS rule_IncompleteTypeDefinition
	;

/*
unconstrained_nature_definition
	: KW_ARRAY TOK_LP index_subtype_definition ( TOK_COMMA index_subtype_definition )*
		TOK_RP OF subnature_indication
	;
*/

rule_UseClause
	: KW_USE names+=rule_SelectedName2 ( TOK_COMMA names+=rule_SelectedName2 )* TOK_SEMICOL
	;

rule_ValueReturnStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )?
		KW_RETURN rule_ConditionalOrUnaffectedExpression TOK_SEMICOL
	;

rule_VariableAssignmentStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? (
				rule_SimpleVariableAssignment
			| rule_SelectedVariableAssignment
		)
	;

// TODO: split rule
rule_VariableDeclaration
	: KW_SHARED? KW_VARIABLE rule_IdentifierList TOK_COLON
		subtypeIndication=rule_SubtypeIndication
		( genericMapAspect=rule_GenericMapAspect )?
		( TOK_VAR_ASSIGN expression=rule_Expression )? TOK_SEMICOL
	;

rule_WaitStatement
	: ( label=LIT_IDENTIFIER TOK_COLON )? KW_WAIT
			rule_SensitivityClause?
			rule_ConditionClause?
			rule_TimeoutClause?
		TOK_SEMICOL
	;

rule_Waveform
	: waveformElement+=rule_WaveformElement ( TOK_COMMA waveformElement+=rule_WaveformElement )*
	| KW_UNAFFECTED
	;

rule_WaveformElement
	: expression=rule_Expression ( KW_AFTER afterExpression=rule_Expression )?
	| KW_NULL ( KW_AFTER afterExpression=rule_Expression )?
	;
