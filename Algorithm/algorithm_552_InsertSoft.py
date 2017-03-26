#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def insert_sort(A):
    '''Sort list of comparable elements into nondecreasing order.'''
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while j>0 and cur < A[j-1]:
            A[j] = A[j-1]
            j -= 1
        A[j] = cur #
        print(k, A)



if __name__ == '__main__':
    Ay = [3,2,4,1,5,9,7,8]
    insert_sort(Ay)
