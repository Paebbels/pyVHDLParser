parser grammar VHDLParser;

options {
	tokenVocab = VHDLLexer;
}

// TODO: Context
// TODO: Protzected Type
// TODO: PSL
// TODO: VHDL-2019
// TODO: VHDL-AMS

access_type_definition
  : KW_ACCESS subtype_indication
  ;

/*
across_aspect
  : identifier_list ( tolerance_aspect )? ( TOK_VAR_ASSIGN expression )? ACROSS
  ;
*/

actual_designator
  : expression
  | KW_OPEN
  ;

actual_parameter_part
  : association_list
  ;

actual_part
  : name TOK_LP actual_designator TOK_RP
  | actual_designator
  ;

// TODO: combine into expression
adding_operator
  : OP_PLUS
  | OP_MINUS
  | OP_CONCAT
  ;

aggregate
  : TOK_LP element_association ( TOK_COMMA element_association )* TOK_RP
  ;

alias_declaration
  : KW_ALIAS alias_designator ( TOK_COLON alias_indication )?
      KW_IS name ( signature )?
    TOK_SEMICOL
  ;

alias_designator
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  | LIT_STRING
  ;

alias_indication
  : /* subnature_indication
  | */ subtype_indication
  ;

allocator
  : KW_NEW (
      qualified_expression
    | subtype_indication
    )
  ;

architecture_body
  : KW_ARCHITECTURE LIT_IDENTIFIER KW_OF LIT_IDENTIFIER KW_IS
      architecture_declarative_part
    KW_BEGIN
      architecture_statement_part
    KW_END KW_ARCHITECTURE? LIT_IDENTIFIER? TOK_SEMICOL
  ;

architecture_declarative_part
  : block_declarative_item*
  ;

architecture_statement
  : block_statement
  | process_statement
  | postponed_process_statement
  | label_colon? concurrent_procedure_call_statement
  | label_colon? concurrent_assertion_statement
  | label_colon? KW_POSTPONED? concurrent_signal_assignment_statement
  | component_instantiation_statement
  | generate_statement
//  | concurrent_break_statement
  | simultaneous_statement
  ;

architecture_statement_part
  : architecture_statement*
  ;

/*
array_nature_definition
  : unconstrained_nature_definition
  | constrained_nature_definition
  ;
*/

array_type_definition
  : unconstrained_array_definition
  | constrained_array_definition
  ;

assertion
  : KW_ASSERT condition
    ( KW_REPORT expression )?
    ( KW_SEVERITY expression )?
  ;

assertion_statement
  : label_colon? assertion TOK_SEMICOL
  ;

association_element
  : ( formal_part TOK_RARROW )? actual_part
  ;

association_list
  : association_element ( TOK_COMMA association_element )*
  ;

// TODO: why label_colon and why just name?
attribute_declaration
  : KW_ATTRIBUTE label_colon name TOK_SEMICOL
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

attribute_designator
  : LIT_IDENTIFIER
  ;

attribute_specification
  : KW_ATTRIBUTE attribute_designator
      KW_OF entity_specification
      KW_IS expression
    TOK_SEMICOL
  ;

base_unit_declaration
  : LIT_IDENTIFIER TOK_SEMICOL
  ;

binding_indication
  : ( KW_USE entity_aspect )?
      generic_map_aspect?
      port_map_aspect?
  ;

block_configuration
  : KW_FOR block_specification
      use_clause*
      configuration_item*
    KW_END KW_FOR TOK_SEMICOL
  ;

block_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | signal_declaration
  | variable_declaration
  | file_declaration
  | alias_declaration
  | component_declaration
  | attribute_declaration
  | attribute_specification
  | configuration_specification
  | disconnection_specification
//  | step_limit_specification
  | use_clause
//  | group_template_declaration
//  | group_declaration
//  | nature_declaration
//  | subnature_declaration
//  | quantity_declaration
//  | terminal_declaration
  ;

block_declarative_part
  : block_declarative_item*
  ;

block_header
  : ( generic_clause ( generic_map_aspect TOK_SEMICOL )? )?
    ( port_clause    ( port_map_aspect    TOK_SEMICOL )? )?
  ;

