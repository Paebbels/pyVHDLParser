from antlr4 import ParseTreeVisitor

from .VHDLParser import VHDLParser


class VHDLParserVisitor(ParseTreeVisitor):
	# Visit a parse tree produced by VHDLParser#rule_AbsolutePathname.
	def visitRule_AbsolutePathname(self, ctx: VHDLParser.Rule_AbsolutePathnameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AccessTypeDefinition.
	def visitRule_AccessTypeDefinition(self, ctx: VHDLParser.Rule_AccessTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ActualDesignator.
	def visitRule_ActualDesignator(self, ctx: VHDLParser.Rule_ActualDesignatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ActualParameterPart.
	def visitRule_ActualParameterPart(self, ctx: VHDLParser.Rule_ActualParameterPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ActualPart.
	def visitRule_ActualPart(self, ctx: VHDLParser.Rule_ActualPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Aggregate.
	def visitRule_Aggregate(self, ctx: VHDLParser.Rule_AggregateContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AliasDeclaration.
	def visitRule_AliasDeclaration(self, ctx: VHDLParser.Rule_AliasDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AliasDesignator.
	def visitRule_AliasDesignator(self, ctx: VHDLParser.Rule_AliasDesignatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AliasIndication.
	def visitRule_AliasIndication(self, ctx: VHDLParser.Rule_AliasIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Allocator.
	def visitRule_Allocator(self, ctx: VHDLParser.Rule_AllocatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Architecture.
	def visitRule_Architecture(self, ctx: VHDLParser.Rule_ArchitectureContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArchitectureDeclarativePart.
	def visitRule_ArchitectureDeclarativePart(self, ctx: VHDLParser.Rule_ArchitectureDeclarativePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArchitectureStatement.
	def visitRule_ArchitectureStatement(self, ctx: VHDLParser.Rule_ArchitectureStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArchitectureStatementPart.
	def visitRule_ArchitectureStatementPart(self, ctx: VHDLParser.Rule_ArchitectureStatementPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayTypeDefinition.
	def visitRule_ArrayTypeDefinition(self, ctx: VHDLParser.Rule_ArrayTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Assertion.
	def visitRule_Assertion(self, ctx: VHDLParser.Rule_AssertionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AssertionStatement.
	def visitRule_AssertionStatement(self, ctx: VHDLParser.Rule_AssertionStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AssociationElement.
	def visitRule_AssociationElement(self, ctx: VHDLParser.Rule_AssociationElementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AssociationList.
	def visitRule_AssociationList(self, ctx: VHDLParser.Rule_AssociationListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AttributeDeclaration.
	def visitRule_AttributeDeclaration(self, ctx: VHDLParser.Rule_AttributeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AttributeDesignator.
	def visitRule_AttributeDesignator(self, ctx: VHDLParser.Rule_AttributeDesignatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AttributeSpecification.
	def visitRule_AttributeSpecification(self, ctx: VHDLParser.Rule_AttributeSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_BaseUnitDeclaration.
	def visitRule_BaseUnitDeclaration(self, ctx: VHDLParser.Rule_BaseUnitDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_BindingIndication.
	def visitRule_BindingIndication(self, ctx: VHDLParser.Rule_BindingIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_BlockConfiguration.
	def visitRule_BlockConfiguration(self, ctx: VHDLParser.Rule_BlockConfigurationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_BlockDeclarativeItem.
	def visitRule_BlockDeclarativeItem(self, ctx: VHDLParser.Rule_BlockDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_BlockSpecification.
	def visitRule_BlockSpecification(self, ctx: VHDLParser.Rule_BlockSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_BlockStatement.
	def visitRule_BlockStatement(self, ctx: VHDLParser.Rule_BlockStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_CaseStatement.
	def visitRule_CaseStatement(self, ctx: VHDLParser.Rule_CaseStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_CaseStatementAlternative.
	def visitRule_CaseStatementAlternative(self, ctx: VHDLParser.Rule_CaseStatementAlternativeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Choice.
	def visitRule_Choice(self, ctx: VHDLParser.Rule_ChoiceContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Choices.
	def visitRule_Choices(self, ctx: VHDLParser.Rule_ChoicesContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ComponentConfiguration.
	def visitRule_ComponentConfiguration(self, ctx: VHDLParser.Rule_ComponentConfigurationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ComponentDeclaration.
	def visitRule_ComponentDeclaration(self, ctx: VHDLParser.Rule_ComponentDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ComponentInstantiationStatement.
	def visitRule_ComponentInstantiationStatement(self, ctx: VHDLParser.Rule_ComponentInstantiationStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ComponentSpecification.
	def visitRule_ComponentSpecification(self, ctx: VHDLParser.Rule_ComponentSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_CompositeTypeDefinition.
	def visitRule_CompositeTypeDefinition(self, ctx: VHDLParser.Rule_CompositeTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentAssertionStatement.
	def visitRule_ConcurrentAssertionStatement(self, ctx: VHDLParser.Rule_ConcurrentAssertionStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentProcedureCallStatement.
	def visitRule_ConcurrentProcedureCallStatement(self, ctx: VHDLParser.Rule_ConcurrentProcedureCallStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentSignalAssignmentStatement.
	def visitRule_ConcurrentSignalAssignmentStatement(self,
																										ctx: VHDLParser.Rule_ConcurrentSignalAssignmentStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Condition.
	def visitRule_Condition(self, ctx: VHDLParser.Rule_ConditionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConditionClause.
	def visitRule_ConditionClause(self, ctx: VHDLParser.Rule_ConditionClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConditionalSignalAssignment.
	def visitRule_ConditionalSignalAssignment(self, ctx: VHDLParser.Rule_ConditionalSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConditionalWaveforms.
	def visitRule_ConditionalWaveforms(self, ctx: VHDLParser.Rule_ConditionalWaveformsContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConfigurationDeclaration.
	def visitRule_ConfigurationDeclaration(self, ctx: VHDLParser.Rule_ConfigurationDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConfigurationDeclarativeItem.
	def visitRule_ConfigurationDeclarativeItem(self, ctx: VHDLParser.Rule_ConfigurationDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConfigurationItem.
	def visitRule_ConfigurationItem(self, ctx: VHDLParser.Rule_ConfigurationItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConfigurationSpecification.
	def visitRule_ConfigurationSpecification(self, ctx: VHDLParser.Rule_ConfigurationSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConstantDeclaration.
	def visitRule_ConstantDeclaration(self, ctx: VHDLParser.Rule_ConstantDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConstrainedArrayDefinition.
	def visitRule_ConstrainedArrayDefinition(self, ctx: VHDLParser.Rule_ConstrainedArrayDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Constraint.
	def visitRule_Constraint(self, ctx: VHDLParser.Rule_ConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ContextItem.
	def visitRule_ContextItem(self, ctx: VHDLParser.Rule_ContextItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_DelayMechanism.
	def visitRule_DelayMechanism(self, ctx: VHDLParser.Rule_DelayMechanismContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_DesignFile.
	def visitRule_DesignFile(self, ctx: VHDLParser.Rule_DesignFileContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_DesignUnit.
	def visitRule_DesignUnit(self, ctx: VHDLParser.Rule_DesignUnitContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Designator.
	def visitRule_Designator(self, ctx: VHDLParser.Rule_DesignatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Direction.
	def visitRule_Direction(self, ctx: VHDLParser.Rule_DirectionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_DisconnectionSpecification.
	def visitRule_DisconnectionSpecification(self, ctx: VHDLParser.Rule_DisconnectionSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_DiscreteRange.
	def visitRule_DiscreteRange(self, ctx: VHDLParser.Rule_DiscreteRangeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementAssociation.
	def visitRule_ElementAssociation(self, ctx: VHDLParser.Rule_ElementAssociationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementDeclaration.
	def visitRule_ElementDeclaration(self, ctx: VHDLParser.Rule_ElementDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementSubtypeDefinition.
	def visitRule_ElementSubtypeDefinition(self, ctx: VHDLParser.Rule_ElementSubtypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityAspect.
	def visitRule_EntityAspect(self, ctx: VHDLParser.Rule_EntityAspectContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityClass.
	def visitRule_EntityClass(self, ctx: VHDLParser.Rule_EntityClassContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityClassEntry.
	def visitRule_EntityClassEntry(self, ctx: VHDLParser.Rule_EntityClassEntryContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityClassEntryList.
	def visitRule_EntityClassEntryList(self, ctx: VHDLParser.Rule_EntityClassEntryListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityDeclaration.
	def visitRule_EntityDeclaration(self, ctx: VHDLParser.Rule_EntityDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityDeclarativeItem.
	def visitRule_EntityDeclarativeItem(self, ctx: VHDLParser.Rule_EntityDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityDeclarativePart.
	def visitRule_EntityDeclarativePart(self, ctx: VHDLParser.Rule_EntityDeclarativePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityDesignator.
	def visitRule_EntityDesignator(self, ctx: VHDLParser.Rule_EntityDesignatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityNameList.
	def visitRule_EntityNameList(self, ctx: VHDLParser.Rule_EntityNameListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntitySpecification.
	def visitRule_EntitySpecification(self, ctx: VHDLParser.Rule_EntitySpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityStatement.
	def visitRule_EntityStatement(self, ctx: VHDLParser.Rule_EntityStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityStatementPart.
	def visitRule_EntityStatementPart(self, ctx: VHDLParser.Rule_EntityStatementPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityTag.
	def visitRule_EntityTag(self, ctx: VHDLParser.Rule_EntityTagContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EnumerationLiteral.
	def visitRule_EnumerationLiteral(self, ctx: VHDLParser.Rule_EnumerationLiteralContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EnumerationTypeDefinition.
	def visitRule_EnumerationTypeDefinition(self, ctx: VHDLParser.Rule_EnumerationTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExitStatement.
	def visitRule_ExitStatement(self, ctx: VHDLParser.Rule_ExitStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Expression.
	def visitRule_Expression(self, ctx: VHDLParser.Rule_ExpressionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Factor.
	def visitRule_Factor(self, ctx: VHDLParser.Rule_FactorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileDeclaration.
	def visitRule_FileDeclaration(self, ctx: VHDLParser.Rule_FileDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileLogicalName.
	def visitRule_FileLogicalName(self, ctx: VHDLParser.Rule_FileLogicalNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileOpenInformation.
	def visitRule_FileOpenInformation(self, ctx: VHDLParser.Rule_FileOpenInformationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileTypeDefinition.
	def visitRule_FileTypeDefinition(self, ctx: VHDLParser.Rule_FileTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FormalParameterList.
	def visitRule_FormalParameterList(self, ctx: VHDLParser.Rule_FormalParameterListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FormalPart.
	def visitRule_FormalPart(self, ctx: VHDLParser.Rule_FormalPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenerateStatement.
	def visitRule_GenerateStatement(self, ctx: VHDLParser.Rule_GenerateStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenerationScheme.
	def visitRule_GenerationScheme(self, ctx: VHDLParser.Rule_GenerationSchemeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenericClause.
	def visitRule_GenericClause(self, ctx: VHDLParser.Rule_GenericClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenericList.
	def visitRule_GenericList(self, ctx: VHDLParser.Rule_GenericListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenericMapAspect.
	def visitRule_GenericMapAspect(self, ctx: VHDLParser.Rule_GenericMapAspectContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GuardedSignalSpecification.
	def visitRule_GuardedSignalSpecification(self, ctx: VHDLParser.Rule_GuardedSignalSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IdentifierList.
	def visitRule_IdentifierList(self, ctx: VHDLParser.Rule_IdentifierListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IfStatement.
	def visitRule_IfStatement(self, ctx: VHDLParser.Rule_IfStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IndexConstraint.
	def visitRule_IndexConstraint(self, ctx: VHDLParser.Rule_IndexConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IndexSpecification.
	def visitRule_IndexSpecification(self, ctx: VHDLParser.Rule_IndexSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IndexSubtypeDefinition.
	def visitRule_IndexSubtypeDefinition(self, ctx: VHDLParser.Rule_IndexSubtypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InstantiatedUnit.
	def visitRule_InstantiatedUnit(self, ctx: VHDLParser.Rule_InstantiatedUnitContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InstantiationList.
	def visitRule_InstantiationList(self, ctx: VHDLParser.Rule_InstantiationListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceConstantDeclaration.
	def visitRule_InterfaceConstantDeclaration(self, ctx: VHDLParser.Rule_InterfaceConstantDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceDeclaration.
	def visitRule_InterfaceDeclaration(self, ctx: VHDLParser.Rule_InterfaceDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceElement.
	def visitRule_InterfaceElement(self, ctx: VHDLParser.Rule_InterfaceElementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceFileDeclaration.
	def visitRule_InterfaceFileDeclaration(self, ctx: VHDLParser.Rule_InterfaceFileDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceSignalList.
	def visitRule_InterfaceSignalList(self, ctx: VHDLParser.Rule_InterfaceSignalListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfacePortList.
	def visitRule_InterfacePortList(self, ctx: VHDLParser.Rule_InterfacePortListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceList.
	def visitRule_InterfaceList(self, ctx: VHDLParser.Rule_InterfaceListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfacePortDeclaration.
	def visitRule_InterfacePortDeclaration(self, ctx: VHDLParser.Rule_InterfacePortDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceSignalDeclaration.
	def visitRule_InterfaceSignalDeclaration(self, ctx: VHDLParser.Rule_InterfaceSignalDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceVariableDeclaration.
	def visitRule_InterfaceVariableDeclaration(self, ctx: VHDLParser.Rule_InterfaceVariableDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IterationScheme.
	def visitRule_IterationScheme(self, ctx: VHDLParser.Rule_IterationSchemeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Label.
	def visitRule_Label(self, ctx: VHDLParser.Rule_LabelContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_LabelWithColon.
	def visitRule_LabelWithColon(self, ctx: VHDLParser.Rule_LabelWithColonContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_LibraryClause.
	def visitRule_LibraryClause(self, ctx: VHDLParser.Rule_LibraryClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_LibraryUnit.
	def visitRule_LibraryUnit(self, ctx: VHDLParser.Rule_LibraryUnitContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Literal.
	def visitRule_Literal(self, ctx: VHDLParser.Rule_LiteralContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_LoopStatement.
	def visitRule_LoopStatement(self, ctx: VHDLParser.Rule_LoopStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SignalMode.
	def visitRule_SignalMode(self, ctx: VHDLParser.Rule_SignalModeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Name.
	def visitRule_Name(self, ctx: VHDLParser.Rule_NameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_NamePart.
	def visitRule_NamePart(self, ctx: VHDLParser.Rule_NamePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedName.
	def visitRule_SelectedName(self, ctx: VHDLParser.Rule_SelectedNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedNamePart.
	def visitRule_SelectedNamePart(self, ctx: VHDLParser.Rule_SelectedNamePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FunctionCallOrIndexedNamePart.
	def visitRule_FunctionCallOrIndexedNamePart(self, ctx: VHDLParser.Rule_FunctionCallOrIndexedNamePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SliceNamePart.
	def visitRule_SliceNamePart(self, ctx: VHDLParser.Rule_SliceNamePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AttributeNamePart.
	def visitRule_AttributeNamePart(self, ctx: VHDLParser.Rule_AttributeNamePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_NextStatement.
	def visitRule_NextStatement(self, ctx: VHDLParser.Rule_NextStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_NumericLiteral.
	def visitRule_NumericLiteral(self, ctx: VHDLParser.Rule_NumericLiteralContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ObjectDeclaration.
	def visitRule_ObjectDeclaration(self, ctx: VHDLParser.Rule_ObjectDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Opts.
	def visitRule_Opts(self, ctx: VHDLParser.Rule_OptsContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PackageBody.
	def visitRule_PackageBody(self, ctx: VHDLParser.Rule_PackageBodyContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PackageBodyDeclarativeItem.
	def visitRule_PackageBodyDeclarativeItem(self, ctx: VHDLParser.Rule_PackageBodyDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PackageDeclaration.
	def visitRule_PackageDeclaration(self, ctx: VHDLParser.Rule_PackageDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PackageDeclarativeItem.
	def visitRule_PackageDeclarativeItem(self, ctx: VHDLParser.Rule_PackageDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ParameterSpecification.
	def visitRule_ParameterSpecification(self, ctx: VHDLParser.Rule_ParameterSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PartialPathName.
	def visitRule_PartialPathName(self, ctx: VHDLParser.Rule_PartialPathNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PathNameElement.
	def visitRule_PathNameElement(self, ctx: VHDLParser.Rule_PathNameElementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PhysicalLiteral.
	def visitRule_PhysicalLiteral(self, ctx: VHDLParser.Rule_PhysicalLiteralContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PhysicalTypeDefinition.
	def visitRule_PhysicalTypeDefinition(self, ctx: VHDLParser.Rule_PhysicalTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PortClause.
	def visitRule_PortClause(self, ctx: VHDLParser.Rule_PortClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PortMapAspect.
	def visitRule_PortMapAspect(self, ctx: VHDLParser.Rule_PortMapAspectContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Primary.
	def visitRule_Primary(self, ctx: VHDLParser.Rule_PrimaryContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcedureCall.
	def visitRule_ProcedureCall(self, ctx: VHDLParser.Rule_ProcedureCallContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcedureCallStatement.
	def visitRule_ProcedureCallStatement(self, ctx: VHDLParser.Rule_ProcedureCallStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessDeclarativeItem.
	def visitRule_ProcessDeclarativeItem(self, ctx: VHDLParser.Rule_ProcessDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessDeclarativePart.
	def visitRule_ProcessDeclarativePart(self, ctx: VHDLParser.Rule_ProcessDeclarativePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessStatement.
	def visitRule_ProcessStatement(self, ctx: VHDLParser.Rule_ProcessStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PostponedProcessStatement.
	def visitRule_PostponedProcessStatement(self, ctx: VHDLParser.Rule_PostponedProcessStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessStatementPart.
	def visitRule_ProcessStatementPart(self, ctx: VHDLParser.Rule_ProcessStatementPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_QualifiedExpression.
	def visitRule_QualifiedExpression(self, ctx: VHDLParser.Rule_QualifiedExpressionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RangeDeclaration.
	def visitRule_RangeDeclaration(self, ctx: VHDLParser.Rule_RangeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExplicitRange.
	def visitRule_ExplicitRange(self, ctx: VHDLParser.Rule_ExplicitRangeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RangeConstraint.
	def visitRule_RangeConstraint(self, ctx: VHDLParser.Rule_RangeConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordTypeDefinition.
	def visitRule_RecordTypeDefinition(self, ctx: VHDLParser.Rule_RecordTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Relation.
	def visitRule_Relation(self, ctx: VHDLParser.Rule_RelationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ReportStatement.
	def visitRule_ReportStatement(self, ctx: VHDLParser.Rule_ReportStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ReturnStatement.
	def visitRule_ReturnStatement(self, ctx: VHDLParser.Rule_ReturnStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ScalarTypeDefinition.
	def visitRule_ScalarTypeDefinition(self, ctx: VHDLParser.Rule_ScalarTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SecondaryUnitDeclaration.
	def visitRule_SecondaryUnitDeclaration(self, ctx: VHDLParser.Rule_SecondaryUnitDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedSignalAssignment.
	def visitRule_SelectedSignalAssignment(self, ctx: VHDLParser.Rule_SelectedSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedWaveforms.
	def visitRule_SelectedWaveforms(self, ctx: VHDLParser.Rule_SelectedWaveformsContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SensitivityClause.
	def visitRule_SensitivityClause(self, ctx: VHDLParser.Rule_SensitivityClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SensitivityList.
	def visitRule_SensitivityList(self, ctx: VHDLParser.Rule_SensitivityListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SequenceOfStatements.
	def visitRule_SequenceOfStatements(self, ctx: VHDLParser.Rule_SequenceOfStatementsContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SequentialStatement.
	def visitRule_SequentialStatement(self, ctx: VHDLParser.Rule_SequentialStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ShiftExpression.
	def visitRule_ShiftExpression(self, ctx: VHDLParser.Rule_ShiftExpressionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SignalAssignmentStatement.
	def visitRule_SignalAssignmentStatement(self, ctx: VHDLParser.Rule_SignalAssignmentStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SignalDeclaration.
	def visitRule_SignalDeclaration(self, ctx: VHDLParser.Rule_SignalDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SignalList.
	def visitRule_SignalList(self, ctx: VHDLParser.Rule_SignalListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Signature.
	def visitRule_Signature(self, ctx: VHDLParser.Rule_SignatureContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleExpression.
	def visitRule_SimpleExpression(self, ctx: VHDLParser.Rule_SimpleExpressionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleName.
	def visitRule_SimpleName(self, ctx: VHDLParser.Rule_SimpleNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramBody.
	def visitRule_SubprogramBody(self, ctx: VHDLParser.Rule_SubprogramBodyContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramDeclaration.
	def visitRule_SubprogramDeclaration(self, ctx: VHDLParser.Rule_SubprogramDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramDeclarativeItem.
	def visitRule_SubprogramDeclarativeItem(self, ctx: VHDLParser.Rule_SubprogramDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramDeclarativePart.
	def visitRule_SubprogramDeclarativePart(self, ctx: VHDLParser.Rule_SubprogramDeclarativePartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramKind.
	def visitRule_SubprogramKind(self, ctx: VHDLParser.Rule_SubprogramKindContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramSpecification.
	def visitRule_SubprogramSpecification(self, ctx: VHDLParser.Rule_SubprogramSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcedureSpecification.
	def visitRule_ProcedureSpecification(self, ctx: VHDLParser.Rule_ProcedureSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FunctionSpecification.
	def visitRule_FunctionSpecification(self, ctx: VHDLParser.Rule_FunctionSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramStatementPart.
	def visitRule_SubprogramStatementPart(self, ctx: VHDLParser.Rule_SubprogramStatementPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubtypeDeclaration.
	def visitRule_SubtypeDeclaration(self, ctx: VHDLParser.Rule_SubtypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubtypeIndication.
	def visitRule_SubtypeIndication(self, ctx: VHDLParser.Rule_SubtypeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Suffix.
	def visitRule_Suffix(self, ctx: VHDLParser.Rule_SuffixContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Target.
	def visitRule_Target(self, ctx: VHDLParser.Rule_TargetContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Term.
	def visitRule_Term(self, ctx: VHDLParser.Rule_TermContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TimeoutClause.
	def visitRule_TimeoutClause(self, ctx: VHDLParser.Rule_TimeoutClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TypeDeclaration.
	def visitRule_TypeDeclaration(self, ctx: VHDLParser.Rule_TypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TypeDefinition.
	def visitRule_TypeDefinition(self, ctx: VHDLParser.Rule_TypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_UnconstrainedArrayDefinition.
	def visitRule_UnconstrainedArrayDefinition(self, ctx: VHDLParser.Rule_UnconstrainedArrayDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_UseClause.
	def visitRule_UseClause(self, ctx: VHDLParser.Rule_UseClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_VariableAssignmentStatement.
	def visitRule_VariableAssignmentStatement(self, ctx: VHDLParser.Rule_VariableAssignmentStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_VariableDeclaration.
	def visitRule_VariableDeclaration(self, ctx: VHDLParser.Rule_VariableDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_WaitStatement.
	def visitRule_WaitStatement(self, ctx: VHDLParser.Rule_WaitStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Waveform.
	def visitRule_Waveform(self, ctx: VHDLParser.Rule_WaveformContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_WaveformElement.
	def visitRule_WaveformElement(self, ctx: VHDLParser.Rule_WaveformElementContext):
		return self.visitChildren(ctx)


del VHDLParser
