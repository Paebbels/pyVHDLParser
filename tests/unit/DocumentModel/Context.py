from textwrap import dedent
from unittest import TestCase, skip

from pyVHDLParser.DocumentModel import Document
from tests.unit.Common import Initializer


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class Context(TestCase):
	@skip("Not working yet")
	def test_Context(self):
		code = dedent("""\
			context ctx1 is
				library lib1;
				use     lib1.pkg1.all;
			end context;
			""")

		document = Document("Context.vhdl")
		document.Parse(code)

		self.assertTrue(len(document.Architectures) == 0,   "Document contains unexpected architectures.")
		self.assertTrue(len(document.Configurations) == 0,  "Document contains unexpected configurations.")
		self.assertTrue(len(document.Contexts) == 1,        "Document doesn't contain the expected context.")
		self.assertTrue(len(document.Entities) == 0,        "Document contains unexpected entities.")
		self.assertTrue(len(document.Libraries) == 0,       "Document contains unexpected libraries.")
		self.assertTrue(len(document.PackageBodies) == 0,   "Document contains unexpected package bodies.")
		self.assertTrue(len(document.Packages) == 0,        "Document contains unexpected packages.")
		self.assertTrue(len(document.Uses) == 0,            "Document contains unexpected uses.")