block_specification
  : LIT_IDENTIFIER ( TOK_LP index_specification TOK_RP )?
  | name
  ;

block_statement
  : label_colon KW_BLOCK ( TOK_LP expression TOK_RP )? KW_IS?
      block_header
      block_declarative_part
    KW_BEGIN
      block_statement_part
    KW_END KW_BLOCK LIT_IDENTIFIER? TOK_SEMICOL
  ;

block_statement_part
  : architecture_statement*
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

case_statement
  : label_colon? KW_CASE expression KW_IS
      case_statement_alternative+
    KW_END KW_CASE LIT_IDENTIFIER? TOK_SEMICOL
  ;

case_statement_alternative
  : KW_WHEN choices TOK_RARROW sequence_of_statements
  ;

choice
  : LIT_IDENTIFIER
  | discrete_range
  | simple_expression
  | KW_OTHERS
  ;

choices
  : choice ( TOK_BAR choice )*
  ;

component_configuration
  : KW_FOR component_specification
      ( binding_indication TOK_SEMICOL )?
      block_configuration?
    KW_END KW_FOR TOK_SEMICOL
  ;

component_declaration
  : KW_COMPONENT LIT_IDENTIFIER KW_IS?
      generic_clause?
      port_clause?
    KW_END KW_COMPONENT LIT_IDENTIFIER? TOK_SEMICOL
  ;

component_instantiation_statement
  : label_colon instantiated_unit
      generic_map_aspect?
      port_map_aspect?
    TOK_SEMICOL
  ;

component_specification
  : instantiation_list TOK_COLON name
  ;

/*
composite_nature_definition
  : array_nature_definition
  | record_nature_definition
  ;
*/

composite_type_definition
  : array_type_definition
  | record_type_definition
  ;

concurrent_assertion_statement
  : label_colon? KW_POSTPONED? assertion TOK_SEMICOL
  ;

/*
concurrent_break_statement
  : ( label_colon )? BREAK ( break_list )? ( sensitivity_clause )?
    ( WHEN condition )? TOK_SEMICOL
  ;
*/

concurrent_procedure_call_statement
  : label_colon? KW_POSTPONED? procedure_call TOK_SEMICOL
  ;

concurrent_signal_assignment_statement
  : label_colon? KW_POSTPONED? (
      conditional_signal_assignment
    | selected_signal_assignment
    )
  ;

// TODO: combine into expression
condition
  : expression
  ;

condition_clause
  : KW_UNTIL condition
  ;

conditional_signal_assignment
  : target TOK_SIG_ASSIGN opts conditional_waveforms TOK_SEMICOL
  ;

conditional_waveforms
  : waveform ( KW_WHEN condition ( KW_ELSE conditional_waveforms )? )?
  ;

configuration_declaration
  : KW_CONFIGURATION LIT_IDENTIFIER KW_OF name KW_IS
      configuration_declarative_part
      block_configuration
    KW_END KW_CONFIGURATION? LIT_IDENTIFIER? TOK_SEMICOL
  ;

configuration_declarative_item
  : use_clause
  | attribute_specification
//  | group_declaration
  ;

configuration_declarative_part
  : configuration_declarative_item*
  ;

configuration_item
  : block_configuration
  | component_configuration
  ;

configuration_specification
  : KW_FOR component_specification binding_indication TOK_SEMICOL
  ;

constant_declaration
  : KW_CONSTANT identifier_list TOK_COLON subtype_indication
    ( TOK_VAR_ASSIGN expression )? TOK_SEMICOL
  ;

constrained_array_definition
  : KW_ARRAY index_constraint KW_OF subtype_indication
  ;

/*
constrained_nature_definition
  : KW_ARRAY index_constraint KW_OF subnature_indication
  ;
*/

constraint
  : range_constraint
  | index_constraint
  ;

context_clause
  : context_item*
  ;

context_item
  : library_clause
  | use_clause
  ;

delay_mechanism
  : KW_TRANSPORT
  | ( KW_REJECT expression )? KW_INERTIAL
  ;

design_file
  : designUnits+=design_unit*
    EOF
  ;

