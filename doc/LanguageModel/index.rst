VHDL Language Model
###################

Concepts not defined by IEEE Std. 1076
**************************************

Design
======

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.Design`:

.. code-block:: Python

   @Export
   class Design(ModelEntity):
     _libraries :  List =  []    #: List of all libraries defined for a design
     _documents :  List =  []    #: List of all documents loaded for a design

     def __init__(self):

     @property
     def Libraries(self):

     @property
     def Documents(self):


Library
=======

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.Library`:

.. code-block:: Python

   @Export
   class Library(ModelEntity):
     _configurations : List =  []    #: List of all configurations defined in a library.
     _entities :       List =  []    #: List of all entities defined in a library.
     _packages :       List =  []    #: List of all packages defined in a library.

     def __init__(self):

     @property
     def Configurations(self):

     @property
     def Entities(self):

     @property
     def Packages(self):


Sourcecode File
===============

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.Document`:

.. code-block:: Python

   @Export
   class Document(ModelEntity):
     _contexts :       List =  []    #: List of all contexts defined in a document.
     _configurations : List =  []    #: List of all configurations defined in a document.
     _entities :       List =  []    #: List of all entities defined in a document.
     _architectures :  List =  []    #: List of all architectures defined in a document.
     _packages :       List =  []    #: List of all packages defined in a document.
     _packageBodies :  List =  []    #: List of all package bodies defined in a document.

     def __init__(self):

     @property
     def Contexts(self):

     @property
     def Entities(self):

     @property
     def Architectures(self):

     @property
     def Packages(self):

     @property
     def PackageBodies(self):

.. todo::
   Describe the language model.
