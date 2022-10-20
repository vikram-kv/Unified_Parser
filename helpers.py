import globals
# contains helper functions used in parser.py

# function - RemoveUnwanted() - referenced in lines 63 - 109 of unified.y
def RemoveUnwanted(input : str) -> str:

    # ignore punctuations
    punctuationList = ["!",";",":","@","#","$","%","^","&","*",",",".","/","'","’","”","“","।"]

    # replacing problematic unicode characters that look the same but have different encodings
    replaceDict =    {"ऩ":"ऩ", "ऱ":"ऱ", "क़":"क़", "ख़":"ख़", "ग़":"ग़", "ज़":"ज़", "ड़":"ड़", "ढ़":"ढ़", "ढ़":"ढ़", "फ़":"फ़", "य़":"य़", "ऴ":"ऴ",
   "ொ":"ொ", "ோ":"ோ",
   "ൊ":"ൊ", "ോ":"ോ", "ല്‍‌":"ൽ", "ള്‍":"ൾ", "ര്‍":"ർ", "ന്‍":"ൻ", "ണ്‍":"ൺ"}

    output = ""
    for c in input:

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

    fileName = globals.rootPath

    # return common file that contains the CPS mapping
    if type == 0:
        fileName += globals.commonFile
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
def SetlangId(fl : str):
    id = ord(fl)
    if(id>=3328 and id<=3455):
        globals.currLang = globals.MALAYALAM; #malayalam
    elif(id>=2944 and id<=3055):
        globals.currLang = globals.TAMIL; #tamil
    elif(id>=3202 and id<=3311):
        globals.currLang = globals.KANNADA; #KANNADA
    elif(id>=3072 and id<=3198):
        globals.currLang = globals.TELUGU; #telugu
    elif(id>=2304 and id<=2431):
        globals.currLang = globals.HINDI; #hindi
    elif(id>=2432 and id<=2559):
        globals.currLang = globals.BENGALI; #BENGALI
    elif(id>=2688 and id<=2815):
        globals.currLang = globals.GUJARATHI; #gujarathi
    elif(id>=2816 and id<=2943):
        globals.currLang = globals.ODIYA; #odia
    elif(id>=64 and id<=123):
        globals.currLang = globals.ENGLISH; #english

    globals.langId = globals.currLang

    if(globals.langId < 5):
        globals.isSouth = 1
    if(globals.langId == 0):
        print(f"UNKNOWN LANGUAGE - id = {fl}")
        exit(-1)
    return 1


# replacement for function in lins 158 - 213. Sets the lanuage features
def SetlanguageFeat(input : str) -> int:

    # open common file
    with open(GetFile(0,0), 'r') as infile:
        lines = infile.readlines()

    str1 = input
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
        globals.symbolTable[i][1] = l[1]
        globals.symbolTable[i][0] = l[1 + globals.langId]

    return 1


# replacement for function in lines 52 - 59. Check if symbol is in symbolTable
def CheckSymbol(input : str) -> int:
    i = 0
    for i in range(globals.ROW):
        if (globals.symbolTable[i][1] == input):
            return 1
    return 0


# replacement for function in lines 249 - 276. Convert utf-8 to cps symbols
def ConvertToSymbols(input : str) -> str:

    output = ""
    str1 = input

    globals.words.syllabifiedWord = "&"
    for j in range(len(str1)):
        if (ord(str1[j]) < 8204):
            globals.words.syllabifiedWord += "&" + globals.symbolTable[ord(str1[j])%128][1]

    output = globals.words.syllabifiedWord
    return output


# function in lines 1278 - 1299. write to wordpronunciation file
def WriteFile(text : str):

    output = open(globals.outputFile, 'w')

    if (globals.flags.fliteHTSFlag):
        print(f"phones : {text}")
        output.write(text + '\n')
        output.close()
        return 
    
    output.write("(set! wordstruct '( ")
    output.write(text)
    output.write("))\n")

    output.close()
    if (globals.flags.writeFormat == 0 and globals.flags.pruiningFlag == 1):
        WritePruneFile(text)


# function in lines 1302-1313. output for pruning
def WritePruneFile(text : str):
    output = open(globals.outputPruneFile, 'w')
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
    phone = input
    count = 1
    i = 0
    phone = phone.split('&')

    for pch in phone:
        count = count + 1
        if (count >= pos):
            break
    
    if (globals.flags.DEBUG):
        print(f"str : {pch} {GetType(pch)}\n")

    return GetType(pch)

