# script to read the common file and convert it to JSON format

# f = open('common', 'r')
# l = f.readlines()
# for ln in l:
#     print(ln.encode('utf-8'))
# f.close()

import json

fields = ['serialnumber', 'phone', 'lan1', 'lan2', 'lan3', 'lan4', 'lan5', 'lan6', 'lan7', 'lan8']

records = []

with open('./common') as f:
    cnts = f.readlines()

for l in cnts:
    l = l.strip().split('\t')
    newrec = dict()
    for i in range(len(fields)):
        newrec[fields[i]] = l[i]
    records.append(newrec)

with open('common.json', 'w') as f:
    json.dump(records, f, ensure_ascii=False,indent=4)

with open('common.json', 'r') as f:
    records = json.load(f)
    print(records) 
