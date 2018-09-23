#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def find_brute(T, P):
	'''Return the lowest index of T at which sustring P begins (or else -1).'''
	n, m = len(T), len(P)
	for i in range(0, n-m+1):
		k = 0
		while k < m and T[i+k] == P[k]:
			k += 1
		if k == m:
			return i
	return -1
