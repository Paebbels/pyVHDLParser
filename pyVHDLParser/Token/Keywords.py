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
from pyVHDLParser.Decorators    import Export
from pyVHDLParser.Token         import StringToken, VHDLToken
from pyVHDLParser.Token.Parser  import TokenizerException

__all__ = []
__api__ = __all__


@Export
class BoundaryToken(VHDLToken):
	def __init__(self, spaceToken):
		super().__init__(spaceToken.PreviousToken, spaceToken.Value, spaceToken.Start, spaceToken.End)


@Export
class BracketToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)


# Round bracket / parenthesis / ()
@Export
class RoundBracketToken(BracketToken):
	pass
@Export
class OpeningRoundBracketToken(RoundBracketToken):
	pass
@Export
class ClosingRoundBracketToken(RoundBracketToken):
	pass

# Square bracket / []
@Export
class SquareBracketToken(BracketToken):
	pass
@Export
class OpeningSquareBracketToken(SquareBracketToken):
	pass
@Export
class ClosingSquareBracketToken(SquareBracketToken):
	pass

# Curly bracket / brace / curved bracket / {}
@Export
class CurlyBracketToken(BracketToken):
	pass
@Export
class OpeningCurlyBracketToken(CurlyBracketToken):
	pass
@Export
class ClosingCurlyBracketToken(CurlyBracketToken):
	pass

# Angle bracket / arrow bracket / <>
@Export
class AngleBracketToken(BracketToken):
	pass
@Export
class OpeningAngleBracketToken(AngleBracketToken):
	pass
@Export
class ClosingAngleBracketToken(AngleBracketToken):
	pass


@Export
class OperatorToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)


@Export
class PlusOperator(OperatorToken):
	pass
@Export
class MinusOperator(OperatorToken):
	pass
@Export
class MultiplyOperator(OperatorToken):
	pass
@Export
class DivideOperator(OperatorToken):
	pass
@Export
class PowerOperator(OperatorToken):
	pass
@Export
class ConcatOperator(OperatorToken):
	pass

@Export
class RelationalOperator(OperatorToken):
	pass
@Export
class EqualOperator(RelationalOperator):
	__KEYWORD__ = "="
@Export
class UnequalOperator(RelationalOperator):
	__KEYWORD__ = "/="
@Export
class LessThanOperator(RelationalOperator):
	__KEYWORD__ = "<"
@Export
class LessThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = "<="
@Export
class GreaterThanOperator(RelationalOperator):
	__KEYWORD__ = ">"
@Export
class GreaterThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = ">="
@Export
class MatchingEqualOperator(RelationalOperator):
	__KEYWORD__ = "?="
@Export
class MatchingUnequalOperator(RelationalOperator):
	__KEYWORD__ = "?/="
@Export
class MatchingLessThanOperator(RelationalOperator):
	__KEYWORD__ = "?<"
@Export
class MatchingLessThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = "?<="
@Export
class MatchingGreaterThanOperator(RelationalOperator):
	__KEYWORD__ = "?>"
@Export
class MatchingGreaterThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = "?>="


@Export
class DelimiterToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)


@Export
class EndToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)


@Export
class IdentifierToken(VHDLToken):
	def __init__(self, stringToken):
		super().__init__(stringToken.PreviousToken, stringToken.Value, stringToken.Start, stringToken.End)


@Export
class RepeatedIdentifierToken(IdentifierToken):
	pass


@Export
class SimpleNameToken(VHDLToken):
	def __init__(self, stringToken):
		super().__init__(stringToken.PreviousToken, stringToken.Value, stringToken.Start, stringToken.End)


@Export
class LabelToken(VHDLToken):
	def __init__(self, stringToken):
		super().__init__(stringToken.PreviousToken, stringToken.Value, stringToken.Start, stringToken.End)


@Export
class RepeatedLabelToken(LabelToken):
	pass


