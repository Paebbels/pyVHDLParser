.. _grpstm-metagroups:

Meta Groups
###########

There are two meta-groups: :class:`~pyVHDLParser.Groups.StartOfDocumentGroup`
and :class:`~pyVHDLParser.Groups.EndOfDocumentGroup`. These groups represent
a start and end of a token stream. These groups have a length of ``0`` characters.



.. _grpstm-sodg:

StartOfDocumentGroup
====================

This group starts a chain of double-linked groups in a group stream. It's used,
if the input source is a whole file, otherwise :class:`~pyVHDLParser.Groups.StartOfSnippetGroup`.
It is derived from base-class :class:`~pyVHDLParser.Groups.StartOfGroup`
and mixin :class:`~pyVHDLParser.StartOfDocument`.

**Interitance diagram:**

.. inheritance-diagram:: pyVHDLParser.Groups.StartOfDocumentGroup
   :parts: 1



.. _grpstm-eodg:

EndOfDocumentGroup
==================

This group ends a chain of double-linked groups in a group stream. It's used,
if the input source is a whole file, otherwise :class:`~pyVHDLParser.Groups.EndOfSnippetGroup`.
It is derived from base-class :class:`~pyVHDLParser.Groups.EndOfGroup`
and mixin :class:`~pyVHDLParser.EndOfDocument`.

**Interitance diagram:**

.. inheritance-diagram:: pyVHDLParser.Groups.EndOfDocumentGroup
   :parts: 1