design_unit
  : contextClause=context_clause
    libraryUnit=library_unit
  ;

designator
  : LIT_IDENTIFIER
  | LIT_STRING     // TODO: should be limited to operator names
  ;

direction
  : KW_TO
  | KW_DOWNTO
  ;

disconnection_specification
  : KW_DISCONNECT guarded_signal_specification
      KW_AFTER expression
    TOK_SEMICOL
  ;

discrete_range
  : range_decl
  | subtype_indication
  ;

element_association
  : ( choices TOK_RARROW )? expression
  ;

element_declaration
  : identifier_list TOK_COLON element_subtype_definition TOK_SEMICOL
  ;

/*
element_subnature_definition
  : subnature_indication
  ;
*/

element_subtype_definition
  : subtype_indication
  ;

entity_aspect
  : KW_ENTITY name ( TOK_LP LIT_IDENTIFIER TOK_RP )?
  | KW_CONFIGURATION name
  | KW_OPEN
  ;

entity_class
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

entity_class_entry
  : entity_class TOK_BOX?
  ;

entity_class_entry_list
  : entity_class_entry ( TOK_COMMA entity_class_entry )*
  ;

entity_declaration
  : KW_ENTITY entityName=LIT_IDENTIFIER KW_IS
      header=entity_header
      declarativePart=entity_declarative_part
    ( KW_BEGIN
      statementPart=entity_statement_part
    )?
    KW_END KW_ENTITY? entityName2=LIT_IDENTIFIER? TOK_SEMICOL
  ;

entity_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | signal_declaration
  | variable_declaration
  | file_declaration
  | alias_declaration
  | attribute_declaration
  | attribute_specification
  | disconnection_specification
//  | step_limit_specification
  | use_clause
//  | group_template_declaration
//  | group_declaration
//  | nature_declaration
//  | subnature_declaration
//  | quantity_declaration
//  | terminal_declaration
  ;

entity_declarative_part
  : entity_declarative_item*
  ;

entity_designator
  : entity_tag signature?
  ;

entity_header
  : genericClause=generic_clause?
    portClause=port_clause?
  ;

entity_name_list
  : entity_designator ( TOK_COMMA entity_designator )*
  | KW_OTHERS
  | KW_ALL
  ;

entity_specification
  : entity_name_list TOK_COLON entity_class
  ;

entity_statement
  : concurrent_assertion_statement
  | process_statement
  | postponed_process_statement
  | concurrent_procedure_call_statement
  ;

entity_statement_part
  : entity_statement*
  ;

entity_tag
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  | LIT_STRING
  ;

enumeration_literal
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  ;

enumeration_type_definition
  : TOK_LP enumeration_literal ( TOK_COMMA enumeration_literal )* TOK_RP
  ;

exit_statement
  : label_colon? KW_EXIT LIT_IDENTIFIER? ( KW_WHEN condition )? TOK_SEMICOL
  ;

// TODO: combine into expression
expression
  : relation (: logical_operator relation )*
  ;

// TODO: combine into expression
factor
  : primary ( : OP_POW primary )?
  | OP_ABS primary
  | OP_NOT primary
  ;

file_declaration
  : KW_FILE identifier_list TOK_COLON subtype_indication
    file_open_information? TOK_SEMICOL
  ;

file_logical_name
  : expression
  ;

file_open_information
  : ( KW_OPEN expression )? KW_IS file_logical_name
  ;

file_type_definition
  : KW_FILE KW_OF subtype_indication
  ;

formal_parameter_list
  : interface_list
  ;

formal_part
  : LIT_IDENTIFIER
  | LIT_IDENTIFIER TOK_LP explicit_range  TOK_RP
  ;

/*
free_quantity_declaration
  : QUANTITY identifier_list TOK_COLON subtype_indication
    ( TOK_VAR_ASSIGN expression )? TOK_SEMICOL
  ;
*/

generate_statement
  : label_colon
    generation_scheme KW_GENERATE
      ( block_declarative_item*
    KW_BEGIN
    )?
      architecture_statement*
    KW_END KW_GENERATE LIT_IDENTIFIER? TOK_SEMICOL
  ;

