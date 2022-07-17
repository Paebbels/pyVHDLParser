from pyVHDLModel import Mode, DesignUnit, MixinDesignUnitWithContext
from pyVHDLModel.SyntaxModel import GenericConstantInterfaceItem, Entity, LibraryClause, UseClause
from .VHDLParser import *
from .VHDLParserVisitor import VHDLParserVisitor


class VHDLVisitor(VHDLParserVisitor):
	def visitRule_DesignFile(self, ctx:VHDLParser.Rule_DesignFileContext):
		designUnits = []
		for designUnit in ctx.designUnits:
			designUnits.append(self.visit(designUnit))

		return designUnits

	def visitRule_ContextItem(self, ctx:VHDLParser.Rule_ContextItemContext):
		if ctx.libraryClause is not None:
			return self.visit(ctx.libraryClause)
		elif ctx.useClause is not None:
			return self.visit(ctx.useClause)

		raise Exception()

	def visitRule_LibraryClause(self, ctx:VHDLParser.Rule_LibraryClauseContext):
		names = []
		for name in ctx.names:
			names.append(name.text)

		return LibraryClause(names)

	def visitRule_DesignUnit(self, ctx:VHDLParser.Rule_DesignUnitContext):
		libraryUnit: MixinDesignUnitWithContext = self.visit(ctx.libraryUnit)

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

	def visitRule_LibraryUnit(self, ctx:VHDLParser.Rule_LibraryUnitContext):
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

	def visitRule_EntityDeclaration(self, ctx:VHDLParser.Rule_EntityDeclarationContext):
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

	def visitRule_GenericClause(self, ctx:VHDLParser.Rule_GenericClauseContext):
		# TODO: can it be optimized?
		return self.visit(ctx.generics)

	def visitRule_GenericList(self, ctx:VHDLParser.Rule_GenericListContext):
		generics = []
		for constant in ctx.constants:
			const = self.visit(constant)
			generics.append(const)

		return generics

	def visitRule_InterfaceConstantDeclaration(self, ctx:VHDLParser.Rule_InterfaceConstantDeclarationContext):
		constantNames = self.visit(ctx.constantNames)
		if ctx.modeName is not None:
			mode = Mode(ctx.modeName.text)
		else:
			mode = Mode.In

		subtypeIndication = self.visit(ctx.subtypeIndication)
		defaultExpression = self.visit(ctx.defaultValue) if ctx.defaultValue is not None else None

		return GenericConstantInterfaceItem(constantNames, mode, subtypeIndication, defaultExpression)

	def visitRule_IdentifierList(self, ctx:VHDLParser.Rule_IdentifierListContext):
		return [identifier.text for identifier in ctx.identifier]
