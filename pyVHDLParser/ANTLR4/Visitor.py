from pyVHDLModel import Mode
from pyVHDLModel.SyntaxModel import GenericConstantInterfaceItem, Entity
from .VHDLParser import *
from .VHDLParserVisitor import VHDLParserVisitor


class VHDLVisitor(VHDLParserVisitor):
	def visitDesign_file(self, ctx:VHDLParser.Design_fileContext):
		designUnits = []
		for designUnit in ctx.designUnits:
			designUnits.append(self.visit(designUnit))

		return designUnits

	def visitLibrary_unit(self, ctx:VHDLParser.Library_unitContext):
		# TODO: can it be optimized?
		if ctx.primaryUnit is not None:
			return self.visit(ctx.primaryUnit)
		elif ctx.secondary_unit is not None:
			return self.visit(ctx.secondaryUnit)

		raise Exception()

	def visitPrimary_unit(self, ctx:VHDLParser.Primary_unitContext):
		# TODO: can it be optimized?
		if ctx.entity is not None:
			return self.visit(ctx.entity)

		raise Exception()

	def visitEntity_declaration(self, ctx:VHDLParser.Entity_declarationContext):
		entityName: str = ctx.entityName.text
		entityName2 = ctx.entityName2
		if entityName2 is not None:
			entityName2: str = entityName2.text
			if entityName.lower() != entityName2.lower():
				raise Exception(f"Repeated entity name '{entityName2}' must match entity name '{entityName}'.")

		generics, ports = self.visit(ctx.header)

		entity = Entity(identifier=entityName, genericItems=generics, portItems=ports)
		return entity

	def visitEntity_header(self, ctx:VHDLParser.Entity_headerContext):
		# TODO: can it be optimized, so no tuple is needed?
		generics = self.visit(ctx.genericClause) if ctx.genericClause is not None else []
		ports = self.visit(ctx.portClause) if ctx.portClause is not None else []

		return (generics, ports)

	def visitGeneric_clause(self, ctx:VHDLParser.Generic_clauseContext):
		# TODO: can it be optimized?
		return self.visit(ctx.generics)

	def visitGeneric_list(self, ctx:VHDLParser.Generic_listContext):
		generics = []
		for constant in ctx.constants:
			const = self.visit(constant)
			generics.append(const)

		return generics

	def visitInterface_constant_declaration(self, ctx:VHDLParser.Interface_constant_declarationContext):
		constantNames = self.visit(ctx.constantNames)
		if ctx.modeName is not None:
			mode = Mode(ctx.modeName.text)
		else:
			mode = Mode.In

		subtypeIndication = self.visit(ctx.subtypeIndication)
		defaultExpression = self.visit(ctx.defaultValue) if ctx.defaultValue is not None else None

		return GenericConstantInterfaceItem(constantNames, mode, subtypeIndication, defaultExpression)

	def visitIdentifier_list(self, ctx:VHDLParser.Identifier_listContext):
		return [identifier.text for identifier in ctx.identifier]
