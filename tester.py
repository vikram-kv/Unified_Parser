import os, shutil
from parallelparser import wordparse
from joblib import Parallel, delayed
from tqdm import tqdm

num_jobs = 20
infolder = 'Original'
outfolder = 'Generated'
difforigfolder = 'OriginalDifferences'
diffgenfolder = 'GeneratedDifferences'

for fdr in [outfolder, difforigfolder, diffgenfolder]:
    if os.path.exists(fdr):
        shutil.rmtree(fdr)
    os.mkdir(fdr)

flist = os.listdir(infolder)
flist = sorted(flist)
for fname in flist:
    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()

    i = 0
    
    words = []
    for l in cnts:
        l = l.strip().split('\t')
        words.append(l[0])
    
    num = len(words)
    anslist = Parallel(n_jobs=num_jobs)(delayed(wordparse)(wd) for wd in tqdm(words))
    
    results = [f'{words[i]}\t{anslist[i]}' for i in range(num)]
    with open(f'{outfolder}/{fname}', 'w') as f:
        for l in results:
            f.write(f'{l}\n')
    
    diff_orig, diff_gen = [], []
    for i in range(num):
        if cnts[i].strip() != results[i]:
            diff_orig.append(cnts[i])
            diff_gen.append(results[i])
    
    if len(diff_gen) == 0:
        continue

    with open(f'{difforigfolder}/{fname}','w') as f:
        for l in diff_orig:
            f.write(l)

    with open(f'{diffgenfolder}/{fname}','w') as f:
        for l in diff_gen:
            f.write(l+'\n')
        
    print(f'Completed {fname}')