@Export
class MultiCharKeyword(VHDLToken):
	__KEYWORD__ = None

	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, self.__KEYWORD__, characterToken.Start, characterToken.End)

	def __str__(self):
		return "<{name: <50} '{value}' at {pos!r}>".format(
			name=self.__class__.__name__[:-7],
			value=self.__KEYWORD__,
			pos=self.Start
		)


@Export
class CommentKeyword(MultiCharKeyword):
	pass
@Export
class SingleLineCommentKeyword(CommentKeyword):
	__KEYWORD__ = "--"
@Export
class MultiLineCommentKeyword(CommentKeyword):
	pass
@Export
class MultiLineCommentStartKeyword(MultiLineCommentKeyword):
	__KEYWORD__ = "/*"
@Export
class MultiLineCommentEndKeyword(MultiLineCommentKeyword):
	__KEYWORD__ = "*/"

@Export
class AssignmentKeyword(MultiCharKeyword):
	pass
@Export
class VariableAssignmentKeyword(AssignmentKeyword):
	__KEYWORD__ = ":="
@Export
class SignalAssignmentKeyword(AssignmentKeyword):
	__KEYWORD__ = "<="

@Export
class AssociationKeyword(MultiCharKeyword):
	pass
@Export
class MapAssociationKeyword(AssociationKeyword):
	__KEYWORD__ = "=>"
@Export
class SignalAssociationKeyword(AssociationKeyword):
	__KEYWORD__ = "<=>"


@Export
class KeywordToken(VHDLToken):
	__KEYWORD__ = None

	def __init__(self, stringToken):
		if (not (isinstance(stringToken, StringToken) and (stringToken <= self.__KEYWORD__))):
			raise TokenizerException("Expected keyword {0}.".format(self.__KEYWORD__.upper()), stringToken)
		super().__init__(stringToken.PreviousToken, self.__KEYWORD__, stringToken.Start, stringToken.End)

	def __str__(self):
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + self.Value + "'  ",
				pos=self.Start
			)

@Export
class DirectionKeyword(KeywordToken):
	pass

@Export
class Operator(KeywordToken):
	pass
@Export
class LogicalOperator(Operator):
	pass
@Export
class MiscellaneousOperator(Operator):
	pass
@Export
class ShiftOperator(Operator):
	pass

@Export
class AbsKeyword(KeywordToken):
	__KEYWORD__ = "abs"
@Export
class AccessKeyword(KeywordToken):
	__KEYWORD__ = "access"
@Export
class AfterKeyword(KeywordToken):
	__KEYWORD__ = "after"
@Export
class AliasKeyword(KeywordToken):
	__KEYWORD__ = "alias"
@Export
class AllKeyword(KeywordToken):
	__KEYWORD__ = "all"
@Export
class AndKeyword(LogicalOperator):
	__KEYWORD__ = "and"
@Export
class ArchitectureKeyword(KeywordToken):
	__KEYWORD__ = "architecture"
@Export
class ArrayKeyword(KeywordToken):
	__KEYWORD__ = "array"
@Export
class AssertKeyword(KeywordToken):
	__KEYWORD__ = "assert"
@Export
class AttributeKeyword(KeywordToken):
	__KEYWORD__ = "attribute"
@Export
class BeginKeyword(KeywordToken):
	__KEYWORD__ = "begin"
@Export
class BlockKeyword(KeywordToken):
	__KEYWORD__ = "block"
@Export
class BodyKeyword(KeywordToken):
	__KEYWORD__ = "body"
@Export
class BufferKeyword(KeywordToken):
	__KEYWORD__ = "buffer"
@Export
class BusKeyword(KeywordToken):
	__KEYWORD__ = "bus"
@Export
class CaseKeyword(KeywordToken):
	__KEYWORD__ = "case"
@Export
class ComponentKeyword(KeywordToken):
	__KEYWORD__ = "component"
@Export
class ConfigurationKeyword(KeywordToken):
	__KEYWORD__ = "configuration"
@Export
class ConstantKeyword(KeywordToken):
	__KEYWORD__ = "constant"
