lexer grammar VHDLLexer;

options {
	caseInsensitive = true;
}

channels {
	WHITESPACE_CHANNEL,
	COMMENT_CHANNEL
}


LINEBREAK:     [\r\n]+            -> channel(WHITESPACE_CHANNEL);
WHITESPACE:    [ \t\f\b]+         -> channel(WHITESPACE_CHANNEL);
//WHITESPACE:    [\p{White_Space}]+ -> channel(WHITESPACE_CHANNEL);
COMMENT_LINE:  '--' ~[\r\n]*      -> channel(COMMENT_CHANNEL)   ;
COMMENT_BLOCK: '/*' .*? '*/'      -> channel(COMMENT_CHANNEL)   ;

OP_ABS: 'abs';
//KW_ACROSS: 'across';
KW_ACCESS: 'access';
KW_AFTER: 'after';
KW_ALIAS: 'alias';
KW_ALL: 'all';
OP_AND: 'and';
KW_ARCHITECTURE: 'architecture';
KW_ARRAY: 'array';
KW_ASSERT: 'assert';
KW_ATTRIBUTE: 'attribute';
KW_BEGIN: 'begin';
KW_BLOCK: 'block';
KW_BODY: 'body';
//KW_BREAK: 'break';
KW_BUFFER: 'buffer';
KW_BUS: 'bus';
KW_CASE: 'case';
KW_COMPONENT: 'component';
KW_CONFIGURATION: 'configuration';
KW_CONSTANT: 'constant';
KW_DISCONNECT: 'disconnect';
KW_DOWNTO: 'downto';
KW_END: 'end';
KW_ENTITY: 'entity';
KW_ELSE: 'else';
KW_ELSIF: 'elsif';
KW_EXIT: 'exit';
KW_FILE: 'file';
KW_FOR: 'for';
KW_FUNCTION: 'function';
KW_GENERATE: 'generate';
KW_GENERIC: 'generic';
KW_GROUP: 'group';
KW_GUARDED: 'guarded';
KW_IF: 'if';
KW_IMPURE: 'impure';
KW_IN: 'in';
KW_INERTIAL: 'inertial';
KW_INOUT: 'inout';
KW_IS: 'is';
KW_LABEL: 'label';
KW_LIBRARY: 'library';
//KW_LIMIT: 'limit';
KW_LINKAGE: 'linkage';
//KW_LITERAL: 'literal';
KW_LOOP: 'loop';
KW_MAP: 'map';
OP_MOD: 'mod';
OP_NAND: 'nand';
//KW_NATURE: 'nature';
KW_NEW: 'new';
KW_NEXT: 'next';
//KW_NOISE: 'noise';
OP_NOR: 'nor';
OP_NOT: 'not';
KW_NULL: 'null';
KW_OF: 'of';
KW_ON: 'on';
KW_OPEN: 'open';
OP_OR: 'or';
KW_OTHERS: 'others';
KW_OUT: 'out';
KW_PACKAGE: 'package';
KW_PORT: 'port';
KW_POSTPONED: 'postponed';
KW_PROCESS: 'process';
KW_PROCEDURE: 'procedure';
//KW_PROCEDURAL: 'procedural';
KW_PURE: 'pure';
//KW_QUANTITY: 'quantity';
KW_RANGE: 'range';
KW_REJECT: 'reject';
OP_REM: 'rem';
KW_RECORD: 'record';
//KW_REFERENCE: 'reference';
KW_REGISTER: 'register';
KW_REPORT: 'report';
KW_RETURN: 'return';
OP_ROL: 'rol';
OP_ROR: 'ror';
KW_SELECT: 'select';
KW_SEVERITY: 'severity';
KW_SHARED: 'shared';
KW_SIGNAL: 'signal';
OP_SLA: 'sla';
OP_SLL: 'sll';
//KW_SPECTRUM: 'spectrum';
OP_SRA: 'sra';
OP_SRL: 'srl';
//KW_SUBNATURE: 'subnature';
KW_SUBTYPE: 'subtype';
//KW_TERMINAL: 'terminal';
KW_THEN: 'then';
//KW_THROUGH: 'through';
KW_TO: 'to';
//KW_TOLERANCE: 'tolerance';
KW_TRANSPORT: 'transport';
KW_TYPE: 'type';
KW_UNAFFECTED: 'unaffected';
KW_UNITS: 'units';
KW_UNTIL: 'until';
KW_USE: 'use';
KW_VARIABLE: 'variable';
KW_WAIT: 'wait';
KW_WITH: 'with';
KW_WHEN: 'when';
KW_WHILE: 'while';
OP_XNOR: 'xnor';
OP_XOR: 'xor';

OP_EQ: '=';
OP_NE: '/=';
OP_LT: '<';
OP_LE: '<=)';
OP_GT: '>';
OP_GE: '>=';
OP_PLUS: '+';
OP_MINUS: '-';
OP_MUL: '*';
OP_DIV: '/';
OP_POW: '**';
OP_CONCAT: '&';

TOK_RARROW: '=>';
TOK_SIG_ASSIGN: '<=';
TOK_VAR_ASSIGN: ':=';
TOK_BOX: '<>';
TOK_LP: '(';
TOK_RP: ')';
TOK_LB: '[';
TOK_RB: ']';
TOK_COLON: ':';
TOK_SEMICOL: ';';
TOK_COMMA: ',';
TOK_BAR: '|';
TOK_DOT: '.';
TOK_TICK: '\'';

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

fragment BinaryBitString:  'b' '"' ([0-1]    | '_')+ '"' ;
fragment OctalBitString:   'o' '"' ([0-7]    | '_')+ '"' ;
fragment DecimalBitString: 'd' '"' ([0-9]    | '_')+ '"' ;
fragment HexBitString:     'x' '"' ([0-9a-f] | '_')+ '"' ;

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

fragment BasicIdentifier:    [a-z] ('_' [a-z0-9] | [a-z0-9])* ;
fragment ExtendedIdentifier: '\\' ([a-z0-9] | '_')+ '\\'      ;

LIT_IDENTIFIER
	: BasicIdentifier
	| ExtendedIdentifier
	;
