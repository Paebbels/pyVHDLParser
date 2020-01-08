Examples
########

List all entity names
*********************

The following example lists all entity names from a given source file. To have
full forward and backward linking between tokens, the chain of tokens must be
fully generated. One easy approach is to use a list comprehension.


.. rubric:: VHDL Sourcefile

.. code-block:: VHDL

   entity myEntity_1 is
   end;

   entity myEntity_2 is
   end;


.. rubric:: Expected Outputs

.. code-block::

   Found entity: myEntity_1
   Found entity: myEntity_2


.. rubric:: Algorithm

1. Forward scan via main iterator searching for a ``WordToken`` of value ``entity``.
2. Start a second (local) forward iteration to search for the next ``WordToken``,
   because an entity keyword must be followed by an identifier.

.. code-block:: Python

   # Open a source file
   with file.open('r') as fileHandle:
     content = fileHandle.read()

   from pyVHDLParser.Base         import ParserException
   from pyVHDLParser.Token        import StartOfDocumentToken, EndOfDocumentToken
   from pyVHDLParser.Token.Parser import Tokenizer

   # get a list of all tokens
   tokenList = [token for token in Tokenizer.GetVHDLTokenizer(content)]

   try:
     for token in tokenList:
       if (isinstance(token, WordToken) and token <= "entity"):
         tok = token.NextToken
         while tok is not None:
           if isinstance(tok, WordToken):
             print("Found entity: {name}".format(name=tok.Value))
             break
           tok = tok.NextToken
     except ParserException as ex:
       print("ERROR: {0!s}".format(ex))
     except NotImplementedError as ex:
       print("NotImplementedError: {0!s}".format(ex))


.. rubric:: Drawbacks

* Reports also ``end entity`` |br|
  Solution: scan backward, if last ``WordToken`` before entity was not of value ``end``.
* Reports also ``entity`` from attribute specifications. |br|
  This is a rare case.
