Expressions
###########

Expression blocks are base-classes for a specific expression implementation. All
four expression base-classes are derived from another base-class called :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlock`
E.g. :class:`~pyVHDLParser.Blocks.Object.Constant.ConstantDeclarationDefaultExpressionBlock`
is derived from :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlockEndedBySemicolon`.

Generic Expression Form
***********************

ExpressionBlock
---------------

**Condensed definition of class** :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlock`:

.. code-block:: Python

   @Export
   class ExpressionBlock(Block):
     CHARACTER_TRANSLATION = {
       "=":    EqualOperator,
       "+":    PlusOperator,
       "-":    MinusOperator,
       "*":    MultiplyOperator,
       "/":    DivideOperator,
       "&":    ConcatOperator,
       "<":    LessThanOperator,
       ">":    GreaterThanOperator,
       ",":    DelimiterToken
       # ";":    EndToken
     }
     FUSED_CHARACTER_TRANSLATION = {
       "**":   PowerOperator,
       "/=":   UnequalOperator,
       "<=":   LessThanOrEqualOperator,
       ">=":   GreaterThanOrEqualOperator,
       "?=":   MatchingEqualOperator,
       "?/=":  MatchingUnequalOperator,
       "?<":   MatchingLessThanOperator,
       "?<=":  MatchingLessThanOrEqualOperator,
       "?>":   MatchingGreaterThanOperator,
       "?>=":  MatchingGreaterThanOrEqualOperator
       # "=>":   MapAssociationKeyword,
       # "<=>":  SignalAssociationKeyword
     }
     OPERATOR_TRANSLATIONS = {
       "or":    OrKeyword,
       "nor":   NorKeyword,
       "and":   AndKeyword,
       "nand":  NandKeyword,
       "xor":   XorKeyword,
       "xnor":  XnorKeyword,
       "sla":   SlaKeyword,
       "sll":   SllKeyword,
       "sra":   SraKeyword,
       "srl":   SrlKeyword,
       "not":   NotKeyword,
       "abs":   AbsKeyword
     }



Specific Expression Forms
*************************

Expressions can be ended by:

``)`` or a user-defined character
  See :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlockEndedByCharORClosingRoundBracket`

* ``)`` or a user-defined keyword
  See :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlockEndedByKeywordORClosingRoundBracket`

* ``to`` or ``downto`` keyword
  See :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlockEndedByKeywordOrToOrDownto`

* ``;``
  See :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlockEndedBySemicolon`



ExpressionBlockEndedByCharORClosingRoundBracket
-----------------------------------------------

This block is derived from :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlock`.
It implements an expression that is either ended by a closing round bracket
(``)``) or a user-defined character. When this base-class is inherited, the user
needs to overwrite:

``EXIT_CHAR``
  The character causing this parser to exit and close this expression block.

``EXIT_TOKEN``
  The token that is emitted as a replacement for the :class:`~pyVHDLParser.Token.CharacterToken`.

``EXIT_BLOCK``
  The block that is generated when exiting the block.


**Condensed definition of class** :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlockEndedByCharORClosingRoundBracket`:

.. code-block:: Python

   @Export
   class ExpressionBlockEndedByCharORClosingRoundBracket(ExpressionBlock):
     EXIT_CHAR  : str =   None
     EXIT_TOKEN : Token = None
     EXIT_BLOCK : Block = None

     @classmethod
     def stateBeforeExpression(cls, parserState: ParserState):

     @classmethod
     def stateExpression(cls, parserState: ParserState):

     @classmethod
     def stateWhitespace1(cls, parserState: ParserState):



ExpressionBlockEndedByKeywordORClosingRoundBracket
--------------------------------------------------

This block is derived from :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlock`.

ExpressionBlockEndedByKeywordOrToOrDownto
-----------------------------------------

This block is derived from :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlock`.

ExpressionBlockEndedBySemicolon
-------------------------------

This block is derived from :class:`~pyVHDLParser.Blocks.Expression.ExpressionBlock`.
