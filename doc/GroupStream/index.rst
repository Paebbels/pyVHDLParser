.. _grpstm:

Stream of Groups
################

In the :ref:`third pass <concept-passes>` a stream of double-linked
:class:`~pyVHDLParser.Block.Block` objects is read and grouped in another Python
:term:`generator` to group's. Groups are again a chain of double-linked
objects of base-class :class:`~pyVHDLParser.Groups.Group`.


**Condensed definition of class** :class:`~pyVHDLParser.Groups.Group`:

.. code-block:: Python

   @Export
   class Group(metaclass=MetaGroup):
     __STATES__ = None

     _previousGroup : 'Group' =              None    #: Reference to the previous group.
     NextGroup :      'Group' =              None    #: Reference to the next group.
     InnerGroup :     'Group' =              None    #: Reference to the first inner group.
     _subGroups :     {MetaGroup: 'Group'} = {}      #: References to all inner groups by group type.

     StartBlock :     Block =                None    #: Reference to the first block in the scope of this group.
     EndBlock :       Block =                None    #: Reference to the last block in the scope of this group.
     MultiPart :      bool =                 False   #: True, if this group has multiple parts.

     def __init__(self, previousGroup, startBlock, endBlock=None):
     def __len__(self):
     def __iter__(self):
     def __repr__(self):
     def __str__(self):

     def GetSubGroups(self, groupTypes=None):

     @property
     def PreviousGroup(self):

     @property
     def Length(self):

     @property
     def States(self):



.. _grpstm-metagroups:

Meta Groups
***********

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




.. todo::
   Describe the stream of groups.
