import os, shutil
from uparser import wordparse
from joblib import Parallel, delayed
from tqdm import tqdm

num_jobs = 20
infolder = 'Words'
outfolder = 'Outputs'

for fdr in [outfolder]:
    if os.path.exists(fdr):
        shutil.rmtree(fdr)
    os.mkdir(fdr)

langs = []
langwdmap = {}

flist = os.listdir(infolder)
for fname in flist:
    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()

    i = 0
    
    words = []
    for l in cnts:
        l = l.strip().split('\t')
        words.append(l[0])
    
    lan = fname.split('.')[0]
    langs.append(lan)
    langwdmap[lan] = words

for opt in [0,1,2]:
    out_cur = outfolder + '/option-' + str(opt)
    os.mkdir(out_cur)

    for l in langs:
        words = langwdmap[l]

        if opt == 1:
            anslist = Parallel(n_jobs=num_jobs)(delayed(wordparse)(wd, 0, opt, 1) for wd in tqdm(words))
        else:
            anslist = Parallel(n_jobs=num_jobs)(delayed(wordparse)(wd, 0, opt, 0) for wd in tqdm(words))

        with open(f'{out_cur}/{l}.output', 'w') as f:
            for i in range(len(words)):
                f.write(f'{words[i]}\t{anslist[i]}\n')
        
        print(f'completed {l}')

    