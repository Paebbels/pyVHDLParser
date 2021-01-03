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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
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
from pydecor.decorators         import export

from pyVHDLParser.Token import Token, WordToken, VHDLToken, CharacterToken
from pyVHDLParser.Token.Parser  import TokenizerException

__all__ = []
__api__ = __all__


@export
class SpecificVHDLToken(VHDLToken):
	"""Base-class for all specific tokens.

	Simple token will be converted to specific tokens while parsing.
	The internal data is copied, and the original token is replaced by this token.
	"""

	def __init__(self, token: Token):
		"""
		Initialize a specific token, by copying the simple token's data and link
		this new token to the previous token as a replacement.
		"""
		super().__init__(token.PreviousToken, token.Value, token.Start, token.End)


@export
class BoundaryToken(SpecificVHDLToken):
	"""
	Token representing a boundary between (reserved) words.

	In many cases, a :class:`SpaceToken`, :class:`CommentToken`,
	:class:`LinebreakToken` or :class:`CharacterToken` becomes a BoundaryToken.
	"""

# ==============================================================================
# Bracket tokens: (), [], {}, <>
# ==============================================================================
@export
class BracketToken(SpecificVHDLToken):
	"""Base-class for all bracket tokens: ``(``, ``)``, ``[``, ``]``, ``{``, ``}``, ``<`` and ``>``."""

# Round bracket / parenthesis / ()
# ----------------------------------------------------------
@export
class RoundBracketToken(BracketToken):
	"""Base-class for all round bracket tokens: ``(`` and ``)``."""

@export
class OpeningRoundBracketToken(RoundBracketToken):
	"""Token representing an opening round bracket: ``(``."""

@export
class ClosingRoundBracketToken(RoundBracketToken):
	"""Token representing a closing round bracket: ``)``."""

# Square bracket / []
# ----------------------------------------------------------
@export
class SquareBracketToken(BracketToken):
	"""Base-class for all square bracket tokens: ``[`` and ``]``."""

@export
class OpeningSquareBracketToken(SquareBracketToken):
	"""Token representing an square round bracket: ``[``."""

@export
class ClosingSquareBracketToken(SquareBracketToken):
	"""Token representing a closing square bracket: ``]``."""

# Curly bracket / brace / curved bracket / {}
# ----------------------------------------------------------
@export
class CurlyBracketToken(BracketToken):
	"""Base-class for all curly bracket tokens: ``{`` and ``}``."""

@export
class OpeningCurlyBracketToken(CurlyBracketToken):
	"""Token representing an opening curly bracket: ``{``."""

@export
class ClosingCurlyBracketToken(CurlyBracketToken):
	"""Token representing a closing curly bracket: ``}``."""

# Angle bracket / arrow bracket / <>
# ----------------------------------------------------------
@export
class AngleBracketToken(BracketToken):
	"""Base-class for all angle bracket tokens: ``<`` and ``>``."""

@export
class OpeningAngleBracketToken(AngleBracketToken):
	"""Token representing an opening angle bracket: ``<``."""

@export
class ClosingAngleBracketToken(AngleBracketToken):
	"""Token representing a closing angle bracket: ``>``."""

# ==============================================================================
# Operator tokens: +, -, *, /, **, &
# ==============================================================================
@export
class OperatorToken(SpecificVHDLToken):
	"""Base-class for all operator tokens."""

@export
class PlusOperator(OperatorToken):
	"""Token representing a plus operator: ``+``."""
	__KEYWORD__ = "+"

@export
class MinusOperator(OperatorToken):
	"""Token representing a minus operator: ``-``."""
	__KEYWORD__ = "-"

@export
class MultiplyOperator(OperatorToken):
	"""Token representing a multiply operator: ``*``."""
	__KEYWORD__ = "*"

@export
class DivideOperator(OperatorToken):
	"""Token representing a divide operator: ``/``."""
	__KEYWORD__ = "/"