# function in lines 631 - 637. get the type of given input
def GetType(input : str):

    for i in range(globals.VOWELSSIZE):
        if globals.VOWELS[i] == input:
            return 1
    for i in range(globals.CONSONANTSSIZE):
        if globals.CONSONANTS[i] == input:
            return 2
    for i in range(globals.SEMIVOWELSSIZE):
        if globals.SEMIVOWELS[i] == input:
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
    for i in range(globals.ROW):
        if (input == globals.symbolTable[i][1]):
            
            return globals.symbolTable[i][0]
    
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
        if (c != '&' and isEngLetter(c) == 0):
            c = '#'
        phonecopy += c

    if (phonecopy.find('$') != -1):
        phonecopy = phonecopy.replace('$','')
    if (phonecopy.find('&&') != -1):
        phonecopy = phonecopy.replace('&&','&')
    
    return phonecopy


# replacement for funciton in lines 321 - 356. Correct if there is a vowel in the middle
def MiddleVowel(phone : str) -> str:

    c1 = ''
    c2 = ''
    phonecopy = phone
    for i in range(globals.CONSONANTSSIZE):
        for j in range(globals.VOWELSSIZE):
            c1 = f'&{globals.CONSONANTS[i]}&{globals.VOWELS[j]}&'
            c2 = f'&{globals.CONSONANTS[i]}&av&{globals.VOWELS[j]}&'

            phonecopy = phonecopy.replace(c1, '@')
            phonecopy = phonecopy.replace('@', c2)

    for i in range(globals.SEMIVOWELSSIZE):
        for j in range(globals.VOWELSSIZE):
            c1 = f'&{globals.SEMIVOWELS[i]}&{globals.VOWELS[j]}&'
            c2 = f'&{globals.SEMIVOWELS[i]}&av&{globals.VOWELS[j]}&'

            phonecopy = phonecopy.replace(c1, '@')
            phonecopy = phonecopy.replace('@', c2)

    return phonecopy


# replacement for function in lines 435 - 459. //cant use this as break syllable rules. 
# NOT USED ANYWHERE
def DoubleModifierCorrection(phone : str) -> str:

    doubleModifierList = ["&nwv&","&nnv&","&rwv&","&lwv&","&lnv&","&aav&","&iiv&","&uuv&","&rqv&","&eev&",
    "&eiv&","&ouv&","&axv&","&oov&","&aiv&","&auv&","&aev&",
    "&iv&","&ov&","&ev&","&uv&"]

    phonecopy = phone
    for i in range(0,21):
        for j in range(0,21):
            c1 = f'{doubleModifierList[i]}#{doubleModifierList[j]}'
            c2 = f'{doubleModifierList[i]}{doubleModifierList[j]}#&'

            phonecopy = phonecopy.replace(c1, '@')
            phonecopy = phonecopy.replace('@', c2)


    if (phonecopy.find("&#&hq&") != -1):
        phonecopy = phonecopy.replace("&#&hq&","&hq&#&")
    
    if (phonecopy.find("&&") != -1):
        phonecopy = phonecopy.replace("&&","&")
    
    return phonecopy



# replacement for funciton in lines 462 - 495. //for eu&C&C&V

def SchwaDoubleConsonent(phone : str) -> str:

    consonentList = ["k","kh","lx","rx","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m","y","r","l","w","sh","sx","zh","y","s","h","f","dxq"]
    vowelList = ["av&","nwv&","nnv&","rwv&","lwv&","lnv&","aav&","iiv&","uuv&","rqv&","eev&","eiv&","ouv&",
    "axv&","oov&","aiv&","nnx&","nxx&","rrx&","llx&","lxx&",
    "aa&","iv&","ov&","mq&","aa&","ii&","uu&","rq&",
    "ee&","ei&","ou&","oo&","ax&","ai&","ev&","uv&",
    "a&","e&","i&","o&","u&"]

    phonecopy = phone
    for i in range(0,39):
        for j in range(0,39):
            for k in range(0,42):

                c1 = f'&euv&{consonentList[i]}&{consonentList[j]}&{vowelList[k]}'
                c2 = f'&euv&{consonentList[i]}&av&{consonentList[j]}&{vowelList[k]}'
                phonecopy = phonecopy.replace(c1, '@')
                phonecopy = phonecopy.replace('@', c2)

    if (phonecopy.find("$") != -1):
        phonecopy = phonecopy.replace("$","")
    
    return phonecopy


