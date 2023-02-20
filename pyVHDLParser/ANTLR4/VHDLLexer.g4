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
lexer grammar VHDLLexer;

options {
	caseInsensitive = true;
}

channels {
	WHITESPACE_CHANNEL,
	COMMENT_CHANNEL,
	TOOLDIRECTIVE_CHANNEL
}

LINEBREAK:     [\r\n]+            -> channel(WHITESPACE_CHANNEL)    ;
WHITESPACE:    [ \t\f\b]+         -> channel(WHITESPACE_CHANNEL)    ;
COMMENT_LINE:  '--' ~[\r\n]*      -> channel(COMMENT_CHANNEL)       ;
COMMENT_BLOCK: '/*' .*? '*/'      -> channel(COMMENT_CHANNEL)       ;
TOOLDIRECTIVE: '`' ~[\r\n]*       -> channel(TOOLDIRECTIVE_CHANNEL) ;

// Reserved words starting with A
OP_ABS:           'abs';
KW_ACCESS:        'access';
KW_AFTER:         'after';
KW_ALIAS:         'alias';
KW_ALL:           'all';
OP_AND:           'and';
KW_ARCHITECTURE:  'architecture';
KW_ARRAY:         'array';
KW_ASSERT:        'assert';
KW_ATTRIBUTE:     'attribute';
KW_PSL_ASSUME:    'assume';
//KW_AMS_ACROSS:    'across';

// Reserved words starting with B
KW_BEGIN:         'begin';
KW_BLOCK:         'block';
KW_BODY:          'body';
KW_BUFFER:        'buffer';
KW_BUS:           'bus';
//KW_AMS_BREAK:     'break';

// Reserved words starting with C
KW_CASE:          'case';
KW_COMPONENT:     'component';
KW_CONFIGURATION: 'configuration';
KW_CONSTANT:      'constant';
KW_CONTEXT:       'context';
KW_PSL_COVER:     'cover';

// Reserved words starting with D
KW_DEFAULT:       'default';
KW_DISCONNECT:    'disconnect';
KW_DOWNTO:        'downto';

// Reserved words starting with E
KW_ELSE:          'else';
KW_ELSIF:         'elsif';
KW_END:           'end';
KW_ENTITY:        'entity';
KW_EXIT:          'exit';

// Reserved words starting with F
KW_FILE:          'file';
KW_FOR:           'for';
KW_FORCE:         'force';
KW_FUNCTION:      'function';
KW_PSL_FAIRNESS:  'fairness';

// Reserved words starting with G
KW_GENERATE:      'generate';
KW_GENERIC:       'generic';
KW_GUARDED:       'guarded';
KW_GROUP:         'group';

// Reserved words starting with I
KW_IF:            'if';
KW_IMPURE:        'impure';
KW_IN:            'in';
KW_INERTIAL:      'inertial';
KW_INOUT:         'inout';
KW_IS:            'is';

// Reserved words starting with L
KW_LABEL:         'label';
KW_LIBRARY:       'library';
KW_LINKAGE:       'linkage';
KW_LOOP:          'loop';
KW_PSL_LITERAL:   'literal';
//KW_AMS_LIMIT:     'limit';

// Reserved words starting with M
KW_MAP:           'map';
OP_MOD:           'mod';

// Reserved words starting with N
OP_NAND:          'nand';
KW_NEW:           'new';
KW_NEXT:          'next';
OP_NOR:           'nor';
OP_NOT:           'not';
KW_NULL:          'null';
//KW_AMS_NATURE:    'nature';
//KW_AMS_NOISE:     'noise';

// Reserved words starting with O
KW_OF:            'of';
KW_ON:            'on';
KW_OPEN:          'open';
OP_OR:            'or';
KW_OTHERS:        'others';
KW_OUT:           'out';

// Reserved words starting with P
KW_PACKAGE:       'package';
KW_PARAMETER:     'parameter';
KW_PORT:          'port';
KW_POSTPONED:     'postponed';
KW_PRIVATE:       'private';
KW_PROCEDURE:     'procedure';
KW_PROCESS:       'process';
KW_PROTECTED:     'protected';
KW_PURE:          'pure';
//KW_AMS_PROCEDURAL:    'procedural';

// Reserved words starting with Q
//KW_AMS_QUANTITY: 'quantity';

// Reserved words starting with R
KW_RANGE:         'range';
KW_RECORD:        'record';
KW_REGISTER:      'register';
KW_REJECT:        'reject';
KW_RELEASE:       'release';
OP_REM:           'rem';
KW_REPORT:        'report';
KW_RETURN:        'return';
OP_ROL:           'rol';
OP_ROR:           'ror';
KW_PSL_RESTRICT:  'restrict';
//KW_AMS_REFERENCE: 'reference';

// Reserved words starting with S
KW_SELECT:        'select';
KW_SEVERITY:      'severity';
KW_SHARED:        'shared';
KW_SIGNAL:        'signal';
OP_SLA:           'sla';
OP_SLL:           'sll';
OP_SRA:           'sra';
OP_SRL:           'srl';
KW_SUBTYPE:       'subtype';
KW_PSL_STRONG:    'strong';
KW_PSL_SEQUENCE:  'sequence';
//KW_AMS_SPECTRUM:  'spectrum';
//KW_AMS_SUBNATURE: 'subnature';