generation_scheme
  : KW_FOR parameter_specification
  | KW_IF condition
  ;

generic_clause
  : KW_GENERIC TOK_LP generics=generic_list TOK_RP TOK_SEMICOL
  ;

generic_list
  : constants+=interface_constant_declaration ( TOK_SEMICOL constants+=interface_constant_declaration )*
  ;

generic_map_aspect
  : KW_GENERIC KW_MAP TOK_LP
      association_list
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

guarded_signal_specification
  : signal_list TOK_COLON name
  ;

/*
identifier
  : BASIC_IDENTIFIER
  | EXTENDED_IDENTIFIER
  ;
*/

identifier_list
  : identifier+=LIT_IDENTIFIER ( TOK_COMMA identifier+=LIT_IDENTIFIER )*
  ;

if_statement
  : label_colon? KW_IF condition KW_THEN
      sequence_of_statements
    ( KW_ELSIF condition KW_THEN
      sequence_of_statements
    )*
    ( KW_ELSE
      sequence_of_statements
    )?
    KW_END KW_IF LIT_IDENTIFIER? TOK_SEMICOL
  ;

index_constraint
  : TOK_LP discrete_range ( TOK_COMMA discrete_range )* TOK_RP
  ;

index_specification
  : discrete_range
  | expression
  ;

index_subtype_definition
  : name KW_RANGE TOK_BOX
  ;

instantiated_unit
  : KW_COMPONENT? name
  | KW_ENTITY name ( TOK_LP LIT_IDENTIFIER TOK_RP )?
  | KW_CONFIGURATION name
  ;

instantiation_list
  : LIT_IDENTIFIER ( TOK_COMMA LIT_IDENTIFIER )*
  | KW_OTHERS
  | KW_ALL
  ;

interface_constant_declaration
  : KW_CONSTANT? constantNames=identifier_list TOK_COLON modeName=KW_IN? subtypeIndication=subtype_indication
    ( TOK_VAR_ASSIGN defaultValue=expression )?
  ;

interface_declaration
  : interface_constant_declaration
  | interface_signal_declaration
  | interface_variable_declaration
  | interface_file_declaration
//  | interface_terminal_declaration
//  | interface_quantity_declaration
  ;

interface_element
  : interface_declaration
  ;

interface_file_declaration
  : KW_FILE identifier_list TOK_COLON subtype_indication
  ;

interface_signal_list
  : interface_signal_declaration ( TOK_SEMICOL interface_signal_declaration )*
  ;

interface_port_list
  : interface_port_declaration ( TOK_SEMICOL interface_port_declaration )*
  ;

interface_list
  : interface_element ( TOK_SEMICOL interface_element )*
  ;

/*
interface_quantity_declaration
  : QUANTITY identifier_list TOK_COLON ( IN | OUT )? subtype_indication
    ( TOK_VAR_ASSIGN expression )?
  ;
*/

interface_port_declaration
  : identifier_list TOK_COLON signal_mode? subtype_indication
    KW_BUS? ( TOK_VAR_ASSIGN expression )?
  ;

interface_signal_declaration
  : KW_SIGNAL identifier_list TOK_COLON signal_mode? subtype_indication
    KW_BUS? ( TOK_VAR_ASSIGN expression )?
  ;

/*
interface_terminal_declaration
  : KW_TERMINAL identifier_list TOK_COLON subnature_indication
  ;
*/

interface_variable_declaration
  : KW_VARIABLE? identifier_list TOK_COLON
    signal_mode? subtype_indication ( TOK_VAR_ASSIGN expression )?
  ;

iteration_scheme
  : KW_WHILE condition
  | KW_FOR parameter_specification
  ;

label_colon
  : LIT_IDENTIFIER TOK_COLON
  ;

library_clause
  : KW_LIBRARY logical_name_list TOK_SEMICOL
  ;

// TODO: can it be merged?
library_unit
  : primaryUnit=primary_unit
  | secondaryUnit=secondary_unit
  ;

literal
  : KW_NULL
  | LIT_BIT_STRING
  | LIT_STRING
  | enumeration_literal
  | numeric_literal
  ;

