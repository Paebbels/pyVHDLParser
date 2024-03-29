from pyVHDLModel import DesignUnit
from pyVHDLModel.Base import Mode
from pyVHDLModel.Symbol import PackageSymbol
from .VHDLLexer import VHDLLexer

from ..LanguageModel.DesignUnit import Context, Entity, Architecture, Configuration, Package, PackageBody
from ..LanguageModel.Reference import LibraryClause, UseClause, ContextReference
from ..LanguageModel.InterfaceItem import GenericConstantInterfaceItem, GenericTypeInterfaceItem, \
	GenericPackageInterfaceItem, GenericFunctionInterfaceItem, GenericProcedureInterfaceItem, PortSignalInterfaceItem
from ..LanguageModel.Expression import AndExpression

from .VHDLParser import *
from .VHDLParserVisitor import VHDLParserVisitor


class VHDLVisitor(VHDLParserVisitor):
	@staticmethod
	def checkRepeatedName(name1: Token, name2: Token, languageEntity: str):
		nameText: str = name1.text
		if name2 is not None:
			name2Text: str = name2.text
			if nameText.lower() != name2Text.lower():
				raise Exception(f"Repeated {languageEntity} name '{name2Text}' must match {languageEntity} name '{nameText}'.")

		return nameText

	def visitRule_DesignFile(self, ctx: VHDLParser.Rule_DesignFileContext):
		return [self.visit(designUnit) for designUnit in ctx.designUnits]

	def visitRule_LibraryClause(self, ctx: VHDLParser.Rule_LibraryClauseContext):
		names = [name.text for name in ctx.names]

		return LibraryClause(names)

	def visitRule_UseClause(self, ctx:VHDLParser.Rule_UseClauseContext):
		names = [self.visit(name) for name in ctx.names]

		return UseClause(names)

	def visitRule_SelectedName2(self, ctx:VHDLParser.Rule_SelectedName2Context):
		# TODO: needs to return a proper 'Name'
		return ctx.getText()

	def visitRule_DesignUnit(self, ctx: VHDLParser.Rule_DesignUnitContext):
		# translate the design unit itself
		libraryUnit: DesignUnit = self.visit(ctx.libraryUnit)

		# check if there are context items and add them to the design unit
		for contextItem in ctx.contextItems:
			ctxItem = self.visit(contextItem)
			libraryUnit.ContextItems.append(ctxItem)

			if isinstance(ctxItem, LibraryClause):
				libraryUnit.LibraryReferences.append(ctxItem)
			elif isinstance(ctxItem, UseClause):
				libraryUnit.LibraryReferences.append(ctxItem)
			#elif isinstance(contextItem, ContextClause):
			#	libraryUnit.LibraryReferences.append(contextItem)

		return libraryUnit

	# def visitRule_ContextDeclaration(self, ctx: VHDLParser.Rule_ContextDeclarationContext):

	def visitRule_EntityDeclaration(self, ctx: VHDLParser.Rule_EntityDeclarationContext):
		entityName = self.checkRepeatedName(ctx.name, ctx.name2, "entity")

		generics = self.visit(ctx.genericClause) if ctx.genericClause is not None else []
		ports = self.visit(ctx.portClause) if ctx.portClause is not None else []

		entity = Entity(identifier=entityName, genericItems=generics, portItems=ports)
		entity.docstring = self.getDocString(ctx)
		return entity

	def getDocString(self, ctx):
		start = ctx.start
		ts = ctx.parser.getTokenStream()
		i = 1
		r = []
		while i <= start.tokenIndex:
			t: Token = ts.get(start.tokenIndex-i)
			if t.channel == VHDLLexer.COMMENT_CHANNEL:
				r.append(t.text)
			elif t.channel != VHDLLexer.WHITESPACE_CHANNEL:
				break
			i += 1
		return tuple(reversed(r))


	def visitRule_Architecture(self, ctx:VHDLParser.Rule_ArchitectureContext):
		architectureName = self.checkRepeatedName(ctx.name, ctx.name2, "architecture")
		entityName: str = ctx.entityName.text  # TODO: needs a Name

		context = []
		declaredItems = []
		statements = []

		return Architecture(architectureName, entityName, context, declaredItems, statements)

	def visitRule_ConfigurationDeclaration(self, ctx:VHDLParser.Rule_ConfigurationDeclarationContext):
		configurationName = self.checkRepeatedName(ctx.name, ctx.name2, "configuration")
		entityName: str = ctx.entityName.getText

		context = []

		return Configuration(configurationName, context)

	def visitRule_PackageDeclaration(self, ctx:VHDLParser.Rule_PackageDeclarationContext):
		packageName = self.checkRepeatedName(ctx.name, ctx.name2, "package")

		return Package(packageName)

	def visitRule_PackageBody(self, ctx:VHDLParser.Rule_PackageBodyContext):
		packageName = self.checkRepeatedName(ctx.name, ctx.name2, "package body")
		packageSymbol = PackageSymbol(packageName)

		return PackageBody(packageSymbol)

	def visitRule_GenericClause(self, ctx: VHDLParser.Rule_GenericClauseContext):
		generics = []
		for element in ctx.elements:
			const = self.visit(element)
			generics.append(const)

		return generics

	def visitRule_InterfaceConstantDeclaration(self, ctx: VHDLParser.Rule_InterfaceConstantDeclarationContext):
		constantNames = self.visit(ctx.constantNames)
		if ctx.modeName is not None:
			mode = Mode(ctx.modeName.text)
		else:
			mode = Mode.Default

		subtypeIndication = self.visit(ctx.subtypeIndication)
		defaultExpression = self.visit(ctx.defaultValue) if ctx.defaultValue is not None else None

		return GenericConstantInterfaceItem(constantNames, mode, subtypeIndication, defaultExpression)

	def visitRule_PortClause(self, ctx: VHDLParser.Rule_PortClauseContext):
		return [self.visit(port) for port in ctx.ports]

	def visitRule_InterfacePortDeclaration(self, ctx:VHDLParser.Rule_InterfaceSignalDeclarationContext):
		signalNames = self.visit(ctx.names)
		if ctx.modeName is not None:
			modeToken:Token = ctx.modeName.name
			modeType = modeToken.type

			if modeType == VHDLParser.KW_IN:
				mode = Mode.In
			elif modeType == VHDLParser.KW_OUT:
				mode = Mode.Out
			elif modeType == VHDLParser.KW_INOUT:
				mode = Mode.InOut
			elif modeType == VHDLParser.KW_BUFFER:
				mode = Mode.Buffer
			elif modeType == VHDLParser.KW_LINKAGE:
				mode = Mode.Linkage
			else:
				raise Exception()
		else:
			mode = Mode.Default

		subtype = None
		defaultExpression = None

		return PortSignalInterfaceItem(signalNames, mode, subtype, defaultExpression)

	def visitRule_IdentifierList(self, ctx: VHDLParser.Rule_IdentifierListContext):
		return [identifier.text for identifier in ctx.identifiers]
