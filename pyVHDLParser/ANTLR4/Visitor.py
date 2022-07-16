from .VHDLParser import *
from .VHDLParserVisitor import VHDLParserVisitor


class VHDLVisitor(VHDLParserVisitor):
	def visitDesign_file(self, ctx:VHDLParser.Design_fileContext):
		print(ctx)
