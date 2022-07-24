# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2022 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
import time
from pathlib        import Path

from antlr4 import CommonTokenStream, InputStream
from pyAttributes.ArgParseAttributes import CommandAttribute

from ..LanguageModel import Document
from ..LanguageModel.Reference import UseClause, LibraryClause
from ..LanguageModel.DesignUnit import Entity, Architecture, Package, PackageBody
from ..LanguageModel.InterfaceItem import GenericConstantInterfaceItem, PortSignalInterfaceItem

from ..ANTLR4 import ANTLR2Token
from ..ANTLR4.VHDLLexer import VHDLLexer
from ..ANTLR4.VHDLParser import VHDLParser
from ..ANTLR4.Visitor import VHDLVisitor

from . import FrontEndProtocol, FilenameAttribute


class ANTLRHandlers:
	# ----------------------------------------------------------------------------
	# create the sub-parser for the "token-stream" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("antlr", help="Create DOM from ANTLR4 grammar.", description="Create DOM from ANTLR4 grammar.")
	@FilenameAttribute()
	def HandleANTLR(self: FrontEndProtocol, args):
		self.PrintHeadline()

		file = Path(args.Filename)

		if not file.exists():
			print(f"File '{file}' does not exist.")

		startTime = time.perf_counter()
		with file.open('r') as fileHandle:
			content = fileHandle.read()
		print(f"Load file: {(time.perf_counter() - startTime):.6f}")

		lexer = VHDLLexer(InputStream(content))
		print(f"Lexer:     {(time.perf_counter() - startTime):.6f}")
		stream = CommonTokenStream(lexer)
		parser = VHDLParser(stream)
		print(f"Parser:    {(time.perf_counter() - startTime):.6f}")
		parserTree = parser.rule_DesignFile()
		print(f"ParseTree: {(time.perf_counter() - startTime):.6f}")
		visitor = VHDLVisitor()
		designUnits = visitor.visit(parserTree)
		print(f"Visitor:   {(time.perf_counter() - startTime):.6f}")

		print(f"{'-' * 40}")
		conv = ANTLR2Token()
		converted = conv.ConvertToTokenChain(stream)
		print(f"ANTLR2Token: {(time.perf_counter() - startTime):.6f}")
		# for token in converted:
		# 	print(f"{token!r}")
		print(f"{'-' * 40}")

		document = Document(file, converted[0], converted[-1])
		for designUnit in designUnits:
			if isinstance(designUnit, Entity):
				document.Entities.append(designUnit)
			elif isinstance(designUnit, Architecture):
				document.Architectures.append(designUnit)
			elif isinstance(designUnit, Package):
				document.Packages.append(designUnit)
			elif isinstance(designUnit, PackageBody):
				document.PackageBodies.append(designUnit)

		print("=" * 80)
		print(f"Sourcefile: {document.Path}")
		print(f"  Entities:")
		for entity in document.Entities:
			print(f"    {entity.Identifier}")
			print(f"      Doc-String:")
			for line in entity.docstring:
				print(f"        {line}")
			print(f"      Context:")
			for item in entity.ContextItems:
				if isinstance(item, LibraryClause):
					print(f"        library: {', '.join(item.Names)}")
				elif isinstance(item, UseClause):
					print(f"        use: {', '.join(item.Names)}")
			print(f"      Generics:")
			for generic in entity.GenericItems:
				if isinstance(generic, GenericConstantInterfaceItem):
					print(f"        constant {', '.join(generic.Identifiers)} : {generic.Mode} {generic.Subtype}")
			print(f"      Ports:")
			for port in entity.PortItems:
				if isinstance(port, PortSignalInterfaceItem):
					print(f"        signal {', '.join(port.Identifiers)} : {port.Mode} {port.Subtype}")

			print(f"  Architectures:")
			for arch in document.Architectures:
				print(f"    {arch.Identifier}")
				print(f"      Context:")
				for item in arch.ContextItems:
					if isinstance(item, LibraryClause):
						print(f"        library: {', '.join(item.Names)}")
					elif isinstance(item, UseClause):
						print(f"        use: {', '.join(item.Names)}")

		print(f"  Packages:")
		for package in document.Packages:
			print(f"    {package.Identifier}")
			print(f"      Context:")
			for item in package.ContextItems:
				if isinstance(item, LibraryClause):
					print(f"        library: {', '.join(item.Names)}")
				elif isinstance(item, UseClause):
					print(f"        use: {', '.join(item.Names)}")
			print(f"      Generics:")
			for generic in package.GenericItems:
				if isinstance(generic, GenericConstantInterfaceItem):
					print(f"        constant {', '.join(generic.Identifiers)} : {generic.Subtype}")

		print(f"  Package bodies:")
		for packageBody in document.PackageBodies:
			print(f"    {packageBody.Identifier}")
			print(f"      Context:")
			for item in packageBody.ContextItems:
				if isinstance(item, LibraryClause):
					print(f"        library: {', '.join(item.Names)}")
				elif isinstance(item, UseClause):
					print(f"        use: {', '.join(item.Names)}")

		self.exit()

