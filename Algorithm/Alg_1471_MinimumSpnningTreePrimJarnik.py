#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1425_Graph import Graph
from Alg_0952_AdaptableHeapPriorityQueue import AdaptableHeapPriorityQueue
from Alg_0934_PriorityQueueHeapArray import HeapPriorityQueue

def MST_PrimJarnik(g):
	'''Conpute a minium spanning tree of weighted graph g.
	Return a list of edges that comprise the MST (in arbitriary order).
	'''
	d = {}
	tree = []
	pq = AdaptableHeapPriorityQueue()
	pqlocator = {}
	for v in g.vertices():
		if len(d) == 0:
			d[v] = 0
		else:
			d[v] = float('inf')
		pqlocator[v] = pq.add(d[v], (v, None))
	
	while not pq.is_empty():
		key, value = pq.remove_min()
		u, edge = value
		del pqlocator[u]
		if edge is not None:
			tree.append(edge)
		for link in g.incident_edges(u):
			v = link.opposite(u)
			if v in pqlocator:
				wgt = link.element()
				if wgt < d[v]:
					d[v] = wgt
					pq.update(pqlocator[v], d[v], (v, link))
	return tree

def MST_Kruskal(g):
	'''Compute a minimum spanning tree of a graph using Kruskal's algorithm.
	Return a list of edges that comprise the MST.
	The elements of graph's edge are assumed to be weighted.
	'''
	tree = []
	pq = HeapPriorityQueue()
	forest = Partition()
	position = {}
	for v in g.vertices():
		position[v] = forest.make_group(v)
	for e in g.edges():
		pq.add(e.element(), e)
	size = g.vertex_count()
	while len(tree) != size-1 and not pq.is_empty():
		weight, edge = pq.remove_min()
		u, v = edge.endpoints()
		a = forest.find(position[u])
		b = forest.find(position[v])
		if a != b:
			tree.append(edge)
			forest.union(a, b)
	return tree

class Partition(object):
	'''Union-find structure for maintaining disjoint sets.'''
	class Position(object):
		__slots__ = '_container', '_element', '_size', '_parent'
		def __init__(self, container, element):
			'''Create a new position that is the leader of its one group.'''
			self._container = container
			self._element = element
			self._size = 1
			self._parent = self

		def element(self):
			'''Return element storted at this position.'''
			return self._element

	def make_group(self, e):
		'''Makes a new group containing element e, and returns its Position.'''
		return self.Position(self, e)

	def find(self, p):
		'''Find the group containging p and return the position of its leader.'''
		if p._parent != p:
			p._parent = self.find(p._parent)
		return p._parent

	def union(self, p, q):
		'''Merge the group containing elements p and q (if distinct).'''
		a = self.find(p)
		b = self.find(q)
		if a is not b:
			if a._size > b._size:
				b._parent = a
				a._size += b._size
			else:
				a._parent = b
				b._size += a._size

if __name__ == '__main__':
	g = Graph(False)
	print('is_directed', g.is_directed())
	# sub-graph
	prev_v = None  # prev vertex
	for i in range(10):
		v = g.insert_vertex(i)  # vertex
		if prev_v is not None:
			dist = i+10
			g.insert_edge(v, prev_v, dist)  # vertex
		prev_v = v
	# sub-graph
	bridge_v = v
	prev_v = None  # prev vertex
	for i in range(100, 110):
		v = g.insert_vertex(i)  # vertex
		if prev_v is not None:
			dist = i+10
			g.insert_edge(v, prev_v, dist)  # vertex
		prev_v = v
	g.insert_edge(v, bridge_v, 100)  # vertex

	for x in g.vertices():
		for y in g.incident_edges(x):
			print(x.element(), '<->',y.opposite(x).element(), 'weight', y.element(), )

	# test
	tree = MST_PrimJarnik(g)
	for edge in tree:
		print(edge.element())

	tree = MST_Kruskal(g)
	for edge in tree:
		print(edge.element())
