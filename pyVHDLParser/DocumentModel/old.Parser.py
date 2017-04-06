# def MultiPartIterator(currentGroup, groupIterator):
# 	def __Generator(currentGroup, groupIterator):
# 		groupType = type(currentGroup)
#
# 		for token in currentGroup:
# 			yield token
# 		for group in groupIterator:
# 			if isinstance(group, groupType):
# 				for token in group:
# 					yield token
# 				if (not group.MultiPart):
# 					break
#
# 	if currentGroup.MultiPart:
# 		return iter(__Generator(currentGroup, groupIterator))
# 	else:
# 		return iter(currentGroup)