logical_name
  : LIT_IDENTIFIER
  ;

logical_name_list
  : logical_name ( TOK_COMMA logical_name )*
  ;

// TODO: combine into expression
logical_operator
  : OP_AND
  | OP_OR
  | OP_NAND
  | OP_NOR
  | OP_XOR
  | OP_XNOR
  ;

loop_statement
  : label_colon?
    iteration_scheme? KW_LOOP
      sequence_of_statements
    KW_END KW_LOOP LIT_IDENTIFIER? TOK_SEMICOL
  ;

signal_mode
  : KW_IN
  | KW_OUT
  | KW_INOUT
  | KW_BUFFER
  | KW_LINKAGE
  ;

// TODO: combine into expression
multiplying_operator
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
name
  : ( LIT_IDENTIFIER | LIT_STRING ) name_part*
  ;

name_part
  : selected_name_part
  | function_call_or_indexed_name_part
  | slice_name_part
  | attribute_name_part
  ;

selected_name
  : LIT_IDENTIFIER ( TOK_DOT suffix )*
  ;

selected_name_part
  : ( TOK_DOT suffix )+
  ;

function_call_or_indexed_name_part
  : TOK_LP actual_parameter_part TOK_RP
  ;

slice_name_part
  : TOK_LP discrete_range TOK_RP
  ;

attribute_name_part
  : signature? TOK_APOSTROPHE attribute_designator ( TOK_LP expression TOK_RP )?
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

next_statement
  : label_colon? KW_NEXT LIT_IDENTIFIER?
    ( KW_WHEN condition )?
    TOK_SEMICOL
  ;

numeric_literal
  : LIT_ABSTRACT
  | physical_literal
  ;

object_declaration
  : constant_declaration
  | signal_declaration
  | variable_declaration
  | file_declaration
//  | terminal_declaration
//  | quantity_declaration
  ;

opts
  : KW_GUARDED? delay_mechanism?
  ;

package_body
  : KW_PACKAGE KW_BODY LIT_IDENTIFIER KW_IS
      package_body_declarative_part
    KW_END ( KW_PACKAGE KW_BODY )? LIT_IDENTIFIER? TOK_SEMICOL
  ;

package_body_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | variable_declaration
  | file_declaration
  | alias_declaration
  | use_clause
//  | group_template_declaration
//  | group_declaration
  ;

package_body_declarative_part
  : package_body_declarative_item*
  ;

package_declaration
  : KW_PACKAGE LIT_IDENTIFIER KW_IS
      package_declarative_part
    KW_END KW_PACKAGE? LIT_IDENTIFIER? TOK_SEMICOL
  ;

package_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | signal_declaration
  | variable_declaration
  | file_declaration
  | alias_declaration
  | component_declaration
  | attribute_declaration
  | attribute_specification
  | disconnection_specification
  | use_clause
//  | group_template_declaration
//  | group_declaration
//  | nature_declaration
//  | subnature_declaration
//  | terminal_declaration
  ;

package_declarative_part
  : package_declarative_item*
  ;

parameter_specification
  : LIT_IDENTIFIER KW_IN discrete_range
  ;

physical_literal
  : LIT_ABSTRACT (: LIT_IDENTIFIER)
  ;

physical_type_definition
  : range_constraint KW_UNITS
      base_unit_declaration
      secondary_unit_declaration*
    KW_END KW_UNITS LIT_IDENTIFIER?
  ;

port_clause
  : KW_PORT TOK_LP port_list TOK_RP TOK_SEMICOL
  ;

port_list
  : interface_port_list
  ;

port_map_aspect
  : KW_PORT KW_MAP TOK_LP
      association_list
    TOK_RP
  ;

// TODO: combine into expression ?
primary
  : literal
  | qualified_expression
  | TOK_LP expression TOK_RP
  | allocator
  | aggregate
  | name
  ;

primary_unit
  : entity=entity_declaration
  | configuration=configuration_declaration
  | package=package_declaration         // TODO: context
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

procedure_call
  : selected_name ( TOK_LP actual_parameter_part TOK_RP )?
  ;

