.. _concept:

Concepts
########

.. _concept-passes:

Passes
******

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
