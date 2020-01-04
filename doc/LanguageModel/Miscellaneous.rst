.. _lngmod-misc:

Concepts not defined by IEEE Std. 1076
######################################

Some features required for a holistic language model are not defined in
the VHDL :term:`LRM` or made explicitly implementation specific to the implementer.

.. _lngmod-design:

Design
======

The root element in the language model is a design mode out of multiple
sourcecode files (documents). Sourcecode files are compiled into libraries. Thus
a design has the two child nodes: ``Libraries`` and ``Documents``. Each is a
:class:`list`.

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



.. _lngmod-library:

Library
=======

A library contains multiple *design units*. Each design unit listed in a library
is a *primary* design unit like: ``configuration``, ``entity``, ``package`` or
``context``.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.Library`:

.. code-block:: Python

   @Export
   class Library(ModelEntity):
     _contexts :       List =  None    #: List of all contexts defined in a library.
     _configurations : List =  None    #: List of all configurations defined in a library.
     _entities :       List =  None    #: List of all entities defined in a library.
     _packages :       List =  None    #: List of all packages defined in a library.

     def __init__(self):

     @property
     def Context(self):

     @property
     def Configurations(self):

     @property
     def Entities(self):

     @property
     def Packages(self):



.. _lngmod-sourcefile:

Sourcecode File
===============

A source file contains multiple *design units*. Each design unit listed in a
sourcecode file is a *primary* or `secondary`design unit like: ``configuration``,
``entity``, ``architecture``, ``package``, ``package body`` or ``context``.

Design unit may be preceded by a context made of ``library``, ``use`` and
``context`` statements. These statements are not directly visible in the ``Document``
object, because design unit contexts are consumed by the design units. See the
``Libraries`` and ``Uses`` fields of each design unit to investigate the consumed
contexts.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.Document`:

.. code-block:: Python

   @Export
   class Document(ModelEntity):
     _contexts :       List =  None    #: List of all contexts defined in a document.
     _configurations : List =  None    #: List of all configurations defined in a document.
     _entities :       List =  None    #: List of all entities defined in a document.
     _architectures :  List =  None    #: List of all architectures defined in a document.
     _packages :       List =  None    #: List of all packages defined in a document.
     _packageBodies :  List =  None    #: List of all package bodies defined in a document.

     def __init__(self):

     @property
     def Contexts(self):

     @property
     def Configurations(self):

     @property
     def Entities(self):

     @property
     def Architectures(self):

     @property
     def Packages(self):

     @property
     def PackageBodies(self):
