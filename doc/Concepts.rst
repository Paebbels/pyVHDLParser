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

   * ☐ file encryption
   * ☐ conditional analysis (new since VHDL-2019)

1. Token generation

   * ☑ slice text file into character groups (tokens/words)
   * ☑ preserve whitespace (space, tab, linebreak)
   * ☑ preserved comments (single-/multi-line comments)

2. Block generation

   * ☑ assemble tokens in blocks (snippets of a statements) for faster document
     navigation
   * ☑ exchange simple tokens (e.g. string token) with specific tokens (e.g.
     identifier)

3. Group generation

   * ☑ assemble blocks in groups (statements)

4. Code-DOM generation

   * ☐ read stream of groups to assemble the Code-DOM
   * ☐ extract information from a group, their blocks or again their specific tokens

5. Comment annotation

   * ☐ Scan the data structure for comments and annotate comment to statements

6. Build language model

   * ☐ Combine multiple Code-DOMs to form a full language model

7. Build dependencies

   * ☐ Analyze order
   * ☐ Type hierarchy
   * ☐ Instance hierarchy

8. Checkers

   * ☐ Check symbols (identifiers, types, ...)
   * ☐ Check code style
   * ☐ Check documentation

9. Statistics

   * ☐ Create statistics (SLoC, Comments vs. Code, ...)
