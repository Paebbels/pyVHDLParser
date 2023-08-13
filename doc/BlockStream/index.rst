.. _blkstm:

2. Pass - Tokens ⇒ Blocks
#########################

In the :ref:`second pass <concept-passes>` a stream of double-linked
:class:`~pyVHDLParser.Token.Token` objects is read and grouped in another Python
:term:`generator` to blocks. Blocks are again a chain of double-linked
objects of base-class :class:`~pyVHDLParser.Blocks.Block`.


**Condensed definition of class** :class:`~pyVHDLParser.Blocks.Block`:

.. code-block:: Python

   @Export
   class Block(metaclass=MetaBlock):
     """Base-class for all :term:`block` classes."""

     __STATES__ :      List = None   #: List of all `state...` methods in this class.

     _previousBlock : Block = None   #: Reference to the previous block.
     NextBlock :      Block = None   #: Reference to the next block.
     StartToken :     Token = None   #: Reference to the first token in the scope of this block.
     EndToken :       Token = None   #: Reference to the last token in the scope of this block.
     MultiPart :      bool =  None   #: True, if this block has multiple parts.

     def __init__(self, previousBlock, startToken, endToken=None, multiPart=False):
     def __len__(self):
     def __iter__(self):
     def __repr__(self):
     def __str__(self):

     @property
     def PreviousBlock(self):

     @property
     def Length(self):

     @property
     def States(self):

     @classmethod
     def stateError(cls, parserState: ParserState):



.. toctree::
   :hidden:

   MetaBlocks
   CommonBlocks
   SpecificBlocks
   BlockGenerator
   Usage
   Examples