# replacement for function in lines 498 - 585. //halant specific correction for aryan langs
def SchwaSpecificCorrection(phone : str) -> str:

    schwaList = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh",
    "nx","t","th","d","dh","n","p","ph","b","bh","m","y",
    "r","l","s","w","sh","sx","zh","h","lx","rx","f","dxq"]

    vowelList = ["av&","nwv&","nnv&","rwv&","lwv&","lnv&","aav&","iiv&","uuv&","rqv&","eev&","eiv&","ouv&",
    "axv&","oov&","aiv&","nnx&","nxx&","rrx&","llx&","lxx&",
    "aa&","iv&","ov&","mq&","aa&","ii&","uu&","rq&",
    "ee&","ei&","ou&","oo&","ax&","ai&","ev&","uv&",
    "a&","e&","i&","o&","u&"]

    if (globals.flags.DEBUG):
        print(f'{len(phone)}\n')
    
    phonecopy = phone + '!'

    if (globals.flags.DEBUG):
        print(f'phone cur - {phonecopy}\n')
    
    # // for end correction &av&t&aav&. //dont want av
    for i in range(0,38):
        for j in range(1,42):
            c1 = f'&av&{schwaList[i]}&{vowelList[j]}!'
            c2 = f'&euv&{schwaList[i]}&{vowelList[j]}!'
            phonecopy = phonecopy.replace(c1, '@')
            phonecopy = phonecopy.replace('@', c2)
    
    phonecopy = phonecopy.replace('!', '')

    for i in range(0,38):
        c1 = f'&av&{schwaList[i]}&av&'
        c2 = f'&euv$&{schwaList[i]}&av$&'
        phonecopy = phonecopy.replace(c1, '@')
        phonecopy = phonecopy.replace('@', c2)

    if(globals.flags.DEBUG):
        print(f"inside schwa{phonecopy}\n")
    

    for i in range(0,38):
        c1 = f'&av&{schwaList[i]}&'
        c3 = f'&{schwaList[i]}&'

        for j in range(0,41):
            c4 = f'&euv&{c3}${vowelList[j]}'
            c2 = f'c1{vowelList[j]}'
            phonecopy = phonecopy.replace(c2, '@')
            phonecopy = phonecopy.replace('@', c4)

    phonecopy = phonecopy.replace("$","")

    #//&q&w&eu& - CORRECTED TO 38 - CHECK
    for i in range(0,38):
        c1 = f'&q&{schwaList[i]}&euv&'
        c2 = f'&q&{schwaList[i]}&av&'
        phonecopy = phonecopy.replace(c1, '@')
        phonecopy = phonecopy.replace('@', c2)

    return phonecopy

# replacement for function in lines . //correct the geminate syllabification ,isReverse --reverse correction

def GeminateCorrection(phone : str, isReverse : int) -> str:

    geminateList = ["k","kh","lx","rx","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m","y",
    "r","l","w","sh","sx","zh","y","s","h","f","dxq"]

    phonecopy = phone
    for i in range(0, 39):
        c1 = f'&{geminateList[i]}&eu&{geminateList[i]}&'
        c2 = f'&{geminateList[i]}&{geminateList[i]}&'
        phonecopy = phonecopy.replace(c2, c1) if isReverse == 1 else phonecopy.replace(c1, c2)
    
    return phonecopy


# replacement for function in  lines 356 - 430.  //Syllabilfy the words