@export
class PowerOperator(OperatorToken):
	"""Token representing a power operator: ``**``."""
	__KEYWORD__ = "**"

@export
class ConcatOperator(OperatorToken):
	"""Token representing a concat operator: ``&``."""
	__KEYWORD__ = "&"

# Relational operatrors
# ----------------------------------------------------------
@export
class RelationalOperator(OperatorToken):
	"""Base-class for all relational operator tokens."""

@export
class EqualOperator(RelationalOperator):
	__KEYWORD__ = "="
@export
class UnequalOperator(RelationalOperator):
	__KEYWORD__ = "/="
@export
class LessThanOperator(RelationalOperator):
	__KEYWORD__ = "<"
@export
class LessThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = "<="
@export
class GreaterThanOperator(RelationalOperator):
	__KEYWORD__ = ">"
@export
class GreaterThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = ">="
@export
class MatchingEqualOperator(RelationalOperator):
	__KEYWORD__ = "?="
@export
class MatchingUnequalOperator(RelationalOperator):
	__KEYWORD__ = "?/="
@export
class MatchingLessThanOperator(RelationalOperator):
	__KEYWORD__ = "?<"
@export
class MatchingLessThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = "?<="
@export
class MatchingGreaterThanOperator(RelationalOperator):
	__KEYWORD__ = "?>"
@export
class MatchingGreaterThanOrEqualOperator(RelationalOperator):
	__KEYWORD__ = "?>="


@export
class DelimiterToken(SpecificVHDLToken):
	"""
	Token representing a delimiter sign in between list items.

	This token is usually created from a :class:`CharacterToken` with values ``,``
	or ``;``.
	"""


@export
class EndToken(SpecificVHDLToken):
	"""
	Token representing an end of a statement.

	This token is usually created from a :class:`CharacterToken` with value ``;``.
	"""


@export
class IdentifierToken(SpecificVHDLToken):
	"""
	Token representing an identifier.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@export
class RepeatedIdentifierToken(IdentifierToken):
	"""
	Token representing a repeated identifier.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@export
class SimpleNameToken(SpecificVHDLToken):
	pass


