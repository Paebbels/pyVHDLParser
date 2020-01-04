.. _tokstm:

Stream of Tokens
################

In the :ref:`first pass <concept-passes>` a source file is sliced into a chain
of double-linked objects of base-class :class:`~pyVHDLParser.Token.Token`. While
token creation, the start and end position of a token is preserved as a
:class:`~pyVHDLParser.SourceCodePosition` object within each token.

In contrast to ordinary parsers, pyVHDLParser preserves cases, whitespaces (space,
tab, ...), linebreaks and comments.


**Condensed definition of class** :class:`~pyVHDLParser.SourceCodePosition`:

.. code-block:: Python

   @Export
   class SourceCodePosition:
     """Represent a position (row, column, absolute) in a source code file."""
     Row :       int = None    #: Row in the source code file
     Column :    int = None    #: Column (character) in the source code file's line
     Absolute :  int = None    #: Absolute character position regardless of linebreaks.


**Condensed definition of class** :class:`~pyVHDLParser.Token.Token`:

.. code-block:: Python

   @Export
   class Token:
     """Base-class for all token classes."""
     _previousToken :  Token =               None    #: Reference to the previous token
     _NextToken :      Token =               None    #: Reference to the next token
     Start :           SourceCodePosition =  None    #: Position for the token start
     End :             SourceCodePosition =  None    #: Position for the token end

     def __init__(self, previousToken : Token, start : SourceCodePosition, end : SourceCodePosition = None):
     def __len__(self):

     @property
     def PreviousToken(self):



.. _tokstm-metatoken:

Meta Tokens
***********

There are two meta-tokens: :class:`~pyVHDLParser.Token.StartOfDocumentToken`
and :class:`~pyVHDLParser.Token.EndOfDocumentToken`. These tokens represent
a start and end of a token stream. These tokens have a length of ``0`` characters.



.. _tokstm-sodt:

StartOfDocumentToken
====================

This token starts a chain of double-linked tokens in a token stream. It's used,
if the input source is a whole file, otherwise :class:`~pyVHDLParser.Token.StartOfSnippetToken`.
It is derived from base-class :class:`~pyVHDLParser.Token.StartOfToken`
and mixin :class:`~pyVHDLParser.StartOfDocument`.

**Interitance diagram:**

.. inheritance-diagram:: pyVHDLParser.Token.StartOfDocumentToken
   :parts: 1



.. _tokstm-eodt:

EndOfDocumentToken
==================

This token ends a chain of double-linked tokens in a token stream. It's used,
if the input source is a whole file, otherwise :class:`~pyVHDLParser.Token.EndOfSnippetToken`.
It is derived from base-class :class:`~pyVHDLParser.Token.EndOfToken`
and mixin :class:`~pyVHDLParser.EndOfDocument`.

**Interitance diagram:**

.. inheritance-diagram:: pyVHDLParser.Token.EndOfDocumentToken
   :parts: 1



.. _tokstm-simpletoken:

Simple Tokens
*************

Simple tokens, are tokens created by the :ref:`tokstm-tokenizer`.

The tokenizer has no deep knowledge of the VHDL language, thus it can only detect
a limited number of distinct tokens. These token require only a context of up to
two characters while parsing.

**List of simple tokens:**

+--------------------------+-------------------------+-------------------------------------------------------+
| Kind                     | Examples                | pyVHDLParser Token Class                              |
+==========================+=========================+=======================================================+
| Single character         | ``;``, ``(``            | :class:`~pyVHDLParser.Token.CharacterToken`           |
+--------------------------+-------------------------+-------------------------------------------------------+
| Multiple characters      | ``<=``, ``:=``, ``**``  | :class:`~pyVHDLParser.Token.FusedCharacterToken`      |
+--------------------------+-------------------------+-------------------------------------------------------+
| Whitespace (space, tab)  |                         | :class:`~pyVHDLParser.Token.SpaceToken`               |
+--------------------------+-------------------------+-------------------------------------------------------+
| Word                     | ``entity``, ``xor``     | :class:`~pyVHDLParser.Token.WordToken`                |
+--------------------------+-------------------------+-------------------------------------------------------+
| Single-line comment      | ``-- TODO``             | :class:`~pyVHDLParser.Token.SingleLineCommentToken`   |
+--------------------------+-------------------------+-------------------------------------------------------+
| Multi-line comment       | ``/*comment*/``         | :class:`~pyVHDLParser.Token.MultiLineCommentToken`    |
+--------------------------+-------------------------+-------------------------------------------------------+
| Integer literal          | ``42``                  | :class:`~pyVHDLParser.Token.IntegerLiteralToken`      |
+--------------------------+-------------------------+-------------------------------------------------------+
| Real literal             | ``1.25``                | :class:`~pyVHDLParser.Token.RealLiteralToken`         |
+--------------------------+-------------------------+-------------------------------------------------------+
| Character literal        | ``'a'``, ``'Z'``        | :class:`~pyVHDLParser.Token.CharacterLiteralToken`    |
+--------------------------+-------------------------+-------------------------------------------------------+
| String literal           | ``"hello"``             | :class:`~pyVHDLParser.Token.StringLiteralToken`       |
+--------------------------+-------------------------+-------------------------------------------------------+
| Bit string literal       | ``x"42"``               | :class:`~pyVHDLParser.Token.BitStringLiteralToken`    |
+--------------------------+-------------------------+-------------------------------------------------------+
| Extended identifiers     | ``\$cell35\``           | :class:`~pyVHDLParser.Token.ExtendedIdentifierToken`  |
+--------------------------+-------------------------+-------------------------------------------------------+
| Tool directives          |                         | :class:`~pyVHDLParser.Token.DirectiveToken`           |
+--------------------------+-------------------------+-------------------------------------------------------+
| Linebreak                | ``\n``                  | :class:`~pyVHDLParser.Token.LineBreakToken`           |
+--------------------------+-------------------------+-------------------------------------------------------+
| indentation              | ``\t``                  | :class:`~pyVHDLParser.Token.IndentationToken`         |
+--------------------------+-------------------------+-------------------------------------------------------+



.. rubric:: Example of a VHDL Entity

**Source code:**

.. code-block:: VHDL

   entity myEntity is
     generic (
       constant BITS : in positive := 8    -- 1 Byte
     );
     port (
       signal Clock : in  std_logic;  -- $IsClock:
       signal Reset : out std_logic   -- @Clock: generated reset pulse
     );
   end entity;

**Token Stream:**

.. image:: /images/TokenStream.vhdl/tokenize.png

.. note::
   The 3 comments have been preserved and are shown in lime green. Please also
   note the preserved positions in the last column.

**Simplified Double-Linked List:**

.. graphviz::
   :caption: Source: TokenStream.vhdl

   digraph Tokenize {
     rankdir=LR;

     node [shape=box];

     n1 [label="StartOfDocumentToken\n"];
     n2 [label="WordToken\n'entity'"];
     n3 [label="SpaceToken\n' '"];
     n4 [label="WordToken\n'myEntity'"];
     n5 [label="..."];
     n6 [label="EndOfDocumentToken\n"];

     n1 -> n2 -> n3 -> n4 -> n5 -> n6 [dir=both];
   }



.. _tokstm-specifictoken:

Specific Tokens
***************

.. todo::

   Explain specifi tokens and token replacement.



.. _tokstm-tokenizer:

Tokenizer
*********

The :class:`~pyVHDLParser.Token.Parser.Tokenizer` is implemented as a Python
:term:`generator` returning one token at a time.


.. todo::

   Describe tokenizer and generators and co-routines/yield.



