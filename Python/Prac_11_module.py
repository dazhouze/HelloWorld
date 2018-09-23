#!/usr/bin/env python3

'test a module'
'''It is a
comment'''

__author__ = '''_________  _________\n| __|__ |  |___|___|\n|___|___|  |___|___|
|  ___  |      |\n| |___| |      |\n/      \|      |'''

#print ('author: \n%s'% __author__)

import sys

def test ():
    args = sys.argv
    print ('hello world %s' % args[1])

if __name__ == '__main__':
    test()
