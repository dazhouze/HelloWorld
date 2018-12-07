#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1425_Graph import Graph

def DFS(g, u, discovered):
	'''Performing of the undiscovered portion of Graph g starting at Vertex u.
	discovered is a dictionary mapping each vertex to the eduge that was used to
	dicover it during the DFS. (u should be "disvovered" prior to the call.)
	Newly discovered vertices will be added to the dictionary as a result.
	'''
	for e in g.incident_edges(u):
		v = e.opposite(u)
		if v not in discovered:
			discovered[v] = e
			DFS(g, v, discovered)

def construct_path(u, v, discovered):
	'''To identify the (directed) path leading from vertex u to v,
	if v is reachable from u.'''
	path = []
	if v in discovered:
		path.append(v)
		walk = v
		while walk is not u:
			e = discovered[walk]
			parent = e.opposite(walk)
			path.append(parent)
			walk = parent
		path.reverse()
	return path

def DFS_complelte(g):
	'''Perform DFS for entire graph and return forest as a dictionary.
	Result mapps each vertex v to the edge that was used to discover it.
	(Vertiecs that are roots of a DFS tree are mapped to None.)
	'''
	forest = {}
	for u in g.vertices():
		if u not in forest:
			forest[u] = None
			DFS(g, u, forest)
	return forest

if __name__ == '__main__':
	# construct Graph
	g = Graph()
	print('is_directed', g.is_directed())
	prev_v = None  # prev vertex
	root_v, tail_v = None, None
	for i in range(10):
		v = g.insert_vertex(i)  # vertex
		if prev_v is not None:
			g.insert_edge(v, prev_v, '%s->%s' % (v.element(), prev_v.element()))  # vertex
		if i == 0:
			root_v = v
		if i == 9:
			tail_v = v
		prev_v = v
	print('#edge(s):', g.edges_count(), '#vertex(ies):', g.vertex_count())

	# Depth first search
	result = {root_v: None}
	DFS(g, root_v, result)
	for x in result:
		print('DFS:', x.element())

	# Computing all Connected Components
	for i in range(10,15):
		v = g.insert_vertex(i)  # vertex
	forest = DFS_complelte(g)
	for e,v in forest.items():
		print('all vertices:', e.element(), v)
