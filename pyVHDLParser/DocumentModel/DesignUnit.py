# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python functions:   A streaming VHDL parser
#
# Description:
# ------------------------------------
#		TODO:
#
# License:
# ==============================================================================
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
# load dependencies
from typing import List

import pyVHDLParser.Blocks.InterfaceObject
from pyVHDLParser.Token.Keywords            import IdentifierToken
from pyVHDLParser.Blocks                    import TokenParserException
from pyVHDLParser.Blocks.List               import GenericList as GenericListBlocks, PortList as PortListBlocks
from pyVHDLParser.Blocks.Object             import Constant
from pyVHDLParser.Blocks.Sequential         import Package as PackageBlock, PackageBody as PackageBodyBlock
from pyVHDLParser.Blocks.Structural         import Entity as EntityBlocks, Architecture as ArchitectureBlocks
from pyVHDLParser.Groups.List               import GenericListGroup, PortListGroup
from pyVHDLParser.VHDLModel                 import Entity as EntityVHDLModel, Architecture as ArchitectureModelModel
from pyVHDLParser.VHDLModel                 import Package as PackageVHDLModel, PackageBody as PackageBodyVHDLModel
from pyVHDLParser.DocumentModel.Reference   import Library, Use
from pyVHDLParser.Functions                 import Console


