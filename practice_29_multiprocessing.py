#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''os.fork , os.getpid() and os.getppid()'''
import os
print ('Process (%s) start ...' % os.getpid())
pid = os.fork()

print ('pid:%s'% pid)

if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

'''Mudule multiproceeing'''
from multiprocessing import Process
import os

def run_proc (name):
    print ('run child process %s (%s) ...' % (name, os.getpid()))

if __name__ == '__main__':
    print ('Parent porcess %s' % (os.getpid()))
    p = Process(target = run_proc, args = ('test',))
    print ('Child process will start.')
    p.start()
    p.join()
    print ('Child process ended.')

'''Pool of process'''
from multiprocessing import Pool
import os, time, random

def long_time_task (name):
    print('Run task %s (%s)' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print ('Task %s runs %0.2f sec' % (name, (end - start)))

if __name__ == '__main__':
    print ('Parent process %s' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args = (i,))
    print ('Waiting for all sub-processes done.')
    p.close()
    p.join()
    print('All sub-processes done')
    
