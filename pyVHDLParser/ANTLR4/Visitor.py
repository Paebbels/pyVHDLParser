from pyVHDLModel import Mode, MixinDesignUnitWithContext

from ..LanguageModel.DesignUnit import Context, Entity, Architecture, Configuration, Package, PackageBody
from ..LanguageModel.Reference import LibraryClause, UseClause, ContextReference
from ..LanguageModel.InterfaceItem import GenericConstantInterfaceItem, GenericTypeInterfaceItem, \
	GenericPackageInterfaceItem, GenericFunctionInterfaceItem, GenericProcedureInterfaceItem, PortSignalInterfaceItem
from ..LanguageModel.Expression import AndExpression

from .VHDLParser import *
from .VHDLParserVisitor import VHDLParserVisitor


class VHDLVisitor(VHDLParserVisitor):
	def visitRule_DesignFile(self, ctx: VHDLParser.Rule_DesignFileContext):
		designUnits = []
		for designUnit in ctx.designUnits:
			designUnits.append(self.visit(designUnit))

		return designUnits

	def visitRule_ContextItem(self, ctx: VHDLParser.Rule_ContextItemContext):
		if ctx.libraryClause is not None:
			return self.visit(ctx.libraryClause)
		elif ctx.useClause is not None:
			return self.visit(ctx.useClause)
		# TODO: Context

		raise Exception()

	def visitRule_LibraryClause(self, ctx: VHDLParser.Rule_LibraryClauseContext):
		names = [name.text for name in ctx.names]

		return LibraryClause(names)

	def visitRule_UseClause(self, ctx:VHDLParser.Rule_UseClauseContext):
		names = [self.visit(name) for name in ctx.names]

		return UseClause(names)

	def visitRule_SelectedName(self, ctx:VHDLParser.Rule_SelectedNameContext):
		# TODO: needs to return a proper 'Name'
		return ctx.getText()

	def visitRule_DesignUnit(self, ctx: VHDLParser.Rule_DesignUnitContext):
		# translate the design unit itself
		libraryUnit: MixinDesignUnitWithContext = self.visit(ctx.libraryUnit)

		# check if there are context items and add them to the design unit
		for contextClause in ctx.contextClauses:
			contextItem = self.visit(contextClause)
			libraryUnit.ContextItems.append(contextItem)

			if isinstance(contextItem, LibraryClause):
				libraryUnit.LibraryReferences.append(contextItem)
			elif isinstance(contextItem, UseClause):
				libraryUnit.LibraryReferences.append(contextItem)
			#elif isinstance(contextItem, ContextClause):
			#	libraryUnit.LibraryReferences.append(contextItem)

		return libraryUnit

	def visitRule_LibraryUnit(self, ctx: VHDLParser.Rule_LibraryUnitContext):
		# TODO: can it be optimized?
		if ctx.entity is not None:
			return self.visit(ctx.entity)
		elif ctx.package is not None:
			return self.visit(ctx.package)
		elif ctx.configuration is not None:
			return self.visit(ctx.configuration)
		elif ctx.architecture is not None:
			return self.visit(ctx.architecture)
		elif ctx.packageBody is not None:
			return self.visit(ctx.packageBody)

		raise Exception()

	# def visitRule_ContextDeclaration(self, ctx: VHDLParser.Rule_ContextDeclarationContext):

	def visitRule_EntityDeclaration(self, ctx: VHDLParser.Rule_EntityDeclarationContext):
		entityName: str = ctx.entityName.text
		entityName2 = ctx.entityName2
		if entityName2 is not None:
			entityName2: str = entityName2.text
			if entityName.lower() != entityName2.lower():
				raise Exception(f"Repeated entity name '{entityName2}' must match entity name '{entityName}'.")

		generics = self.visit(ctx.genericClause) if ctx.genericClause is not None else []
		ports = self.visit(ctx.portClause) if ctx.portClause is not None else []

		entity = Entity(identifier=entityName, genericItems=generics, portItems=ports)
		return entity

	def visitRule_Architecture(self, ctx:VHDLParser.Rule_ArchitectureContext):
		architectureName: str = ctx.architectureName.text
		architectureName2 = ctx.architectureName
		entityName: str = ctx.entityName.text

		if architectureName2 is not None:
			architectureName2: str = architectureName2.text
			if architectureName.lower() != architectureName2.lower():
				raise Exception(f"Repeated architecture name '{architectureName2}' must match architecture name '{architectureName}'.")

		context = []
		declaredItems = []
		statements = []

		return Architecture(architectureName, entityName, context, declaredItems, statements)

	def visitRule_ConfigurationDeclaration(self, ctx:VHDLParser.Rule_ConfigurationDeclarationContext):
		configurationName = ctx.configurationName.text
		configurationName2 = ctx.configurationName2
		entityName: str = ctx.entityName.getText

		if configurationName2 is not None:
			configurationName2: str = configurationName2.text
			if configurationName.lower() != configurationName2.lower():
				raise Exception(f"Repeated configuration name '{configurationName2}' must match configuration name '{configurationName}'.")

		context = []

		return Configuration(configurationName, context)

	def visitRule_PackageDeclaration(self, ctx:VHDLParser.Rule_PackageDeclarationContext):
		packageName:str = ctx.packageName.text
		packageName2 = ctx.packageName

		if packageName2 is not None:
			packageName2: str = packageName2.text
			if packageName.lower() != packageName2.lower():
				raise Exception(f"Repeated package name '{packageName2}' must match package name '{packageName}'.")

		return Package(packageName)

	def visitRule_PackageBody(self, ctx:VHDLParser.Rule_PackageBodyContext):
		packageName:str = ctx.packageName.text
		packageName2 = ctx.packageName

		if packageName2 is not None:
			packageName2: str = packageName2.text
			if packageName.lower() != packageName2.lower():
				raise Exception(f"Repeated package name '{packageName2}' must match package name '{packageName}'.")

		return PackageBody(packageName)

	def visitRule_GenericClause(self, ctx: VHDLParser.Rule_GenericClauseContext):
		# TODO: can it be optimized?
		return self.visit(ctx.genericList)

	def visitRule_GenericList(self, ctx: VHDLParser.Rule_GenericListContext):
		generics = []
		for constant in ctx.constants:
			const = self.visit(constant)
			generics.append(const)

		return generics

	def visitRule_InterfaceConstantDeclaration(self, ctx: VHDLParser.Rule_InterfaceConstantDeclarationContext):
		constantNames = self.visit(ctx.constantNames)
		if ctx.modeName is not None:
			mode = Mode(ctx.modeName.text)
		else:
			mode = Mode.In

		subtypeIndication = self.visit(ctx.subtypeIndication)
		defaultExpression = self.visit(ctx.defaultValue) if ctx.defaultValue is not None else None

		return GenericConstantInterfaceItem(constantNames, mode, subtypeIndication, defaultExpression)

	def visitRule_PortClause(self, ctx: VHDLParser.Rule_PortClauseContext):
		# TODO: can it be optimized?
		return self.visit(ctx.portList)

	def visitRule_InterfacePortList(self, ctx:VHDLParser.Rule_InterfacePortListContext):
		ports = []
		for port in ctx.interfacePortDeclarations:
			const = self.visit(port)
			ports.append(const)

		return ports

	def visitRule_InterfacePortDeclaration(self, ctx:VHDLParser.Rule_InterfacePortDeclarationContext):
		signalNames = self.visit(ctx.names)
		if ctx.signalMode is not None:
			m:str = ctx.signalMode.getText().lower()

			if m == "in":
				mode = Mode.In
			elif m == "out":
				mode = Mode.Out
			elif m == "inout":
				mode = Mode.InOut
			elif m == "buffer":
				mode = Mode.Buffer
			elif m == "linkage":
				mode = Mode.Linkage
		else:
			mode = Mode.In

		subtype = None
		defaultExpression = None

		return PortSignalInterfaceItem(signalNames, mode, subtype, defaultExpression)

	def visitRule_IdentifierList(self, ctx: VHDLParser.Rule_IdentifierListContext):
		return [identifier.text for identifier in ctx.identifier]
