#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Disk size look up.
'''
import os
def disk_usage(path):
	'''Return the number of bytes used by a file/folder and any descendents.'''
	total = os.path.getsize(path)
	if os.path.isdir(path) == True:
	    for filename in os.listdir(path):
	        childpath = os.path.join(path, filename)
	        total += disk_usage(childpath) # recursion
	print('%d,%s'%(total, path))
	return total
if __name__ == '__main__':
	print('total bytes',disk_usage('/home/zhouze/Desktop'))
	pass
