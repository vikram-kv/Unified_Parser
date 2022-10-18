with open('dict/english.dict', 'r') as f:
    cnts = f.readlines()


for l in  cnts:
    l = l.strip()
    print(l)