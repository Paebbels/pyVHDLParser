.. _blkstm-metablocks:

Meta Blocks
###########

There are two meta-blocks: :class:`~pyVHDLParser.Blocks.StartOfDocumentBlock`
and :class:`~pyVHDLParser.Blocks.EndOfDocumentBlock`. These blocks represent
a start and end of a token stream. These blocks have a length of ``0`` characters.



.. _blkstm-sodb:

StartOfDocumentBlock
--------------------

This block starts a chain of double-linked blocks in a block stream. It's used,
if the input source is a whole file, otherwise :class:`~pyVHDLParser.Blocks.StartOfSnippetBlock`.
It is derived from base-class :class:`~pyVHDLParser.Blocks.StartOfBlock`
and mixin :class:`~pyVHDLParser.StartOfDocument`.

**Interitance diagram:**

.. inheritance-diagram:: pyVHDLParser.Blocks.StartOfDocumentBlock
   :parts: 1



.. _blkstm-eodb:

EndOfDocumentBlock
------------------

This block ends a chain of double-linked blocks in a block stream. It's used,
if the input source is a whole file, otherwise :class:`~pyVHDLParser.Blocks.EndOfSnippetBlock`.
It is derived from base-class :class:`~pyVHDLParser.Blocks.EndOfBlock`
and mixin :class:`~pyVHDLParser.EndOfDocument`.

**Interitance diagram:**

.. inheritance-diagram:: pyVHDLParser.Blocks.EndOfDocumentBlock
   :parts: 1
