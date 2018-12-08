#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1425_Graph import Graph

def topological_sort(g):
	'''Return a list of verticies of directed acycclic graph g in topological order.
	If graph g has a cycle, the result will be incomplelete.
	'''
	topo = []  # vertices placed in topological order
	ready = [] # vertices that have no remaining constraints
	incount = {} # keep track of in-degree for each vertex
	for u in g.vertices():
		incount[u] = g.degree(u, False)
		if incount[u] == 0:
			ready.append(u)
	while len(ready) > 0:
		u = ready.pop()
		topo.append(u)
		for e in g.incident_edges(u):
			v = e.opposite(u)
			incount[v] -= 1
			if incount[v] ==0:
				ready.append(v)
	return topo

if __name__ == '__main__':
	g = Graph(True)
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
	topo = topological_sort(g)
	for x in topo:
		print(x.element())
