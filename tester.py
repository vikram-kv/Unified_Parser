import os, shutil
import subprocess
from unittest import result

infolder = input('Enter source folder name :')

outfolder = input('Enter dest folder name :')

if os.path.exists(outfolder):
    shutil.rmtree(outfolder)

os.mkdir(outfolder)

for fname in os.listdir(infolder):

    with open(f'{infolder}/{fname}', 'r') as f:
        cnts = f.readlines()
    
    results = []
    i = 0
    for l in cnts:
        l = l.strip().split('\t')
        wd = l[0]
        proc = subprocess.run(['python3', 'parser.py', wd, 'output/temp.txt', '1', '1', '1', '0'], capture_output=True)
        results.append([wd, proc.stdout.decode('utf-8').strip()])
        if i == 100:
            break
        i += 1
    
    with open(f'{outfolder}/{fname}', 'w') as f:
        for l in results:
            f.write(f'{l[0]}\t{l[1]}\n')
        
        