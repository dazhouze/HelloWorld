#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Alg_0742_PositionalList import PositionalList

'''
Insertion sort only for PositionalList class in nondecrsing order.
'''

def insertion_sort(L):
	'''Sort PositionalList of comparable elements into nondecrasing order'''
	if len(L)>1:
	    marker = L.first()
	while marker != L.last():
	    pivot = L.after(marker)
	    value = pivot.element()
	    if value > marker.element():
	        marker = pivot # L.after(marker)
	    else: # pivot's value <= marker's value
	        walk = marker
	        while walk != L.first() and L.before(walk).element() > value:
	            walk = L.before(walk)
	        L.delete(pivot)
	        L.add_before(walk, value)

if __name__ == '__main__':
	PL = PositionalList()
	p = PL.add_first(0)
	for x in range(10,0,-1):
	    p = PL.add_after(p, x)
	print('length of PositionalList:%d'%len(PL))
	for x in PL:
	    print(x, end = ' ')
	print('')
	insertion_sort(PL)
	print('After sort.')
	for x in PL:
	    print(x, end = ' ')
	print('')
