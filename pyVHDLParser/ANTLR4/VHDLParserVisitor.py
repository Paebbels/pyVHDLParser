from antlr4 import ParseTreeVisitor

from .VHDLParser import VHDLParser


class VHDLParserVisitor(ParseTreeVisitor):
	# Visit a parse tree produced by VHDLParser#rule_AbsolutePathname.
	def visitRule_AbsolutePathname(self, ctx: VHDLParser.Rule_AbsolutePathnameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AccessIncompleteTypeDefinition.
	def visitRule_AccessIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_AccessIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AccessTypeDefinition.
	def visitRule_AccessTypeDefinition(self, ctx: VHDLParser.Rule_AccessTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ActualDesignator.
	def visitRule_ActualDesignator(self, ctx: VHDLParser.Rule_ActualDesignatorContext):
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

	# Visit a parse tree produced by VHDLParser#rule_ArchitectureStatement.
	def visitRule_ArchitectureStatement(self, ctx: VHDLParser.Rule_ArchitectureStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayConstraint.
	def visitRule_ArrayConstraint(self, ctx: VHDLParser.Rule_ArrayConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayElementConstraint.
	def visitRule_ArrayElementConstraint(self, ctx: VHDLParser.Rule_ArrayElementConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayElementResolution.
	def visitRule_ArrayElementResolution(self, ctx: VHDLParser.Rule_ArrayElementResolutionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayIncompleteTypeDefinition.
	def visitRule_ArrayIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_ArrayIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayIndexIncompleteType.
	def visitRule_ArrayIndexIncompleteType(self, ctx: VHDLParser.Rule_ArrayIndexIncompleteTypeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayIndexIncompleteTypeList.
	def visitRule_ArrayIndexIncompleteTypeList(self, ctx: VHDLParser.Rule_ArrayIndexIncompleteTypeListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ArrayModeViewIndication.
	def visitRule_ArrayModeViewIndication(self, ctx: VHDLParser.Rule_ArrayModeViewIndicationContext):
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

	# Visit a parse tree produced by VHDLParser#rule_CaseGenerateAlternative.
	def visitRule_CaseGenerateAlternative(self, ctx: VHDLParser.Rule_CaseGenerateAlternativeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_CaseGenerateStatement.
	def visitRule_CaseGenerateStatement(self, ctx: VHDLParser.Rule_CaseGenerateStatementContext):
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

	# Visit a parse tree produced by VHDLParser#rule_CompoundConfigurationSpecification.
	def visitRule_CompoundConfigurationSpecification(self,
																									 ctx: VHDLParser.Rule_CompoundConfigurationSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentAssertionStatement.
	def visitRule_ConcurrentAssertionStatement(self, ctx: VHDLParser.Rule_ConcurrentAssertionStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentConditionalSignalAssignment.
	def visitRule_ConcurrentConditionalSignalAssignment(self,
																											ctx: VHDLParser.Rule_ConcurrentConditionalSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentProcedureCallStatement.
	def visitRule_ConcurrentProcedureCallStatement(self, ctx: VHDLParser.Rule_ConcurrentProcedureCallStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentSelectedSignalAssignment.
	def visitRule_ConcurrentSelectedSignalAssignment(self,
																									 ctx: VHDLParser.Rule_ConcurrentSelectedSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentSignalAssignmentStatement.
	def visitRule_ConcurrentSignalAssignmentStatement(self,
																										ctx: VHDLParser.Rule_ConcurrentSignalAssignmentStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConcurrentSimpleSignalAssignment.
	def visitRule_ConcurrentSimpleSignalAssignment(self, ctx: VHDLParser.Rule_ConcurrentSimpleSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConditionClause.
	def visitRule_ConditionClause(self, ctx: VHDLParser.Rule_ConditionClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConditionalExpression.
	def visitRule_ConditionalExpression(self, ctx: VHDLParser.Rule_ConditionalExpressionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ConditionalOrUnaffectedExpression.
	def visitRule_ConditionalOrUnaffectedExpression(self, ctx: VHDLParser.Rule_ConditionalOrUnaffectedExpressionContext):
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

	# Visit a parse tree produced by VHDLParser#rule_ContextDeclaration.
	def visitRule_ContextDeclaration(self, ctx: VHDLParser.Rule_ContextDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ContextItem.
	def visitRule_ContextItem(self, ctx: VHDLParser.Rule_ContextItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ContextReference.
	def visitRule_ContextReference(self, ctx: VHDLParser.Rule_ContextReferenceContext):
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

	# Visit a parse tree produced by VHDLParser#rule_DiscreteIncompleteTypeDefinition.
	def visitRule_DiscreteIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_DiscreteIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementArrayModeViewIndication.
	def visitRule_ElementArrayModeViewIndication(self, ctx: VHDLParser.Rule_ElementArrayModeViewIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementAssociation.
	def visitRule_ElementAssociation(self, ctx: VHDLParser.Rule_ElementAssociationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementConstraint.
	def visitRule_ElementConstraint(self, ctx: VHDLParser.Rule_ElementConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementDeclaration.
	def visitRule_ElementDeclaration(self, ctx: VHDLParser.Rule_ElementDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementModeIndication.
	def visitRule_ElementModeIndication(self, ctx: VHDLParser.Rule_ElementModeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementModeViewIndication.
	def visitRule_ElementModeViewIndication(self, ctx: VHDLParser.Rule_ElementModeViewIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementRecordModeViewIndication.
	def visitRule_ElementRecordModeViewIndication(self, ctx: VHDLParser.Rule_ElementRecordModeViewIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ElementResolution.
	def visitRule_ElementResolution(self, ctx: VHDLParser.Rule_ElementResolutionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityAspect.
	def visitRule_EntityAspect(self, ctx: VHDLParser.Rule_EntityAspectContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityClass.
	def visitRule_EntityClass(self, ctx: VHDLParser.Rule_EntityClassContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityDeclaration.
	def visitRule_EntityDeclaration(self, ctx: VHDLParser.Rule_EntityDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_EntityDeclarativeItem.
	def visitRule_EntityDeclarativeItem(self, ctx: VHDLParser.Rule_EntityDeclarativeItemContext):
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

	# Visit a parse tree produced by VHDLParser#binaryOp.
	def visitBinaryOp(self, ctx: VHDLParser.BinaryOpContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#primaryOp.
	def visitPrimaryOp(self, ctx: VHDLParser.PrimaryOpContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#unaryOp.
	def visitUnaryOp(self, ctx: VHDLParser.UnaryOpContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExpressionOrUnaffected.
	def visitRule_ExpressionOrUnaffected(self, ctx: VHDLParser.Rule_ExpressionOrUnaffectedContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExternalName.
	def visitRule_ExternalName(self, ctx: VHDLParser.Rule_ExternalNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExternalConstantName.
	def visitRule_ExternalConstantName(self, ctx: VHDLParser.Rule_ExternalConstantNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExternalSignalName.
	def visitRule_ExternalSignalName(self, ctx: VHDLParser.Rule_ExternalSignalNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExternalVariableName.
	def visitRule_ExternalVariableName(self, ctx: VHDLParser.Rule_ExternalVariableNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ExternalPathname.
	def visitRule_ExternalPathname(self, ctx: VHDLParser.Rule_ExternalPathnameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileDeclaration.
	def visitRule_FileDeclaration(self, ctx: VHDLParser.Rule_FileDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileIncompleteTypeDefinition.
	def visitRule_FileIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_FileIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileOpenInformation.
	def visitRule_FileOpenInformation(self, ctx: VHDLParser.Rule_FileOpenInformationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FileTypeDefinition.
	def visitRule_FileTypeDefinition(self, ctx: VHDLParser.Rule_FileTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FloatingIncompleteTypeDefinition.
	def visitRule_FloatingIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_FloatingIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FloatingTypeDefinition.
	def visitRule_FloatingTypeDefinition(self, ctx: VHDLParser.Rule_FloatingTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ForGenerateStatement.
	def visitRule_ForGenerateStatement(self, ctx: VHDLParser.Rule_ForGenerateStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ForceMode.
	def visitRule_ForceMode(self, ctx: VHDLParser.Rule_ForceModeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FormalDesignator.
	def visitRule_FormalDesignator(self, ctx: VHDLParser.Rule_FormalDesignatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FormalParameterList.
	def visitRule_FormalParameterList(self, ctx: VHDLParser.Rule_FormalParameterListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FormalPart.
	def visitRule_FormalPart(self, ctx: VHDLParser.Rule_FormalPartContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FullTypeDeclaration.
	def visitRule_FullTypeDeclaration(self, ctx: VHDLParser.Rule_FullTypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FunctionCall.
	def visitRule_FunctionCall(self, ctx: VHDLParser.Rule_FunctionCallContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_FunctionSpecification.
	def visitRule_FunctionSpecification(self, ctx: VHDLParser.Rule_FunctionSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenerateSpecification.
	def visitRule_GenerateSpecification(self, ctx: VHDLParser.Rule_GenerateSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenerateStatement.
	def visitRule_GenerateStatement(self, ctx: VHDLParser.Rule_GenerateStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenerateStatementBody.
	def visitRule_GenerateStatementBody(self, ctx: VHDLParser.Rule_GenerateStatementBodyContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_GenericClause.
	def visitRule_GenericClause(self, ctx: VHDLParser.Rule_GenericClauseContext):
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

	# Visit a parse tree produced by VHDLParser#rule_IfGenerateStatement.
	def visitRule_IfGenerateStatement(self, ctx: VHDLParser.Rule_IfGenerateStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IfStatement.
	def visitRule_IfStatement(self, ctx: VHDLParser.Rule_IfStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IncompleteSubtypeIndication.
	def visitRule_IncompleteSubtypeIndication(self, ctx: VHDLParser.Rule_IncompleteSubtypeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IncompleteTypeDeclaration.
	def visitRule_IncompleteTypeDeclaration(self, ctx: VHDLParser.Rule_IncompleteTypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IncompleteTypeDefinition.
	def visitRule_IncompleteTypeDefinition(self, ctx: VHDLParser.Rule_IncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IncompleteTypeMark.
	def visitRule_IncompleteTypeMark(self, ctx: VHDLParser.Rule_IncompleteTypeMarkContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IndexConstraint.
	def visitRule_IndexConstraint(self, ctx: VHDLParser.Rule_IndexConstraintContext):
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

	# Visit a parse tree produced by VHDLParser#rule_IntegerIncompleteTypeDefinition.
	def visitRule_IntegerIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_IntegerIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IntegerTypeDefinition.
	def visitRule_IntegerTypeDefinition(self, ctx: VHDLParser.Rule_IntegerTypeDefinitionContext):
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

	# Visit a parse tree produced by VHDLParser#rule_InterfaceFunctionSpecification.
	def visitRule_InterfaceFunctionSpecification(self, ctx: VHDLParser.Rule_InterfaceFunctionSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceList.
	def visitRule_InterfaceList(self, ctx: VHDLParser.Rule_InterfaceListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfacePackageDeclaration.
	def visitRule_InterfacePackageDeclaration(self, ctx: VHDLParser.Rule_InterfacePackageDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfacePackageGenericMapAspect.
	def visitRule_InterfacePackageGenericMapAspect(self, ctx: VHDLParser.Rule_InterfacePackageGenericMapAspectContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceProcedureSpecification.
	def visitRule_InterfaceProcedureSpecification(self, ctx: VHDLParser.Rule_InterfaceProcedureSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceSignalDeclaration.
	def visitRule_InterfaceSignalDeclaration(self, ctx: VHDLParser.Rule_InterfaceSignalDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceSubprogramDeclaration.
	def visitRule_InterfaceSubprogramDeclaration(self, ctx: VHDLParser.Rule_InterfaceSubprogramDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceSubprogramDefault.
	def visitRule_InterfaceSubprogramDefault(self, ctx: VHDLParser.Rule_InterfaceSubprogramDefaultContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceSubprogramSpecification.
	def visitRule_InterfaceSubprogramSpecification(self, ctx: VHDLParser.Rule_InterfaceSubprogramSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceTypeDeclaration.
	def visitRule_InterfaceTypeDeclaration(self, ctx: VHDLParser.Rule_InterfaceTypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceTypeIndication.
	def visitRule_InterfaceTypeIndication(self, ctx: VHDLParser.Rule_InterfaceTypeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_InterfaceVariableDeclaration.
	def visitRule_InterfaceVariableDeclaration(self, ctx: VHDLParser.Rule_InterfaceVariableDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IterationScheme.
	def visitRule_IterationScheme(self, ctx: VHDLParser.Rule_IterationSchemeContext):
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

	# Visit a parse tree produced by VHDLParser#rule_Mode.
	def visitRule_Mode(self, ctx: VHDLParser.Rule_ModeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ModeIndication.
	def visitRule_ModeIndication(self, ctx: VHDLParser.Rule_ModeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ModeViewDeclaration.
	def visitRule_ModeViewDeclaration(self, ctx: VHDLParser.Rule_ModeViewDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ModeViewElementDefinition.
	def visitRule_ModeViewElementDefinition(self, ctx: VHDLParser.Rule_ModeViewElementDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Char.
	def visitRule_Char(self, ctx: VHDLParser.Rule_CharContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_IndexedName.
	def visitRule_IndexedName(self, ctx: VHDLParser.Rule_IndexedNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleName.
	def visitRule_SimpleName(self, ctx: VHDLParser.Rule_SimpleNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_External.
	def visitRule_External(self, ctx: VHDLParser.Rule_ExternalContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_AttributeName.
	def visitRule_AttributeName(self, ctx: VHDLParser.Rule_AttributeNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedName.
	def visitRule_SelectedName(self, ctx: VHDLParser.Rule_SelectedNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SliceName.
	def visitRule_SliceName(self, ctx: VHDLParser.Rule_SliceNameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Operator.
	def visitRule_Operator(self, ctx: VHDLParser.Rule_OperatorContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_NextStatement.
	def visitRule_NextStatement(self, ctx: VHDLParser.Rule_NextStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_NullStatement.
	def visitRule_NullStatement(self, ctx: VHDLParser.Rule_NullStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_NumericLiteral.
	def visitRule_NumericLiteral(self, ctx: VHDLParser.Rule_NumericLiteralContext):
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

	# Visit a parse tree produced by VHDLParser#rule_PackageInstantiationDeclaration.
	def visitRule_PackageInstantiationDeclaration(self, ctx: VHDLParser.Rule_PackageInstantiationDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PackagePathname.
	def visitRule_PackagePathname(self, ctx: VHDLParser.Rule_PackagePathnameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ParameterMapAspect.
	def visitRule_ParameterMapAspect(self, ctx: VHDLParser.Rule_ParameterMapAspectContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ParameterSpecification.
	def visitRule_ParameterSpecification(self, ctx: VHDLParser.Rule_ParameterSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PartialPathname.
	def visitRule_PartialPathname(self, ctx: VHDLParser.Rule_PartialPathnameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PathnameElement.
	def visitRule_PathnameElement(self, ctx: VHDLParser.Rule_PathnameElementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PhysicalIncompleteTypeDefinition.
	def visitRule_PhysicalIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_PhysicalIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PhysicalLiteral.
	def visitRule_PhysicalLiteral(self, ctx: VHDLParser.Rule_PhysicalLiteralContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PhysicalTypeDefinition.
	def visitRule_PhysicalTypeDefinition(self, ctx: VHDLParser.Rule_PhysicalTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PlainReturnStatement.
	def visitRule_PlainReturnStatement(self, ctx: VHDLParser.Rule_PlainReturnStatementContext):
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

	# Visit a parse tree produced by VHDLParser#rule_PrivateVariableDeclaration.
	def visitRule_PrivateVariableDeclaration(self, ctx: VHDLParser.Rule_PrivateVariableDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PrivateIncompleteTypeDefinition.
	def visitRule_PrivateIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_PrivateIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcedureCall.
	def visitRule_ProcedureCall(self, ctx: VHDLParser.Rule_ProcedureCallContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcedureCallStatement.
	def visitRule_ProcedureCallStatement(self, ctx: VHDLParser.Rule_ProcedureCallStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcedureSpecification.
	def visitRule_ProcedureSpecification(self, ctx: VHDLParser.Rule_ProcedureSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessDeclarativeItem.
	def visitRule_ProcessDeclarativeItem(self, ctx: VHDLParser.Rule_ProcessDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessSensitivityList.
	def visitRule_ProcessSensitivityList(self, ctx: VHDLParser.Rule_ProcessSensitivityListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProcessStatement.
	def visitRule_ProcessStatement(self, ctx: VHDLParser.Rule_ProcessStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_PostponedProcessStatement.
	def visitRule_PostponedProcessStatement(self, ctx: VHDLParser.Rule_PostponedProcessStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProtectedTypeBody.
	def visitRule_ProtectedTypeBody(self, ctx: VHDLParser.Rule_ProtectedTypeBodyContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProtectedTypeBodyDeclarativeItem.
	def visitRule_ProtectedTypeBodyDeclarativeItem(self, ctx: VHDLParser.Rule_ProtectedTypeBodyDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProtectedTypeDeclaration.
	def visitRule_ProtectedTypeDeclaration(self, ctx: VHDLParser.Rule_ProtectedTypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProtectedTypeDeclarativeItem.
	def visitRule_ProtectedTypeDeclarativeItem(self, ctx: VHDLParser.Rule_ProtectedTypeDeclarativeItemContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProtectedTypeDefinition.
	def visitRule_ProtectedTypeDefinition(self, ctx: VHDLParser.Rule_ProtectedTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ProtectedTypeInstantiationDefinition.
	def visitRule_ProtectedTypeInstantiationDefinition(self,
																										 ctx: VHDLParser.Rule_ProtectedTypeInstantiationDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_QualifiedExpression.
	def visitRule_QualifiedExpression(self, ctx: VHDLParser.Rule_QualifiedExpressionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_Range.
	def visitRule_Range(self, ctx: VHDLParser.Rule_RangeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RangeConstraint.
	def visitRule_RangeConstraint(self, ctx: VHDLParser.Rule_RangeConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordConstraint.
	def visitRule_RecordConstraint(self, ctx: VHDLParser.Rule_RecordConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordElementConstraint.
	def visitRule_RecordElementConstraint(self, ctx: VHDLParser.Rule_RecordElementConstraintContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordElementList.
	def visitRule_RecordElementList(self, ctx: VHDLParser.Rule_RecordElementListContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordElementResolution.
	def visitRule_RecordElementResolution(self, ctx: VHDLParser.Rule_RecordElementResolutionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordResolution.
	def visitRule_RecordResolution(self, ctx: VHDLParser.Rule_RecordResolutionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordTypeDefinition.
	def visitRule_RecordTypeDefinition(self, ctx: VHDLParser.Rule_RecordTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RecordModeViewIndication.
	def visitRule_RecordModeViewIndication(self, ctx: VHDLParser.Rule_RecordModeViewIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_RelativePathname.
	def visitRule_RelativePathname(self, ctx: VHDLParser.Rule_RelativePathnameContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ReportStatement.
	def visitRule_ReportStatement(self, ctx: VHDLParser.Rule_ReportStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ResolutionIndication.
	def visitRule_ResolutionIndication(self, ctx: VHDLParser.Rule_ResolutionIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ReturnStatement.
	def visitRule_ReturnStatement(self, ctx: VHDLParser.Rule_ReturnStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ScalarIncompleteTypeDefinition.
	def visitRule_ScalarIncompleteTypeDefinition(self, ctx: VHDLParser.Rule_ScalarIncompleteTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ScalarTypeDefinition.
	def visitRule_ScalarTypeDefinition(self, ctx: VHDLParser.Rule_ScalarTypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SecondaryUnitDeclaration.
	def visitRule_SecondaryUnitDeclaration(self, ctx: VHDLParser.Rule_SecondaryUnitDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedExpressions.
	def visitRule_SelectedExpressions(self, ctx: VHDLParser.Rule_SelectedExpressionsContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedForceAssignment.
	def visitRule_SelectedForceAssignment(self, ctx: VHDLParser.Rule_SelectedForceAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedName2.
	def visitRule_SelectedName2(self, ctx: VHDLParser.Rule_SelectedName2Context):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedSignalAssignment.
	def visitRule_SelectedSignalAssignment(self, ctx: VHDLParser.Rule_SelectedSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedVariableAssignment.
	def visitRule_SelectedVariableAssignment(self, ctx: VHDLParser.Rule_SelectedVariableAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SelectedWaveformAssignment.
	def visitRule_SelectedWaveformAssignment(self, ctx: VHDLParser.Rule_SelectedWaveformAssignmentContext):
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

	# Visit a parse tree produced by VHDLParser#rule_SequentialBlockStatement.
	def visitRule_SequentialBlockStatement(self, ctx: VHDLParser.Rule_SequentialBlockStatementContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SequentialStatement.
	def visitRule_SequentialStatement(self, ctx: VHDLParser.Rule_SequentialStatementContext):
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

	# Visit a parse tree produced by VHDLParser#rule_SimpleConfigurationSpecification.
	def visitRule_SimpleConfigurationSpecification(self, ctx: VHDLParser.Rule_SimpleConfigurationSpecificationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleForceAssignment.
	def visitRule_SimpleForceAssignment(self, ctx: VHDLParser.Rule_SimpleForceAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleModeIndication.
	def visitRule_SimpleModeIndication(self, ctx: VHDLParser.Rule_SimpleModeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleRange.
	def visitRule_SimpleRange(self, ctx: VHDLParser.Rule_SimpleRangeContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleReleaseAssignment.
	def visitRule_SimpleReleaseAssignment(self, ctx: VHDLParser.Rule_SimpleReleaseAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleSignalAssignment.
	def visitRule_SimpleSignalAssignment(self, ctx: VHDLParser.Rule_SimpleSignalAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleWaveformAssignment.
	def visitRule_SimpleWaveformAssignment(self, ctx: VHDLParser.Rule_SimpleWaveformAssignmentContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SimpleVariableAssignment.
	def visitRule_SimpleVariableAssignment(self, ctx: VHDLParser.Rule_SimpleVariableAssignmentContext):
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

	# Visit a parse tree produced by VHDLParser#rule_SubprogramInstantiationDeclaration.
	def visitRule_SubprogramInstantiationDeclaration(self,
																									 ctx: VHDLParser.Rule_SubprogramInstantiationDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramKind.
	def visitRule_SubprogramKind(self, ctx: VHDLParser.Rule_SubprogramKindContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_SubprogramSpecification.
	def visitRule_SubprogramSpecification(self, ctx: VHDLParser.Rule_SubprogramSpecificationContext):
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

	# Visit a parse tree produced by VHDLParser#rule_TimeoutClause.
	def visitRule_TimeoutClause(self, ctx: VHDLParser.Rule_TimeoutClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TypeConversion.
	def visitRule_TypeConversion(self, ctx: VHDLParser.Rule_TypeConversionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TypeDeclaration.
	def visitRule_TypeDeclaration(self, ctx: VHDLParser.Rule_TypeDeclarationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TypeDefinition.
	def visitRule_TypeDefinition(self, ctx: VHDLParser.Rule_TypeDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_TypeMark.
	def visitRule_TypeMark(self, ctx: VHDLParser.Rule_TypeMarkContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_UnboundArrayDefinition.
	def visitRule_UnboundArrayDefinition(self, ctx: VHDLParser.Rule_UnboundArrayDefinitionContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_UnspecifiedTypeIndication.
	def visitRule_UnspecifiedTypeIndication(self, ctx: VHDLParser.Rule_UnspecifiedTypeIndicationContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_UseClause.
	def visitRule_UseClause(self, ctx: VHDLParser.Rule_UseClauseContext):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by VHDLParser#rule_ValueReturnStatement.
	def visitRule_ValueReturnStatement(self, ctx: VHDLParser.Rule_ValueReturnStatementContext):
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
