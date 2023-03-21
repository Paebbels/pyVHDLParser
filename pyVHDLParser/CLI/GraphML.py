from pyTooling.Graph import Graph, Subgraph, Vertex
from pyTooling.Graph.GraphML import GraphMLDocument
from pyVHDLParser.Blocks import Block

from pyVHDLParser.Token import Token


class GraphML:
	_graph: Graph

	def __init__(self):
		self._graph = Graph(name="Streams")

	def AddTokenStream(self, firstToken: Token):
		tokenStreamSubgraph = Subgraph(name="TokenStream", graph=self._graph)

		firstVertex = Vertex(vertexID=id(firstToken), value=f"{firstToken!s}", subgraph=tokenStreamSubgraph)
		firstVertex["order"] = 0
		firstVertex["kind"] = type(firstToken).__name__

		tokenIterator = firstToken.GetIterator(inclusiveStopToken=False)
		for tokenID, token in enumerate(tokenIterator, start=1):
			vertex = Vertex(vertexID=id(token), value=f"{token!s}", subgraph=tokenStreamSubgraph)
			vertex["order"] = tokenID
			vertex["kind"] = type(token).__name__

		tokenIterator = token.GetIterator()
		lastToken = next(tokenIterator)
		lastVertex = Vertex(vertexID=id(lastToken), value=f"{lastToken!s}", subgraph=tokenStreamSubgraph)
		lastVertex["order"] = tokenID + 1
		lastVertex["kind"] = type(lastToken).__name__

		firstVertex.EdgeToVertex(tokenStreamSubgraph._verticesWithID[id(firstToken.NextToken)], edgeID=f"n0_next")
		tokenIterator = firstToken.GetIterator(inclusiveStopToken=False)
		for tokenID, token in enumerate(tokenIterator, start=1):
			vertex = tokenStreamSubgraph._verticesWithID[id(token)]
			vertex.EdgeToVertex(tokenStreamSubgraph._verticesWithID[id(token.PreviousToken)], edgeID=f"n{tokenID}_prev")
			vertex.EdgeToVertex(tokenStreamSubgraph._verticesWithID[id(token.NextToken)], edgeID=f"n{tokenID}_next")
		tokenIterator = token.GetIterator()
		lastToken = next(tokenIterator)
		lastVertex = tokenStreamSubgraph._verticesWithID[id(lastToken)]
		lastVertex.EdgeToVertex(tokenStreamSubgraph._verticesWithID[id(lastToken.PreviousToken)], edgeID=f"n{tokenID + 1}_prev")

		return tokenStreamSubgraph

	def AddBlockStream(self, firstBlock: Block, tokenStreamSubgraph: Subgraph):
		blockStreamSubgraph = Subgraph(name="BlockStream", graph=self._graph)

		firstVertex = Vertex(vertexID=id(firstBlock), value=f"{firstBlock}", subgraph=blockStreamSubgraph)
		firstVertex["order"] = 0
		firstVertex["kind"] = type(firstBlock).__name__
		firstLink = firstVertex.LinkToVertex(tokenStreamSubgraph._verticesWithID[id(firstBlock.StartToken)])
		firstLink["kind"] = "block2token"

		blockIterator = firstBlock.GetIterator(inclusiveStopBlock=False)
		for blockID, block in enumerate(blockIterator, start=1):
			vertex = Vertex(vertexID=id(block), value=f"{block!s}", subgraph=blockStreamSubgraph)
			vertex["order"] = blockID
			vertex["kind"] = type(block).__name__
			startTokenLink = vertex.LinkToVertex(tokenStreamSubgraph._verticesWithID[id(block.StartToken)])
			startTokenLink["kind"] = "block2token"
			if block.EndToken is not block.StartToken:
				endTokenLink = vertex.LinkToVertex(tokenStreamSubgraph._verticesWithID[id(block.EndToken)])
				endTokenLink["kind"] = "block2token"

		blockIterator = block.GetIterator()
		lastBlock = next(blockIterator)
		lastVertex = Vertex(vertexID=id(lastBlock), value=f"{lastBlock}", subgraph=blockStreamSubgraph)
		lastVertex["order"] = blockID + 1
		lastVertex["kind"] = type(lastBlock).__name__
		lastLink = lastVertex.LinkToVertex(tokenStreamSubgraph._verticesWithID[id(lastBlock.StartToken)])
		lastLink["kind"] = "block2token"

		firstVertex.EdgeToVertex(blockStreamSubgraph._verticesWithID[id(firstBlock.NextBlock)], edgeID=f"n0_next")
		blockIterator = firstBlock.GetIterator(inclusiveStopBlock=False)
		for blockID, block in enumerate(blockIterator, start=1):
			vertex = blockStreamSubgraph._verticesWithID[id(block)]
			vertex.EdgeToVertex(blockStreamSubgraph._verticesWithID[id(block.PreviousBlock)], edgeID=f"n{blockID}_prev")
			vertex.EdgeToVertex(blockStreamSubgraph._verticesWithID[id(block.NextBlock)], edgeID=f"n{blockID}_next")
		blockIterator = block.GetIterator()
		lastBlock = next(blockIterator)
		lastVertex = blockStreamSubgraph._verticesWithID[id(lastBlock)]
		lastVertex.EdgeToVertex(blockStreamSubgraph._verticesWithID[id(lastBlock.PreviousBlock)], edgeID=f"n{blockID + 1}_prev")

		return blockStreamSubgraph

	def WriteDocument(self, path):
		graphMLDocument = GraphMLDocument("Streams")
		graphMLDocument.FromGraph(self._graph)
		graphMLDocument.WriteToFile(path)
