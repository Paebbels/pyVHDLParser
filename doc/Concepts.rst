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

   * :fa:`square-o` File decryption
   * :fa:`square-o` Conditional analysis (new since VHDL-2019)

1. Token generation

   * :fa:`check-square-o` Slice a text file into character groups (tokens/words)
   * :fa:`check-square-o` Preserve whitespace (space, tab, linebreak)
   * :fa:`check-square-o` Preserved comments (single-/multi-line comments)

2. Block generation

   * :fa:`check-square-o` Assemble tokens in blocks (snippets of a statements) for faster document
     navigation
   * :fa:`check-square-o` Exchange simple tokens (e.g. string token) with specific tokens (e.g.
     identifier or keyword)

3. Group generation

   * :fa:`check-square-o` Assemble blocks in groups (statements)

4. Code-DOM generation

   * :fa:`square-o` Consume a stream of groups to assemble the Code-DOM
   * :fa:`square-o` Extract information from a group, their blocks or their specific tokens

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
modifying a single source.


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
:term:`iterated <iterator>`. Iterators can consume such linked lists and reemit
the content in a modified way.

More over, such iterators can be packaged into Python generators.

Iterators and generators can be used in Python's ``for`` [1]_ loops.



Python iterators
****************

A Python iterable is an object implementing an ``__iter__`` method returning an
iterator. The iterator implements a ``__next__`` method to return the next
element in line. Usually, the iterator has some internal state, so it can compute
the next element. At the end of an iteration, :exc:`StopIteration` is raised.

.. code-block:: Python

   class Data:
     list : List = []

     class Iterator:
       obj :   Data = None
       value : Int =  None

       def __init__(self, obj):
         self.obj =   obj
         self.value = 1

       def __next__(self):
         x = self.value
         try:
           self.value += 1
           return obj.list[x]
         except KeyError:
           raise StopIteration

     def __iter__(self):
       return Iterator(self)

   myData = Data()

   for x in myData:
     print(x)



Python generators
*****************

A Python generator is a co-routine (function or method) that return execution
flow from callee and in most cases with a return value to the caller. The state
of the routine is preserved (e.g. local variables). When the execution in the
co-routine is continued, it continues right after the ``yield`` statement.

It's also possible to send parameters from caller to callee, when continuing the
co-routines execution. (use ``send`` method.)

The generation of tokens, blocks and groups is implemented as a generator heavily
using the ``yield`` statement.



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

.. topic:: Design principles

* Clearly named classes that model the semantics of VHDL.
* All language constructs (statements, declarations, specifications, ...)
  have their own classes. These classes are arranged in a logical hierarchy,
  with a single common base-class.
* Child objects shall have a reference to their parent.
* Comments will be associated with a particular code object.
* Easy modifications of the object tree.
* Support formatting code objects as text for export and debugging.
* Allow creating a CodeDOM from input file or via API calls.
* Support resolving of symbolic references into direct references to other
  objects.

.. note::

   CodeDOM is based on the ideas of `Project Roslyn <https://github.com/dotnet/roslyn>`__
   and a series of `CodeProject <https://www.codeproject.com/>`__ articles
   written by `Ken Beckett <https://www.codeproject.com/script/Membership/View.aspx?mid=473427>`__
   in 2012.

   * `The Future of Software Development: CodeDOMs (Part 1) <https://www.codeproject.com/Articles/488657/The-Future-of-Software-Development-CodeDOMs-Part-1>`__
   * `Creating a CodeDOM: Modeling the Semantics of Code (Part 2) <https://www.codeproject.com/Articles/490184/Creating-a-CodeDOM-Modeling-the-Semantics-of-Code>`__
   * `Displaying a CodeDOM using WPF (Part 3) <https://www.codeproject.com/Articles/491550/Displaying-a-CodeDOM-using-WPF-Part-3>`__
   * `Object-Oriented Parsing: Breaking With Tradition (Part 4) <https://www.codeproject.com/Articles/492466/Object-Oriented-Parsing-Breaking-With-Tradition-Pa>`__
   * `CodeDOM Classes for Solution and Project Files (Part 5) <https://www.codeproject.com/Articles/495311/CodeDOM-Classes-for-Solution-and-Project-Files-Par>`__
   * `Accessing Assembly Metadata with Reflection or Mono Cecil (Part 6) <https://www.codeproject.com/Articles/499960/Accessing-Assembly-Metadata-with-Reflection-or-Mon>`__
   * `Resolving Symbolic References in a CodeDOM (Part 7) <https://www.codeproject.com/Articles/502354/Resolving-Symbolic-References-in-a-CodeDOM-Part-7>`__
   * `Calculating Metrics and Searching with a CodeDOM (Part 8) <https://www.codeproject.com/Articles/505579/Calculating-Metrics-and-Searching-with-a-CodeDOM-P>`__

------------------------

.. rubric:: Footnotes:

.. [1] Actually, Python's ``for``-loop is a ``foreach``-loop.
