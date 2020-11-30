Command Line Interface :file:`VHDLParser`
#########################################

Commands:

Common Options
**************

``-q`` - quiet
  Print almost no messages.

``-v`` - verbose
  Print more messages.

``-d`` - debug
  Print all messages.


Miscellaneous Commands
**********************

List all available commands and options.

.. rubric:: Usage

.. code-block::

   > VHDLParser help


Print version information.

.. rubric:: Usage

.. code-block::

   > VHDLParser version


Token Generation
****************

The command ``token-stream`` creates a colored stream of tokens.

.. rubric:: Usage

.. code-block::

   > VHDLParser token-stream <filename>

.. rubric:: Result

.. image:: /images/TokenStream.vhdl/tokenize.png


Testing Token Generation
************************

The double-linking between tokens can be tested with the following command:

.. code-block::

   > VHDLParser token-check <filename>

.. rubric:: Result

Only errors are reported.

.. image:: /images/TokenStream.vhdl/check-tokenize.png



Block Generation
****************

The command ``block-stream`` creates a colored stream of blocks. The tokens per
block can be displayed as nested items by enabling the verbose mode (``-v``).

.. rubric:: Usage

.. code-block::

   > VHDLParser block-stream <filename>

.. rubric:: Result

.. image:: /images/TokenStream.vhdl/blockstream.png


.. rubric:: Usage (verbose)

.. code-block::

   > VHDLParser -v block-stream <filename>

.. rubric:: Result (verbose)

.. image:: /images/TokenStream.vhdl/blockstream-verbose.png


Testing Blocks Generation
*************************

.. rubric:: Usage

.. code-block::

   > VHDLParser block-check <filename>

.. rubric:: Result

.. todo:: add image


Testing Groups Generation
*************************

.. rubric:: Usage

.. code-block::

   > VHDLParser group-stream <filename>

.. rubric:: Result

.. todo:: add image


Testing CodeDOM Generation
**************************

.. rubric:: Usage

.. code-block::

   > VHDLParser CodeDOM <filename>

.. rubric:: Result

.. todo:: add image
