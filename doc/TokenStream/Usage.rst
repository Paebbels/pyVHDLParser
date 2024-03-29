Usage
#####

The following shows two code examples on how to use the Tokenizer. The first is
generator-based. The second one retrieves an iterator from the generator and
uses low-level access to the chain of tokens.

Token Generator
***************

At first, a file is opened and the file content is read into a string buffer
called ``content``. Strings are iterable, thus a string can be an input for the
Tokenizer.

At second, a generator object is created by ``GetVHDLTokenizer(...)``.

Finally, a *for*-loop can process each token from :class:`~pyVHDLParser.Token.StartOfDocumentToken`
to :class:`~pyVHDLParser.Token.EndOfDocumentToken`.

.. code-block:: Python

   # Open a source file
   with file.open('r') as fileHandle:
     content = fileHandle.read()

   from pyVHDLParser.Base         import ParserException
   from pyVHDLParser.Token        import StartOfDocumentToken, EndOfDocumentToken
   from pyVHDLParser.Token.Parser import Tokenizer

   # get a token generator
   tokenStream = Tokenizer.GetVHDLTokenizer(content)

   try:
     for token in tokenStream:
       print("{token}".format(token=token))
     except ParserException as ex:
       print("ERROR: {0!s}".format(ex))
     except NotImplementedError as ex:
       print("NotImplementedError: {0!s}".format(ex))



Token Iterator
**************

Similar to the previous example, a stream of tokens is generated by a token
generator. This time, iteration is manually implemented with a *while*-loop. The
function :func:`iter` creates an iterator object from a generator object. At
next, calling :func:`next` returns a new token for each call.

The example wants to print the outer objects (first and last) of the token chain.
So at first, :func:`next` is called once to get the first element. Then an
endless loop is used to generate all tokens. If the generator ends, it raises
a :exc:`StopIteration` exception. The last token will be stored in variable
``lastToken``.

.. code-block:: Python

   # Open a source file
   with file.open('r') as fileHandle:
     content = fileHandle.read()

   from pyVHDLParser.Base         import ParserException
   from pyVHDLParser.Token        import StartOfDocumentToken, EndOfDocumentToken
   from pyVHDLParser.Token.Parser import Tokenizer

   # get a token generator
   tokenStream = Tokenizer.GetVHDLTokenizer(content)

   # get the iterator for that generator
   tokenIterator = iter(tokenStream)
   firstToken =    next(tokenIterator)

   try:
     while lastToken := next(tokenIterator):
       pass
   except StopIteration:
     pass

   print("first token: {token}".format(token=firstToken))
   print("last token:  {token}".format(token=lastToken))