def Syllabilfy(phone : str) -> str:

    phonecopy = phone

    phonecopy = phonecopy.replace("&&","&")
    phonecopy = phonecopy.replace("&eu&","@")
    phonecopy = phonecopy.replace("@","&eu&#&")


    phonecopy = phonecopy.replace("&euv&","@")
    phonecopy = phonecopy.replace("@","&euv&#&")
    phonecopy = phonecopy.replace("&avq","&q&av")
    phonecopy = phonecopy.replace("&av&","@")
    phonecopy = phonecopy.replace("@","&av&#&")
    phonecopy = phonecopy.replace("&q","@")
    phonecopy = phonecopy.replace("@","&q&#")

    removeList = ["&nwv&","&nnv&","&rwv&","&lwv&","&lnv&","&aav&","&iiv&","&uuv&","&rqv&","&eev&",
                "&eiv&","&ouv&","&axv&","&oov&","&aiv&","&auv&","&aev&",
                "&nnx&","&nxx&","&rrx&","&llx&","&lxx&",
                "&aa&","&iv&","&ov&","&mq&","&aa&","&ii&","&uu&","&rq&","&au&","&ee&",
                "&ei&","&ou&","&oo&","&ax&","&ai&","&ev&","&uv&","&ae&",
                "&a&","&e&","&i&","&o&","&u&"]

    for i in range(0,45):
        c1 = removeList[i]
        c2 = c1 + '#&'
        phonecopy = phonecopy.replace(c1, '@')
        phonecopy = phonecopy.replace('@', c2)

    
    phonecopy = phonecopy.replace("&#&hq&","&hq&#&")

    # //for vowel in between correction
    pureVowelList = ["&a&","&e&","&i&","&o&","&u&"]
    for i in range(0,5):
        c1 = f'&#{pureVowelList[i]}'
        phonecopy = phonecopy.replace(pureVowelList[i], '@')
        phonecopy = phonecopy.replace('@', c1)
    
    
    consonantList = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh",
                    "nx","t","th","d","dh","n","p","ph","b","bh","m","y",
                    "r","l","w","sh","sx","zh","y","s","h","lx","rx","f","dxq"]

    # // &eu&#&r&eu&#& syllabification correction

    for i in range(0,39):
        c1 = f'&eu&#&{consonantList[i]}&euv&#&'
        c2 = f'&eu&{consonantList[i]}&av&#&'
        phonecopy = phonecopy.replace(c1, '@')
        phonecopy = phonecopy.replace('@', c2)

    for i in range(0,39):
        c1 = f'&euv&#&{consonantList[i]}&euv&#&'
        c2 = f'&euv&{consonantList[i]}&av&#&'
        phonecopy = phonecopy.replace(c1, '@')
        phonecopy = phonecopy.replace('@', c2)

    phonecopy = phonecopy.replace("&eu&","@")
    phonecopy = phonecopy.replace("@","&eu&#&")
    return phonecopy


# replacement for function in lines 279 - 317. //check the word in Dict.
# REMOVED EXIT(1) ON ENGLISH. WAS USELESS
def CheckDictionary(input : str) -> int:

    fileName = GetFile(globals.langId, 1)
    if (globals.flags.DEBUG):
        print(f'dict : {fileName}')
    try:
        with open(fileName, 'r') as output:
            cnts = output.readlines()
    except:
        if globals.flags.DEBUG:
            print(f'Dict not found')
        if(globals.langId == globals.ENGLISH):
            exit(1)
        return 0

    if (globals.langId == globals.ENGLISH):
        input1 = ''
        for c in input:
            if ord(c) < 97:
                c = c.lower()
            input1 += c
        input = input1
    
    for l in cnts:
        l = l.strip().split('\t')
        assert(len(l) == 3)
        if globals.flags.DEBUG:
            print(f"word : {l[0]}\n")
        if input == l[0]:
            if globals.flags.DEBUG:
                print(f"match found")
                print(f'Syllables : {l[1]}')
                print(f'monophones : {l[2]}')
            if globals.flags.writeFormat == 1:
                WriteFile(l[1])
            if globals.flags.writeFormat == 0:
                WriteFile(l[2])
            return 1

    return 0

# replacement for function in lines 801-821. 
def PositionCorrection(phone : str, left : str, right :str, isReverse:int) -> str:

    geminateList = ["k","kh","lx","rx","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh",
    "n","p","ph","b","bh","m","y","r","l","w","sh","sx","zh","y","s","h","f","dxq"]

    phonecopy = phone
    for i in range(0,39):
        c1 = left
        c2 = right
        c1 = c1.replace('@', geminateList[i])
        c2 = c2.replace('@', geminateList[i])
        phonecopy = phonecopy.replace(c2, c1) if isReverse == 1 else phonecopy.replace(c1, c2)

    return phonecopy

# replacement for function in lines 711 - 713.
def CountChars(s : str, c : str) -> int:

    count = 0
    for x in s:
        if x == c:
            count += 1

    return count