class Entity(EntityVHDLModel):
	def __init__(self, entityName):
		super().__init__()
		self._name = entityName

	@classmethod
	def stateParse(cls, document, group):
		for block in group:
			if isinstance(block, EntityBlocks.NameBlock):
				for token in block:
					if isinstance(token, IdentifierToken):
						entityName = token.Value
						break
				else:
					raise TokenParserException("EntityName not found.", None)

				entity = cls(entityName)
				entity.AddLibraryReferences(document.Libraries)
				entity.AddUses(document.Uses)

				print("Found library '{0}'. Adding to current node '{1!s}'.".format(entityName, document))
				document.AddEntity(entity)
				break

		subGroupIterator = iter(group.GetSubGroups())
		subGroup =         next(subGroupIterator)

		if isinstance(subGroup, GenericListGroup):
			cls.stateParseGenericList(document, subGroup)
			subGroup = next(subGroupIterator)

		if isinstance(subGroup, PortListGroup):
			cls.stateParsePortList(document, subGroup)
			subGroup = next(subGroupIterator)

		# FIXME entity declarative region
		# if isinstance(subGroup, ):
		# 	cls.stateParsePortList(document, subGroup)
		# 	subGroup = next(subGroupIterator)

		# FIXME entity statements
		# if isinstance(subGroup, ):
		# 	cls.stateParsePortList(document, subGroup)
		# 	subGroup = next(subGroupIterator)

		# FIXME: how to check if everthing is consumed?


	@classmethod
	def stateParseGenericList(cls, document, group):
		assert isinstance(parserState.CurrentGroup, GenericListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock):
				cls.stateParseGeneric(parserState)
			elif isinstance(block, GenericListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParseGeneric(cls, document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				genericName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddGeneric(genericName)

	@classmethod
	def stateParsePortList(cls, document, group):
		assert isinstance(parserState.CurrentGroup, PortListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock):
				cls.stateParsePort(parserState)
			elif isinstance(block, PortListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParsePort(cls, document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				portName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddPort(portName)

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraries.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._uses.append(use)

	def AddGeneric(self, generic):
		self._genericItems.append(generic)

	def AddPort(self, port):
		self._portItems.append(port)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}ENTITY{NOCOLOR} {YELLOW}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(name=self._name, indent=indentation, **Console.Foreground))
		if (len(self._genericItems) > 0):
			print("{indent}  {DARK_CYAN}GENERIC{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for generic in self._genericItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=generic, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation, **Console.Foreground))
		if (len(self._portItems) > 0):
			print("{indent}  {DARK_CYAN}PORT{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for port in self._portItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=port, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation, **Console.Foreground))
		print("{indent}{DARK_CYAN}END ENTITY{NOCOLOR};".format(name=self._name, indent=indentation, **Console.Foreground))


class Architecture(ArchitectureModelModel):
	def __init__(self, architectureName, entityName):
		super().__init__()
		self._name =    architectureName
		self._entity =  entityName

	@classmethod
	def stateParse(cls, document, group):
		# cls.stateParseArchitectureName(parserState)
		#
		# for block in parserState.GroupIterator:
		# 	if isinstance(block, Constant.ConstantBlock):
		# 		raise NotImplementedError()
		# 	# elif isinstance(block, ArchitectureBlock.ConcurrentBeginBlock):
		# 	# 	raise NotImplementedError()
		# 	elif isinstance(block, ArchitectureBlock.EndBlock):
		# 		break
		# else:
		# 	raise TokenParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParseArchitectureName(cls, document, group):
		assert isinstance(parserState.CurrentGroup, ArchitectureBlock.NameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				architectureName = token.Value
				break
		else:
			raise TokenParserException("", None)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				entityName = token.Value
				break
		else:
			raise TokenParserException("", None)

		oldNode = parserState.CurrentNode
		architecture = cls(architectureName, entityName)

		parserState.CurrentNode.AddArchitecture(architecture)
		parserState.CurrentNode = architecture
		parserState.CurrentNode.AddLibraryReferences(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.Uses)

		oldNode.Libraries.clear()
		oldNode.Uses.clear()

	def AddLibraries(self, libraries):
		for library in libraries:
			self._libraryReferences.append(library)

	def AddUses(self, uses):
		for use in uses:
			self._uses.append(use)


	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraryReferences:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}ARCHITECTURE {YELLOW}{name}{NOCOLOR} {DARK_CYAN}OF{NOCOLOR} {GREEN}{entity}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, entity=self._entity, **Console.Foreground))
		print("{indent}{DARK_CYAN}BEGIN{NOCOLOR}".format(indent=indentation, **Console.Foreground))
		print("{indent}{DARK_CYAN}END ARCHITECTURE{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))


class Package(PackageVHDLModel):
	def __init__(self, packageName):
		super().__init__()
		self._name = packageName

	@classmethod
	def stateParse(cls, document, group):
		assert isinstance(parserState.CurrentGroup, PackageBlock.NameBlock)
		cls.stateParsePackageName(parserState)

		for block in parserState.GroupIterator:
			if isinstance(block, GenericListBlocks.OpenBlock):
				parserState.PushState = cls.stateParseGenericList
				parserState.ReIssue()
			elif isinstance(block, ConstantBlock):
				parserState.PushState = Constant.stateParse
				parserState.ReIssue()
			elif isinstance(block, FunctionBlock.NameBlock):
				parserState.PushState = Function.stateParse
				parserState.ReIssue()
			elif isinstance(block, PackageBlock.EndBlock):
				break
			else:
				raise TokenParserException("Block '{0!r}' not supported in a package.".format(block), block)
		else:
			raise TokenParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParsePackageName(cls, document, group):
		assert isinstance(parserState.CurrentGroup, PackageBlock.NameBlock)

		tokenIterator = iter(parserState)
		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise TokenParserException("", None)

		oldNode = parserState.CurrentNode
		package = cls(packageName)

		parserState.CurrentNode.AddPackage(package)
		parserState.CurrentNode = package
		parserState.CurrentNode.AddLibraryReferences(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.Uses)

		oldNode.Libraries.clear()
		oldNode.Uses.clear()

	@classmethod
	def stateParseGenericList(cls, document, group):
		assert isinstance(parserState.CurrentGroup, GenericListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock):
				cls.stateParseGeneric(parserState)
			elif isinstance(block, GenericListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParseGeneric(cls, document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock)

		tokenIterator = iter(parserState)
		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				genericName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddGeneric(genericName)

	def AddLibraryReferences(self, libraries : List[Library]):
		if ((DEBUG is True) and (len(libraries) > 0)): print("{DARK_CYAN}Adding libraries to package {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for library in libraries:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(library, **Console.Foreground))
			self._libraryReferences.append(library._library)

	def AddUses(self, uses : List[Use]):
		if ((DEBUG is True) and (len(uses) > 0)): print("{DARK_CYAN}Adding uses to package {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for use in uses:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(use, **Console.Foreground))
			self._uses.append(use)

	def AddGeneric(self, generic):
		if DEBUG: print("{DARK_CYAN}Adding generic to package {GREEN}{0}{NOCOLOR}:\n  {YELLOW}{1}{NOCOLOR} : {2}".format(self._name, generic, "", **Console.Foreground))
		self._genericItems.append(generic)

	def AddConstant(self, constant):
		if DEBUG: print("{DARK_CYAN}Adding constant to package {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, constant, **Console.Foreground))
		self._declaredItems.append(constant)

	def AddFunction(self, function):
		if DEBUG: print("{DARK_CYAN}Adding function to package {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, function, **Console.Foreground))
		self._declaredItems.append(function)

	def AddProcedure(self, procedure):
		if DEBUG: print("{DARK_CYAN}Adding procedure to package {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, procedure, **Console.Foreground))
		self._declaredItems.append(procedure)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for use in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{item}{NOCOLOR};".format(indent=indentation, lib=use._library, pack=use._package, item=use._item, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}PACKAGE{NOCOLOR} {YELLOW}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, **Console.Foreground))
		if (len(self._genericItems) > 0):
			print("{indent}  {DARK_CYAN}GENERIC{NOCOLOR} (".format(indent=indentation, **Console.Foreground))
			for generic in self._genericItems:
				print("{indent}    {YELLOW}{name}{NOCOLOR} : {GREEN}{type}{NOCOLOR}".format(indent=indentation, name=generic, type="", **Console.Foreground))
			print("{indent}  );".format(indent=indentation))
		if (len(self._declaredItems) > 0):
			for item in self._declaredItems:
				item.Print(indent+1)
		print("{indent}{DARK_CYAN}END PACKAGE{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))


class PackageBody(PackageBodyVHDLModel):
	def __init__(self, packageBodyName):
		super().__init__()
		self._name = packageBodyName

	@classmethod
	def stateParse(cls, document, group):
		assert isinstance(parserState.CurrentGroup, PackageBodyBlock.NameBlock)
		cls.stateParsePackageBodyName(parserState)

		for block in parserState.GroupIterator:
			if isinstance(block, GenericListBlocks.OpenBlock):
				parserState.PushState = cls.stateParseGenericList
				parserState.ReIssue()
			elif isinstance(block, PortListBlocks.OpenBlock):
				parserState.PushState = cls.stateParsePortList
				parserState.ReIssue()
			elif isinstance(block, ConstantBlock):
				parserState.PushState = Constant.stateParse
				parserState.ReIssue()
			elif isinstance(block, Function.BeginBlock):
				parserState.PushState = Function.stateParse
				parserState.ReIssue()
			elif isinstance(block, PackageBodyBlock.EndBlock):
				break
			else:
				raise TokenParserException("Block '{0!r}' not supported in a package body.".format(block), block)
		else:
			raise TokenParserException("", None)

		parserState.Pop()
		# parserState.CurrentBlock = None

	@classmethod
	def stateParsePackageBodyName(cls, document, group):
		assert isinstance(parserState.CurrentGroup, PackageBodyBlock.NameBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				packageName = token.Value
				break
		else:
			raise TokenParserException("", None)

		oldNode = parserState.CurrentNode
		packageBody = cls(packageName)

		parserState.CurrentNode.AddPackageBody(packageBody)
		parserState.CurrentNode = packageBody
		parserState.CurrentNode.AddLibraryReferences(oldNode.Libraries)
		parserState.CurrentNode.AddUses(oldNode.Uses)

		oldNode.Libraries.clear()
		oldNode.Uses.clear()

	@classmethod
	def stateParseGenericList(cls, document, group):
		assert isinstance(parserState.CurrentGroup, GenericListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock):
				cls.stateParseGeneric(parserState)
			elif isinstance(block, GenericListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParseGeneric(cls, document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceConstantBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				genericName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddGeneric(genericName)

	@classmethod
	def stateParsePortList(cls, document, group):
		assert isinstance(parserState.CurrentGroup, PortListBlocks.OpenBlock)

		for block in parserState.GroupIterator:
			if isinstance(block, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock):
				cls.stateParsePort(parserState)
			elif isinstance(block, PortListBlocks.CloseBlock):
				break
		else:
			raise TokenParserException("", None)

		parserState.Pop()

	@classmethod
	def stateParsePort(cls, document, group):
		assert isinstance(parserState.CurrentGroup, pyVHDLParser.Blocks.InterfaceObject.InterfaceSignalBlock)

		tokenIterator = iter(parserState)

		for token in tokenIterator:
			if isinstance(token, IdentifierToken):
				portName = token.Value
				break
		else:
			raise TokenParserException("", None)

		parserState.CurrentNode.AddPort(portName)

	def AddLibraries(self, libraries : List[Library]):
		if ((DEBUG is True) and (len(libraries) > 0)): print("{DARK_CYAN}Adding libraries to package body {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for library in libraries:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(library, **Console.Foreground))
			self._libraries.append(library._library)

	def AddUses(self, uses : List[Use]):
		if ((DEBUG is True) and (len(uses) > 0)): print("{DARK_CYAN}Adding uses to package body {GREEN}{0}{NOCOLOR}:".format(self._name, **Console.Foreground))
		for use in uses:
			if DEBUG: print("  {GREEN}{0!s}{NOCOLOR}".format(use, **Console.Foreground))
			self._uses.append(use)

	def AddConstant(self, constant):
		if DEBUG: print("{DARK_CYAN}Adding constant to package body {GREEN}{0}{NOCOLOR}:\n  {1!s}".format(self._name, constant, **Console.Foreground))
		self._declaredItems.append(constant)

	def Print(self, indent=0):
		indentation = "  "*indent
		for lib in self._libraries:
			print("{indent}{DARK_CYAN}LIBRARY{NOCOLOR} {GREEN}{lib}{NOCOLOR};".format(indent=indentation, lib=lib, **Console.Foreground))
		for lib, pack, obj in self._uses:
			print("{indent}{DARK_CYAN}USE {GREEN}{lib}{NOCOLOR}.{GREEN}{pack}{NOCOLOR}.{GREEN}{obj}{NOCOLOR};".format(indent=indentation, lib=lib, pack=pack, obj=obj, **Console.Foreground))
		print()
		print("{indent}{DARK_CYAN}PACKAGE BODY{NOCOLOR} {GREEN}{name}{NOCOLOR} {DARK_CYAN}IS{NOCOLOR}".format(indent=indentation, name=self._name, **Console.Foreground))
		if (len(self._declaredItems) > 0):
			for item in self._declaredItems:
				item.Print(indent+1)
		print("{indent}{DARK_CYAN}END PACKAGE BODY{NOCOLOR};".format(indent=indentation, name=self._name, **Console.Foreground))