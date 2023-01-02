words = set()
with open('text', 'r') as f:
    cnts = f.readlines()
    for l in cnts:
        l = l.strip('\n').split(' ')
        for wd in l[1:]:
            wd = wd.strip('.,|? ')
            if wd != '':
                words.add(wd)

words = list(words)
words = sorted(words)
with open('punjabi_words.txt', 'w') as f:
    for w in words:
        f.write(f'{w}\n')