# replacement for function in lines 719 - 744.
def GenerateAllCombinations(j : int, s : str, c : list, isRight : int):
    t = ''
    if (c[j][0][0] == '#'):
        if isRight == 1:
            globals.combvars.rightStr[globals.combvars.bi] = s + '&'
            globals.combvars.bi += 1
        else:
            globals.combvars.leftStr[globals.combvars.bi] = s + '&'
            globals.combvars.bi += 1
    else:
        i = 0
        while (c[j][i][0] != '#'):
            t = s + '&' + c[j][i]
            GenerateAllCombinations(j+1, t, c, isRight)
            i += 1

# replacement for function in lines 746 - 768.
def GenerateMatrix(combMatrix : list, regex : str):

    row = 0
    col = 0
    item = 0
    for i in range(0, len(regex)):
        if regex[i] == '&':
            combMatrix[row][col+1] = '#'
            row += 1
            col = 0
            item = 0
            combMatrix[row][col] = ''
        elif regex[i] == '|':
            col += 1
            item = 0
            combMatrix[row][col] = ''     
        else:
            combMatrix[row][col] = combMatrix[row][col][:item] + regex[i] + combMatrix[row][col][(item+1):]
            item += 1
        if globals.flags.DEBUG:
            print(f'{row} {col} {combMatrix[row][col]}')

    combMatrix[row][col+1] = '#'
    combMatrix[row+1][0] = '#'

# replacement for function in lines 770 - 799.
def CombinationCorrection(phone : str, left : str, right : str, isReverse : int) -> str:
    leftComb = [['' for _ in range(256)] for _ in range(256)]
    rightComb = [['' for _ in range(256)] for _ in range(256)]
    GenerateMatrix(leftComb, left)
    GenerateMatrix(rightComb, right)

    globals.combvars.bi = 0
    GenerateAllCombinations(0, '', leftComb, 0)
    globals.combvars.bi = 0
    GenerateAllCombinations(0, '', rightComb, 1)

    i = 0
    phonecopy = phone
    while globals.combvars.leftStr[i] != '':
        if isReverse == 1:
            phonecopy = phonecopy.replace(globals.combvars.rightStr[i], "!")
            phonecopy = phonecopy.replace("!", globals.combvars.leftStr[i])
        else:
            phonecopy = phonecopy.replace(globals.combvars.leftStr[i], "!")
            phonecopy = phonecopy.replace("!", globals.combvars.rightStr[i])

        if globals.flags.DEBUG:
            print(f'{globals.combvars.leftStr[i]} {globals.combvars.rightStr[i]}')
        
        i += 1
    
    globals.combvars.refresh()
    return phonecopy

