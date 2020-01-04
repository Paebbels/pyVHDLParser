.. _lngmod:

VHDL Language Model
###################

Concepts not defined by IEEE Std. 1076
**************************************

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



Enumerations
************

Modes
=====

.. todo::

   Write documentation.

Object Classes
==============

.. todo::

   Write documentation.

Interface Items
***************

Interface items are used in generic, port and parameter declarations.

* :class:`~pyVHDLParser.VHDLModel.GenericInterfaceItem`

  * :class:`~pyVHDLParser.VHDLModel.GenericConstantInterfaceItem`
  * :class:`~pyVHDLParser.VHDLModel.GenericTypeInterfaceItem`
  * :class:`~pyVHDLParser.VHDLModel.GenericSubprogramInterfaceItem`
  * :class:`~pyVHDLParser.VHDLModel.GenericPackageInterfaceItem`

* :class:`~pyVHDLParser.VHDLModel.PortInterfaceItem`

  * :class:`~pyVHDLParser.VHDLModel.PortSignalInterfaceItem`

* :class:`~pyVHDLParser.VHDLModel.ParameterInterfaceItem`

  * :class:`~pyVHDLParser.VHDLModel.ParameterConstantInterfaceItem`
  * :class:`~pyVHDLParser.VHDLModel.ParameterVariableInterfaceItem`
  * :class:`~pyVHDLParser.VHDLModel.ParameterSignalInterfaceItem`
  * :class:`~pyVHDLParser.VHDLModel.ParameterFileInterfaceItem`


Generic Interface Item
======================

GenericConstantInterfaceItem
----------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.GenericConstantInterfaceItem`:

.. code-block:: Python

   @Export
   class GenericConstantInterfaceItem(GenericInterfaceItem):



GenericTypeInterfaceItem
------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.GenericTypeInterfaceItem`:

.. code-block:: Python

   @Export
   class GenericTypeInterfaceItem(GenericInterfaceItem):



GenericSubprogramInterfaceItem
------------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.GenericSubprogramInterfaceItem`:

.. code-block:: Python

   @Export
   class GenericSubprogramInterfaceItem(GenericInterfaceItem):



GenericPackageInterfaceItem
---------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.GenericPackageInterfaceItem`:

.. code-block:: Python

   @Export
   class GenericPackageInterfaceItem(GenericInterfaceItem):



Port Interface Item
===================


PortSignalInterfaceItem
-----------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.PortSignalInterfaceItem`:

.. code-block:: Python

   @Export
   class PortSignalInterfaceItem(PortInterfaceItem):


Parameter Interface Item
=========================


ParameterConstantInterfaceItem
------------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.ParameterConstantInterfaceItem`:

.. code-block:: Python

   @Export
   class ParameterConstantInterfaceItem(ParameterInterfaceItem):



ParameterVariableInterfaceItem
------------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.ParameterVariableInterfaceItem`:

.. code-block:: Python

   @Export
   class ParameterVariableInterfaceItem(ParameterInterfaceItem):



ParameterSignalInterfaceItem
----------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.ParameterSignalInterfaceItem`:

.. code-block:: Python

   @Export
   class ParameterSignalInterfaceItem(ParameterInterfaceItem):



ParameterFileInterfaceItem
--------------------------

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLParser.VHDLModel.ParameterFileInterfaceItem`:

.. code-block:: Python

   @Export
   class ParameterFileInterfaceItem(ParameterInterfaceItem):



Design Units
************

* Primary Units

  * Context
  * Configuration
  * Entity
  * Package

* Secondary Units

  * Architeture
  * Package Body

Primary Units
=============

Context
-------

.. todo::

   Write documentation.

Configuration
-------------

.. todo::

   Write documentation.

Entity
------

.. todo::

   Write documentation.

Package
-------

.. todo::

   Write documentation.

Secondary Units
===============

Architeture
-----------

.. todo::

   Write documentation.

Package Body
------------

.. todo::

   Write documentation.

Type Declarations
*****************

* Types

  * Scalar types

    * Enumeration
    * Integer
    * Real
    * Physical

  * Composite types

    * Array
    * Record

  * Access
  * File
  * Protected

* Subtype


Scalar Types
============

Enumeration
-----------

.. todo::

   Write documentation.

Integer
-------

.. todo::

   Write documentation.

Real
----

.. todo::

   Write documentation.

Physical
--------

.. todo::

   Write documentation.

Composite Types
===============

Array
-----

.. todo::

   Write documentation.

Record
------

.. todo::

   Write documentation.

Access
======

.. todo::

   Write documentation.

File
====

.. todo::

   Write documentation.

Protected
=========

.. todo::

   Write documentation.

Object Declartions
******************

* Constant
* Variable
* Shared variable
* Signal
* File

Constant
========

.. todo::

   Write documentation.

Variable
========

.. todo::

   Write documentation.

Shared Variable
===============

.. todo::

   Write documentation.

Signal
======

.. todo::

   Write documentation.

File
====

.. todo::

   Write documentation.


Subprogram Declarations
***********************

* Procedure
* Function

Procedure
=========

.. todo::

   Write documentation.

Function
========

.. todo::

   Write documentation.

Concurrent Statements
*********************

* Assert
* Signal assignment
* Instantiation
* If generate
* Case generate
* For generate
* Procedure call
* Process

Assert
======

.. todo::

   Write documentation.

Signal Assignment
=================

.. todo::

   Write documentation.

Instantiation
=============

.. todo::

   Write documentation.

If Generate
===========

.. todo::

   Write documentation.

Case Generate
=============

.. todo::

   Write documentation.

For Generate
============

.. todo::

   Write documentation.

Procedure Call
==============

.. todo::

   Write documentation.

Process
=======

.. todo::

   Write documentation.


Sequential Statements
*********************

* Signal assignment
* Variable assignment
* If statement
* Case statement+
* For loop
* While loop
* Report statement
* Assert statement
* Procedure call

Signal Assignment
=================

.. todo::

   Write documentation.

Variable Assignment
===================

.. todo::

   Write documentation.

If Statement
============

.. todo::

   Write documentation.

Case Statement
==============

.. todo::

   Write documentation.

For Loop
========

.. todo::

   Write documentation.

While Loop
==========

.. todo::

   Write documentation.

Report Statement
================

.. todo::

   Write documentation.

Assert Statement
================

.. todo::

   Write documentation.

Procedure Call
==============

.. todo::

   Write documentation.
