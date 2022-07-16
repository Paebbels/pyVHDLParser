from antlr4 import ParseTreeVisitor

from .VHDLParser import VHDLParser


class VHDLParserVisitor(ParseTreeVisitor):
    # Visit a parse tree produced by VHDLParser#access_type_definition.
    def visitAccess_type_definition(self, ctx:VHDLParser.Access_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#actual_designator.
    def visitActual_designator(self, ctx:VHDLParser.Actual_designatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#actual_parameter_part.
    def visitActual_parameter_part(self, ctx:VHDLParser.Actual_parameter_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#actual_part.
    def visitActual_part(self, ctx:VHDLParser.Actual_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#adding_operator.
    def visitAdding_operator(self, ctx:VHDLParser.Adding_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#aggregate.
    def visitAggregate(self, ctx:VHDLParser.AggregateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#alias_declaration.
    def visitAlias_declaration(self, ctx:VHDLParser.Alias_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#alias_designator.
    def visitAlias_designator(self, ctx:VHDLParser.Alias_designatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#alias_indication.
    def visitAlias_indication(self, ctx:VHDLParser.Alias_indicationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#allocator.
    def visitAllocator(self, ctx:VHDLParser.AllocatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#architecture_body.
    def visitArchitecture_body(self, ctx:VHDLParser.Architecture_bodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#architecture_declarative_part.
    def visitArchitecture_declarative_part(self, ctx:VHDLParser.Architecture_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#architecture_statement.
    def visitArchitecture_statement(self, ctx:VHDLParser.Architecture_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#architecture_statement_part.
    def visitArchitecture_statement_part(self, ctx:VHDLParser.Architecture_statement_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#array_type_definition.
    def visitArray_type_definition(self, ctx:VHDLParser.Array_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#assertion.
    def visitAssertion(self, ctx:VHDLParser.AssertionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#assertion_statement.
    def visitAssertion_statement(self, ctx:VHDLParser.Assertion_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#association_element.
    def visitAssociation_element(self, ctx:VHDLParser.Association_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#association_list.
    def visitAssociation_list(self, ctx:VHDLParser.Association_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#attribute_declaration.
    def visitAttribute_declaration(self, ctx:VHDLParser.Attribute_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#attribute_designator.
    def visitAttribute_designator(self, ctx:VHDLParser.Attribute_designatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#attribute_specification.
    def visitAttribute_specification(self, ctx:VHDLParser.Attribute_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#base_unit_declaration.
    def visitBase_unit_declaration(self, ctx:VHDLParser.Base_unit_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#binding_indication.
    def visitBinding_indication(self, ctx:VHDLParser.Binding_indicationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_configuration.
    def visitBlock_configuration(self, ctx:VHDLParser.Block_configurationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_declarative_item.
    def visitBlock_declarative_item(self, ctx:VHDLParser.Block_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_declarative_part.
    def visitBlock_declarative_part(self, ctx:VHDLParser.Block_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_header.
    def visitBlock_header(self, ctx:VHDLParser.Block_headerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_specification.
    def visitBlock_specification(self, ctx:VHDLParser.Block_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_statement.
    def visitBlock_statement(self, ctx:VHDLParser.Block_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#block_statement_part.
    def visitBlock_statement_part(self, ctx:VHDLParser.Block_statement_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#case_statement.
    def visitCase_statement(self, ctx:VHDLParser.Case_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#case_statement_alternative.
    def visitCase_statement_alternative(self, ctx:VHDLParser.Case_statement_alternativeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#choice.
    def visitChoice(self, ctx:VHDLParser.ChoiceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#choices.
    def visitChoices(self, ctx:VHDLParser.ChoicesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#component_configuration.
    def visitComponent_configuration(self, ctx:VHDLParser.Component_configurationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#component_declaration.
    def visitComponent_declaration(self, ctx:VHDLParser.Component_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#component_instantiation_statement.
    def visitComponent_instantiation_statement(self, ctx:VHDLParser.Component_instantiation_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#component_specification.
    def visitComponent_specification(self, ctx:VHDLParser.Component_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#composite_type_definition.
    def visitComposite_type_definition(self, ctx:VHDLParser.Composite_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#concurrent_assertion_statement.
    def visitConcurrent_assertion_statement(self, ctx:VHDLParser.Concurrent_assertion_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#concurrent_procedure_call_statement.
    def visitConcurrent_procedure_call_statement(self, ctx:VHDLParser.Concurrent_procedure_call_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#concurrent_signal_assignment_statement.
    def visitConcurrent_signal_assignment_statement(self, ctx:VHDLParser.Concurrent_signal_assignment_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#condition.
    def visitCondition(self, ctx:VHDLParser.ConditionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#condition_clause.
    def visitCondition_clause(self, ctx:VHDLParser.Condition_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#conditional_signal_assignment.
    def visitConditional_signal_assignment(self, ctx:VHDLParser.Conditional_signal_assignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#conditional_waveforms.
    def visitConditional_waveforms(self, ctx:VHDLParser.Conditional_waveformsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#configuration_declaration.
    def visitConfiguration_declaration(self, ctx:VHDLParser.Configuration_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#configuration_declarative_item.
    def visitConfiguration_declarative_item(self, ctx:VHDLParser.Configuration_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#configuration_declarative_part.
    def visitConfiguration_declarative_part(self, ctx:VHDLParser.Configuration_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#configuration_item.
    def visitConfiguration_item(self, ctx:VHDLParser.Configuration_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#configuration_specification.
    def visitConfiguration_specification(self, ctx:VHDLParser.Configuration_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#constant_declaration.
    def visitConstant_declaration(self, ctx:VHDLParser.Constant_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#constrained_array_definition.
    def visitConstrained_array_definition(self, ctx:VHDLParser.Constrained_array_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#constraint.
    def visitConstraint(self, ctx:VHDLParser.ConstraintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#context_clause.
    def visitContext_clause(self, ctx:VHDLParser.Context_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#context_item.
    def visitContext_item(self, ctx:VHDLParser.Context_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#delay_mechanism.
    def visitDelay_mechanism(self, ctx:VHDLParser.Delay_mechanismContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#design_file.
    def visitDesign_file(self, ctx:VHDLParser.Design_fileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#design_unit.
    def visitDesign_unit(self, ctx:VHDLParser.Design_unitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#designator.
    def visitDesignator(self, ctx:VHDLParser.DesignatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#direction.
    def visitDirection(self, ctx:VHDLParser.DirectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#disconnection_specification.
    def visitDisconnection_specification(self, ctx:VHDLParser.Disconnection_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#discrete_range.
    def visitDiscrete_range(self, ctx:VHDLParser.Discrete_rangeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#element_association.
    def visitElement_association(self, ctx:VHDLParser.Element_associationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#element_declaration.
    def visitElement_declaration(self, ctx:VHDLParser.Element_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#element_subtype_definition.
    def visitElement_subtype_definition(self, ctx:VHDLParser.Element_subtype_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_aspect.
    def visitEntity_aspect(self, ctx:VHDLParser.Entity_aspectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_class.
    def visitEntity_class(self, ctx:VHDLParser.Entity_classContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_class_entry.
    def visitEntity_class_entry(self, ctx:VHDLParser.Entity_class_entryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_class_entry_list.
    def visitEntity_class_entry_list(self, ctx:VHDLParser.Entity_class_entry_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_declaration.
    def visitEntity_declaration(self, ctx:VHDLParser.Entity_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_declarative_item.
    def visitEntity_declarative_item(self, ctx:VHDLParser.Entity_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_declarative_part.
    def visitEntity_declarative_part(self, ctx:VHDLParser.Entity_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_designator.
    def visitEntity_designator(self, ctx:VHDLParser.Entity_designatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_header.
    def visitEntity_header(self, ctx:VHDLParser.Entity_headerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_name_list.
    def visitEntity_name_list(self, ctx:VHDLParser.Entity_name_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_specification.
    def visitEntity_specification(self, ctx:VHDLParser.Entity_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_statement.
    def visitEntity_statement(self, ctx:VHDLParser.Entity_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_statement_part.
    def visitEntity_statement_part(self, ctx:VHDLParser.Entity_statement_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#entity_tag.
    def visitEntity_tag(self, ctx:VHDLParser.Entity_tagContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#enumeration_literal.
    def visitEnumeration_literal(self, ctx:VHDLParser.Enumeration_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#enumeration_type_definition.
    def visitEnumeration_type_definition(self, ctx:VHDLParser.Enumeration_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#exit_statement.
    def visitExit_statement(self, ctx:VHDLParser.Exit_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#expression.
    def visitExpression(self, ctx:VHDLParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#factor.
    def visitFactor(self, ctx:VHDLParser.FactorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#file_declaration.
    def visitFile_declaration(self, ctx:VHDLParser.File_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#file_logical_name.
    def visitFile_logical_name(self, ctx:VHDLParser.File_logical_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#file_open_information.
    def visitFile_open_information(self, ctx:VHDLParser.File_open_informationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#file_type_definition.
    def visitFile_type_definition(self, ctx:VHDLParser.File_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#formal_parameter_list.
    def visitFormal_parameter_list(self, ctx:VHDLParser.Formal_parameter_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#formal_part.
    def visitFormal_part(self, ctx:VHDLParser.Formal_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#generate_statement.
    def visitGenerate_statement(self, ctx:VHDLParser.Generate_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#generation_scheme.
    def visitGeneration_scheme(self, ctx:VHDLParser.Generation_schemeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#generic_clause.
    def visitGeneric_clause(self, ctx:VHDLParser.Generic_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#generic_list.
    def visitGeneric_list(self, ctx:VHDLParser.Generic_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#generic_map_aspect.
    def visitGeneric_map_aspect(self, ctx:VHDLParser.Generic_map_aspectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#guarded_signal_specification.
    def visitGuarded_signal_specification(self, ctx:VHDLParser.Guarded_signal_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#identifier_list.
    def visitIdentifier_list(self, ctx:VHDLParser.Identifier_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#if_statement.
    def visitIf_statement(self, ctx:VHDLParser.If_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#index_constraint.
    def visitIndex_constraint(self, ctx:VHDLParser.Index_constraintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#index_specification.
    def visitIndex_specification(self, ctx:VHDLParser.Index_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#index_subtype_definition.
    def visitIndex_subtype_definition(self, ctx:VHDLParser.Index_subtype_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#instantiated_unit.
    def visitInstantiated_unit(self, ctx:VHDLParser.Instantiated_unitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#instantiation_list.
    def visitInstantiation_list(self, ctx:VHDLParser.Instantiation_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_constant_declaration.
    def visitInterface_constant_declaration(self, ctx:VHDLParser.Interface_constant_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_declaration.
    def visitInterface_declaration(self, ctx:VHDLParser.Interface_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_element.
    def visitInterface_element(self, ctx:VHDLParser.Interface_elementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_file_declaration.
    def visitInterface_file_declaration(self, ctx:VHDLParser.Interface_file_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_signal_list.
    def visitInterface_signal_list(self, ctx:VHDLParser.Interface_signal_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_port_list.
    def visitInterface_port_list(self, ctx:VHDLParser.Interface_port_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_list.
    def visitInterface_list(self, ctx:VHDLParser.Interface_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_port_declaration.
    def visitInterface_port_declaration(self, ctx:VHDLParser.Interface_port_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_signal_declaration.
    def visitInterface_signal_declaration(self, ctx:VHDLParser.Interface_signal_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#interface_variable_declaration.
    def visitInterface_variable_declaration(self, ctx:VHDLParser.Interface_variable_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#iteration_scheme.
    def visitIteration_scheme(self, ctx:VHDLParser.Iteration_schemeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#label_colon.
    def visitLabel_colon(self, ctx:VHDLParser.Label_colonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#library_clause.
    def visitLibrary_clause(self, ctx:VHDLParser.Library_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#library_unit.
    def visitLibrary_unit(self, ctx:VHDLParser.Library_unitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#literal.
    def visitLiteral(self, ctx:VHDLParser.LiteralContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#logical_name.
    def visitLogical_name(self, ctx:VHDLParser.Logical_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#logical_name_list.
    def visitLogical_name_list(self, ctx:VHDLParser.Logical_name_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#logical_operator.
    def visitLogical_operator(self, ctx:VHDLParser.Logical_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#loop_statement.
    def visitLoop_statement(self, ctx:VHDLParser.Loop_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#signal_mode.
    def visitSignal_mode(self, ctx:VHDLParser.Signal_modeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#multiplying_operator.
    def visitMultiplying_operator(self, ctx:VHDLParser.Multiplying_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#name.
    def visitName(self, ctx:VHDLParser.NameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#name_part.
    def visitName_part(self, ctx:VHDLParser.Name_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#selected_name.
    def visitSelected_name(self, ctx:VHDLParser.Selected_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#selected_name_part.
    def visitSelected_name_part(self, ctx:VHDLParser.Selected_name_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#function_call_or_indexed_name_part.
    def visitFunction_call_or_indexed_name_part(self, ctx:VHDLParser.Function_call_or_indexed_name_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#slice_name_part.
    def visitSlice_name_part(self, ctx:VHDLParser.Slice_name_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#attribute_name_part.
    def visitAttribute_name_part(self, ctx:VHDLParser.Attribute_name_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#next_statement.
    def visitNext_statement(self, ctx:VHDLParser.Next_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#numeric_literal.
    def visitNumeric_literal(self, ctx:VHDLParser.Numeric_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#object_declaration.
    def visitObject_declaration(self, ctx:VHDLParser.Object_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#opts.
    def visitOpts(self, ctx:VHDLParser.OptsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#package_body.
    def visitPackage_body(self, ctx:VHDLParser.Package_bodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#package_body_declarative_item.
    def visitPackage_body_declarative_item(self, ctx:VHDLParser.Package_body_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#package_body_declarative_part.
    def visitPackage_body_declarative_part(self, ctx:VHDLParser.Package_body_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#package_declaration.
    def visitPackage_declaration(self, ctx:VHDLParser.Package_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#package_declarative_item.
    def visitPackage_declarative_item(self, ctx:VHDLParser.Package_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#package_declarative_part.
    def visitPackage_declarative_part(self, ctx:VHDLParser.Package_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#parameter_specification.
    def visitParameter_specification(self, ctx:VHDLParser.Parameter_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#physical_literal.
    def visitPhysical_literal(self, ctx:VHDLParser.Physical_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#physical_type_definition.
    def visitPhysical_type_definition(self, ctx:VHDLParser.Physical_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#port_clause.
    def visitPort_clause(self, ctx:VHDLParser.Port_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#port_list.
    def visitPort_list(self, ctx:VHDLParser.Port_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#port_map_aspect.
    def visitPort_map_aspect(self, ctx:VHDLParser.Port_map_aspectContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#primary.
    def visitPrimary(self, ctx:VHDLParser.PrimaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#primary_unit.
    def visitPrimary_unit(self, ctx:VHDLParser.Primary_unitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#procedure_call.
    def visitProcedure_call(self, ctx:VHDLParser.Procedure_callContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#procedure_call_statement.
    def visitProcedure_call_statement(self, ctx:VHDLParser.Procedure_call_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#process_declarative_item.
    def visitProcess_declarative_item(self, ctx:VHDLParser.Process_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#process_declarative_part.
    def visitProcess_declarative_part(self, ctx:VHDLParser.Process_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#process_statement.
    def visitProcess_statement(self, ctx:VHDLParser.Process_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#postponed_process_statement.
    def visitPostponed_process_statement(self, ctx:VHDLParser.Postponed_process_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#process_statement_part.
    def visitProcess_statement_part(self, ctx:VHDLParser.Process_statement_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#qualified_expression.
    def visitQualified_expression(self, ctx:VHDLParser.Qualified_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#range_decl.
    def visitRange_decl(self, ctx:VHDLParser.Range_declContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#explicit_range.
    def visitExplicit_range(self, ctx:VHDLParser.Explicit_rangeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#range_constraint.
    def visitRange_constraint(self, ctx:VHDLParser.Range_constraintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#record_type_definition.
    def visitRecord_type_definition(self, ctx:VHDLParser.Record_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#relation.
    def visitRelation(self, ctx:VHDLParser.RelationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#relational_operator.
    def visitRelational_operator(self, ctx:VHDLParser.Relational_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#report_statement.
    def visitReport_statement(self, ctx:VHDLParser.Report_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#return_statement.
    def visitReturn_statement(self, ctx:VHDLParser.Return_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#scalar_type_definition.
    def visitScalar_type_definition(self, ctx:VHDLParser.Scalar_type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#secondary_unit.
    def visitSecondary_unit(self, ctx:VHDLParser.Secondary_unitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#secondary_unit_declaration.
    def visitSecondary_unit_declaration(self, ctx:VHDLParser.Secondary_unit_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#selected_signal_assignment.
    def visitSelected_signal_assignment(self, ctx:VHDLParser.Selected_signal_assignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#selected_waveforms.
    def visitSelected_waveforms(self, ctx:VHDLParser.Selected_waveformsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#sensitivity_clause.
    def visitSensitivity_clause(self, ctx:VHDLParser.Sensitivity_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#sensitivity_list.
    def visitSensitivity_list(self, ctx:VHDLParser.Sensitivity_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#sequence_of_statements.
    def visitSequence_of_statements(self, ctx:VHDLParser.Sequence_of_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#sequential_statement.
    def visitSequential_statement(self, ctx:VHDLParser.Sequential_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#shift_expression.
    def visitShift_expression(self, ctx:VHDLParser.Shift_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#shift_operator.
    def visitShift_operator(self, ctx:VHDLParser.Shift_operatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#signal_assignment_statement.
    def visitSignal_assignment_statement(self, ctx:VHDLParser.Signal_assignment_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#signal_declaration.
    def visitSignal_declaration(self, ctx:VHDLParser.Signal_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#signal_kind.
    def visitSignal_kind(self, ctx:VHDLParser.Signal_kindContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#signal_list.
    def visitSignal_list(self, ctx:VHDLParser.Signal_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#signature.
    def visitSignature(self, ctx:VHDLParser.SignatureContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simple_expression.
    def visitSimple_expression(self, ctx:VHDLParser.Simple_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simple_simultaneous_statement.
    def visitSimple_simultaneous_statement(self, ctx:VHDLParser.Simple_simultaneous_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simultaneous_alternative.
    def visitSimultaneous_alternative(self, ctx:VHDLParser.Simultaneous_alternativeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simultaneous_case_statement.
    def visitSimultaneous_case_statement(self, ctx:VHDLParser.Simultaneous_case_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simultaneous_if_statement.
    def visitSimultaneous_if_statement(self, ctx:VHDLParser.Simultaneous_if_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simultaneous_statement.
    def visitSimultaneous_statement(self, ctx:VHDLParser.Simultaneous_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#simultaneous_statement_part.
    def visitSimultaneous_statement_part(self, ctx:VHDLParser.Simultaneous_statement_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_body.
    def visitSubprogram_body(self, ctx:VHDLParser.Subprogram_bodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_declaration.
    def visitSubprogram_declaration(self, ctx:VHDLParser.Subprogram_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_declarative_item.
    def visitSubprogram_declarative_item(self, ctx:VHDLParser.Subprogram_declarative_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_declarative_part.
    def visitSubprogram_declarative_part(self, ctx:VHDLParser.Subprogram_declarative_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_kind.
    def visitSubprogram_kind(self, ctx:VHDLParser.Subprogram_kindContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_specification.
    def visitSubprogram_specification(self, ctx:VHDLParser.Subprogram_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#procedure_specification.
    def visitProcedure_specification(self, ctx:VHDLParser.Procedure_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#function_specification.
    def visitFunction_specification(self, ctx:VHDLParser.Function_specificationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subprogram_statement_part.
    def visitSubprogram_statement_part(self, ctx:VHDLParser.Subprogram_statement_partContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subtype_declaration.
    def visitSubtype_declaration(self, ctx:VHDLParser.Subtype_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#subtype_indication.
    def visitSubtype_indication(self, ctx:VHDLParser.Subtype_indicationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#suffix.
    def visitSuffix(self, ctx:VHDLParser.SuffixContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#target.
    def visitTarget(self, ctx:VHDLParser.TargetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#term.
    def visitTerm(self, ctx:VHDLParser.TermContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#timeout_clause.
    def visitTimeout_clause(self, ctx:VHDLParser.Timeout_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#type_declaration.
    def visitType_declaration(self, ctx:VHDLParser.Type_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#type_definition.
    def visitType_definition(self, ctx:VHDLParser.Type_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#unconstrained_array_definition.
    def visitUnconstrained_array_definition(self, ctx:VHDLParser.Unconstrained_array_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#use_clause.
    def visitUse_clause(self, ctx:VHDLParser.Use_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#variable_assignment_statement.
    def visitVariable_assignment_statement(self, ctx:VHDLParser.Variable_assignment_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#variable_declaration.
    def visitVariable_declaration(self, ctx:VHDLParser.Variable_declarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#wait_statement.
    def visitWait_statement(self, ctx:VHDLParser.Wait_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#waveform.
    def visitWaveform(self, ctx:VHDLParser.WaveformContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by VHDLParser#waveform_element.
    def visitWaveform_element(self, ctx:VHDLParser.Waveform_elementContext):
        return self.visitChildren(ctx)


del VHDLParser