// Reserved words starting with T
KW_THEN:          'then';
KW_TO:            'to';
KW_TRANSPORT:     'transport';
KW_TYPE:          'type';
//KW_AMS_TERMINAL:  'terminal';
//KW_AMS_THROUGH:   'through';
//KW_AMS_TOLERANCE: 'tolerance';

// Reserved words starting with U
KW_UNAFFECTED:    'unaffected';
KW_UNITS:         'units';
KW_UNTIL:         'until';
KW_USE:           'use';

// Reserved words starting with V
KW_VARIABLE:      'variable';
KW_VIEW:          'view';
KW_PSL_VPKG:      'vpkg';
KW_PSL_VMODE:     'vmode';
KW_PSL_VPROP:     'vprop';
KW_PSL_VUNIT:     'vunit';

// Reserved words starting with W
KW_WAIT:          'wait';
KW_WITH:          'with';
KW_WHEN:          'when';
KW_WHILE:         'while';

// Reserved words starting with X
OP_XNOR:          'xnor';
OP_XOR:           'xor';

OP_EQ: '=';
OP_NE: '/=';
OP_LT: '<';
//OP_LE: '<=';
OP_GT: '>';
OP_GE: '>=';
OP_IEQ: '?=';
OP_INE: '?/=';
OP_ILT: '?<';
OP_ILE: '?<=';
OP_IGT: '?>';
OP_IGE: '?>=';
OP_PLUS: '+';
OP_MINUS: '-';
OP_MUL: '*';
OP_DIV: '/';
OP_POW: '**';
OP_CONCAT: '&';
OP_CONDITION: '??';

TOK_RARROW: '=>';
TOK_SIG_ASSIGN: '<=';
TOK_VAR_ASSIGN: ':=';
TOK_BOX: '<>';
TOK_LP: '(';
TOK_RP: ')';
TOK_LB: '[';
TOK_RB: ']';
TOK_DLA: '<<';
TOK_DRA: '>>';
TOK_COLON: ':';
TOK_SEMICOL: ';';
TOK_COMMA: ',';
TOK_BAR: '|';
TOK_DOT: '.';
TOK_QUESTION: '?';
TOK_AT: '@';
TOK_CIRCUMFLEX: '^';
TOK_TICK: '\'';
TOK_DQUOTE: '"';

fragment Letter:        [a-z] ;
fragment Digit:         [0-9] ;
fragment ExtendedDigit: [0-9a-z] ;

fragment Integer:       [0-9][_0-9]* ;
fragment BasedInteger:  ExtendedDigit ('_' | ExtendedDigit)* ;
fragment Exponent:      'e' ( '+' | '-' )? Integer ;
fragment Real:          Integer '.' Integer Exponent? ;

fragment BaseLiteral:   Integer '#' BasedInteger ( '.' BasedInteger )? '#' Exponent? ;

LIT_ABSTRACT
  : Integer
  | Real
  | BaseLiteral
  ;

fragment BinaryBitString:  Integer? [us]? 'b' '"' ([0-1]    | '_')+ '"' ;
fragment OctalBitString:   Integer? [us]? 'o' '"' ([0-7]    | '_')+ '"' ;
fragment DecimalBitString: Integer?       'd' '"' ([0-9]    | '_')+ '"' ;
fragment HexBitString:     Integer? [us]? 'x' '"' ([0-9a-f] | '_')+ '"' ;

LIT_BIT_STRING
  : BinaryBitString
  | OctalBitString
  | DecimalBitString
  | HexBitString
  ;

LIT_CHARACTER:           '\'' . '\'' ;
LIT_STRING:              '"' (~('"' | '\n' | '\r') | '""')* '"' ;

/*
LIT_OTHER_CHARACTER
  : '!' | '$' | '%' | '@' | '?' | '^' | '`' | '{' | '}' | '~'
  | ' ' | 'Ў' | 'ў' | 'Ј' | '¤' | 'Ґ' | '¦' | '§'
  | 'Ё' | '©' | 'Є' | '«' | '¬' | '­' | '®' | 'Ї'
  | '°' | '±' | 'І' | 'і' | 'ґ' | 'µ' | '¶' | '·'
  | 'ё' | '№' | 'є' | '»' | 'ј' | 'Ѕ' | 'ѕ' | 'ї'
  | 'А' | 'Б' | 'В' | 'Г' | 'Д' | 'Е' | 'Ж' | 'З'
  | 'И' | 'Й' | 'К' | 'Л' | 'М' | 'Н' | 'О' | 'П'
  | 'Р' | 'С' | 'Т' | 'У' | 'Ф' | 'Х' | 'Ц' | 'Ч'
  | 'Ш' | 'Щ' | 'Ъ' | 'Ы' | 'Ь' | 'Э' | 'Ю' | 'Я'
  | 'а' | 'б' | 'в' | 'г' | 'д' | 'е' | 'ж' | 'з'
  | 'и' | 'й' | 'к' | 'л' | 'м' | 'н' | 'о' | 'п'
  | 'р' | 'с' | 'т' | 'у' | 'ф' | 'х' | 'ц' | 'ч'
  | 'ш' | 'щ' | 'ъ' | 'ы' | 'ь' | 'э' | 'ю' | 'я'
  ;
*/

fragment BasicIdentifier:    [a-z] ('_'? [a-z0-9])* ;
fragment ExtendedIdentifier: '\\' .+? '\\' ;

LIT_IDENTIFIER
	: BasicIdentifier
	| ExtendedIdentifier
	;
