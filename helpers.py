# contains helper functions used in parser.py

# global CONSTANTs for languages. Uses the same values as the enum at 
# lines 11-13 of unified.y

MALAYALAM = 1
TAMIL = 2
TELUGU = 3
KANNADA = 4
HINDI = 5
BENGALI = 6
GUJARATHI = 7
ODIYA = 8
ENGLISH = 9

langId = 0
isSouth = False


# variable to indicate current language being parsed.
currLang = ENGLISH


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



# function to replace SetlangId in lines 62-80 of unified.y

def SetlangId(id : int):
    if(id>=3328 and id<=3455):
        currLang = MALAYALAM; #malayalam
    elif(id>=2944 and id<=3055):
        currLang = TAMIL; #tamil
    elif(id>=3202 and id<=3311):
        currLang = KANNADA; #KANNADA
    elif(id>=3072 and id<=3198):
        currLang = TELUGU; #telugu
    elif(id>=2304 and id<=2431):
        currLang = HINDI; #hindi
    elif(id>=2432 and id<=2559):
        currLang = BENGALI; #BENGALI
    elif(id>=2688 and id<=2815):
        currLang = GUJARATHI; #gujarathi
    elif(id>=2816 and id<=2943):
        currLang = ODIYA; #odia
    elif(id>=64 and id<=123):
        currLang = ENGLISH; #english

    langId = currLang

    if(langId < 5):
        isSouth = 1
    if(langId == 0):
        print(f"UNKNOWN LANGUAGE - id = {id}")
        exit(-1)
    return 1