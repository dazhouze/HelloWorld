#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def LCS(X, Y):
	'''Return table such that L[j][k] is length of LCS for X[0:j] and Y[0:k].'''
	n, m = len(X), len(Y)
	L = [[0]*(m+1) for k in range(0, n+1)]
	for j in range(0, n):
		for k in range(m):
			if X[j] ==Y[k]:
				L[j+1][k+1] = L[j][k] + 1
			else:
				L[j+1][k+1] = max(L[j][k+1], L[j+1][k])
	return L

def LSC_selution(X, Y, L):
	'''Return the longest common substring of X and Y, given LCS table L.'''
	solution = []
	j, k = len(X), len(Y)
	while L[j][k] > 0:
		if X[j-1] == Y[k-1]:  # seq equal
			solution.append(X[j-1])
			j -= 1
			k -= 1
		elif L[j-1][k] >= L[j][k]:  # matrix value, go to larger
			j -= 1
		else:
			k -= 1
	return  ''.join(reversed(solution))

def print_matrix(X, Y, L):
	'''Return the matrix of X and Y and L.'''
	mat_X, mat_Y = list(X), list(Y)
	j, k = len(X), len(Y)
	# anno common seq
	route = set()
	while L[j][k] > 0:
		route.add((j,k))
		if X[j-1] == Y[k-1]:  # seq equal
			mat_X[j-1] = '"%s"' % X[j-1]
			mat_Y[k-1] = '"%s"' % Y[k-1]
			j -= 1
			k -= 1
		elif L[j-1][k] >= L[j][k]:  # matrix value, go to larger
			j -= 1
		else:
			k -= 1
	# output 
	matrix = 'qry\\ref'  # start with a space
	for base in mat_Y:  # ref
		matrix += '\t%s' % base  # start with a space
	matrix += '\t$\n'
	for j in range(len(mat_X)+1):  # 
		matrix = matrix + '%s' % mat_X[j] if j < len(mat_X) else matrix + '$'  # query
		for k in range(len(mat_Y)+1):  # 
			matrix = matrix + '\t"%d"' % L[j][k] if (j, k) in route else matrix + '\t%d' % L[j][k] 
		matrix += '\n'
	return matrix

if __name__ == '__main__':
	X = 'GTTCCTAATGG'
	Y = 'CGATAATTGAGA'
	L = LCS(X, Y)
	print('query: ', X)
	print('refer: ', Y)
	print(L)
	print(print_matrix(X, Y, L))
	print(LSC_selution(X, Y, L))
