#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_1425_Graph import Graph
from Alg_0952_AdaptableHeapPriorityQueue import AdaptableHeapPriorityQueue

def shortest_path_lengths(g, src):
	'''Compute shortest-path distances from src to reachabel vertices of g.
	Graph g can be undirected or directed, but must be weigethed such that
	e.element() returns a numeric weigth for each edge e.
	Return dictionary mapping each reachable vertex to its distance from src.
	'''
	d = {}  # d[v] is upper bound from s to v
	cloud = {}  # map reachabel v to its d[v] value
	pq = AdaptableHeapPriorityQueue()  # vertex v will have key d[v]
	pqlocator = {}  # map form vertex to its pq locator
	for v in g.vertices():
		if v is src:
			d[v] = 0
		else:
			d[v] = float('inf')
		pqlocator[v] = pq.add(d[v], v)
	
	while not pq.is_empty():
		key, u = pq.remove_min()
		cloud[u] = key
		del pqlocator[u]
		for e in g.incident_edges(u):
			v = e.opposite(u)
			if v not in cloud:
				wgt = e.element()
				if d[u] + wgt < d[v]:
					d[v] = d[u] + wgt
					pq.update(pqlocator[v], d[v], v)
	return cloud

def shortest_path_tree(g, s, d):
	'''Reconstruct shortest path tree rooted at vertex s, given distance map d.
	Return tree as a map from each reachable vertex v (other than s) to the
	edge e=(u, v) than is used to reach v from its parent u in the tree.
	'''
	tree = {}
	for v in d:
		if v is not s:
			for e in g.incident_edges(v, False):
				u = e.opposite(v)
				wgt = e.element()
				if d[v] == d[u] + wgt:
					tree[v] = e
	return tree

if __name__ == '__main__':
	g = Graph(True)
	print('is_directed', g.is_directed())
	prev_v = None  # prev vertex
	root_v, tail_v = None, None
	for i in range(10):
		v = g.insert_vertex(i)  # vertex
		if prev_v is not None:
			dist = i+10 if i % 2 == 0 else i*4
			g.insert_edge(v, prev_v, dist)  # vertex
		if i == 0:
			root_v = v
		if i == 9:
			tail_v = v
		prev_v = v
	for x in g.vertices():
		for y in g.incident_edges(x):
			print(x.element(), '->',y.opposite(x).element(), 'weight', y.element(), )
	# test
	for src in (root_v, tail_v):
		cloud = shortest_path_lengths(g, src)
		for k,v in cloud.items():
			print('%d->%d, dist:%f' % (src.element(), k.element(), v))

		tree = shortest_path_tree(g, src, cloud)
		for k, v in tree.items():
			print(k.element(), 'from parent dist:',v.element())
