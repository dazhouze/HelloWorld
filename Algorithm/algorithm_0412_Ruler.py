#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Engilsh rule
'''

def draw_line(tick_length, tick_label=''):
    '''Draw one line with given length.'''
    line = '-' * tick_length
    if tick_label:
        line += ' ' + tick_label
    print(line)

def draw_interval(center_length):
    '''Draw tick interval based upon a central tick length.'''
    if center_length > 0:
        draw_interval(center_length -1) # top
        draw_line(center_length) # draw center tick
        draw_interval(center_length -1) # bottom

def draw_ruler(num_inches, major_length):
    '''
    Draw English ruler with given number of inches, major tick lenght
    num_inches:   the total length
    major_length: the major tick height
    '''
    draw_line(major_length, '0')
    for j in range(1, 1+num_inches):
        draw_interval(major_length -1)
        draw_line(major_length, str(j))

if __name__ == '__main__':
    draw_ruler(4, 3)
    draw_ruler(6, 2)
    pass
