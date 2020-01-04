.. _concept:

Concepts
########

.. _concept-passes:

Multiple Passes
***************

The parser is implemented as a multiple-pass parser, so the gained knowledge is
deepened pass-by-pass. More over, the parser is implemented as a
streaming-parser implemented with Python generators.

**Passes:**

0. VHDL file pre-processing - needed for tool directives:

   * :fa:`square-o` file encryption
   * :fa:`square-o` conditional analysis (new since VHDL-2019)

1. Token generation

   * :fa:`check-square-o` slice text file into character groups (tokens/words)
   * :fa:`check-square-o` preserve whitespace (space, tab, linebreak)
   * :fa:`check-square-o` preserved comments (single-/multi-line comments)

2. Block generation

   * :fa:`check-square-o` assemble tokens in blocks (snippets of a statements) for faster document
     navigation
   * :fa:`check-square-o` exchange simple tokens (e.g. string token) with specific tokens (e.g.
     identifier)

3. Group generation

   * :fa:`check-square-o` assemble blocks in groups (statements)

4. Code-DOM generation

   * :fa:`square-o` read stream of groups to assemble the Code-DOM
   * :fa:`square-o` extract information from a group, their blocks or again their specific tokens

5. Comment annotation

   * :fa:`square-o` Scan the data structure for comments and annotate comment to statements

6. Build language model

   * :fa:`square-o` Combine multiple Code-DOMs to form a full language model

7. Build dependencies

   * :fa:`square-o` Analyze order
   * :fa:`square-o` Type hierarchy
   * :fa:`square-o` Instance hierarchy

8. Checkers

   * :fa:`square-o` Check symbols (identifiers, types, ...)
   * :fa:`square-o` Check code style
   * :fa:`square-o` Check documentation

9. Statistics

   * :fa:`square-o` Create statistics (SLoC, Comments vs. Code, ...)


Object-Oriented Programming
***************************

Data Structures
===============

All internal data structures are implemented as classes with fields (Python
calls it attributes), methods, properties (getter and setters) and references
(pointers) to other instances of classes.

All data is accompanied by its modification procedures in form of methods. New
instances of a class can be created by calling the class and implicitly
executing its initializer method ``__init__`` or by calling a classmethod to
help constructing that instance.

Inheritance
===========

pyVHDLParser makes heavy use of inheritance to share implementations and to
allow other classes or a user to modify the behavior of all derived classes by
modifying a single point.


Multiple Inheritance (Mixins)
=============================

pyVHDLParser uses multiple inheritance via mixin classes. This allows e.g. an
abstract definition of data models, which are later combined with a parser.


Properties
==========

Instead of individual getter and setter methods, pyVHDLParser user Python
properties.


Overwriting
===========

.. todo::

   Concepts -> OOP -> Overwriting

Overloading
===========

.. todo::

   Concepts -> OOP -> Overloading

Meta-Classes
============

Some additional behaviour can be easier implemented by modifying the class
constructing other classes. Python calls this a meta-class. One prominent
example is :class:`type`.

Type Annotations
================

pyVHDLParser uses type annotations in method parameter definitions and in
class field declarations to give hints in IDEs and documentation, what objects
of which types are expected.


Double-Linked Lists
*******************

Data structures with direct references (pointers) in general and double linked
lists in specific are approaches to implement fast and typed navigation from
object to object. If a reference has multiple endpoints, it is either an
order-preserving :class:`list` or :class:`OrderedDict`.

Many parts in pyVHDLParser form a chain of double-linked objects like tokens,
blocks and groups. These object chains (or linked lists) can easily be
:term:`iterated <iterator>`. Iterators can consume such  and reemit the content
in a modified way.

More over, such iterators can be packaged into Python generators.

Iterators and generators can be used in Python's ``for`` [1]_ loops.



Python generators
*****************

.. todo::

   Describe why pyVHDLParser uses Pythons generators, co-routines and ``yield``.



Parallelism
***********

.. todo::

   Describe how to parallelize on multiple cores.


Token replacement
*****************

.. todo::

   Describe why and how tokens are replaced. Describe why this is not corrupting data.


Classmethods as States
**********************

.. todo::

   Describe why pyVHDLParser uses classmethods to represent parser states.

Parser State Machine
********************

.. todo::

   Describe how the parser works in pyVHDLParser.

Code-DOM
********

.. todo::

   Describe what a Code-DOM is.


------------------------

.. rubric:: Footnotes:

.. [1] Actually, Python's ``for``-loop is a ``foreach``-loop.
