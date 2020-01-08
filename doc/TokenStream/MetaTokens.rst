.. _tokstm-metatoken:

Meta Tokens
###########

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