@Export
class ContextKeyword(KeywordToken):
	__KEYWORD__ = "context"
@Export
class DefaultKeyword(KeywordToken):
	__KEYWORD__ = "default"
@Export
class DisconnectKeyword(KeywordToken):
	__KEYWORD__ = "disconnect"
@Export
class DowntoKeyword(DirectionKeyword):
	__KEYWORD__ = "downto"
@Export
class ElseKeyword(KeywordToken):
	__KEYWORD__ = "else"
@Export
class ElsIfKeyword(KeywordToken):
	__KEYWORD__ = "elsif"
@Export
class EndKeyword(KeywordToken):
	__KEYWORD__ = "end"
@Export
class EntityKeyword(KeywordToken):
	__KEYWORD__ = "entity"
@Export
class ExitKeyword(KeywordToken):
	__KEYWORD__ = "exit"
@Export
class FileKeyword(KeywordToken):
	__KEYWORD__ = "file"
@Export
class ForKeyword(KeywordToken):
	__KEYWORD__ = "for"
@Export
class ForceKeyword(KeywordToken):
	__KEYWORD__ = "force"
@Export
class FunctionKeyword(KeywordToken):
	__KEYWORD__ = "function"
@Export
class GenerateKeyword(KeywordToken):
	__KEYWORD__ = "generate"
@Export
class GenericKeyword(KeywordToken):
	__KEYWORD__ = "generic"
@Export
class GroupKeyword(KeywordToken):
	__KEYWORD__ = "group"
@Export
class GuardedKeyword(KeywordToken):
	__KEYWORD__ = "guarded"
@Export
class IfKeyword(KeywordToken):
	__KEYWORD__ = "if"
@Export
class IsKeyword(KeywordToken):
	__KEYWORD__ = "is"
@Export
class InKeyword(KeywordToken):
	__KEYWORD__ = "in"
@Export
class InoutKeyword(KeywordToken):
	__KEYWORD__ = "inout"
@Export
class ImpureKeyword(KeywordToken):
	__KEYWORD__ = "impure"
@Export
class InertialKeyword(KeywordToken):
	__KEYWORD__ = "inertial"
@Export
class LableKeyword(KeywordToken):
	__KEYWORD__ = "lable"
@Export
class LibraryKeyword(KeywordToken):
	__KEYWORD__ = "library"
@Export
class LinkageKeyword(KeywordToken):
	__KEYWORD__ = "linkage"
@Export
class LiteralKeyword(KeywordToken):
	__KEYWORD__ = "literal"
@Export
class LoopKeyword(KeywordToken):
	__KEYWORD__ = "loop"
@Export
class MapKeyword(KeywordToken):
	__KEYWORD__ = "map"
@Export
class NandKeyword(LogicalOperator):
	__KEYWORD__ = "nand"
@Export
class NewKeyword(KeywordToken):
	__KEYWORD__ = "new"
@Export
class NextKeyword(KeywordToken):
	__KEYWORD__ = "next"
@Export
class NorKeyword(LogicalOperator):
	__KEYWORD__ = "nor"
@Export
class NotKeyword(KeywordToken):
	__KEYWORD__ = "not"
@Export
class NullKeyword(KeywordToken):
	__KEYWORD__ = "null"
@Export
class OfKeyword(KeywordToken):
	__KEYWORD__ = "of"
@Export
class OnKeyword(KeywordToken):
	__KEYWORD__ = "on"
@Export
class OpenKeyword(KeywordToken):
	__KEYWORD__ = "open"
@Export
class OrKeyword(LogicalOperator):
	__KEYWORD__ = "or"
@Export
class OthersKeyword(KeywordToken):
	__KEYWORD__ = "others"
@Export
class OutKeyword(KeywordToken):
	__KEYWORD__ = "out"
@Export
class PackageKeyword(KeywordToken):
	__KEYWORD__ = "package"
@Export
class ParameterKeyword(KeywordToken):
	__KEYWORD__ = "parameter"
