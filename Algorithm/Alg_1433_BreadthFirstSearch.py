#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1425_Graph import Graph

def BFS(g, s, discovered):
	'''Perform BFS of undiscovered portion of Graph g stranding at Vertex s.
	discovered is a dictionary mapping each vertex to the edge that was used to
	dicover it during the BFS (s should be maaped to None prior to the call).
	Newly discovered vertices witll be added to the dictionary as a result.
	'''
	level = [s]
	while len(level) > 0:
		next_level = []
		for u in level:
			for e in g.incident_edges(u):
				v = e.opposite(u)
				if v not in discovered:
					discovered[v] = e
					next_level.append(v)
		level = next_level

if __name__ == '__main__':
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
	for i in range(10,15):
		v = g.insert_vertex(i)  # vertex
	print('#edge(s):', g.edges_count(), '#vertex(ies):', g.vertex_count())
	result = {tail_v: None}
	BFS(g, tail_v, result)
	for v in result.items():
		print(v[0].element())  # vertex
