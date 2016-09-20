from src.Blocks.Base      import Block
from src.Blocks.Common    import IndentationBlock
from src.Token.Parser     import CharacterToken, SpaceToken
from src.Token.Keywords   import IndentationToken, SingleLineCommentKeyword, MultiLineCommentStartKeyword, MultiLineCommentEndKeyword


class CommentBlock(Block):
	pass

class SingleLineCommentBlock(CommentBlock):
	def RegisterStates(self):
		return [
			self.statePossibleCommentStart,
			self.stateConsumeComment
		]

	@classmethod
	def statePossibleCommentStart(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "-")):
			parserState.NewToken =    SingleLineCommentKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return

		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateConsumeComment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken)and (token == "\n")):
			parserState.NewBlock =    SingleLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.Token)
			parserState.NextState =   cls.stateLinebreak
			return
		else:
			pass	# consume everything until "\n"

	@classmethod
	def stateLinebreak(cls, parserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken = IndentationToken(token)
			parserState.NewBlock = IndentationBlock(parserState.LastBlock, parserState.NewToken, endToken=parserState.NewToken)
			parserState.Pop()
		else:
			parserState.Pop()
			if (parserState.TokenMarker is None):
				# print("  new marker: None -> {0!s}".format(token))
				parserState.TokenMarker = token
			# print("  re-issue: {0!s}".format(parserState))
			parserState.NextState(parserState)


class MultiLineCommentBlock(CommentBlock):
	def RegisterStates(self):
		return [
			self.statePossibleCommentStart,
			self.stateConsumeComment,
			self.statePossibleCommentEnd
		]

	@classmethod
	def statePossibleCommentStart(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "*")):
			parserState.NewToken =    MultiLineCommentStartKeyword(parserState.TokenMarker)
			parserState.TokenMarker = parserState.NewToken
			parserState.NextState =   cls.stateConsumeComment
			return

		raise NotImplementedError("State=PossibleCommentStart: {0!r}".format(token))

	@classmethod
	def stateConsumeComment(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "*")):
			parserState.PushState =   cls.statePossibleCommentEnd
			parserState.TokenMarker = token
			return
		else:
			pass  # consume everything until "*/"

	@classmethod
	def statePossibleCommentEnd(cls, parserState):
		token = parserState.Token
		if (isinstance(token, CharacterToken) and (token == "/")):
			parserState.NewToken = MultiLineCommentEndKeyword(parserState.TokenMarker)
			parserState.Pop()
			parserState.NewBlock = MultiLineCommentBlock(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.Pop()
			return
		else:
			parserState.Pop()
