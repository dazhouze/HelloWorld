#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1425_Graph import Graph
from copy import deepcopy

def floyd_warshall(g):
	'''Return a new graph that is the transivive closure of g.'''
	closure = deepcopy(g)
	verts = list(closure.vertices())
	n = len(verts)
	for k in range(n):
		for i in range(n):
			if i != k and closure.get_edge(verts[i], verts[k]) is not None:
				for j in range(n):
					if i != j != k and closure.get_edge(verts[k], verts[j]) is not None:
						if closure.get_edge(verts[i], verts[j]) is None:
							closure.insert_edge(verts[i], verts[j])
	return closure

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
	g_closure = floyd_warshall(g)
	for v in g_closure.vertices():  # vertex
		print('vertex: %s' % v.element())
		for e in g_closure.incident_edges(v):  # edge incident vertex
			print('  Edges: %s' % (e.element()),)