@export
class LabelToken(SpecificVHDLToken):
	"""
	Token representing a label.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@export
class RepeatedLabelToken(LabelToken):
	"""
	Token representing a repeated label.

	This token is usually created from a :class:`WordToken` or :class:`ExtendedIdentifierToken`.
	"""


@export
class MultiCharKeyword(VHDLToken):
	__KEYWORD__ = None

	def __init__(self, characterToken: CharacterToken):
		super().__init__(characterToken.PreviousToken, self.__KEYWORD__, characterToken.Start, characterToken.End)

	def __str__(self) -> str:
		return "<{name: <50} '{value}' at {pos!r}>".format(
			name=self.__class__.__name__[:-7],
			value=self.__KEYWORD__,
			pos=self.Start
		)


@export
class CommentKeyword(MultiCharKeyword):
	"""Base-class for all comment keywords: ``--``, ``/*`` and ``*/``."""

@export
class SingleLineCommentKeyword(CommentKeyword):
	"""Token representing a starting sequence for a single-line comment: ``--``."""
	__KEYWORD__ = "--"

@export
class MultiLineCommentKeyword(CommentKeyword):
	"""Base-class for all tokens related to multi-line comments: ``/*`` and ``*/``."""

@export
class MultiLineCommentStartKeyword(MultiLineCommentKeyword):
	"""Token representing a starting sequence for a multi-line comment: ``/*``."""
	__KEYWORD__ = "/*"
@export
class MultiLineCommentEndKeyword(MultiLineCommentKeyword):
	"""Token representing a closing sequence for a multi-line comment: ``*/``."""
	__KEYWORD__ = "*/"

@export
class AssignmentKeyword(MultiCharKeyword):
	"""Base-class for all assignment keywords: ``:=`` and ``<=``."""

@export
class VariableAssignmentKeyword(AssignmentKeyword):
	"""Token representing a variable assignment: ``:=``."""
	__KEYWORD__ = ":="

@export
class SignalAssignmentKeyword(AssignmentKeyword):
	"""Token representing a signal assignment: ``<=``."""
	__KEYWORD__ = "<="

@export
class AssociationKeyword(MultiCharKeyword):
	pass
@export
class MapAssociationKeyword(AssociationKeyword):
	__KEYWORD__ = "=>"
@export
class SignalAssociationKeyword(AssociationKeyword):
	__KEYWORD__ = "<=>"


@export
class KeywordToken(VHDLToken):
	__KEYWORD__ : str

	def __init__(self, wordToken: WordToken):
		if (not (isinstance(wordToken, WordToken) and (wordToken <= self.__KEYWORD__))):
			raise TokenizerException("Expected keyword {0}.".format(self.__KEYWORD__.upper()), wordToken)
		super().__init__(wordToken.PreviousToken, self.__KEYWORD__, wordToken.Start, wordToken.End)

	def __str__(self) -> str:
		return "<{name: <50}  {value:.<59} at {pos!r}>".format(
				name=self.__class__.__name__,
				value="'" + self.Value + "'  ",
				pos=self.Start
			)

@export
class DirectionKeyword(KeywordToken):
	pass

@export
class Operator(KeywordToken):
	pass
@export
class LogicalOperator(Operator):
	pass
@export
class MiscellaneousOperator(Operator):
	pass
@export
class ShiftOperator(Operator):
	pass

@export
class AbsKeyword(KeywordToken):
	"""Reserved word 'abs' for unary operator *absolute value*."""
	__KEYWORD__ = "abs"

@export
class AccessKeyword(KeywordToken):
	"""Reserved word 'access' to defined access types."""
	__KEYWORD__ = "access"

@export
class AfterKeyword(KeywordToken):
	"""Reserved word 'after'."""
	__KEYWORD__ = "after"

@export
class AliasKeyword(KeywordToken):
	"""Reserved word 'alias' to declare aliases."""
	__KEYWORD__ = "alias"

@export
class AllKeyword(KeywordToken):
	"""Reserved word 'all'."""
	__KEYWORD__ = "all"

@export
class AndKeyword(LogicalOperator):
	"""Reserved word 'and' for binary logical operator *and*."""
	__KEYWORD__ = "and"

@export
class ArchitectureKeyword(KeywordToken):
	"""Reserved word 'architecture' to define architectures."""
	__KEYWORD__ = "architecture"

@export
class ArrayKeyword(KeywordToken):
	"""Reserved word 'array' to define array types."""
	__KEYWORD__ = "array"

@export
class AssertKeyword(KeywordToken):
	"""Reserved word 'assert' for *assert*-statements."""
	__KEYWORD__ = "assert"

@export
class AttributeKeyword(KeywordToken):
	"""Reserved word 'attribute'."""
	__KEYWORD__ = "attribute"

@export
class BeginKeyword(KeywordToken):
	"""Reserved word 'begin' to distinguish declarative regions from statements regions."""
	__KEYWORD__ = "begin"

@export
class BlockKeyword(KeywordToken):
	"""Reserved word 'block' for *block*-statements."""
	__KEYWORD__ = "block"

@export
class BodyKeyword(KeywordToken):
	"""Reserved word 'body' to distinguish declarations from implementations (bodies)."""
	__KEYWORD__ = "body"

@export
class BufferKeyword(KeywordToken):
	"""Reserved word 'buffer' for mode *buffer*."""
	__KEYWORD__ = "buffer"

@export
class BusKeyword(KeywordToken):
	"""Reserved word 'bus'."""
	__KEYWORD__ = "bus"

@export
class CaseKeyword(KeywordToken):
	__KEYWORD__ = "case"
@export
class ComponentKeyword(KeywordToken):
	__KEYWORD__ = "component"
@export
class ConfigurationKeyword(KeywordToken):
	__KEYWORD__ = "configuration"
@export
class ConstantKeyword(KeywordToken):
	__KEYWORD__ = "constant"
@export
class ContextKeyword(KeywordToken):
	__KEYWORD__ = "context"
@export
class DefaultKeyword(KeywordToken):
	__KEYWORD__ = "default"
@export
class DisconnectKeyword(KeywordToken):
	__KEYWORD__ = "disconnect"
@export
class DowntoKeyword(DirectionKeyword):
	__KEYWORD__ = "downto"
@export
class ElseKeyword(KeywordToken):
	__KEYWORD__ = "else"
@export
class ElsIfKeyword(KeywordToken):
	__KEYWORD__ = "elsif"
@export
class EndKeyword(KeywordToken):
	__KEYWORD__ = "end"
@export
class EntityKeyword(KeywordToken):
	__KEYWORD__ = "entity"
@export
class ExitKeyword(KeywordToken):
	__KEYWORD__ = "exit"
@export
class FileKeyword(KeywordToken):
	__KEYWORD__ = "file"
@export
class ForKeyword(KeywordToken):
	__KEYWORD__ = "for"
@export
class ForceKeyword(KeywordToken):
	__KEYWORD__ = "force"
@export
class FunctionKeyword(KeywordToken):
	__KEYWORD__ = "function"
@export
class GenerateKeyword(KeywordToken):
	__KEYWORD__ = "generate"
@export
class GenericKeyword(KeywordToken):
	__KEYWORD__ = "generic"
@export
class GroupKeyword(KeywordToken):
	__KEYWORD__ = "group"
@export
class GuardedKeyword(KeywordToken):
	__KEYWORD__ = "guarded"
@export
class IfKeyword(KeywordToken):
	__KEYWORD__ = "if"
@export
class IsKeyword(KeywordToken):
	__KEYWORD__ = "is"
@export
class InKeyword(KeywordToken):
	__KEYWORD__ = "in"
@export
class InoutKeyword(KeywordToken):
	__KEYWORD__ = "inout"
@export
class ImpureKeyword(KeywordToken):
	__KEYWORD__ = "impure"
@export
class InertialKeyword(KeywordToken):
	__KEYWORD__ = "inertial"
@export
class LableKeyword(KeywordToken):
	__KEYWORD__ = "lable"
@export
class LibraryKeyword(KeywordToken):
	__KEYWORD__ = "library"
@export
class LinkageKeyword(KeywordToken):
	__KEYWORD__ = "linkage"
@export
class LiteralKeyword(KeywordToken):
	__KEYWORD__ = "literal"
@export
class LoopKeyword(KeywordToken):
	__KEYWORD__ = "loop"
@export
class MapKeyword(KeywordToken):
	__KEYWORD__ = "map"
@export
class NandKeyword(LogicalOperator):
	__KEYWORD__ = "nand"
@export
class NewKeyword(KeywordToken):
	__KEYWORD__ = "new"
@export
class NextKeyword(KeywordToken):
	__KEYWORD__ = "next"
@export
class NorKeyword(LogicalOperator):
	__KEYWORD__ = "nor"
@export
class NotKeyword(KeywordToken):
	__KEYWORD__ = "not"
@export
class NullKeyword(KeywordToken):
	__KEYWORD__ = "null"
@export
class OfKeyword(KeywordToken):
	__KEYWORD__ = "of"
@export
class OnKeyword(KeywordToken):
	__KEYWORD__ = "on"
@export
class OpenKeyword(KeywordToken):
	__KEYWORD__ = "open"
@export
class OrKeyword(LogicalOperator):
	__KEYWORD__ = "or"
@export
class OthersKeyword(KeywordToken):
	__KEYWORD__ = "others"
@export
class OutKeyword(KeywordToken):
	__KEYWORD__ = "out"
@export
class PackageKeyword(KeywordToken):
	__KEYWORD__ = "package"
@export
class ParameterKeyword(KeywordToken):
	__KEYWORD__ = "parameter"
@export
class PortKeyword(KeywordToken):
	__KEYWORD__ = "port"
@export
class PostponendKeyword(KeywordToken):
	__KEYWORD__ = "postponend"
@export
class ProcedureKeyword(KeywordToken):
	__KEYWORD__ = "procedure"
@export
class ProcessKeyword(KeywordToken):
	__KEYWORD__ = "process"
@export
class PropertyKeyword(KeywordToken):
	__KEYWORD__ = "property"
@export
class ProtectedKeyword(KeywordToken):
	__KEYWORD__ = "protected"
@export
class PureKeyword(KeywordToken):
	__KEYWORD__ = "pure"
@export
class RangeKeyword(KeywordToken):
	__KEYWORD__ = "range"
@export
class RecordKeyword(KeywordToken):
	__KEYWORD__ = "record"
@export
class RegisterKeyword(KeywordToken):
	__KEYWORD__ = "register"
@export
class RejectKeyword(KeywordToken):
	__KEYWORD__ = "reject"
@export
class ReleaseKeyword(KeywordToken):
	__KEYWORD__ = "release"
@export
class ReportKeyword(KeywordToken):
	__KEYWORD__ = "report"
@export
class ReturnKeyword(KeywordToken):
	__KEYWORD__ = "return"
@export
class RolKeyword(ShiftOperator):
	__KEYWORD__ = "rol"
@export
class RorKeyword(ShiftOperator):
	__KEYWORD__ = "ror"
@export
class SelectKeyword(KeywordToken):
	__KEYWORD__ = "select"
@export
class SequenceKeyword(KeywordToken):
	__KEYWORD__ = "sequence"
@export
class SeverityKeyword(KeywordToken):
	__KEYWORD__ = "severity"
@export
class SharedKeyword(KeywordToken):
	__KEYWORD__ = "shared"
@export
class SignalKeyword(KeywordToken):
	__KEYWORD__ = "signal"
@export
class SlaKeyword(ShiftOperator):
	__KEYWORD__ = "sla"
@export
class SllKeyword(ShiftOperator):
	__KEYWORD__ = "sll"
@export
class SraKeyword(ShiftOperator):
	__KEYWORD__ = "sra"
@export
class SrlKeyword(ShiftOperator):
	__KEYWORD__ = "srl"
@export
class SubtypeKeyword(KeywordToken):
	__KEYWORD__ = "subtype"
@export
class ThenKeyword(KeywordToken):
	__KEYWORD__ = "then"
@export
class ToKeyword(DirectionKeyword):
	__KEYWORD__ = "to"
@export
class TransportKeyword(KeywordToken):
	__KEYWORD__ = "transport"
@export
class TypeKeyword(KeywordToken):
	__KEYWORD__ = "type"
@export
class UnitsKeyword(KeywordToken):
	__KEYWORD__ = "units"
@export
class UntilKeyword(KeywordToken):
	__KEYWORD__ = "until"
@export
class UseKeyword(KeywordToken):
	__KEYWORD__ = "use"
@export
class UnbufferedKeyword(KeywordToken):
	__KEYWORD__ = "unbuffered"
@export
class VariableKeyword(KeywordToken):
	__KEYWORD__ = "variable"
@export
class VunitKeyword(KeywordToken):
	__KEYWORD__ = "vunit"
@export
class WaitKeyword(KeywordToken):
	__KEYWORD__ = "wait"
@export
class WhenKeyword(KeywordToken):
	__KEYWORD__ = "when"
@export
class WhileKeyword(KeywordToken):
	__KEYWORD__ = "while"
@export
class WithKeyword(KeywordToken):
	__KEYWORD__ = "with"
@export
class XorKeyword(LogicalOperator):
	__KEYWORD__ = "xor"
@export
class XnorKeyword(LogicalOperator):
	__KEYWORD__ = "xnor"
