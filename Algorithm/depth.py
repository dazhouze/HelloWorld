#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Zhou Ze'
__version__ = '0.0.1'

import sys, os.path, pysam  

##########
bam_p = '/home/zhouze/Documents/IGV_2.3.80/5YH.best.sorted.bam'
win = 1000 # window size: 1000bp
##########

mhc_s = 28477797 # GRCh37.p13 MHC region start coordinate
mhc_e = 33448354 # GRCh37.p13 MHC region end coordinate

mhc_sw = mhc_s//win
mhc_ew = mhc_e//win + 1
ind_len = mhc_ew - mhc_sw + 4
#print('index max:',ind_len)



CovF = [0]*ind_len #array for coverage fold/ sequencing depth

##### Identify SAM/BAM file to open different pysam IO handle. #####
if os.path.splitext(bam_p)[1] == '.sam': # SAM file
    bamfile = pysam.AlignmentFile(bam_p, "r")
elif os.path.splitext(bam_p)[1] == '.bam': # BAM file
    bamfile = pysam.AlignmentFile(bam_p, "rb") # file handle of BAM file
else:
    raise IOError('Please choose a SAM/BAM file!')

target = bamfile.fetch('chr6', mhc_s-1000, mhc_e+1000) # iterable method of target region read

for read in target: # deal with every line & ignore the soft/hard clipping of reads
    if read.is_unmapped==False: # mapped reads only, MHC region only
        start = (read.reference_start - mhc_s) // win + 1
        end   = (read.reference_end   - mhc_s) // win - 1
        head = 1 - ((read.reference_start)% win) / win
        tail = ((read.reference_end) % win) / win
        #print(start,end,head,tail)
        for i in range(start, end+1):
            if i >= 0 and i <= ind_len:
                CovF[i] += 1
        CovF[start-1] += head
        if end < ind_len:
            CovF[end+1] += tail
bamfile.close()

for x  in range(len(CovF)):
    start = (x + mhc_sw)*win + 1 # 4001-5000
    end = start + win
    print('hs6\t%d\t%d\t%d' % (start, end, CovF[x]))
