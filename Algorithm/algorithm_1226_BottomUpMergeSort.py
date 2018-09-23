#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def merge(src, result, start, inc):
	'''Merge src[start : start+inc] and src[start+inc : start+2*inc] into result.'''
	end1 = start + inc
	end2 = min(start + 2*inc, len(src))
	x, y, z = start, start+inc, start
	while x<end1 and y<end2:
		if src[x] < src[y]:
			result[z] =src[x]
			x += 1
		else:
			result[z] = src[y]
			y += 1
		z += 1
	if x < end1:
		result[z:end2] = src[x:end1]
	elif y < end2:
		result[z:end2] = src[y:end2]

def merge_sort(S):
	'''Sort the elements of queue S using the merge-sort algorithm.'''
	import math
	n = len(S)
	logn = math.ceil(math.log(n, 2))
	src, dest = S, [None]*n
	for i in (2**k for k in range(logn)):
		for j in range(0, n, 2*i):
			merge(src, dest, j, i)
		src, dest = dest, src
	if S is not src:
		S[0:n] = src[0:n]

if __name__ == '__main__':
	S = [1, 5, 3, 4, 2, 35, 17]
	merge_sort(S)
	print(S)
