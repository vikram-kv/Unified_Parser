import os, shutil
from uparser import wordparse
from joblib import Parallel, delayed
from tqdm import tqdm

num_jobs = 20
infolder = 'Original'
outfolder = 'Words'

for fdr in [outfolder]:
    if os.path.exists(fdr):
        shutil.rmtree(fdr)
    os.mkdir(fdr)

flist = os.listdir(infolder)
for fname in flist:
    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()

    i = 0
    
    words = []
    for l in cnts:
        l = l.strip().split('\t')
        words.append(l[0])
    
    fout = fname.split('_')[1]
    fout = fout.split('.')[0]
    print(fout)

    with open(f'{outfolder}/{fout}.words', 'w') as f:
        for w in words:
            f.write(w + '\n')