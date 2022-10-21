import os, shutil
from parallelparser import wordparse
from joblib import Parallel, delayed

num_jobs = 20
infolder = 'Original'
outfolder = 'Generated'

if os.path.exists(outfolder):
    shutil.rmtree(outfolder)

os.mkdir(outfolder)
flist = os.listdir(infolder)
for fname in ['lexicon.cls_hi']:
    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()

    i = 0
    num = len(cnts)
    words = []
    for l in cnts:
        l = l.strip().split('\t')
        words.append(l[0])
    
    anslist = Parallel(n_jobs=num_jobs)(delayed(wordparse)(wd) for wd in words)
    
    results = [[words[i], anslist[i]] for i in range(num)]
    with open(f'{outfolder}/{fname}', 'w') as f:
        for l in results:
            f.write(f'{l[0]}\t{l[1]}\n')