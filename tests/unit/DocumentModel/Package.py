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


class Package(TestCase):
	@skip("Not working yet")
	def test_Package(self):
		code = dedent("""\
			package p is
			end package;
			""")

		document = Document("Package.vhdl")
		document.Parse(code)

		self.assertTrue(len(document.Architectures) == 0,   "Document contains unexpected architectures.")
		self.assertTrue(len(document.Configurations) == 0,  "Document contains unexpected configurations.")
		self.assertTrue(len(document.Contexts) == 0,        "Document contains unexpected contexts.")
		self.assertTrue(len(document.Entities) == 0,        "Document contains unexpected entities.")
		self.assertTrue(len(document.Libraries) == 0,       "Document contains unexpected libraries.")
		self.assertTrue(len(document.PackageBodies) == 0,   "Document contains unexpected packageBodies.")
		self.assertTrue(len(document.Packages) == 1,        "Document doesn't contain the expected package.")
		self.assertTrue(len(document.Uses) == 0,            "Document contains unexpected uses.")
