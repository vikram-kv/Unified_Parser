# contains helper functions used in parser.py



# function - removeUnwanted() - referenced in lines 63 - 109 of unified.y
def removeUnwanted(input : str) -> str:

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


# function to replace GetFile in lines 132 - 156 of unified.y
# gives the filename according to language and type
def GetFile(LangId : int, type : int) -> str:

    rootPath = "./" 
    commonFile = "common"
    fileName = rootPath

    # return common file that contains the CPS mapping
    if type == 0:
        fileName += commonFile
        return fileName
    
    elif type == 1:
        fileName += "dict/"
    
    elif type == 2:
        fileName += "rules/"

    langIdNameMapping = { 1 : "malayalam", 2 : "tamil", 3 : "telugu",
        4 : "kannada", 5 : "hindi", 6 : "bengali",
        7 : "gujarathi", 8 : "odiya", 9 : "english" }
    
    if LangId in langIdNameMapping.keys():
        fileName += langIdNameMapping[LangId]
    
    if type == 1:
        fileName += ".dict"
    elif type == 2:
        fileName += ".rules"
    
    return fileName