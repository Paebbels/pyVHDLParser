from pyVHDLModel import Mode
from pyVHDLModel.SyntaxModel import GenericConstantInterfaceItem, Entity
from .VHDLParser import *
from .VHDLParserVisitor import VHDLParserVisitor


class VHDLVisitor(VHDLParserVisitor):
	def visitRule_DesignFile(self, ctx:VHDLParser.Rule_DesignFileContext):
		designUnits = []
		for designUnit in ctx.designUnits:
			designUnits.append(self.visit(designUnit))

		return designUnits

	def visitRule_LibraryUnit(self, ctx:VHDLParser.Rule_LibraryUnitContext):
		# TODO: can it be optimized?
		if ctx.primaryUnit is not None:
			return self.visit(ctx.primaryUnit)
		elif ctx.secondaryUnit is not None:
			return self.visit(ctx.secondaryUnit)

		raise Exception()

	def visitRule_PrimaryUnit(self, ctx:VHDLParser.Rule_PrimaryUnitContext):
		# TODO: can it be optimized?
		if ctx.entity is not None:
			return self.visit(ctx.entity)

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