procedure_call_statement
  : label_colon? procedure_call TOK_SEMICOL
  ;

process_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | variable_declaration
  | file_declaration
  | alias_declaration
  | attribute_declaration
  | attribute_specification
  | use_clause
//  | group_template_declaration
//  | group_declaration
  ;

process_declarative_part
  : process_declarative_item*
  ;

process_statement
  : label_colon? KW_PROCESS
      ( TOK_LP sensitivity_list TOK_RP )?
    KW_IS?
      process_declarative_part
    KW_BEGIN
      process_statement_part
    KW_END KW_PROCESS LIT_IDENTIFIER? TOK_SEMICOL
  ;

postponed_process_statement
  : label_colon? KW_POSTPONED? KW_PROCESS
      ( TOK_LP sensitivity_list TOK_RP )?
    KW_IS?
      process_declarative_part
    KW_BEGIN
      process_statement_part
    KW_END KW_POSTPONED? KW_PROCESS LIT_IDENTIFIER? TOK_SEMICOL
  ;

process_statement_part
  : sequential_statement*
  ;

// TODO: combine into expression
qualified_expression
  : subtype_indication TOK_APOSTROPHE  ( aggregate | TOK_LP expression TOK_RP )
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

range_decl
  : explicit_range
  | name
  ;

explicit_range
  : simple_expression ( direction simple_expression )?
  ;

range_constraint
  : KW_RANGE range_decl
  ;

/*
record_nature_definition
  : RECORD ( nature_element_declaration )+
    END RECORD ( LIT_IDENTIFIER )?
  ;
*/

record_type_definition
  : KW_RECORD element_declaration+
    KW_END KW_RECORD LIT_IDENTIFIER?
  ;

// TODO: combine into expression
relation
  : shift_expression
    (: relational_operator shift_expression )?
  ;

// TODO: combine into expression
relational_operator
  : OP_EQ
  | OP_NE
  | OP_LT
  | OP_LE
  | OP_GT
  | OP_GE
  ;

report_statement
  : label_colon? KW_REPORT expression
    ( KW_SEVERITY expression )?
    TOK_SEMICOL
  ;

return_statement
  : label_colon? KW_RETURN expression? TOK_SEMICOL
  ;

/*
scalar_nature_definition
  : name ACROSS name THROUGH name REFERENCE
  ;
*/

scalar_type_definition
  : physical_type_definition
  | enumeration_type_definition
  | range_constraint
  ;

secondary_unit
  : architecture_body
  | package_body
  ;

secondary_unit_declaration
  : LIT_IDENTIFIER OP_EQ physical_literal TOK_SEMICOL
  ;

selected_signal_assignment
  : KW_WITH expression KW_SELECT target TOK_SIG_ASSIGN opts selected_waveforms TOK_SEMICOL
  ;

selected_waveforms
  : waveform KW_WHEN choices ( TOK_COMMA waveform KW_WHEN choices )*
  ;

sensitivity_clause
  : KW_ON sensitivity_list
  ;

sensitivity_list
  : name ( TOK_COMMA name )*
  ;

sequence_of_statements
  : sequential_statement*
  ;

sequential_statement
  : wait_statement
  | assertion_statement
  | report_statement
  | signal_assignment_statement
  | variable_assignment_statement
  | if_statement
  | case_statement
  | loop_statement
  | next_statement
  | exit_statement
  | return_statement
  | label_colon? KW_NULL TOK_SEMICOL
//  | break_statement
  | procedure_call_statement
  ;

// TODO: combine into expression
shift_expression
  : simple_expression
    (: shift_operator simple_expression )?
  ;

// TODO: combine into expression
shift_operator
  : OP_SLL
  | OP_SRL
  | OP_SLA
  | OP_SRA
  | OP_ROL
  | OP_ROR
  ;

signal_assignment_statement
  : label_colon?
    target TOK_SIG_ASSIGN delay_mechanism? waveform TOK_SEMICOL
  ;

signal_declaration
  : KW_SIGNAL identifier_list TOK_COLON
    subtype_indication signal_kind? ( TOK_VAR_ASSIGN expression )? TOK_SEMICOL
  ;

