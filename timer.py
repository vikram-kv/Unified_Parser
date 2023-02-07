import os, shutil
from uparser import wordparse
import time

infolder = 'Original'
outfolder = 'Generated'
difforigfolder = 'OriginalDifferences'
diffgenfolder = 'GeneratedDifferences'

flist = ['lexicon.cls_hi']
for fname in flist:
    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()

    i = 0
    
    words = []
    for l in cnts:
        l = l.strip().split('\t')
        words.append(l[0])
    
    for w in words:
    	stime = time.time()
    	ans = wordparse(w)
    	etime = time.time()
    	print(f'{ans} - {etime-stime}')
    	
