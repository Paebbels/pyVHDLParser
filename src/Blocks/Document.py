from src.Blocks.Comment   import SingleLineCommentBlock, MultiLineCommentBlock
from src.Blocks.Common    import Block, EmptyLineBlock, IndentationBlock
from src.Blocks.Reference import Context
from src.Blocks.Reference.Library import LibraryBlock
from src.Blocks.Reference.Use import UseBlock
from src.Blocks.Sequential import Package
from src.Blocks.Structural import Entity
from src.Model.VHDLModel import Architecture
from src.Token.Parser import CharacterToken, SpaceToken, StringToken, ParserException, EndOfDocumentToken
from src.Token.Keywords import LinebreakToken, IndentationToken, LibraryKeyword, UseKeyword, ContextKeyword, EntityKeyword, ArchitectureKeyword, \
	PackageKeyword


class StartOfDocumentBlock(Block):
	def __init__(self, startToken):
		self._previousBlock =     None
		self._nextBlock =         None
		self.StartToken =         startToken
		self._endToken =          startToken
		self.MultiPart =          False

	def __len__(self):
		return 0

	def __str__(self):
		return "[StartOfDocumentBlock]"

	def RegisterStates(self):
		return [
			self.stateDocument
		]

	@classmethod
	def stateDocument(cls, parserState):
		token = parserState.Token
		errorMessage = "Expected keywords: architecture, context, entity, library, package, use."
		if isinstance(parserState.Token, CharacterToken):
			if (token == "\n"):
				parserState.NewToken =    LinebreakToken(token)
				parserState.NewBlock =    EmptyLineBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
				parserState.TokenMarker = parserState.NewToken
				return
			elif (token == "-"):
				parserState.PushState =   SingleLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
			elif (token == "/"):
				parserState.PushState =   MultiLineCommentBlock.statePossibleCommentStart
				parserState.TokenMarker = token
				return
		elif isinstance(token, SpaceToken):
			parserState.NewToken =      IndentationToken(token)
			parserState.NewBlock =      IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			return
		elif isinstance(token, StringToken):
			keyword = token.Value.lower()
			if (keyword == "library"):
				newToken = LibraryKeyword(token)
				parserState.PushState =   LibraryBlock.stateLibraryKeyword
			elif (keyword == "use"):
				newToken = UseKeyword(token)
				parserState.PushState =   UseBlock.stateUseKeyword
			elif (keyword == "context"):
				newToken = ContextKeyword(token)
				parserState.PushState =   Context.NameBlock.stateContextKeyword
			elif (keyword == "entity"):
				newToken = EntityKeyword(token)
				parserState.PushState =   Entity.NameBlock.stateEntityKeyword
			elif (keyword == "architecture"):
				newToken = ArchitectureKeyword(token)
				parserState.PushState =   Architecture.NameBlock.stateArchitectureKeyword
			elif (keyword == "package"):
				newToken = PackageKeyword(token)
				parserState.PushState =   Package.NameBlock.statePackageKeyword
			else:
				raise ParserException(errorMessage, token)

			parserState.NewToken =      newToken
			parserState.TokenMarker =   newToken
			return
		elif isinstance(token, EndOfDocumentToken):
			parserState.NewBlock =      EndOfDocumentBlock(token)
			raise StopIteration()
		else:  # tokenType
			raise ParserException(errorMessage, token)


class EndOfDocumentBlock(Block):
	def __init__(self, endToken):
		self._previousBlock =     None
		self._nextBlock =         None
		self.StartToken =         endToken
		self._endToken =          endToken
		self.MultiPart =          False

	def __len__(self):
		return 0

	def __str__(self):
		return "[EndOfDocumentBlock]"
