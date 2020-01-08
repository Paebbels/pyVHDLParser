.. _grpstm:

3. Pass - Groups
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



.. toctree::
   :hidden:

   MetaGroups
   GroupGenerator