# replacement for function in lines 825 - 930. //Language specific corrections
def LangSpecificCorrection(phone : str, langSpecFlag : int) -> str:
    phonecopy = phone

    if globals.isSouth:
        phonecopy = phonecopy.replace("&ei&","&ai&")
        phonecopy = phonecopy.replace("&eiv&","&aiv&")
    else:
        phonecopy = phonecopy.replace("&oo&","&o&")
        phonecopy = phonecopy.replace("&oov&","&ov&")

    phonecopy = phonecopy.replace("&q&","!")
    phonecopy = phonecopy.replace("!","&av&q&")

    phonecopy = phonecopy.replace("&a&av&","&a&")
    phonecopy = phonecopy.replace("&e&av&","&e&")
    phonecopy = phonecopy.replace("&i&av&","&i&")
    phonecopy = phonecopy.replace("&o&av&","&o&")
    phonecopy = phonecopy.replace("&u&av&","&u&")

    phonecopy = phonecopy.replace("&a&rqv&","&rq&")
    phonecopy = phonecopy.replace("&aa&av&","&aa&")
    phonecopy = phonecopy.replace("&ae&av&","&ae&")
    phonecopy = phonecopy.replace("&ax&av&","&ax&")
    phonecopy = phonecopy.replace("&ee&av&","&ee&")
    phonecopy = phonecopy.replace("&ii&av&","&ii&")
    phonecopy = phonecopy.replace("&ai&av&","&ai&")
    phonecopy = phonecopy.replace("&au&av&","&au&")
    phonecopy = phonecopy.replace("&oo&av&","&oo&")
    phonecopy = phonecopy.replace("&uu&av&","&uu&")
    phonecopy = phonecopy.replace("&rq&av&","&rq&")
    phonecopy = phonecopy.replace("&av&av&","&av&")
    phonecopy = phonecopy.replace("&ev&av&","&ev&")
    phonecopy = phonecopy.replace("&iv&av&","&iv&")
    phonecopy = phonecopy.replace("&ov&av&","&ov&")
    phonecopy = phonecopy.replace("&uv&av&","&uv&")

    phonecopy = phonecopy.replace("&av&rqv&","&rqv&")
    phonecopy = phonecopy.replace("&aav&av&","&aav&")
    phonecopy = phonecopy.replace("&aev&av&","&aev&")
    phonecopy = phonecopy.replace("&auv&av&","&auv&")
    phonecopy = phonecopy.replace("&axv&av&","&axv&")
    phonecopy = phonecopy.replace("&aiv&av&","&aiv&")
    phonecopy = phonecopy.replace("&eev&av&","&eev&")
    phonecopy = phonecopy.replace("&eiv&av&","&eiv&")
    phonecopy = phonecopy.replace("&iiv&av&","&iiv&")
    phonecopy = phonecopy.replace("&oov&av&","&oov&")
    phonecopy = phonecopy.replace("&ouv&av&","&ouv&")
    phonecopy = phonecopy.replace("&uuv&av&","&uuv&")
    phonecopy = phonecopy.replace("&rqv&av&","&rqv&")

    if langSpecFlag == 0:
        return phonecopy
    
    fileName = GetFile(globals.langId, 2)
    with open(fileName, 'r') as output:
        cnts = output.readlines()

    left = ''
    right = ''
    phonecopy = '^' + phonecopy + '$'

    if (globals.flags.DEBUG):
        print(f'phone : {phonecopy}')
    
    for l in cnts:
        l = l.strip()
        if (l.find('#') != -1):
            continue
        
        l = l.split('\t')
        assert(len(l) == 2)
        left, right = l[0], l[1]

        if left.find('|') != -1:
            a1 = left[1:-1]
            a2 = right[1:-1]
            phonecopy = CombinationCorrection(phonecopy, a1, a2, 0)
            if globals.flags.DEBUG:
                print(f'{a1}\t{a2}')
        elif left.find('@') != -1:
            phonecopy = PositionCorrection(phonecopy, left, right, 0)
        else:
            phonecopy = phonecopy.replace(left, '!')
            phonecopy = phonecopy.replace('!', right)

    # //remove head and tail in phone
    phonecopy = phonecopy.replace('^', '')
    phonecopy = phonecopy.replace('$', '')
    # //end correction
    count = 0
    for i in range(len(phonecopy)):
        if phonecopy[i] == '&':
            count = i
    return phonecopy[:(count+1)]


# Replacement for function in lines 934 - 991. //Reverse syllable correction for syllable parsing
def SyllableReverseCorrection(phone : str, langSpecFlag : int) -> str:
    phonecopy = phone

    if globals.isSouth:
        phonecopy = phonecopy.replace("&ai&","&ei&")
        phonecopy = phonecopy.replace("&aiv&","&eiv&")
    else:
        phonecopy = phonecopy.replace("&o&","&oo&")
        phonecopy = phonecopy.replace("&ov&","&oov&")
    
    if langSpecFlag == 0:
        return phonecopy

    fileName = GetFile(globals.langId, 2)
    with open(fileName, 'r') as output:
        cnts = output.readlines()

    left = ''
    right = ''
    # //update head and tail in phone
    phonecopy = '^' + phonecopy + '$'

    if globals.flags.DEBUG:
        print(f'before phone : {phonecopy}')
    
    for l in cnts:
        l = l.strip()
        if (l.find('#') != -1):
            continue
        
        l = l.split('\t')
        assert(len(l) == 2)
        left, right = l[0], l[1]

        if left.find('|') != -1:
            a1 = left[1:-1]
            a2 = right[1:-1]
            phonecopy = CombinationCorrection(phonecopy, a1, a2, 1)
            if globals.flags.DEBUG:
                print(f'{a1}\t{a2}')
        elif left.find('@') != -1:
            phonecopy = PositionCorrection(phonecopy, left, right, 1)
        else:
            phonecopy = phonecopy.replace(right, '!')
            phonecopy = phonecopy.replace('!', left)

    # //remove head and tail in phone
    phonecopy = phonecopy.replace('^', '')
    phonecopy = phonecopy.replace('$', '')
    # //end correction
    if (globals.flags.DEBUG):
        print(f'after phone : {phonecopy}')
    return phonecopy

