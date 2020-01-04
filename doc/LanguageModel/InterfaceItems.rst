.. _lngmod-inter:

Interface Items
###################

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
