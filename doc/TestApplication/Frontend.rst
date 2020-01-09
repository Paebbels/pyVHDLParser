Command Line Interface :file:`Frontend.py`
##########################################

Commands:

Common Options
**************

``-q`` - quiet
  Print almost no messages

``-v`` - verbose
  Print more messages

``-d`` - debug
  Print all messages


Token Generation
****************

The command ``tokenize`` creates a colored stream of tokens.

.. rubric:: Usage

.. code-block::

   > Frontend.py tokenize <filename>

.. rubric:: Result

.. image:: /images/TokenStream.vhdl/tokenize.png


Testing Token Generation
************************

The double-linking between tokens can be tested with the following command:

.. code-block::

   > Frontend.py check-tokenize <filename>

.. rubric:: Result

Only errors are reported.

.. image:: /images/TokenStream.vhdl/check-tokenize.png



Block Generation
****************

The command ``blockstream`` creates a colored stream of blocks. The tokens per
block can be displayed as nested items by enabling the verbose mode (``-v``).

.. rubric:: Usage

.. code-block::

   > Frontend.py blockstreaming <filename>

.. rubric:: Result

.. image:: /images/TokenStream.vhdl/blockstream.png


.. rubric:: Usage (verbose)

.. code-block::

   > Frontend.py blockstreaming <filename>

.. rubric:: Result (verbose)

.. image:: /images/TokenStream.vhdl/blockstream-verbose.png


Testing Blocks Generation
*************************

.. todo::

   Document the ``check-blockstream <filename>`` command.


Testing Groups Generation
*************************

.. todo::

   Document the ``groupstreaming <filename>`` command.