# //language specific syllable correction
def LangSyllableCorrection(input : str) -> int:
    if input == "&av&q&":
        return 1
    else:
        return 0

# replacement for function in lines 1000 - 1160. //split into syllable array
def SplitSyllables(input : str) -> int:
    incopy = input

    if globals.flags.writeFormat == 2:
        i = 0
        j = 0
        fullList = ["k","kh","lx","rx","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m","y","r","l","w","sh","sx","zh","y","s","h","f","dxq"]

        for i in range(0,39):
            for j in range(0,39):
                c1 = f'&{fullList[i]}&{fullList[j]}&'
                c2 = f'&{fullList[i]}&euv&#&{fullList[j]}&'
                incopy = incopy.replace(c1, '@')
                incopy = incopy.replace('@', c2)
        
        incopy = incopy.replace("&#&mq&","&mq&")
        incopy = incopy.replace("&#&q&","&q&")


    pch = incopy.split('#')
    globals.syllableList = []
    for c in pch:
        if c != '&':
            globals.syllableList.append(c)
    
    # ln -> len
    ln = len(globals.syllableList)

    if globals.flags.DEBUG:
        for i in range(ln):
            print(f"initStack : {globals.syllableList[i]}\n")
    
    # //south specific av addition
    if CheckVowel(globals.syllableList[ln-1],1,0) == 0 and CheckChillu(globals.syllableList[ln-1]) == 0:
        if globals.isSouth:
            globals.syllableList[ln-1] += '&av&'
        else:
            globals.syllableList[ln-1] += '&euv&'

    # //round 2 correction

    if globals.flags.writeFormat == 2:
        globals.syllableCount = ln
        globals.flags.writeFormat = 1
        return 1

    euFlag = 1
    if ln > 1:
        for i in range(ln-1,-1,-1):
            if LangSyllableCorrection(globals.syllableList[i]) == 1:
                globals.syllableList[i-1] += globals.syllableList[i]
                globals.syllableList[i] = ''

            if globals.syllableList[i].find("&eu&") != -1:
                globals.syllableList[i] = globals.syllableList[i].replace("&eu&", "!")
                euFlag = 1

            if globals.syllableList[i].find("&euv&") != -1:
                globals.syllableList[i] = globals.syllableList[i].replace("&euv&", "!")
                euFlag = 2
            
            if CheckVowel(globals.syllableList[i],0,1) == 0:
                if i-1 >= 0:
                    globals.syllableList[i-1] += globals.syllableList[i]
                    globals.syllableList[i] = ''
                else:
                    globals.syllableList[i] += globals.syllableList[i+1]
                    globals.syllableList[i+1] = ''
            
            if i-1 > 0:
                if euFlag == 1:
                    globals.syllableList[i-1] = globals.syllableList[i-1].replace("!","&eu&")
                elif euFlag == 2:
                    globals.syllableList[i-1] = globals.syllableList[i-1].replace("!","&euv&")
                globals.syllableList[i-1] = globals.syllableList[i-1].replace("&&","&")
            
            if euFlag == 1:
                globals.syllableList[i] = globals.syllableList[i].replace("!","&eu&")
            elif euFlag == 2:
                globals.syllableList[i] = globals.syllableList[i].replace("!","&euv&")
    else:
        print(f" syll 0 {globals.syllableList[0]}")
        if (CheckVowel(globals.syllableList[0],1,0) == 0 and globals.flags.writeFormat != 3) or Checkeuv(globals.syllableList[0]) == 1:
            globals.syllableList[0] += '&av'

    if globals.flags.DEBUG:
        for i in range(ln):
            print(f'syllablifiedStack : {globals.syllableList[i]}')

    # //round 3 double syllable correction
    for i in range(ln):

        # //corrections
        globals.syllableList[i] = globals.syllableList[i].replace('1','')
        if globals.flags.DEBUG:
            print(f'LenStack : {len(globals.syllableList[i])}')
        
        if len(globals.syllableList[i]) > 0:
            if globals.syllableList[i].find("&eu&") != -1:
                globals.syllableList[i] = globals.syllableList[i].replace("&eu&", "!")
                euFlag = 1

            if globals.syllableList[i].find("&euv&") != -1:
                globals.syllableList[i] = globals.syllableList[i].replace("&euv&", "!")
                euFlag = 2
            
            if CheckVowel(globals.syllableList[i],0,1) == 0 and globals.flags.writeFormat != 3:
                if globals.flags.DEBUG:
                    print(f'Stack : {globals.syllableList[i]}')
                globals.syllableList[i] += '&av'
            
            if globals.syllableList[i].find('!') != -1:
                if euFlag == 1:
                    globals.syllableList[i] = globals.syllableList[i].replace("!","&eu&")
                elif euFlag == 2:
                    globals.syllableList[i] = globals.syllableList[i].replace("!","&euv&")
                globals.syllableList[i] = globals.syllableList[i].replace('!', 'eu')
        
        if globals.syllableList[i].find('&&') != -1:
            globals.syllableList[i] = globals.syllableList[i].replace('&&', '&')
        
        globals.syllableList[i] = GeminateCorrection(globals.syllableList[i],1)
    
    if globals.flags.DEBUG:
        for i in range(ln):
            print(f'syllablifiedStack1 : {globals.syllableList[i]}')
        print(f'No of syllables : {ln}')

    globals.syllableCount = ln

    if globals.flags.writeFormat == 3:
        globals.flags.writeFormat = 0
    
    return 1


