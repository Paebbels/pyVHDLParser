.. include:: shields.inc

.. raw:: latex

   \part{Introduction}

--------------------------------------------------------------------------------

.. only:: html

   |SHIELD:svg:GH-Logo|

.. #
   |SHIELD:svg:Travis-CI|
   |SHIELD:svg:AppVeyor|
   |SHIELD:svg:Landscape|
   |SHIELD:svg:Requirements|
   |br|
   |SHIELD:svg:Gitter:PoC|
   |SHIELD:svg:Gitter:News|
   |br|
   |SHIELD:svg:GH-Tag|
   |SHIELD:svg:GH-Release|
   |SHIELD:svg:License-Code|
   |SHIELD:svg:License-Docs|
   |hr|

.. only:: latex

   .. image:: https://img.shields.io/badge/-VLSI--EDA/PoC-323131.png?style=flat&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABKVBMVEX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FOe9X6AAAAYnRSTlMAAQIDBAcIDA0PEBESFBUWGBkeHyEoMTIzNDU4OTw%2BP0JGWVxeX2BiY2RlZ2hvc3R1eHp%2Bio%2BXm52epKmqq62usLe5wcLDxMnQ0dLW2tvc3t%2Fh4uPo6uvs8fLz9fb3%2Bvv8%2FsuNaVkAAAF7SURBVHgBjdHZW9NAFAXwE0iElCARZCkuIotEUFyQBSJERBEILaAo6d6e%2F%2F%2BPcO58aZslD%2Fxe5mHuPfOdbzA06R1e1sn65aE3ibw5v8OBjj%2BHNHuvx5Tenp1av2bOdSJkKWKBaAmxhYiFogVoEzckw%2BModXcckryZgDigsgLLu1MVT09V1TvPwgqVAyhlinmpMjsCZWRWCsxTlAEEFIvIWKQIALdLsYaMNYqui02KPw4ynN8Um%2FAp1pGzTuEj1Ek2cmz9dogmlVsUuKXSBEUFBaoUoKihQI0iPqaQMxWvnlOsImeV4hz7FBcmMswLin0sU9tBxg61ZYw3qB25SHhyRK0xDuySX179INtfN8qjOvz5u6BNjbsAplvsbVm%2FqAQGFOMb%2B1rTULZJPnsqf%2FMC2kv2bUOYZ%2BR3lLzPr0ehPWbszITmVsn3GCqRWtVFbKZC%2Fvz45tOj1EBlBgPOCUUpOXDiIMF4%2Bzc98G%2FDQNrY1tW9Bc26v%2Fowhof6D6AkqSgsdGGuAAAAAElFTkSuQmCC
      :target: https://www.github.com/VLSI-EDA/PoC
      :alt: Source Code on GitHub

.. #
   |SHIELD:png:GH-Logo|
   |SHIELD:png:Travis-CI|
   |SHIELD:png:AppVeyor|
   |SHIELD:png:Landscape|
   |SHIELD:png:Requirements|
   |br|
   |SHIELD:png:Gitter:PoC|
   |SHIELD:png:Gitter:News|
   |br|
   |SHIELD:png:GH-Tag|
   |SHIELD:png:GH-Release|
   |SHIELD:png:License-Code|
   |SHIELD:png:License-Docs|

The pyVHDLParser Documentation
##############################

This is a token-stream based parser for VHDL-2008.

Main Goals
**********

* **Parsing**

  * slice an input document into **tokens** and text **blocks** which are categorized
  * preserve case, whitespace and comments
  * recover on parsing errors
  * good error reporting / throw exceptions

* **Fast Processing**

  * multi-pass parsing and analysis
  * delay analysis if not needed at current pass
  * link tokens and blocks for fast-forward scanning

* **Generic VHDL Language Model**

  * Assemble a document-object-model (Code-DOM)
  * Provide an API for code introspection

See chapter :ref:`goal` for details.


Use Cases
*********

* generate :ref:`documentation <usecase-doc>` by using the fast-forward scanner
* generate a :ref:`document <usecase-codedom>`/:ref:`language <usecase-vhdlmodel>` model by using the grouped text-block scanner
* extract compile orders and other dependency :ref:`graphs <usecase-graphs>`
* generate :ref:`highlighted syntax <usecase-highlight>`

.. seealso::

   See chapter :ref:`usecase` for details.

Parsing Approach
****************

1. slice an input document into **tokens**
2. assemble tokens to text **blocks** which are categorized
3. assemble text blocks for fast-forward scanning into **groups**
4. translate groups into a document-object-model (DOM)
5. provide a generic VHDL language model

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

   Dec. 2019 - Major reworks
   =========================

.. only:: latex

   .. rubric:: Dec. 2019 - Major reworks

* Reworked and updated documentation.
* Implemented a new test frontend.

.. only:: html

   Dec. 2018 - Minor updates
   ==========================

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

* `Patrick Lehmann <https://github.com/Paebbels>`_ (Maintainer)


License
*******

This library is licensed under **Apache License 2.0**.

------------------------------------

.. |docdate| date:: %b %d, %Y - %H:%M

.. only:: html

   This document was generated on |docdate|.


.. toctree::
   :caption: Introduction
   :hidden:

   ProjectGoals
   UseCases
   Concepts
   Installation
   Dependencies

.. raw:: latex

   \part{Main Documentation}

.. toctree::
   :caption: Main Documentation
   :hidden:

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

.. raw:: latex

   \part{Appendix}

.. toctree::
   :caption: Appendix
   :hidden:

   ChangeLog/index
   License
   Glossary
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
