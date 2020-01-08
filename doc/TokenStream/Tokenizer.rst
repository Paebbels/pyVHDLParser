.. _tokstm-tokenizer:

Token Generator (Tokenizer)
###########################

.. todo::

   Describe tokenizer and generators and co-routines/yield.


The :class:`~pyVHDLParser.Token.Parser.Tokenizer` is implemented as a Python
:term:`generator` returning one token at a time. It has 15 states defined in
:class:`pyVHDLParser.Token.Parser.Tokenizer.TokenKind`.



**Tokenizer States:**

.. graphviz:: ../diagrams/Tokenizer.gv
   :caption: State Transitions of Tokenizer


**Parser states defined in** :class:`~pyVHDLParser.Token.Parser.Tokenizer.TokenKind`:

.. code-block:: Python

   class TokenKind(Enum):
     """Enumeration of all Tokenizer states."""

     SpaceChars =                       0   #: Last char was a space
     NumberChars =                      1   #: Last char was a digit
     AlphaChars =                       2   #: Last char was a letter
     DelimiterChars =                   3   #: Last char was a delimiter character
     PossibleSingleLineCommentStart =   4   #: Last char was a dash
     PossibleLinebreak =                5   #: Last char was a ``\r``
     PossibleCharacterLiteral =         6   #: Last char was a ``'``
     PossibleStringLiteralStart =       7   #: Last char was a ``"``
     PossibleExtendedIdentifierStart =  8   #: Last char was a ``\``
     SingleLineComment =                9   #: Found ``--`` before
     MultiLineComment =                10   #: Found ``/*`` before
     Linebreak =                       11   #: Last char was a ``\n``
     Directive =                       12   #: Last char was a `` ` ``
     FuseableCharacter =               13   #: Last char was a character that could be fused
     OtherChars =                      14   #: Any thing else