# replacement for function in lines 1164 - 1275. //make to write format
def WritetoFiles() -> int:

    if globals.flags.DEBUG:
        for i in range(0,globals.syllableCount):
            print(f'syllablifiedStackfinal : {globals.syllableList[i]}')
    
    validSyllable = 0
    for i in range(0,globals.syllableCount):
        if globals.syllableList[i] != '':
            validSyllable += 1
    
    if globals.flags.DEBUG:
        print(f'a correction {globals.syllableList[0]}')
    
    globals.words.outputText = ''

    # //phone
    j = 0
    if globals.flags.writeFormat == 0:
        syllablesPrint = 0
        for i in range(globals.syllableCount):
            globals.words.outputText += '(( '
            for pch in l:
                if pch == '':
                    continue
                if globals.flags.DEBUG:
                    print(f'syl  output{pch} {globals.words.outputText}')
                j = 1
                globals.words.outputText += f'"{pch}" '
            if j != 0:
                if globals.flags.syllTagFlag != 0:
                    if syllablesPrint == 0:
                        globals.words.outputText += '_beg'
                    elif syllablesPrint == validSyllable - 1:
                        globals.words.outputText += '_end'
                    else:
                        globals.words.outputText += '_mid'
                    syllablesPrint += 1
                globals.words.outputText += ') 0) '
            else:
                globals.words.outputText = globals.words.outputText[:(len(globals.outputText) - 3)]
            j = 0
    
        globals.words.outputText = globals.words.outputText.replace('v', '')
        globals.words.outputText = globals.words.outputText.replace('"eu"', '')
        globals.words.outputText = globals.words.outputText.replace('!', '')
    
    # //syllable
    elif globals.flags.writeFormat == 1:
        syllablesPrint = 0
        for i in range(globals.syllableCount):
            globals.syllableList[i] = globals.syllableList[i].replace('euv', 'eu')
            globals.syllableList[i] = SyllableReverseCorrection(globals.syllableList[i], globals.flags.LangSpecificCorrectionFlag)
            if globals.flags.DEBUG:
                print(f'{globals.syllableList[i]}')
            globals.words.outputText += '(( "'
            l = globals.syllableList[i].split('&')
            for pch in l:
                if pch == '':
                    continue
                if globals.flags.DEBUG:
                    print(f'syl {pch}')
                j = 1
                if CheckSymbol(pch) != 0:
                    globals.words.outputText += GetUTF(pch)
                    if pch == 'av' and globals.flags.DEBUG:
                        print('av found')
            if j != 0:
                if globals.flags.syllTagFlag != 0:
                    if syllablesPrint == 0:
                        globals.words.outputText += '_beg'
                    elif syllablesPrint == validSyllable - 1:
                        globals.words.outputText += '_end'
                    else:
                        globals.words.outputText += '_mid'
                    syllablesPrint += 1
                globals.words.outputText += '" ) 0) '
            else:
                globals.words.outputText = globals.words.outputText[:(len(globals.words.outputText) - 4)]
            j = 0
    
    globals.words.outputText = globals.words.outputText.replace('#', '')
    if globals.flags.DEBUG:
        print(f'Print text : {globals.words.outputText}')
    
    WriteFile(globals.words.outputText)
    return 1