# contains helper functions used in parser.py



# function - removeUnwanted() - referenced in lines 63 - 109 of unified.y

def removeUnwanted(input : str):

    # ignore punctuations
    punctuationList = ["!",";",":","@","#","$","%","^","&","*",",",".","/","'","’","”","“","।"]

    # replacing problematic unicode characters that look the same but have different encodings
    replaceDict =    {"ऩ":"ऩ", "ऱ":"ऱ", "क़":"क़", "ख़":"ख़", "ग़":"ग़", "ज़":"ज़", "ड़":"ड़", "ढ़":"ढ़", "ढ़":"ढ़", "फ़":"फ़", "य़":"य़", "ऴ":"ऴ",
   "ொ":"ொ", "ோ":"ோ",
   "ൊ":"ൊ", "ോ":"ോ", "ല്‍‌":"ൽ", "ള്‍":"ൾ", "ര്‍":"ർ", "ന്‍":"ൻ", "ണ്‍":"ൺ"}

    output = ""
    for c in str:

        if c in punctuationList: 
            continue
        elif c in replaceDict.keys():
            output += replaceDict[c]
        else:
            output += c
    
    return output