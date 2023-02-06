from parser import wordparse
from joblib import Parallel, delayed
from tqdm import tqdm

with open('punjabi_words.txt', 'r') as f:
    words = f.readlines()

words = [wd.strip() for wd in words]
anslist = Parallel(n_jobs=1)(delayed(wordparse)(wd, 0, 0) for wd in tqdm(words))

with open('punjabi_results.txt', 'w') as f:
    for i in range(len(words)):
        f.write(f'{words[i]} = {anslist[i]}\n')