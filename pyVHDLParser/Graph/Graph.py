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
from enum import Enum


class NodeColors(Enum):
	Black = 0
	Gray = 1
	White = 2


class EdgeKinds(Enum):
	Unknown =  0
	Forward =  1
	Backward = 2
	Sideward = 3


class Graph:
	def __init__(self):
		self._nodes =           []
		self._roots =           []
		self._forwardEdges =    []
		self._backwardEdges =   []
		self._sidewardEdges =   []

	def AddNode(self, node):
		node.Graph =    self
		self._nodes.append(node)

	def __colorize(self, node):
		if (node.Color is NodeColors.Black):
			node.Color = NodeColors.Gray
			for edge in node._edges:
				edge.EdgeKind = self.__colorize(edge.End)
				if (edge.EdgeKind is EdgeKinds.Forward):
					self._forwardEdges.append(edge)
				elif (edge.EdgeKind is EdgeKinds.Backward):
					self._backwardEdges.append(edge)
				elif (edge.EdgeKind is EdgeKinds.Sideward):
					self._sidewardEdges.append(edge)

			return EdgeKinds.Forward
		elif (node.Color is NodeColors.Gray):
			return EdgeKinds.Backward
		elif (node.Color is NodeColors.White):
			return  EdgeKinds.Sideward

	def Colorize(self):
		for startNode in self._nodes:
			if startNode.Color is not NodeColors.White:
				self.__colorize(startNode)

	def GetTopologicalOrder(self):
		workList =    []
		resultList =  []

		for node in self._nodes:
			node.Weight = len(node._incomingEdges)
			if (node.Weight > 0):
				workList.append(node)

		while (len(workList) > 0):
			node = workList.pop()
			for edge in node._outgoingEdges:
				end = edge.End
				end.Weight -= 1
				if (end.Weight == 0):
					workList.append(end)

			resultList.append(node)

		return resultList

	def ClearColors(self):
		for node in self._nodes:
			node.Color = NodeColors.Black

	def ClearWeights(self):
		for node in self._nodes:
			node.Weight = 0


class Node:
	def __init__(self):
		self.Graph =          None
		self._outgoingEdges = []
		self._incomingEdges = []
		self.Weight =         0
		self.Color =          NodeColors.Black

	def DependsOn(self, node):
		edge = Edge(self.Graph, self, node)
		self._outgoingEdges.append(edge)
		node._incomingEdges.append(edge)


class Edge:
	def __init__(self, graph, start, end):
		self.Graph =    graph
		self.EdgeKind = EdgeKinds.Unknown
		self.Start =    start
		self.End =      end
