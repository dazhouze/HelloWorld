#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def find_kmp(T, P):
	'''Return the lowest index of T an which substring P begins (or else -1).'''
	n, m = len(T), len(P)
	if m == 0:  return 0
	fail = compute_kmp_fail(P)
	j = 0
	k = 0
	while j < n:
		if T[j] == P[k]:
			if k == m-1:
				return j-m+1
			j += 1
			k += 1
		elif k > 0:
			k = fail[k-1]
		else:
			j += 1
	return -1

def compute_kmp_fail(P):
	'''Utility that computes and returns KMP 'fail' list.'''
	m = len(P)
	fail = [0] * m
	j = 1
	k = 0
	while j < m:
		if P[j] == P[k]:
			fail[j] = k + 1
			j += 1
			k += 1
		elif k > 0:
			k = fail[k-1]
		else:
			j += 1
	return fail

if __name__ == '__main__':
	T = '012301234012356789'
	P = '01235'
	print(T, P)
	print(find_kmp(T, P))
