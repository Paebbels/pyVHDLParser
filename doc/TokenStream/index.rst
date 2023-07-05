.. _tokstm:

1. Pass - String ⇒ Tokens
#########################

In the :ref:`first pass <concept-passes>` a source file (string) is sliced into a chain of double-linked token objects
of base-class :class:`~pyVHDLParser.Token.Token`. While creating tokens, the start and end position of the token is
preserved as two :class:`~pyVHDLParser.SourceCodePosition` object within each token.

In contrast to ordinary lexers/parsers, pyVHDLParser preserves cases, whitespaces (space, tab, ...), linebreaks and
comments.


**Condensed definition of class** :class:`~pyVHDLParser.SourceCodePosition`:

.. code-block:: Python

   @export
   class SourceCodePosition(metaclass=ExtendedType, slots=True):
     """Represent a position (row, column, absolute) in a source code file."""

     Row:       int    #: Row in the source code file (starting at 1)
     Column:    int    #: Column (character) in the source code file's line (starting at 1)
     Absolute:  int    #: Absolute character position regardless of linebreaks.


**Condensed definition of class** :class:`~pyVHDLParser.Token.Token`:

.. code-block:: Python

   @export
   class Token(metaclass=ExtendedType, slots=True):
     """Base-class for all token classes."""

     _previousToken:  Token                #: Reference to the previous token (backward pointer)
     NextToken:       Nullable[Token]      #: Reference to the next token (forward pointer)
     Start:           SourceCodePosition   #: Position in the file for the token start
     End:             SourceCodePosition   #: Position in the file for the token end

     def __init__(self, previousToken : Token, start : SourceCodePosition, end : SourceCodePosition = None):
     def __len__(self) -> int:
     def __iter__(self) -> Iterator[Token]:

     def GetIterator(self, inclusiveStartToken: bool = False, inclusiveStopToken: bool = True, stopToken: Token = None) -> Iterator[Token]:
     def GetReverseIterator(self, inclusiveStartToken: bool = False, inclusiveStopToken: bool = True, stopToken: Token = None) -> Iterator[Token]:

     @property
     def PreviousToken(self) -> Token:

     @property
     def Length(self) -> int:



.. toctree::
   :hidden:

   MetaTokens
   SimpleTokens
   SpecificTokens
   Tokenizer
   Usage
   Examples


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

