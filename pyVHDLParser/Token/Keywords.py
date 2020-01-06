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
from pyVHDLParser.Token         import Token, WordToken, VHDLToken
from pyVHDLParser.Token.Parser  import TokenizerException

__all__ = []
__api__ = __all__


@Export
class SpecificVHDLToken(VHDLToken):
	"""Base-class for all specific tokens.

	Simple token will be converted to specific tokens while parsing.
	The internal data is copied, and the original token is replaced by this token.
	"""

	def __init__(self, token : Token):
		"""
		Initialize a specific token, by copying the simple token's data and link
		this new token to the previous token as a replacement.
		"""
		super().__init__(token.PreviousToken, token.Value, token.Start, token.End)


@Export
class BoundaryToken(SpecificVHDLToken):
	"""
	Token representing a boundary between (reserved) words.

	In many cases, a :class:`SpaceToken`, :class:`CommentToken`,
	:class:`LinebreakToken` or :class:`CharacterToken` becomes a BoundaryToken.
	"""

# ==============================================================================
# Bracket tokens: (), [], {}, <>
# ==============================================================================
@Export
class BracketToken(SpecificVHDLToken):
	"""Base-class for all bracket tokens: ``(``, ``)``, ``[``, ``]``, ``{``, ``}``, ``<`` and ``>``."""

# Round bracket / parenthesis / ()
# ----------------------------------------------------------
@Export
class RoundBracketToken(BracketToken):
	"""Base-class for all round bracket tokens: ``(`` and ``)``."""

@Export
class OpeningRoundBracketToken(RoundBracketToken):
	"""Token representing an opening round bracket: ``(``."""

@Export
class ClosingRoundBracketToken(RoundBracketToken):
	"""Token representing a closing round bracket: ``)``."""

# Square bracket / []
# ----------------------------------------------------------
@Export
class SquareBracketToken(BracketToken):
	"""Base-class for all square bracket tokens: ``[`` and ``]``."""

@Export
class OpeningSquareBracketToken(SquareBracketToken):
	"""Token representing an square round bracket: ``[``."""

@Export
class ClosingSquareBracketToken(SquareBracketToken):
	"""Token representing a closing square bracket: ``]``."""

# Curly bracket / brace / curved bracket / {}
# ----------------------------------------------------------
@Export
class CurlyBracketToken(BracketToken):
	"""Base-class for all curly bracket tokens: ``{`` and ``}``."""

@Export
class OpeningCurlyBracketToken(CurlyBracketToken):
	"""Token representing an opening curly bracket: ``{``."""

@Export
class ClosingCurlyBracketToken(CurlyBracketToken):
	"""Token representing a closing curly bracket: ``}``."""

# Angle bracket / arrow bracket / <>
# ----------------------------------------------------------
@Export
class AngleBracketToken(BracketToken):
	"""Base-class for all angle bracket tokens: ``<`` and ``>``."""

@Export
class OpeningAngleBracketToken(AngleBracketToken):
	"""Token representing an opening angle bracket: ``<``."""

@Export
class ClosingAngleBracketToken(AngleBracketToken):
	"""Token representing a closing angle bracket: ``>``."""

# ==============================================================================
# Operator tokens: +, -, *, /, **, &
# ==============================================================================
@Export
class OperatorToken(SpecificVHDLToken):
	"""Base-class for all operator tokens."""

@Export
class PlusOperator(OperatorToken):
	"""Token representing a plus operator: ``+``."""
	__KEYWORD__ = "+"

@Export
class MinusOperator(OperatorToken):
	"""Token representing a minus operator: ``-``."""
	__KEYWORD__ = "-"

@Export
class MultiplyOperator(OperatorToken):
	"""Token representing a multiply operator: ``*``."""
	__KEYWORD__ = "*"

@Export
class DivideOperator(OperatorToken):
	"""Token representing a divide operator: ``/``."""
	__KEYWORD__ = "/"

@Export
class PowerOperator(OperatorToken):
	"""Token representing a power operator: ``**``."""
	__KEYWORD__ = "**"

@Export
class ConcatOperator(OperatorToken):
	"""Token representing a concat operator: ``&``."""
	__KEYWORD__ = "&"

# Relational operatrors
# ----------------------------------------------------------
@Export
class RelationalOperator(OperatorToken):
	"""Base-class for all relational operator tokens."""

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
class DelimiterToken(SpecificVHDLToken):
	"""
	Token representing a delimiter sign in between list items.

	This token is usually created from a :class:`CharacterToken` with values ``,``
	or ``;``.
	"""


