.. # Load pre-defined aliases and graphical characters like © from docutils
   # <file> is used to denote the special path
   # <Python>\Lib\site-packages\docutils\parsers\rst\include
.. include:: <isonum.txt>
.. include:: <mmlalias.txt>

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />

.. # define horizontal line for HTML
.. |hr| raw:: html

   <hr />

.. # define additional CSS based styles and ReST roles for HTML
.. raw:: html

   <style type="text/css">
     span.bolditalic {font-weight: bold; font-style: italic; }
     span.underline {text-decoration: underline; }
   </style>

.. role:: bolditalic
   :class: bolditalic

.. role:: underline
   :class: underline

.. role:: xlarge
   :class: xlarge

.. role:: pycode(code)
   :language: python
   :class: highlight
