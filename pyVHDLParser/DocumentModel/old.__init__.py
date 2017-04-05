

class _GroupIterator:
	def __init__(self, parserState, groupGenerator: Iterator):
		self._parserState =     parserState
		self._groupIterator =   iter(FastForward(groupGenerator))

	def __iter__(self):
		return self

	def __next__(self):
		nextGroup = self._groupIterator.__next__()
		self._parserState.CurrentGroup = nextGroup
		return nextGroup

class GroupToModelParser:


	@staticmethod
	def _TokenGenerator(currentGroup, groupIterator):
		groupType = type(currentGroup)

		for token in currentGroup:
			yield token
		for group in groupIterator:
			if isinstance(group, groupType):
				for token in group:
					yield token
				if (not group.MultiPart):
					break



		def __iter__(self):
			if self.CurrentGroup.MultiPart:
				return iter(GroupToModelParser._TokenGenerator(self.CurrentGroup, self.GroupIterator))
			else:
				return iter(self.CurrentGroup)