@Export
class EndToken(SpecificVHDLToken):
	"""
	Token representing an end of a statement.

	This token is usually created from a :class:`CharacterToken` with value ``;``.
	"""


@Export
class IdentifierToken(SpecificVHDLToken):
	"""
	Token representing an identifier.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@Export
class RepeatedIdentifierToken(IdentifierToken):
	"""
	Token representing a repeated identifier.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@Export
class SimpleNameToken(SpecificVHDLToken):
	pass


@Export
class LabelToken(SpecificVHDLToken):
	"""
	Token representing a label.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@Export
class RepeatedLabelToken(LabelToken):
	"""
	Token representing a repeated label.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


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
	"""Base-class for all comment keywords: ``--``, ``/*`` and ``*/``."""

@Export
class SingleLineCommentKeyword(CommentKeyword):
	"""Token representing a starting sequence for a single-line comment: ``--``."""
	__KEYWORD__ = "--"

@Export
class MultiLineCommentKeyword(CommentKeyword):
	"""Base-class for all tokens related to multi-line comments: ``/*`` and ``*/``."""

@Export
class MultiLineCommentStartKeyword(MultiLineCommentKeyword):
	"""Token representing a starting sequence for a multi-line comment: ``/*``."""
	__KEYWORD__ = "/*"
@Export
class MultiLineCommentEndKeyword(MultiLineCommentKeyword):
	"""Token representing a closing sequence for a multi-line comment: ``*/``."""
	__KEYWORD__ = "*/"

@Export
class AssignmentKeyword(MultiCharKeyword):
	"""Base-class for all assignment keywords: ``:=`` and ``<=``."""

@Export
class VariableAssignmentKeyword(AssignmentKeyword):
	"""Token representing a variable assignment: ``:=``."""
	__KEYWORD__ = ":="

@Export
class SignalAssignmentKeyword(AssignmentKeyword):
	"""Token representing a signal assignment: ``<=``."""
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

	def __init__(self, wordToken : WordToken):
		if (not (isinstance(wordToken, WordToken) and (wordToken <= self.__KEYWORD__))):
			raise TokenizerException("Expected keyword {0}.".format(self.__KEYWORD__.upper()), wordToken)
		super().__init__(wordToken.PreviousToken, self.__KEYWORD__, wordToken.Start, wordToken.End)

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
	"""Reserved word 'abs' for unary operator *absolute value*."""
	__KEYWORD__ = "abs"

@Export
class AccessKeyword(KeywordToken):
	"""Reserved word 'access' to defined access types."""
	__KEYWORD__ = "access"

@Export
class AfterKeyword(KeywordToken):
	"""Reserved word 'after'."""
	__KEYWORD__ = "after"

@Export
class AliasKeyword(KeywordToken):
	"""Reserved word 'alias' to declare aliases."""
	__KEYWORD__ = "alias"

@Export
class AllKeyword(KeywordToken):
	"""Reserved word 'all'."""
	__KEYWORD__ = "all"

@Export
class AndKeyword(LogicalOperator):
	"""Reserved word 'and' for binary logical operator *and*."""
	__KEYWORD__ = "and"

@Export
class ArchitectureKeyword(KeywordToken):
	"""Reserved word 'architecture' to define architectures."""
	__KEYWORD__ = "architecture"

@Export
class ArrayKeyword(KeywordToken):
	"""Reserved word 'array' to define array types."""
	__KEYWORD__ = "array"

@Export
class AssertKeyword(KeywordToken):
	"""Reserved word 'assert' for *assert*-statements."""
	__KEYWORD__ = "assert"

@Export
class AttributeKeyword(KeywordToken):
	"""Reserved word 'attribute'."""
	__KEYWORD__ = "attribute"

@Export
class BeginKeyword(KeywordToken):
	"""Reserved word 'begin' to distinguish declarative regions from statements regions."""
	__KEYWORD__ = "begin"

@Export
class BlockKeyword(KeywordToken):
	"""Reserved word 'block' for *block*-statements."""
	__KEYWORD__ = "block"

@Export
class BodyKeyword(KeywordToken):
	"""Reserved word 'body' to distinguish declarations from implementations (bodies)."""
	__KEYWORD__ = "body"

@Export
class BufferKeyword(KeywordToken):
	"""Reserved word 'buffer' for mode *buffer*."""
	__KEYWORD__ = "buffer"

@Export
class BusKeyword(KeywordToken):
	"""Reserved word 'bus'."""
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
