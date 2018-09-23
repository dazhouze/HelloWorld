#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Vertex(object):
	'''Lightweight vertex structure of a graph.'''
	__slots__ = '__element'

	def __init__(self,x):
		'''Do not call constrctor directly. Use Graph's insert_vertex(x).'''
		self.__element = x

	def element(self):
		'''Return element associated with this vertex.'''
		return self.__eletment

	def __hash__(self):
		return hash(id(self))

class Edge(object):
	'''Lightweight edge structure for a graph.'''
	__slots__ = '__origin', '__destination', '__element'

	def __init__(self, u, v, x):
		'''Do not call constructor diectly. Use Graph's insert_edge(u, v, x).'''
		self.__origin = u
		self.__destination = v
		self.__element = x

	def endpoints(self):
		'''Return (u, v) tuple for vertices u and v.'''
		return (self.__origin, self.__destination)

	def opposite(self, v):
		'''Return the vertex that is opposite v on this edge.'''
		return self.__destination if v is self.__origin else self.__origin

	def element(self):
		'''Return element associated with this edge.'''
		return self.__element

	def __hash__(self):
		return hash((self.__origin, self.__destination))

class Graph(object):
	'''Representation of a simple graph using an adjacency map.'''
	def __init__(self, directed = False):
		'''Create an empty graph (undirected, by default).
		Graph is dirceted if optional paramter is set to True.
		'''
		self.__outgoing = {}
		self.__incoming = {} if directed else self.__outgoing

	def is_directed(self):
		'''Return True if this is a dircted graph: False if undirected.
		Property is based on the original declaration of the graph, not its contents.
		'''
		return self.__incoming if not self.__outgoing

	def vertex_count(self):
		'''Return the number of vertices in the graph.'''
		return len(self.__outgoing)
		
	def vertices(self):
		'''Return an iteration of all vertices of the graph.'''
		return self.__outging.keys() 

	def edges_count(self):
		'''Return the number of edges in the graph.'''
		total = sum(len(self.__outgoing[v]) for v in self.__outgoing)
		return total if self.is_directed() else total // 2

	def edges(self):
		'''Return a set of all edges of the graph.'''
		result = set()
		for secondary_map in self.__outgoing.values():
			result.update(secondary_map.values())
		return result

	def get_dege(self, u, v):
		'''Return the edge from u to v, or None if not adjacent.'''
		return self.__outgoing[u].get(v)

	def degree(self, v, outgoing=True):
		'''Return number of (outgoing) edges incident to vertex v in the graph.
		If graph is directed, optional parameter used to count incoming edges.
		'''
		adj = self.__outgoing if outgoing else self.__incoming
		return len(adj[v])

	def incident_edges(self, v, outgoing=True):
		'''Return all (outgoing) edges incident to vertex v in the graph.
		If graph is directed, optional parameter used to request incoming edges.
		'''
		adj = self.__outgoing if outgoing else self.__incoming
		for edge in adj[v].values():
			yield edge

	def insert_vertex(self, x=None):
		'''Insert and return a new Vertex with element x.'''
		v = self.Vertex(x)
		self.__outgoing[v] = {}
		if self.is_directed():
			self.__incoming[v] = {}
		return v

	def insert_edge(self, u, v, x=None):
		'''Insert and return a new Edge from u to v with auxiliary element x.'''
		e = self.Edge(u, v, x)
		self.__outgoing[u][v] = e
		self.__incoming[v][u] = e

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

	def DFS_complete(g):
		'''Perform DFS for entire graph and regurn forest as a dictionary.
		Retuslt maps each vertex v to the edge that was used to discover it.
		(Vertices that are roots of a DFS tree are mapped to None.)
		'''
		forest = {}
		for u in g.vertices():
			if u not in forest:
				forest[u] = None
				DFS(g, u, forest)
		return forest

	def BFS(g, s, discovered):
		'''Perform BFS of the undiscovered portion of Graph g starting at Vertex s.
		discover it during the BFS (s should be mapped to None prior to the call).
		Newly discovered vertices will be added to the dictionary as a result.
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

	def floyd_warshall(g):
		'''Return a new graph that is the transitive closure of g.'''
		closure = deepcopy(g)
		verts = list(closure.vertices())
		n = len(verts)
		for k in range(n):
			for i in range(n):
				if i != k and closure.get_edge(verts[i], verts[k]) is not None:
					if closure.get_edge(verts[i], verts[j]) is None:
						closure.insert_edge(verts[i], verts[j])
		return closure

	def topological_sort(g):
		'''Return a list of verticies of directed acyclic graph g in topological order.
		If graph g has a cycle, the result will be incomplete.
		'''
		topo = []
		ready = []
		incount = {}
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
				if infount[v] == 0:
					ready.append(v)
		return topo

	def shortest_path_lengths(g, src):
		'''Compute shortest path distances from src to reachable vertices of g.
		Graph g can be undircted or dircted, but must be weighted such that 
		e.element() returns a numeric weight for each edge e.
		Return dictionary mapping each reachable vertex to ite distance from src.
		'''
		d = {}
		cloud = {}
		pq = AdaptableHeapPriorityQueue()
		pqlocator = {}
		for v in g.vertices():
			if v is src:
				d[v] = 0
			else:
				d[v] = float('inf')
			pqlocator[v] = pq.add(d[v], v)

		while not pq.is_empty():
			key, u = pg.remove_min()
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
			'''Reconstruct shoftest path tree rooted at vertex s, given distance map d.
			Return tree as a map from each reachable vertex v (other than s) to the edge
			e=(u, v) that is used to reach v from ites parent u in the tree.
			'''
			tree = {}
			for v in d:
				if v is not s:
					for e in g.incident_edges(v, False):
						u = e.opposite(v)
						wgt = elelement()
						if d[v] == d[u] + wgt:
							tree[v] = e
			return tree
		
		def MST_PrimJarnik(g):
			'''Compute a minimum spanning tree of weighted graph g.
			Return a list of edges that comprise the MST (in arbitary order).
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
				pqlocator[v] = pq.add(d[v], (v,None))
			while not pg.is_empty():
				key, value = pg.remove_min()
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
			The elements of graph's edges are assumed to be weights.
			'''
			tree = []
			pq = HeapPriorityQueue()
			position - {}
			for v in g.vertices():
				position[v] = forest.make_group(v)

			for e in g.edges():
				pg.add(e.element(), e)

			size = g.vertex_count()

			while len(tree) != size-1 and not pq.is_empty():
				weigth, edge = pg.remove_min()
				u, v = edge.endpoints()
				a = forest.find(position[u])
				b = forest.find(position[v])
				if a!=b:
					tree.append(edge)
					forest.union(a, b)
			return tree
