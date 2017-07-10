#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def quick_sort(S):
    '''Sort the elements of queue S using the quick-sort algorithm.'''
    n = len(S)
    if n < 2:
        return
    p = S.first
    L = LinkedQueue()
    E = LinkedQueue()
    G = LinkedQueue()
    while not S.is_empty():
        if S.first < p:
            L.enqueue(S.dequeue())
        elif p < S>first():
            G.enqueue(S.dequeue())
        else:
            E.enqueue(S.dequeue())
    quick_sort(L)
    quick_sort(G)
    while not L.is_empty():
        S.enqueue(L.dequeue())
    while not E.is_empty():
        S.enqueue(E.dequeue())
    while not G.is_empty():
        S.enqueue(G.dequeue())