@Export
class PortKeyword(KeywordToken):
	__KEYWORD__ = "port"
@Export
class PostponendKeyword(KeywordToken):
	__KEYWORD__ = "postponend"
@Export
class ProcedureKeyword(KeywordToken):
	__KEYWORD__ = "procedure"
@Export
class ProcessKeyword(KeywordToken):
	__KEYWORD__ = "process"
@Export
class PropertyKeyword(KeywordToken):
	__KEYWORD__ = "property"
@Export
class ProtectedKeyword(KeywordToken):
	__KEYWORD__ = "protected"
@Export
class PureKeyword(KeywordToken):
	__KEYWORD__ = "pure"
@Export
class RangeKeyword(KeywordToken):
	__KEYWORD__ = "range"
@Export
class RecordKeyword(KeywordToken):
	__KEYWORD__ = "record"
@Export
class RegisterKeyword(KeywordToken):
	__KEYWORD__ = "register"
@Export
class RejectKeyword(KeywordToken):
	__KEYWORD__ = "reject"
@Export
class ReleaseKeyword(KeywordToken):
	__KEYWORD__ = "release"
@Export
class ReportKeyword(KeywordToken):
	__KEYWORD__ = "report"
@Export
class ReturnKeyword(KeywordToken):
	__KEYWORD__ = "return"
@Export
class RolKeyword(ShiftOperator):
	__KEYWORD__ = "rol"
@Export
class RorKeyword(ShiftOperator):
	__KEYWORD__ = "ror"
@Export
class SelectKeyword(KeywordToken):
	__KEYWORD__ = "select"
@Export
class SequenceKeyword(KeywordToken):
	__KEYWORD__ = "sequence"
@Export
class SeverityKeyword(KeywordToken):
	__KEYWORD__ = "severity"
@Export
class SharedKeyword(KeywordToken):
	__KEYWORD__ = "shared"
@Export
class SignalKeyword(KeywordToken):
	__KEYWORD__ = "signal"
@Export
class SlaKeyword(ShiftOperator):
	__KEYWORD__ = "sla"
@Export
class SllKeyword(ShiftOperator):
	__KEYWORD__ = "sll"
@Export
class SraKeyword(ShiftOperator):
	__KEYWORD__ = "sra"
@Export
class SrlKeyword(ShiftOperator):
	__KEYWORD__ = "srl"
@Export
class SubtypeKeyword(KeywordToken):
	__KEYWORD__ = "subtype"
@Export
class ThenKeyword(KeywordToken):
	__KEYWORD__ = "then"
@Export
class ToKeyword(DirectionKeyword):
	__KEYWORD__ = "to"
@Export
class TransportKeyword(KeywordToken):
	__KEYWORD__ = "transport"
@Export
class TypeKeyword(KeywordToken):
	__KEYWORD__ = "type"
@Export
class UnitsKeyword(KeywordToken):
	__KEYWORD__ = "units"
@Export
class UntilKeyword(KeywordToken):
	__KEYWORD__ = "until"
@Export
class UseKeyword(KeywordToken):
	__KEYWORD__ = "use"
@Export
class UnbufferedKeyword(KeywordToken):
	__KEYWORD__ = "unbuffered"
@Export
class VariableKeyword(KeywordToken):
	__KEYWORD__ = "variable"
@Export
class VunitKeyword(KeywordToken):
	__KEYWORD__ = "vunit"
@Export
class WaitKeyword(KeywordToken):
	__KEYWORD__ = "wait"
@Export
class WhenKeyword(KeywordToken):
	__KEYWORD__ = "when"
@Export
class WhileKeyword(KeywordToken):
	__KEYWORD__ = "while"
@Export
class WithKeyword(KeywordToken):
	__KEYWORD__ = "with"
@Export
class XorKeyword(LogicalOperator):
	__KEYWORD__ = "xor"
@Export
class XnorKeyword(LogicalOperator):
	__KEYWORD__ = "xnor"
