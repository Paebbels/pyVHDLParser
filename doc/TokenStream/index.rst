.. _tokstm:

1. Pass - Tokens
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



.. toctree::
   :hidden:

   MetaTokens
   SimpleTokens
   SpecificTokens
   Tokenizer


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

