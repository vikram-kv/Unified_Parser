import os, shutil
from parallelparser import wordparse
import time

infolder = 'Original'

outfolder = 'Generated'

if os.path.exists(outfolder):
    shutil.rmtree(outfolder)

os.mkdir(outfolder)

for fname in os.listdir(infolder):

    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()
    
    results = []
    i = 0
    for l in cnts:
        if i == 50:
            break
        l = l.strip().split('\t')
        wd = l[0]
        t1 = time.time()
        ans = wordparse(wd)
        t2 = time.time()
        print(f'{wd} - {t2-t1}')
        results.append([wd, ans])
        i += 1
    
    with open(f'{outfolder}/{fname}', 'w') as f:
        for l in results:
            f.write(f'{l[0]}\t{l[1]}\n')
        
        