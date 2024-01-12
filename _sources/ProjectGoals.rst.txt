.. _goal:

Project Goals
#############

The main goal of this project is to parse VHDL source files for language
revisions (1987), 1993, 2002/2008 and soon for 2019. The result of the parser
is a Code Document-Object-Model (Code-DOM), for deep inspection of VHDL source
files.

The inspection capabilities and the Code-DOM offers:

* Object-oriented data model
* Bidirectional linking / fast navigation
* Python iterators / generators

The parser is implemented as a multiple-pass parser, so the gained knowledge is
deepened pass-by-pass. More over, the parser is implemented as a
streaming-parser / Python generator. This means for example, the first pass
slices a source file into a chain of double-linked :class:`~pyVHDLParser.Token.Token`. While token
creation, the start and end of a token is preserved as a :class:`~pyVHDLParser.SourceCodePosition`.
In contrast to ordinary parsers, pyVHDLParser preserves cases, whitespaces and
comments.

The finally generated Code-DOM offers an API for single file introspections. It
can be used for static documentation generation or rule-based coding style
checking.

When multiple Code-DOMs are combined to a project, a *Generic VHDL Language Model*
can be assembled. It's possible to implement two model flavors for simulation
(full model) and synthesis (limited model). With such information, a
documentation with detailed type information and cross-references can be
generated.
