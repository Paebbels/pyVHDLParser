from typing import Dict, List

from antlr4 import CommonTokenStream, Token as antlrToken

from .. import SourceCodePosition
from ..Token import Token, StartOfDocumentToken, EndOfDocumentToken, FusedCharacterToken, IntegerLiteralToken, \
	IndentationToken, LinebreakToken, WhitespaceToken, SingleLineCommentToken, MultiLineCommentToken, CharacterToken, \
	StringLiteralToken, BitStringLiteralToken
from ..Token.Keywords import *

from .VHDLLexer import VHDLLexer


class ANTLR2Token:
	TRANSLATE: Dict[int, type(KeywordToken)] = {
		VHDLLexer.OP_ABS: AbsOperator,
		# VHDLLexer.KW_ACROSS: AcrossKeyword,
		VHDLLexer.KW_ACCESS: AccessKeyword,
		VHDLLexer.KW_AFTER: AfterKeyword,
		VHDLLexer.KW_ALIAS: AliasKeyword,
		VHDLLexer.KW_ALL: AllKeyword,
		VHDLLexer.OP_AND: AndOperator,
		VHDLLexer.KW_ARCHITECTURE: ArchitectureKeyword,
		VHDLLexer.KW_ARRAY: ArrayKeyword,
		VHDLLexer.KW_ASSERT: AssertKeyword,
		VHDLLexer.KW_ATTRIBUTE: AttributeKeyword,
		# VHDLLexer.KW_PSL_ASSUME: AssumeKeyword,
		# VHDLLexer.KW_AMS_ACROSS: AcrossKeyword,
		VHDLLexer.KW_BEGIN: BeginKeyword,
		VHDLLexer.KW_BLOCK: BlockKeyword,
		VHDLLexer.KW_BODY: BodyKeyword,
		VHDLLexer.KW_BUFFER: BufferKeyword,
		VHDLLexer.KW_BUS: BusKeyword,
		# VHDLLexer.KW_BREAK: BreakKeyword,
		VHDLLexer.KW_CASE: CaseKeyword,
		VHDLLexer.KW_COMPONENT: ComponentKeyword,
		VHDLLexer.KW_CONFIGURATION: ConfigurationKeyword,
		VHDLLexer.KW_CONSTANT: ConstantKeyword,
		VHDLLexer.KW_CONTEXT: ContextKeyword,
		# VHDLLexer.KW_PSL_COVER: CoverKeyword,
		VHDLLexer.KW_DEFAULT: DefaultKeyword,
		VHDLLexer.KW_DISCONNECT: DisconnectKeyword,
		VHDLLexer.KW_DOWNTO: DowntoKeyword,
		VHDLLexer.KW_ELSE: ElseKeyword,
		VHDLLexer.KW_ELSIF: ElsIfKeyword,
		VHDLLexer.KW_END: EndKeyword,
		VHDLLexer.KW_ENTITY: EntityKeyword,
		VHDLLexer.KW_EXIT: ExitKeyword,
		VHDLLexer.KW_FILE: FileKeyword,
		VHDLLexer.KW_FOR: ForKeyword,
		VHDLLexer.KW_FORCE: ForceKeyword,
		VHDLLexer.KW_FUNCTION: FunctionKeyword,
		VHDLLexer.KW_GENERATE: GenerateKeyword,
		VHDLLexer.KW_GENERIC: GenericKeyword,
		# VHDLLexer.KW_GROUP: GroupKeyword,
		VHDLLexer.KW_GUARDED: GuardedKeyword,
		VHDLLexer.KW_IF: IfKeyword,
		VHDLLexer.KW_IMPURE: ImpureKeyword,
		VHDLLexer.KW_IN: InKeyword,
		VHDLLexer.KW_INERTIAL: InertialKeyword,
		VHDLLexer.KW_INOUT: InoutKeyword,
		VHDLLexer.KW_IS: IsKeyword,
		VHDLLexer.KW_LABEL: LabelKeyword,
		VHDLLexer.KW_LIBRARY: LibraryKeyword,
		VHDLLexer.KW_LINKAGE: LinkageKeyword,
		VHDLLexer.KW_LOOP: LoopKeyword,
		VHDLLexer.KW_PSL_LITERAL: LiteralKeyword,
		# VHDLLexer.KW_LIMIT: LimitKeyword,
		VHDLLexer.KW_MAP: MapKeyword,
		VHDLLexer.OP_MOD: ModuloOperator,
		VHDLLexer.OP_NAND: NandOperator,
		VHDLLexer.KW_NEW: NewKeyword,
		VHDLLexer.KW_NEXT: NextKeyword,
		VHDLLexer.OP_NOR: NorOperator,
		VHDLLexer.OP_NOT: NotOperator,
		VHDLLexer.KW_NULL: NullKeyword,
		# VHDLLexer.KW_NATURE: NatureKeyword,
		# VHDLLexer.KW_NOISE: NoiseKeyword,
		VHDLLexer.KW_OF: OfKeyword,
		VHDLLexer.KW_ON: OnKeyword,
		VHDLLexer.KW_OPEN: OpenKeyword,
		VHDLLexer.OP_OR: OrOperator,
		VHDLLexer.KW_OTHERS: OthersKeyword,
		VHDLLexer.KW_OUT: OutKeyword,
		VHDLLexer.KW_PACKAGE: PackageKeyword,
		VHDLLexer.KW_PARAMETER: ParameterKeyword,
		VHDLLexer.KW_PORT: PortKeyword,
		VHDLLexer.KW_POSTPONED: PostponedKeyword,
		VHDLLexer.KW_PRIVATE: PrivateKeyword,
		VHDLLexer.KW_PROCEDURE: ProcedureKeyword,
		VHDLLexer.KW_PROCESS: ProcessKeyword,
		VHDLLexer.KW_PROTECTED: ProtectedKeyword,
		VHDLLexer.KW_PURE: PureKeyword,
		# VHDLLexer.KW_PROCEDURAL: ProceduralKeyword,
		# VHDLLexer.KW_QUANTITY: 'quantityKeyword,
		VHDLLexer.KW_RANGE: RangeKeyword,
		VHDLLexer.KW_RECORD: RecordKeyword,
		VHDLLexer.KW_REGISTER: RegisterKeyword,
		VHDLLexer.KW_REJECT: RejectKeyword,
		VHDLLexer.KW_RELEASE: ReleaseKeyword,
		VHDLLexer.OP_REM: RemainderOperator,
		VHDLLexer.KW_REPORT: ReportKeyword,
		VHDLLexer.KW_RETURN: ReturnKeyword,
		VHDLLexer.OP_ROL: RolOperator,
		VHDLLexer.OP_ROR: RorOperator,
		# VHDLLexer.KW_PSL_RESTRICT: RestrictKeyword,
		# VHDLLexer.KW_REFERENCE: ReferenceKeyword,
		VHDLLexer.KW_SELECT: SelectKeyword,
		VHDLLexer.KW_SEVERITY: SeverityKeyword,
		VHDLLexer.KW_SHARED: SharedKeyword,
		VHDLLexer.KW_SIGNAL: SignalKeyword,
		VHDLLexer.OP_SLA: SlaOperator,
		VHDLLexer.OP_SLL: SllOperator,
		VHDLLexer.OP_SRA: SraOperator,
		VHDLLexer.OP_SRL: SrlOperator,
		VHDLLexer.KW_SUBTYPE: SubtypeKeyword,
		# VHDLLexer.KW_PSL_STRONG: StrongKeyword,
		# VHDLLexer.KW_PSL_SEQUENCE: SequenceKeyword,
		# VHDLLexer.KW_SPECTRUM: SpectrumKeyword,
		# VHDLLexer.KW_SUBNATURE: SubnatureKeyword,
		VHDLLexer.KW_THEN: ThenKeyword,
		VHDLLexer.KW_TO: ToKeyword,
		VHDLLexer.KW_TRANSPORT: TransportKeyword,
		VHDLLexer.KW_TYPE: TypeKeyword,
		# VHDLLexer.KW_TERMINAL: TerminalKeyword,
		# VHDLLexer.KW_THROUGH: ThroughKeyword,
		# VHDLLexer.KW_TOLERANCE: ToleranceKeyword,
		VHDLLexer.KW_UNAFFECTED: UnaffectedKeyword,
		VHDLLexer.KW_UNITS: UnitsKeyword,
		VHDLLexer.KW_UNTIL: UntilKeyword,
		VHDLLexer.KW_USE: UseKeyword,
		VHDLLexer.KW_VARIABLE: VariableKeyword,
		VHDLLexer.KW_VIEW: ViewKeyword,
		# VHDLLexer.KW_PSL_VMODE: VModeKeyword,
		# VHDLLexer.KW_PSL_VPKG: VPackageKeyword,
		# VHDLLexer.KW_PSL_VPROP: VPropertyKeyword,,
		# VHDLLexer.KW_PSL_VUNIT: VunitKeyword,
		VHDLLexer.KW_WAIT: WaitKeyword,
		VHDLLexer.KW_WITH: WithKeyword,
		VHDLLexer.KW_WHEN: WhenKeyword,
		VHDLLexer.KW_WHILE: WhileKeyword,
		VHDLLexer.OP_XNOR: XnorOperator,
		VHDLLexer.OP_XOR: XorOperator,
	}

	def ConvertToTokenChain(self, tokenStream: CommonTokenStream) -> List[Token]:
		allTokens: List[Token] = []
		tokenIndex: int = -1

		lastToken = StartOfDocumentToken()
		while True:
			allTokens.append(lastToken)
			tokenIndex += 1

			aToken: antlrToken = tokenStream.get(tokenIndex)
			start = SourceCodePosition(aToken.line, aToken.column, -1)

			if aToken.type == antlrToken.EOF:
				allTokens.append(EndOfDocumentToken(lastToken, start))
				return allTokens

			try:
				tokenType = self.TRANSLATE[aToken.type]
				lastToken = tokenType(lastToken, aToken.text, start)
				continue

			except KeyError:
				pass

			if aToken.type in (
				VHDLLexer.TOK_SEMICOL, VHDLLexer.TOK_COMMA, VHDLLexer.TOK_COLON, VHDLLexer.TOK_DOT, VHDLLexer.TOK_LP,
				VHDLLexer.TOK_RP, VHDLLexer.TOK_LB, VHDLLexer.TOK_RB, VHDLLexer.OP_MINUS, VHDLLexer.OP_PLUS, VHDLLexer.OP_MUL,
				VHDLLexer.OP_DIV, VHDLLexer.TOK_BAR, VHDLLexer.TOK_TICK, VHDLLexer.OP_CONCAT, VHDLLexer.OP_CONDITION):
				lastToken = CharacterToken(lastToken, aToken.text, start)
			elif aToken.type in (
				VHDLLexer.TOK_SIG_ASSIGN, VHDLLexer.TOK_VAR_ASSIGN, VHDLLexer.TOK_BOX, VHDLLexer.OP_POW, VHDLLexer.OP_EQ,
				VHDLLexer.OP_NE, VHDLLexer.OP_LT, VHDLLexer.OP_LT, VHDLLexer.OP_GT, VHDLLexer.OP_GE, VHDLLexer.OP_IEQ,
				VHDLLexer.OP_INE, VHDLLexer.OP_ILT, VHDLLexer.OP_ILE, VHDLLexer.OP_IGT, VHDLLexer.OP_IGE, VHDLLexer.TOK_RARROW):
				lastToken = FusedCharacterToken(lastToken, aToken.text, start, start)
			elif aToken.type == VHDLLexer.LIT_IDENTIFIER:
				lastToken = IdentifierToken(lastToken, aToken.text, start)
			elif aToken.type == VHDLLexer.LIT_ABSTRACT:
				lastToken = IntegerLiteralToken(lastToken, aToken.text, start)
			elif aToken.type == VHDLLexer.LIT_CHARACTER:
				lastToken = CharacterToken(lastToken, aToken.text, start)
			elif aToken.type == VHDLLexer.LIT_STRING:
				lastToken = StringLiteralToken(lastToken, aToken.text, start, start)
			elif aToken.type == VHDLLexer.LIT_BIT_STRING:
				lastToken = BitStringLiteralToken(lastToken, aToken.text, start, start)
			elif aToken.type == VHDLLexer.WHITESPACE:
				tokenType = IndentationToken if isinstance(lastToken, LinebreakToken) else WhitespaceToken
				lastToken = tokenType(lastToken, aToken.text, start)
			elif aToken.type == VHDLLexer.LINEBREAK:
				lastToken = LinebreakToken(lastToken, aToken.text, start)
			elif aToken.type == VHDLLexer.COMMENT_LINE:
				lastToken = SingleLineCommentToken(lastToken, aToken.text, start)
			elif aToken.type == VHDLLexer.COMMENT_BLOCK:
				lastToken = MultiLineCommentToken(lastToken, aToken.text, start)
			else:
				raise Exception(
					f"Unknown ANTLR4 token type '{VHDLLexer.symbolicNames[aToken.type]}' ({aToken.type}) with value '{aToken.text}'.")
