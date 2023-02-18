.. include:: shields.inc

.. raw:: latex

   \part{Introduction}

.. only:: html

   |SHIELD:svg:pyVHDLParser-github| |SHIELD:svg:pyVHDLParser-tag| |SHIELD:svg:pyVHDLParser-release| |SHIELD:svg:pyVHDLParser-date| |br|
   |SHIELD:svg:pyVHDLParser-lib-status| |SHIELD:svg:pyVHDLParser-lib-dep| |br|
   |SHIELD:svg:pyVHDLParser-travis| |SHIELD:svg:pyVHDLParser-pypi-tag| |SHIELD:svg:pyVHDLParser-pypi-status| |SHIELD:svg:pyVHDLParser-pypi-python| |br|
   |SHIELD:svg:pyVHDLParser-codacy-quality| |SHIELD:svg:pyVHDLParser-codacy-coverage| |SHIELD:svg:pyVHDLParser-codecov-coverage| |SHIELD:svg:pyVHDLParser-lib-rank| |br|
   |SHIELD:svg:pyVHDLParser-rtd| |SHIELD:svg:pyVHDLParser-license|

.. only:: latex

   |SHIELD:png:pyVHDLParser-github| |SHIELD:png:pyVHDLParser-tag| |SHIELD:png:pyVHDLParser-release| |SHIELD:png:pyVHDLParser-date| |br|
   |SHIELD:png:pyVHDLParser-lib-status| |SHIELD:png:pyVHDLParser-lib-dep| |br|
   |SHIELD:png:pyVHDLParser-travis| |SHIELD:png:pyVHDLParser-pypi-tag| |SHIELD:png:pyVHDLParser-pypi-status| |SHIELD:png:pyVHDLParser-pypi-python| |br|
   |SHIELD:png:pyVHDLParser-codacy-quality| |SHIELD:png:pyVHDLParser-codacy-coverage| |SHIELD:png:pyVHDLParser-codecov-coverage| |SHIELD:png:pyVHDLParser-lib-rank| |br|
   |SHIELD:png:pyVHDLParser-rtd| |SHIELD:png:pyVHDLParser-license|

--------------------------------------------------------------------------------

The pyVHDLParser Documentation
##############################

This is a token-stream based parser for VHDL-2008 creating a document object model (DOM).

.. important:: **This package requires Python 3.8+**, because it uses some of the latest Python feature for effective code writing:

   * `Pathlib <https://docs.python.org/3/library/pathlib.html>`__ (Python 3.4)
   * `Type hints <https://docs.python.org/3/library/typing.html#module-typing>`__ (Python 3.5) and for `variables <https://docs.python.org/3/whatsnew/3.6.html#pep-526-syntax-for-variable-annotations>`__ (Python 3.6)
   * `Data classes <https://docs.python.org/3/library/dataclasses.html>`__ (Python 3.7)
   * `Assignment expressions <https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions>`__ (Python 3.8)


Main Goals
**********

* **Parsing**

  * Slice an input document into **tokens** and text **blocks** which are categorized in **groups** for fast indexing
  * Preserve case, whitespace and comments
  * Recover on parsing errors
  * Good error reporting / throw exceptions

* **Fast Processing**

  * Multi-pass parsing and analysis
  * Delay analysis if not needed for current pass
  * Link tokens and blocks for fast-forward scanning (triple helix)

* **Generic VHDL Language Model**

  * Assemble a sourcecode document-object-model (Code-DOM)
  * Provide an API for code introspection
  * Provide an API for code modification / transformation

See chapter :ref:`goal` for details.


Use Cases
*********

* Generate :ref:`documentation <usecase-doc>` by using the fast-forward scanner
* Generate a :ref:`document <usecase-codedom>`/:ref:`language <usecase-vhdlmodel>` model by using the grouped text-block scanner
* Extract compile orders and other dependency :ref:`graphs <usecase-graphs>`
* Generate :ref:`highlighted syntax <usecase-highlight>`

.. seealso::

   See chapter :ref:`usecase` for details.

Parsing Approach
****************

1. Slice an input document into **tokens**
2. Assemble tokens to text **blocks** which are categorized
3. Assemble text blocks for fast-forward scanning into **groups** (indexing)
4. Translate groups into a sourcecode document-object-model (Code-DOM)
5. Provide a generic VHDL language model

.. seealso::

   See chapter :ref:`concept` for details.

Additional Aims
***************

* A VHDL domain for Sphinx

  * A autodoc plugin for the VHDL domain in Sphinx
* VHDL plugins/extensions for style checkers supported by CI environments
* Testing new VHDL language features beyond VHDL-2008/VHDL-2019


News
****

.. only:: html

   Jun. 2021 - Enhancements
   ========================

.. only:: latex

   .. rubric:: Jun. 2021 - Enhancements

* Added infrastructure to run example code provided in issues as testcase.
*
* New Single-File GitHub Action workflow (pipeline).
* Added Dependabot configuration file.
* Updated dependencies

  * Sphinx uses now v4.0.2
  * Removed 2 patched Sphinx extensions &rarr; now using original extensions.

* ...


.. only:: html

   Nov. 2020 - Test cases
   ======================

.. only:: latex

   .. rubric:: Nov. 2020 - Test cases

* Added testcases for Tokenizer and block generation.
* Added first testcases for pass 4 (Code-DOM)
* Collect code and branch coverage.
* ``Frontend.py`` |rarr| pyVHDLParser executable installed via pip


.. only:: html

   Dec. 2019 - Major reworks
   =========================

.. only:: latex

   .. rubric:: Dec. 2019 - Major reworks

* Reworked and updated documentation.
* Implemented a new test frontend.


.. only:: html

   Dec. 2018 - Minor updates
   =========================

.. only:: latex

   .. rubric:: Dec. 2018 - Minor updates

Fixed some NextToken linking problems.


.. only:: html

   Nov. 2017 - New features
   ========================

.. only:: latex

   .. rubric:: Nov. 2017 - New features

Implemented new features like case statements.


.. only:: html

   20.09.2017 - Project started
   ============================

.. only:: latex

   .. rubric:: 20.09.2016 - Project started

Let's create a new parser in Python to process VHDL code.


Contributors
************

* `Patrick Lehmann <https://github.com/Paebbels>`__ (Maintainer)
* `and more... <https://github.com/Paebbels/pyVHDLParser/graphs/contributors>`__


License
*******

This library is licensed under **Apache License 2.0**.

------------------------------------

.. |docdate| date:: %d.%b %Y - %H:%M

.. only:: html

   This document was generated on |docdate|.


.. toctree::
   :caption: Introduction
   :hidden:

   ProjectGoals
   UseCases
   Concepts
   Installation
   TestApplication/index

.. raw:: latex

   \part{Main Documentation}

.. toctree::
   :caption: Main Documentation
   :hidden:

   Preprocessing/index
   TokenStream/index
   BlockStream/index
   GroupStream/index
   DocumentObjectModel/index
   LanguageModel/index

.. #
   SimulationModel/index
   SynthesisModel/index
   Examples/index

.. raw:: latex

   \part{References}

.. toctree::
   :caption: References
   :hidden:

   pyVHDLParser/index
   References/index

.. raw:: latex

   \part{Appendix}

.. toctree::
   :caption: Appendix
   :hidden:

   ChangeLog/index
   License
   Glossary
   TODOs
   genindex
   py-modindex

.. #
   ifconfig:: visibility in ('Internal')

   .. raw:: latex

      \part{Internal}

   .. toctree::
      :caption: Internal
      :hidden:

      Internal/ToDo
