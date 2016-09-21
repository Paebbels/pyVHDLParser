# pyVHDLParser

[![Apache License 2.0](https://img.shields.io/github/license/VLSI-EDA/PoC.svg?style=flat)](LICENSE.md)

This is a token-stream based parser for VHDL-2008.

Main goals:
 * slice a input document into text blocks, which are categorized
 * group text blocks for fast-forward scanning
 * provide a generic VHDL language model

Use cases:
 * generate a documentations by using the fast-forward scanner
 * generate a document/language model by using the grouped text-block scanner
 * extract compile orders and other dependency graphs
 * generate highlighted syntax
 * re-annotate documenting comments to there objects for doc extraction

Long time goals:
 * A Sphinx language plugin for VHDL 


#### License

Licensed under [Apache License 2.0](LICENSE.md).
