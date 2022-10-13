# contains helper functions used in parser.py

# global CONSTANTs for languages. Uses the same values as the enum at 
# lines 11-13 of unified.y


from dataclasses import replace
from sys import flags
from tkinter import W


class FLAGS:
    DEBUG = 0
    parseLevel = 0
    pruiningFlag = 0
    syllTagFlag = 0
    fliteHTSFlag = 0
    doubleParseSyl = 0
    directParseFlag = 0
    LangSpecificCorrectionFlag = 1
    writeFormat = 0

class WORDS:
    wordCopy = ""
    syllabifiedWord = ""
    phonifiedWord = ""
    unicodeWord = ""
    syllabifiedWordOut = ""
    outputText = ""

flags = FLAGS()
words = WORDS()
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
syllableCount = 0

# files and paths
rootPath = "./"
commonFile = "common"
outputFile = ""
outputPruneFile = "rag_pho"


# mapping from utf8 language chars to the phoneme
# implemented as list of lists [rows ~ 128, cols - 2]
# mimics the construction in unified.y but may be replaced with a dictionary
symbolTable = [[]]
ROW = 128
COL = 2
syllableList = []

VOWELSSIZE=18
CONSONANTSSIZE=25
SEMIVOWELSSIZE=13

VOWELS = ["a","e","i","o","u","aa","mq","aa","ii", "uu","rq","au","ee","ei","ou","oo","ax","ai"]
CONSONANTS = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m"]
SEMIVOWELS = ["y","r","l","w","sh","sx","zh","s","h","lx","rx","f","dxq"]


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
    global langId, isSouth 
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


# replacement for function in lins 158 - 213. Sets the lanuage features
def SetlanguageFeat(input : str) -> int:

    global symbolTable, langId

    # open common file
    with open(GetFile(0,0), 'r') as infile:
        lines = infile.readlines()

    str1 = str
    length = len(str1)
    if (length == 0):
        length = 1

    for j in range(0,length):
        # for skipping invisible char
        if (ord(str1[j]) < 8204):
            firstLet = str1[j]
            break
    
    SetlangId(firstLet) # set global langId

    for i in range(len(lines)):
        l = lines[i].strip().split('\t')
        assert(len(l) == 10)
        symbolTable[i][1] = l[1]
        symbolTable[i][0] = l[1 + langId]

    return 1


# replacement for function in lines 52 - 59. Check if symbol is in symbolTable
def CheckSymbol(input : str) -> int:
    i = 0
    for i in range(ROW):
        if (symbolTable[i][0] == input):
            return 1
    return 0


# replacement for function in lines 249 - 276. Convert utf-8 to cps symbols
def ConvertToSymbols(input : str) -> str:
    global flags, words, symbolTable

    output = ""
    str1 = input

    words.syllabifiedWord = "&"

    for j in range(len(str1)):
        if (ord(str1[j]) < 8204):
            words.syllabifiedWord += "&" + symbolTable[ord(str[1])%128][1]

    output = words.syllabifiedWord
    return output



# function in lines 1278 - 1299. write to wordpronunciation file
def WriteFile(text : str):
    global flags, outputFile

    output = open(outputFile, 'w')

    if (flags.fliteHTSFlag):
        print(f"phones : {text}")
        output.write(text + '\n')
        output.close()
        return 
    
    output.write("(set! wordstruct '( ")
    output.write(text)
    output.write("))\n")

    output.close()
    if ((not flags.writeFormat) and flags.pruiningFlag):
        WritePruneFile(text)


# function in lines 1302-1313. output for pruning
def WritePruneFile(text : str):
    global outputPruneFile
    output = open(outputPruneFile, 'w')
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace("0", "")
    text = text.replace("   ", " ")
    text = text.replace("  ", "")
    text = text.replace("\"\"","\" \"")
    output.write(text)
    output.close()

# function in lines 588-597. checnk if vowel is in input. 'q' special case, 'rq' special case
def CheckVowel(input : str, q : int, rq : int) -> int:
    if (input.find("a") != -1):
        return 1
    if (input.find("e") != -1):
        return 1
    if (input.find("i") != -1):
        return 1
    if (input.find("o") != -1):
        return 1
    if (input.find("u") != -1):
        return 1
    if (q and input.find("q") != -1):
        return 1
    if (rq and input.find("rq") != -1):
        return 1
    return 0

# function in lines 599-602.
def Checkeuv(input : str) -> int:
    if (input.find("euv") != -1):
        return 1
    return 0

# function in lines 605-613
def CheckSingleVowel(input : str, q : int) -> int:
    if (input in ['a', 'e', 'i', 'o', 'u']):
        return 1
    if (q and input == 'q'):
        return 1
    return 0

# function in lines 616 - 629. get the type of phone in the position
def GetPhoneType(input : str, pos : int) -> int:
    global flags
    phone = input
    count = 1
    i = 0
    phone = phone.split('&')

    for pch in phone:
        count = count + 1
        if (count >= pos):
            break
    
    if (flags.DEBUG):
        print(f"str : {pch} {GetType(pch)}\n")

    return GetType(pch)

# function in lines 631 - 637. get the type of given input
def GetType(input : str):

    for i in range(VOWELSSIZE):
        if VOWELS[i] == input:
            return 1
    for i in range(CONSONANTSSIZE):
        if CONSONANTS[i] == input:
            return 2
    for i in range(SEMIVOWELSSIZE):
        if SEMIVOWELS[i] == input:
            return 3
    
    return 0

# function in lines 640 - 647. check if chillaksharas are there --for malayalam
def CheckChillu(input : str) -> int:
    l = ["nwv", "nnv", "rwv", "lwv", "lnv"]
    for x in l:
        if (input.find(x) != -1):
            return 1
    
    return 0

# function in lines 650 - 660. get UTF-8 from CPS
def GetUTF(input : str) -> str :

    global symbolTable
    for i in range(ROW):
        if (input == symbolTable[i][1]):
            return symbolTable[i][0]
    
    return 0

# function in lines 663 - 666. verify the letter is english char -- CLS
def isEngLetter(p : str) -> int:
    if (ord(p) >= 97 and ord(p) <= 122):
        return 1
    return 0

# function in lines 669-682. remove unwanted Symbols from word
def CleanseWord(phone : str) -> str:

    phonecopy = ""

    for c in phone:
        if ((not (c == '&')) and (not isEngLetter(c))):
            c = '#'
        phonecopy += c

    if (phonecopy.find('$') != -1):
        phonecopy = phonecopy.replace('$','')
    if (phonecopy.find('&&') != -1):
        phonecopy = phonecopy.replace('&&','&')
    
    return phonecopy




''' !!!!!!!!!!!!!!!!!! NOT COMPLETE !!!!!!!!!!!!!!!!!! '''

# replacement for function in lines 278 - 317. check the word in Dict

def CheckDictionary(input : str) -> int:
    global flags, langId
    fileName = GetFile(langId, 1)
    if flags.DEBUG:
        print(f"dict : {fileName}\n")
    
    if (langId == ENGLISH):
        pass