signal_kind
  : KW_REGISTER
  | KW_BUS
  ;

signal_list
  : name ( TOK_COMMA name )*
  | KW_OTHERS
  | KW_ALL
  ;

signature
  : TOK_LB ( name ( TOK_COMMA name )* )? ( KW_RETURN name )? TOK_RB
  ;

// NOTE that sign is applied to first operand only (LRM does not permit
// `a op -b' - use `a op (-b)' instead).
// (3.2.2004, e.f.)
// TODO: combine into expression
simple_expression
  : ( OP_PLUS | OP_MINUS )? term (: adding_operator term )*
  ;

simple_simultaneous_statement
  : label_colon?
    simple_expression TOK_SIG_ASSIGN simple_expression /* ( tolerance_aspect )? */ TOK_SEMICOL
  ;

simultaneous_alternative
  : KW_WHEN choices TOK_RARROW simultaneous_statement_part
  ;

simultaneous_case_statement
  : label_colon? KW_CASE expression KW_USE
      simultaneous_alternative+
    KW_END KW_CASE LIT_IDENTIFIER? TOK_SEMICOL
  ;

simultaneous_if_statement
  : label_colon? KW_IF condition KW_USE
      simultaneous_statement_part
    ( KW_ELSIF condition KW_USE
      simultaneous_statement_part
    )*
    ( KW_ELSE
      simultaneous_statement_part
    )?
    KW_END KW_USE LIT_IDENTIFIER? TOK_SEMICOL
  ;

/*
simultaneous_procedural_statement
  : ( label_colon )? KW_PROCEDURAL ( IS )?
    procedural_declarative_part KW_BEGIN
    procedural_statement_part
    KW_END KW_PROCEDURAL ( LIT_IDENTIFIER )? TOK_SEMICOL
  ;
*/
simultaneous_statement
  : simple_simultaneous_statement
  | simultaneous_if_statement
  | simultaneous_case_statement
//  | simultaneous_procedural_statement
  | label_colon? KW_NULL TOK_SEMICOL
  ;

simultaneous_statement_part
  : simultaneous_statement*
  ;

/*
source_aspect
  : KW_SPECTRUM simple_expression TOK_COMMA simple_expression
  | KW_NOISE simple_expression
  ;

source_quantity_declaration
  : QUANTITY identifier_list TOK_COLON subtype_indication source_aspect TOK_SEMICOL
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

subprogram_body
  : subprogram_specification KW_IS
      subprogram_declarative_part
    KW_BEGIN
      subprogram_statement_part
    KW_END subprogram_kind? designator? TOK_SEMICOL
  ;

subprogram_declaration
  : subprogram_specification TOK_SEMICOL
  ;

subprogram_declarative_item
  : subprogram_declaration
  | subprogram_body
  | type_declaration
  | subtype_declaration
  | constant_declaration
  | variable_declaration
  | file_declaration
  | alias_declaration
  | attribute_declaration
  | attribute_specification
  | use_clause
//  | group_template_declaration
//  | group_declaration
  ;

subprogram_declarative_part
  : subprogram_declarative_item*
  ;

subprogram_kind
  : KW_PROCEDURE
  | KW_FUNCTION
  ;

subprogram_specification
  : procedure_specification
  | function_specification
  ;

procedure_specification
  : KW_PROCEDURE designator ( TOK_LP formal_parameter_list TOK_RP )?
  ;

function_specification
  : ( KW_PURE | KW_IMPURE )? KW_FUNCTION designator
    ( TOK_LP formal_parameter_list TOK_RP )? KW_RETURN subtype_indication
  ;

subprogram_statement_part
  : sequential_statement*
  ;

subtype_declaration
  : KW_SUBTYPE LIT_IDENTIFIER KW_IS subtype_indication TOK_SEMICOL
  ;

subtype_indication
  : selected_name selected_name? constraint? /* ( tolerance_aspect )? */
  ;

suffix
  : LIT_IDENTIFIER
  | LIT_CHARACTER
  | LIT_STRING
  | KW_ALL
  ;

target
  : name
  | aggregate
  ;

