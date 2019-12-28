.. _usecase:

Use Cases
#########

Here is a list of possible use cases for such a parser solution.


.. _usecase-codedom:

Sourcecode Document Model
*************************

A sourcecode document object model (Code-DOM) is a object-oriented programming
model to represent a sourcecode file as a complex structure of object instances.
A Code-DOM can offer a read-only access to source files e.g. to find identifiers
and defined entities. This is called introspection. But it's possible to go a
step further and offer a manipulation API. This is called reflection.


.. _usecase-vhdlmodel:

Language Model
**************

While a Code-DOM focuses on a single file, a language model combines multiple
files, thus Code-DOMs, to an overall project or design understanding. In such
an extended scenario, a language model can offer several additional features
compared to a Code-DOM like: type analysis, cross-references, design hierarchy,
component and package dependencies and compile order.


.. _usecase-graphs:

Dependency Graphs and Cross-References
**************************************

Using a language model, a tool can calculate and visualize the following
dependency graphs:

* compile order
* component hierarchy
* type system / type graphs


.. _usecase-highlight:

Syntax Highlighting
*******************

As a Code-DOM has already knowledge about comments, keywords, identifiers, etc.
it's straight forward to colorize a source document. While syntax-highlighting
and cross-referencing based on pure Code-DOMs might be limited, it can be at
full beauty if syntax highlighting is based on a language model.


.. _usecase-syntax:

Syntax-Checking
***************

A parser is already checking the input for syntax correctness, but pyVHDLParser
is not very strict with all parts of an input file, because some parts might be
parsed to its full depth. Therefore, the Code-DOM can get an additional syntax
checking pass.

As an example, pyVHDLParser considers any number as an integer literal,
regardless of the integers value. Thus an integer literal might exceed an
(universal) integers value range. An additional check can catch such mistakes.


.. _usecase-doc:

Documentation Extraction
************************

A Code-DOM, which still includes all comments, can be used in another pass for
correlation of comments and language elements. The resulting mapping can be
exported in various documentation format like JSON, XML, Restructured Text, ...

.. seealso::

   A VHDL domain for Sphinx: `sphinxcontrib-vhdldomain <https://github.com/Paebbels/sphinxcontrib-vhdldomain>`_


.. _usecase-analysis:

Static Code Analysis
********************

The Code-DOM also allows for static checks like:

* coding style
* code statistics / complexity checks


.. _usecase-transform:

Document Transformation
***********************

As a combination of coding style checks and a Code-DOM or language model,
source files can be manipulated or reformatted according to rules.


.. _usecase-codegen:

Code Generation
***************

As a Code-DOM is a structure of object instances, a Code-DOM can be constructed
from code itself. Thus, a sourcefile can be created from scratch purely in
memory. By using a rule-based formatting from objects to text, a Code-DOM can
be persisted as a VHDL source file.


.. _usecase-upcoming:

Test Platform for new Language Revisions
****************************************

And finally, this project could be used to test upcoming language features in
syntax and functionality.
