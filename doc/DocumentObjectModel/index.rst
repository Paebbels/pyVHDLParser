Code-DOM
########

A Code-DOM is a Document-Object-Model for source code files.

**Condensed definition of class** :class:`~pyVHDLParser.DocumentObjectModel.Document`:

.. code-block:: Python

   class Document(DocumentModel):
     def __init__(self, file):

     def Parse(self, content=None):

     @classmethod
     def stateParse(cls, document, startOfDocumentGroup):

     def AddLibrary(self, library):
     def AddUse(self, use):

     @property
     def Libraries(self):

     @property
     def Uses(self):

     def AddEntity(self, entity):
     def AddArchitecture(self, architecture):
     def AddPackage(self, package):
     def AddPackageBody(self, packageBody):

     def Print(self, indent=0):



.. todo::
   Describe the Code-DOM.