// TODO: combine into expression
term
  : factor (: multiplying_operator factor )*
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

timeout_clause
  : KW_FOR expression
  ;

/*
tolerance_aspect
  : TOLERANCE expression
  ;
*/

type_declaration
  : KW_TYPE LIT_IDENTIFIER ( KW_IS type_definition )? TOK_SEMICOL
  ;

type_definition
  : scalar_type_definition
  | composite_type_definition
  | access_type_definition
  | file_type_definition
  ;

unconstrained_array_definition
  : KW_ARRAY TOK_LP index_subtype_definition ( TOK_COMMA index_subtype_definition )*
    TOK_RP KW_OF subtype_indication
  ;

/*
unconstrained_nature_definition
  : KW_ARRAY TOK_LP index_subtype_definition ( TOK_COMMA index_subtype_definition )*
    TOK_RP OF subnature_indication
  ;
*/

use_clause
  : KW_USE selected_name ( TOK_COMMA selected_name )* TOK_SEMICOL
  ;

variable_assignment_statement
  : label_colon? target TOK_VAR_ASSIGN expression TOK_SEMICOL
  ;

variable_declaration
  : KW_SHARED? KW_VARIABLE identifier_list TOK_COLON
    subtype_indication ( TOK_VAR_ASSIGN expression )? TOK_SEMICOL
  ;

wait_statement
  : label_colon? KW_WAIT
      sensitivity_clause?
      condition_clause?
      timeout_clause?
    TOK_SEMICOL
  ;

waveform
  : waveform_element ( TOK_COMMA waveform_element )*
  | KW_UNAFFECTED
  ;

waveform_element
  : expression ( KW_AFTER expression )?
  ;




/*




library_clause
	:	KW_LIBRARY LIT_IDENTIFIER TOK_SEMICOL
	;

use_clause
	: KW_USE library=LIT_IDENTIFIER TOK_DOT package=LIT_IDENTIFIER TOK_DOT symbol=(KW_ALL | LIT_IDENTIFIER) TOK_SEMICOL
	;

context
	: library_clause*
		use_clause*
	;

generic_clause
	:	KW_CONSTANT? name=LIT_IDENTIFIER TOK_COLON mmode=KW_IN? type=LIT_IDENTIFIER (TOK_COLONEQ value=LIT_INTEGER)?  #generic_constant
	| KW_TYPE name=LIT_IDENTIFIER #generic_type
	;

generic_decl
	: KW_GENERIC TOK_LP
			generic_clause (TOK_SEMICOL generic_clause)*
		TOK_RP TOK_SEMICOL
	;

port_clause
	:	KW_SIGNAL? name=LIT_IDENTIFIER TOK_COLON mmode=(KW_IN|KW_OUT)? type=LIT_IDENTIFIER  #port_signal
	;

port_decl
	: KW_PORT TOK_LP
			port_clause (TOK_SEMICOL port_clause)*
		TOK_RP TOK_SEMICOL
	;

entity_unit
	: KW_ENTITY LIT_IDENTIFIER KW_IS
		generic_decl?
		port_decl?
		KW_END KW_ENTITY? LIT_IDENTIFIER? TOK_SEMICOL
	;

enum_list
	: LIT_IDENTIFIER (TOK_COMMA LIT_IDENTIFIER)*
	;

type_decl
	: KW_TYPE name=LIT_IDENTIFIER KW_IS TOK_LP enum_list TOK_RP TOK_SEMICOL #type_enum
	| KW_TYPE name=LIT_IDENTIFIER KW_IS KW_ARRAY TOK_LP type=LIT_IDENTIFIER KW_RANGE TOK_BOX TOK_RP KW_OF etype=LIT_IDENTIFIER
		TOK_SEMICOL #type_array
	;

package_unit
	: KW_PACKAGE LIT_IDENTIFIER KW_IS
		type_decl*
		KW_END KW_PACKAGE? LIT_IDENTIFIER? TOK_SEMICOL
	;

primary_unit
	: context
		(entity_unit | package_unit)
	;

//secondary_unit
//	:
//	;

design_file
	: (primary_unit /* | secondary_unit/ )*
		EOF
	;

*/
