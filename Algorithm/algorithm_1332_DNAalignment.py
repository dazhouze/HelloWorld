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

if __name__ == '__main__':
    X = 'GTTCCTAATA'
    Y = 'CGATAATTGAGA'
    print(LCS(X, Y))
