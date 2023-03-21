from pyTooling.Graph import Graph, Subgraph, Vertex
from pyTooling.Graph.GraphML import GraphMLDocument

from pyVHDLParser.Token import Token


class GraphML:
	_graph: Graph

	def __init__(self):
		self._graph = Graph(name="Streams")

	def AddTokenStream(self, firstToken: Token):
		subgraph = Subgraph(name="TokenStream", graph=self._graph)

		firstVertex = Vertex(vertexID=id(firstToken), value=f"{firstToken!s}", subgraph=subgraph)
		firstVertex["order"] = 0
		firstVertex["kind"] = type(firstToken).__name__

		tokenIterator = firstToken.GetIterator(inclusiveStopToken=False)
		for tokenID, token in enumerate(tokenIterator, start=1):
			vertex = Vertex(vertexID=id(token), value=f"{token!s}", subgraph=subgraph)
			vertex["order"] = tokenID
			vertex["kind"] = type(token).__name__

		tokenIterator = token.GetIterator()
		lastToken = next(tokenIterator)
		lastVertex = Vertex(vertexID=id(lastToken), value=f"{lastToken!s}", subgraph=subgraph)
		lastVertex["order"] = tokenID + 1
		lastVertex["kind"] = type(lastToken).__name__

		firstVertex.EdgeToVertex(subgraph._verticesWithID[id(firstToken.NextToken)], edgeID=f"n0_next")
		tokenIterator = firstToken.GetIterator(inclusiveStopToken=False)
		for tokenID, token in enumerate(tokenIterator, start=1):
			vertex = subgraph._verticesWithID[id(token)]
			vertex.EdgeToVertex(subgraph._verticesWithID[id(token.PreviousToken)], edgeID=f"n{tokenID}_prev")
			vertex.EdgeToVertex(subgraph._verticesWithID[id(token.NextToken)], edgeID=f"n{tokenID}_next")
		tokenIterator = token.GetIterator()
		lastToken = next(tokenIterator)
		lastVertex = subgraph._verticesWithID[id(lastToken)]
		lastVertex.EdgeToVertex(subgraph._verticesWithID[id(lastToken.PreviousToken)], edgeID=f"n{tokenID + 1}_prev")

	def WriteDocument(self, path):
		graphMLDocument = GraphMLDocument("Streams")
		graphMLDocument.FromGraph(self._graph)
		graphMLDocument.WriteToFile(path)
