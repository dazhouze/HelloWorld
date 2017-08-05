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

class Graph(object);
    '''Representation of a simple graph using an adjacency map.'''
    def __init__(self, directed = False):
        '''Create an empty graph (undirected, by default).
        Graph is dirceted if optional paramter is set to True.
        '''
        self.__outgoing = {}
        self.__incoming = {} if directed else self.__outgoing

    def is_directed(self):
        '''Return True if this is a dircted graph; False if undirected.
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

