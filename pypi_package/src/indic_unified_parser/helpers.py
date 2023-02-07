import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from globals import *
# contains helper functions used in parser.py

# repeated replacement of a subtring sub with tar in input until no change happens
def rec_replace(input : str, sub : str, tar : str):
    while True:
        output = input.replace(sub, tar)
        if output == input:
            break
        input = output
    return output

# function - RemoveUnwanted() - referenced in lines 63 - 109 of unified.y
def RemoveUnwanted(input : str) -> str:
    # ignore punctuations
    punctuationList = ["!",";",":","@","#","$","%","^","&","*",",",".","/","'","’","”","“","।", "]", "["]

    # replacing problematic unicode characters that look the same but have different encodings.
    # punjabi update 
    replaceDict =    {"ऩ":"ऩ", "ऱ":"ऱ", "क़":"क़", "ख़":"ख़", "ग़":"ग़", "ज़":"ज़", "ड़":"ड़", "ढ़":"ढ़", "ढ़":"ढ़", "फ़":"फ़", "य़":"य़", "ऴ":"ऴ",
   "ொ":"ொ", "ோ":"ோ",
   "ൊ":"ൊ", "ോ":"ോ", "ല്‍‌":"ൽ", "ള്‍":"ൾ", "ര്‍":"ർ", "ന്‍":"ൻ", "ണ്‍":"ൺ"}

    output = ""
    for c in input:
        if c in punctuationList: 
            continue
        output += c
    
    for k in replaceDict.keys():
        output = rec_replace(output, k, replaceDict[k])
    return output

# function to replace GetFile in lines 132 - 156 of unified.y
# gives the filename according to language and type
def GetFile(g : GLOBALS, LangId : int, type : int) -> str:
    fileName = g.rootPath

    # return common file that contains the CPS mapping
    if type == 0:
        fileName += g.commonFile
        return fileName
    
    elif type == 1:
        fileName += "dict/"
    
    elif type == 2:
        fileName += "rules/"

    langIdNameMapping = { 1 : "malayalam", 2 : "tamil", 3 : "telugu",
        4 : "kannada", 5 : "hindi", 6 : "bengali",
        7 : "gujarathi", 8 : "odiya", 9 : "punjabi", 10 : "english" }
    
    if LangId in langIdNameMapping.keys():
        fileName += langIdNameMapping[LangId]
    
    if type == 1:
        fileName += ".dict"
    elif type == 2:
        fileName += ".rules"
    
    return fileName

# function to replace SetlangId in lines 62-80 of unified.y
def SetlangId(g : GLOBALS, fl : str):
    id = ord(fl)
    if(id>=3328 and id<=3455):
        g.currLang = g.MALAYALAM; #malayalam
    elif(id>=2944 and id<=3055):
        g.currLang = g.TAMIL; #tamil
    elif(id>=3202 and id<=3311):
        g.currLang = g.KANNADA; #KANNADA
    elif(id>=3072 and id<=3198):
        g.currLang = g.TELUGU; #telugu
    elif(id>=2304 and id<=2431):
        g.currLang = g.HINDI; #hindi
    elif(id>=2432 and id<=2559):
        g.currLang = g.BENGALI; #BENGALI
    elif(id>=2688 and id<=2815):
        g.currLang = g.GUJARATHI; #gujarathi
    elif(id>=2816 and id<=2943):
        g.currLang = g.ODIYA; #odia
    elif(id>=2560 and id <= 2687): # punjabi
        g.currLang = g.PUNJABI
    elif(id>=64 and id<=123):
        g.currLang = g.ENGLISH; #english

    g.langId = g.currLang

    if(g.langId < 5):
        g.isSouth = 1
    if(g.langId == 0):
        print(f"UNKNOWN LANGUAGE - id = {fl}")
        exit(0)
    return 1

# replacement for function in lins 158 - 213. Sets the lanuage features
def SetlanguageFeat(g : GLOBALS, input : str) -> int:

    # # open common file
    # try:
    #     with open(GetFile(g, 0,0), 'r') as infile:
    #         lines = infile.readlines()
    # except:
    #     print("Couldn't open common file for reading")
    #     return 0

    lines = ['0\t$\t#\t#\t#\t#\tऀ\t#\t#\t#\t#\n',
            '1\tmq\t#\t#\t#\t#\tँ\tঁ\tઁ\tଁ\tਁ\n',
            '2\tq\tം\tஂ\tం\tಂ\tं\tং\tં\tଂ\tਂ\n',
            '3\thq\tഃ\tஃ\tః\tಃ\tः\tঃ\tઃ\tଃ\tਃ\n',
            '4\t$\t#\t#\t#\t#\tऄ\t#\t#\t#\t#\n',
            '5\ta\tഅ\tஅ\tఅ\tಅ\tअ\tঅ\tઅ\tଅ\tਅ\n',
            '6\taa\tആ\tஆ\tఆ\tಆ\tआ\tআ\tઆ\tଆ\tਆ\n',
            '7\ti\tഇ\tஇ\tఇ\tಇ\tइ\tই\tઇ\tଇ\tਇ\n',
            '8\tii\tഈ\tஈ\tఈ\tಈ\tई\tঈ\tઈ\tଈ\tਈ\n',
            '9\tu\tഉ\tஉ\tఉ\tಉ\tउ\tউ\tઉ\tଉ\tਉ\n',
            '10\tuu\tഊ\tஊ\tఊ\tಊ\tऊ\tঊ\tઊ\tଊ\tਊ\n',
            '11\trq\tഋ\t#\tఋ\tಋ\tऋ\tঋ\tઋ\tଋ\t#\n',
            '12\t$\t#\t#\t#\t#\tऌ\tঌ\tઌ\tଌ\t#\n',
            '13\tae\t#\t#\t#\t#\tऍ\t#\tઍ\t#\t#\n',
            '14\te\tഎ\tஎ\tఎ\tಎ\tऎ\t#\t#\t#\t#\n',
            '15\tee\tഏ\tஏ\tఏ\tಏ\tए\tএ\tએ\tଏ\tਏ\n',
            '16\tei\tഐ\tஐ\tఐ\tಐ\tऐ\tঐ\tઐ\tଐ\tਐ\n',
            '17\tax\t#\t#\t#\t#\tऑ\t#\tઑ\t#\t#\n',
            '18\to\tഒ\tஒ\tఒ\tಒ\tऒ\t#\t#\t#\t#\n',
            '19\too\tഓ\tஓ\tఓ\tಓ\tओ\tও\tઓ\tଓ\tਓ\n',
            '20\tou\tഔ\tஔ\tఔ\tಔ\tऔ\tঔ\tઔ\tଔ\tਔ\n',
            '21\tk\tക\tக\tక\tಕ\tक\tক\tક\tକ\tਕ\n',
            '22\tkh\tഖ\t#\tఖ\tಖ\tख\tখ\tખ\tଖ\tਖ\n',
            '23\tg\tഗ\t#\tగ\tಗ\tग\tগ\tગ\tଗ\tਗ\n',
            '24\tgh\tഘ\t#\tఘ\tಘ\tघ\tঘ\tઘ\tଘ\tਘ\n',
            '25\tng\tങ\tங\tఙ\tಙ\tङ\tঙ\tઙ\tଙ\tਙ\n',
            '26\tc\tച\tச\tచ\tಚ\tच\tচ\tચ\tଚ\tਚ\n',
            '27\tch\tഛ\t#\tఛ\tಛ\tछ\tছ\tછ\tଛ\tਛ\n',
            '28\tj\tജ\tஜ\tజ\tಜ\tज\tজ\tજ\tଜ\tਜ\n',
            '29\tjh\tഝ\t#\tఝ\tಝ\tझ\tঝ\tઝ\tଝ\tਝ\n',
            '30\tnj\tഞ\tஞ\tఞ\tಞ\tञ\tঞ\tઞ\tଞ\tਞ\n',
            '31\ttx\tട\tட\tట\tಟ\tट\tট\tટ\tଟ\tਟ\n',
            '32\ttxh\tഠ\t#\tఠ\tಠ\tठ\tঠ\tઠ\tଠ\tਠ\n',
            '33\tdx\tഡ\t#\tడ\tಡ\tड\tড\tડ\tଡ\tਡ\n',
            '34\tdxh\tഢ\t#\tఢ\tಢ\tढ\tঢ\tઢ\tଢ\tਢ\n',
            '35\tnx\tണ\tண\tణ\tಣ\tण\tণ\tણ\tଣ\tਣ\n',
            '36\tt\tത\tத\tత\tತ\tत\tত\tત\tତ\tਤ\n',
            '37\tth\tഥ\t#\tథ\tಥ\tथ\tথ\tથ\tଥ\tਥ\n',
            '38\td\tദ\t#\tద\tದ\tद\tদ\tદ\tଦ\tਦ\n',
            '39\tdh\tധ\t#\tధ\tಧ\tध\tধ\tધ\tଧ\tਧ\n',
            '40\tn\tന\tந\tన\tನ\tन\tন\tન\tନ\tਨ\n',
            '41\tnd\tഩ\tன\t#\t#\tऩ\t#\t#\t#\t#\n',
            '42\tp\tപ\tப\tప\tಪ\tप\tপ\tપ\tପ\tਪ\n',
            '43\tph\tഫ\t#\tఫ\tಫ\tफ\tফ\tફ\tଫ\tਫ\n',
            '44\tb\tബ\t#\tబ\tಬ\tब\tব\tબ\tବ\tਬ\n',
            '45\tbh\tഭ\t#\tభ\tಭ\tभ\tভ\tભ\tଭ\tਭ\n',
            '46\tm\tമ\tம\tమ\tಮ\tम\tম\tમ\tମ\tਮ\n',
            '47\ty\tയ\tய\tయ\tಯ\tय\tয\tય\tୟ\tਯ\n',
            '48\tr\tര\tர\tర\tರ\tर\tর\tર\tର\tਰ\n',
            '49\trx\tറ\tற\t#\t#\tऱ\t#\t#\t#\t#\t\n',
            '50\tl\tല\tல\tల\tಲ\tल\tল\tલ\tଲ\tਲ\n',
            '51\tlx\tള\tள\tళ\tಳ\tळ\t#\tળ\tଳ\tਲ਼\n',
            '52\tzh\tഴ\tழ\t#\t#\tऴ\t#\t#\t#\t#\n',
            '53\tw\tവ\tவ\tవ\tವ\tव\t#\tવ\tଵ\tਵ\n',
            '54\tsh\tശ\tஶ\tశ\tಶ\tश\tশ\tશ\tଶ\tਸ਼\n',
            '55\tsx\tഷ\tஷ\tష\tಷ\tष\tষ\tષ\tଷ\t#\n',
            '56\ts\tസ\tஸ\tస\tಸ\tस\tস\tસ\tସ\tਸ\n',
            '57\th\tഹ\tஹ\tహ\tಹ\tह\tহ\tહ\tହ\tਹ\n',
            '58\t$\t#\t#\t#\t#\tऺ\t#\t#\t#\t#\n',
            '59\t$\t#\t#\t#\t#\tऻ\t#\t#\t#\t#\n',
            '60\tnk\t#\t#\t#\t#\t़\t়\t઼\t଼\t਼\n',
            '61\tag\t#\t#\t#\t#\tऽ\tঽ\tઽ\tଽ\t#\n',
            '62\taav\tാ\tா\tా\tಾ\tा\tা\tા\tା\tਾ\n',
            '63\tiv\tി\tி\tి\tಿ\tि\tি\tિ\tି\tਿ\n',
            '64\tiiv\tീ\tீ\tీ\tೀ\tी\tী\tી\tୀ\tੀ\n',
            '65\tuv\tു\tு\tు\tು\tु\tু\tુ\tୁ\tੁ\n',
            '66\tuuv\tൂ\tூ\tూ\tೂ\tू\tূ\tૂ\tୂ\tੂ\n',
            '67\trqv\tൃ\t#\tృ\tೃ\tृ\tৃ\tૃ\tୃ\t#\n',
            '68\trqwv\tൄ\t#\tౄ\tೄೄ\tॄ\tৄ\tૄ\t#\t#\n',
            '69\taev\t#\t#\t#\t#\tॅ\t#\t#\t#\t#\n',
            '70\tev\tെ\tெ\tె\tೆೆ\tॆ\t#\t#\tୄ\t#\n',
            '71\teev\tേ\tே\tే\tೇ\tे\tে\tે\tେ\tੇ\n',
            '72\teiv\tൈ\tை\tై\tೇೈ\tै\tৈ\tૈ\tୈ\tੈ\n',
            '73\taxv\t#\t#\t#\t#\tॉ\t#\tૉ\t#\t#\n',
            '74\tov\tൊ\tொ\tొ\tೊ\tॊ\t#\t#\t#\t#\n',
            '75\toov\tോ\tோ\tో\tೋ\tो\tো\tો\tୋ\tੋ\n',
            '76\touv\tൌ\tௌ\tౌ\tೌ\tौ\tৌ\tૌ\tୌ\tੌ\n',
            '77\teu\t്\t்\t్\t್\t्\t্\t્\t୍\t੍\n',
            '78\ttv\t#\t#\t#\t#\tॎ\tৎ\t#\t#\t#\n',
            '79\t$\t#\t#\t#\t#\tॏ\t#\t#\t#\t#\n',
            '80\t$\t#\t#\t#\t#\tॐ\t#\tૐ\t#\tੴ\n',
            '81\t$\t#\t#\t#\t#\t॓\t#\t#\t#\t#\n',
            '82\t$\t#\t#\t#\t#\t॔\t#\t#\t#\t#\n',
            '83\t$\t#\t#\t#\t#\t#\t#\t#\t#\t#\n',
            '84\t$\t#\t#\t#\t#\t#\t#\t#\t#\t#\n',
            '85\t$\t#\t#\t#\t#\tॕ\t#\t#\t#\t#\n',
            '86\t$\t#\t#\t#\t#\tॖ\t#\t#\tୖ\t#\n',
            '87\tauv\tൗ\t#\t#\t#\tॗ\tৗ\t#\tୗ\t#\n',
            '88\tkq\t#\t#\t#\t#\tक़\t#\t#\t#\t#\n',
            '89\tkhq\t#\t#\t#\t#\tख़\t#\t#\t#\tਖ਼\n',
            '90\tgq\t#\t#\t#\t#\tग़\t#\t#\t#\tਗ਼\n',
            '91\tz\t#\t#\t#\t#\tज़\t#\t#\t#\tਜ਼\n',
            '92\tdxq\t#\t#\t#\t#\tड़\tড়\t#\tଡ଼\tੜ\n',
            '93\tdxhq\t#\t#\t#\t#\tढ़\tঢ়\t#\tଢ଼\t#\n',
            '94\tf\t#\t#\t#\t#\tफ़\t#\t#\t#\tਫ਼\n',
            '95\ty\t#\t#\t#\t#\tय़\tয়\t#\tୟ\t#\n',
            '96\trqw\t#\t#\t#\t#\tॠ\tৠ\tૠ\tୠ\t#\n',
            '97\t$\t#\t#\t#\t#\tॡ\tৡ\tૡ\tୡ\t#\n',
            '98\t$\t#\t#\t#\t#\tॢ\tৢ\tૢ\t#\t#\n',
            '99\t$\t#\t#\t#\t#\tॣ\tৣ\tૣ\tୢ\t#\n',
            '100\t$\t#\t#\t#\t#\t।\t#\t#\t#\t#\n',
            '101\t$\t#\t#\t#\t#\t॥\t#\t#\tୣ\t#\n',
            '102\t$\t#\t#\t#\t#\t०\t০\t૦\t୦\t੦\n',
            '103\t$\t#\t#\t#\t#\t१\t১\t૧\t୧\t੧\n',
            '104\t$\t#\t#\t#\t#\t२\t২\t૨\t୨\t੨\n',
            '105\t$\t#\t#\t#\t#\t३\t৩\t૩\t୩\t੩\t\n',
            '106\t$\t#\t#\t#\t#\t४\t৪\t૪\t୪\t੪\n',
            '107\t$\t#\t#\t#\t#\t५\t৫\t૫\t୫\t੫\n',
            '108\t$\t#\t#\t#\t#\t६\t৬\t૬\t୬\t੬\n',
            '109\t$\t#\t#\t#\t#\t७\t৭\t૭\t୭\t੭\n',
            '110\t$\t#\t#\t#\t#\t८\t৮\t૮\t୮\t੮\n',
            '111\t$\t#\t#\t#\t#\t९\t৯\t૯\t୯\t੯\n',
            '112\trv\t#\t#\t#\t#\t॰\tৰ\t૰\t୰\t#\n',
            '113\twv\t#\t#\t#\t#\tॱ\tৱ\t૱\tୱ\t#\n',
            '114\t$\t#\t#\t#\t#\tॲ\t৲\t#\t୲\t#\n',
            '115\t$\t#\t#\t#\t#\tॳ\t৳\t#\t୳\t#\n',
            '116\t$\t#\t#\t#\t#\tॴ\t৴\t#\t୴\t#\n',
            '117\t$\t#\t#\t#\t#\tॵ\t৵\t#\t୵\t#\n',
            '118\t$\t#\t#\t#\t#\tॶ\t৶\t#\t୶\t#\n',
            '119\t$\t#\t#\t#\t#\tॷ\t৷\t#\t୷\t#\n',
            '120\t$\t#\t#\t#\t#\tॸ\t৸\t#\t#\t#\n',
            '121\t$\t#\t#\t#\t#\tॹ\t৹\t#\t#\t#\n',
            '122\tnwv\tൺ\t#\t#\t#\tॺ\t৺\t#\t#\t#\n',
            '123\tnnv\tൻ\t#\t#\t#\tॻ\t৻\t#\t#\t#\n',
            '124\trwv\tർ\t#\t#\t#\tॼ\t#\t#\t#\t#\n',
            '125\tlwv\tൽ\t#\t#\t#\tॽ\t#\t#\t#\t#\n',
            '126\tlnv\tൾ\t#\t#\t#\tॾ\t#\t#\t#\t#\n',
            '127\t$\t#\t#\t#\t#\tॿ\t#\t#\t#\t#']

    str1 = input
    length = len(str1)
    if (length == 0):
        length = 1

    for j in range(0,length):
        # for skipping invisible char
        if (ord(str1[j]) < 8204):
            firstLet = str1[j]
            break
    
    SetlangId(g, firstLet) # set global langId
    for i in range(len(lines)):
        l = lines[i].strip().split('\t')
        g.symbolTable[i][1] = l[1]
        g.symbolTable[i][0] = l[1 + g.langId]

    return 1

# replacement for function in lines 52 - 59. Check if symbol is in symbolTable
def CheckSymbol(g : GLOBALS, input : str) -> int:
    i = 0
    for i in range(g.ROW):
        if (g.symbolTable[i][1] == input):
            return 1
    return 0

# replacement for function in lines 249 - 276. Convert utf-8 to cps symbols
def ConvertToSymbols(g : GLOBALS, input : str) -> str:
    str1 = input

    g.words.syllabifiedWord = "&"
    for j in range(len(str1)):
        if (ord(str1[j]) < 8204):
            g.words.syllabifiedWord += "&" + g.symbolTable[ord(str1[j])%128][1]

    g.words.syllabifiedWord = g.words.syllabifiedWord[1:]
    return g.words.syllabifiedWord 

# function in lines 1278 - 1299. save answer in g.answer
def WriteFile(g : GLOBALS, text : str):
    g.answer = f"(set! wordstruct '( {text}))"

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
    if (q != 0 and input == 'q'):
        return 1
    return 0

# function in lines 616 - 629. get the type of phone in the position
def GetPhoneType(g : GLOBALS, input : str, pos : int) -> int:
    phone = input
    phone = phone.split('&')
    phone = list(filter(lambda x : x != '', phone))
    pos = min(pos, len(phone))
    pch = phone[pos - 1]
    
    if (g.flags.DEBUG):
        print(f'input : {input}')
        print(f"str : {pch} {GetType(g, pch)}")

    return GetType(g, pch)

# function in lines 631 - 637. get the type of given input
def GetType(g : GLOBALS, input : str):
    for i in range(g.VOWELSSIZE):
        if g.VOWELS[i] == input:
            return 1
    for i in range(g.CONSONANTSSIZE):
        if g.CONSONANTS[i] == input:
            return 2
    for i in range(g.SEMIVOWELSSIZE):
        if g.SEMIVOWELS[i] == input:
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
def GetUTF(g : GLOBALS, input : str) -> str :
    for i in range(g.ROW):
        if (input == g.symbolTable[i][1]):
            return g.symbolTable[i][0]
    
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
    phonecopy = rec_replace(phonecopy, '$','')
    phonecopy = rec_replace(phonecopy, '&&','&')
    return phonecopy

# replacement for funciton in lines 321 - 356. Correct if there is a vowel in the middle
def MiddleVowel(g : GLOBALS, phone : str) -> str:

    c1 = ''
    c2 = ''
    phonecopy = phone
    for i in range(g.CONSONANTSSIZE):
        for j in range(g.VOWELSSIZE):
            c1 = f'&{g.CONSONANTS[i]}&{g.VOWELS[j]}&'
            c2 = f'&{g.CONSONANTS[i]}&av&{g.VOWELS[j]}&'

            phonecopy = phonecopy.replace(c1, c2)

    for i in range(g.SEMIVOWELSSIZE):
        for j in range(g.VOWELSSIZE):
            c1 = f'&{g.SEMIVOWELS[i]}&{g.VOWELS[j]}&'
            c2 = f'&{g.SEMIVOWELS[i]}&av&{g.VOWELS[j]}&'

            phonecopy = phonecopy.replace(c1, c2)

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
            phonecopy = phonecopy.replace(c1, c2)

    phonecopy = rec_replace(phonecopy, "&#&hq&","&hq&#&")
    phonecopy = rec_replace(phonecopy, "&&","&")
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
                phonecopy = phonecopy.replace(c1, c2)
    phonecopy = rec_replace(phonecopy, "$","")
    return phonecopy

# replacement for function in lines 498 - 585. //halant specific correction for aryan langs
def SchwaSpecificCorrection(g : GLOBALS, phone : str) -> str:
    schwaList = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh",
    "nx","t","th","d","dh","n","p","ph","b","bh","m","y",
    "r","l","s","w","sh","sx","zh","h","lx","rx","f","dxq"]

    vowelList = ["av&","nwv&","nnv&","rwv&","lwv&","lnv&","aav&","iiv&","uuv&","rqv&","eev&","eiv&","ouv&",
    "axv&","oov&","aiv&","nnx&","nxx&","rrx&","llx&","lxx&",
    "aa&","iv&","ov&","mq&","aa&","ii&","uu&","rq&",
    "ee&","ei&","ou&","oo&","ax&","ai&","ev&","uv&",
    "a&","e&","i&","o&","u&"]

    if (g.flags.DEBUG):
        print(f'{len(phone)}')
    
    phonecopy = phone + '!'

    if (g.flags.DEBUG):
        print(f'phone cur - {phonecopy}')
    
    # // for end correction &av&t&aav&. //dont want av
    for i in range(0,38):
        for j in range(1,42):
            c1 = f'&av&{schwaList[i]}&{vowelList[j]}!'
            c2 = f'&euv&{schwaList[i]}&{vowelList[j]}!'
            phonecopy = phonecopy.replace(c1, c2)
    
    phonecopy = rec_replace(phonecopy, '!', '')

    for i in range(0,38):
        c1 = f'&av&{schwaList[i]}&av&'
        c2 = f'&euv$&{schwaList[i]}&av$&'
        phonecopy = phonecopy.replace(c1, c2)

    if(g.flags.DEBUG):
        print(f"inside schwa {phonecopy}")
    
    for i in range(0,38):
        c1 = f'&av&{schwaList[i]}&'
        c3 = f'&{schwaList[i]}&'

        for j in range(0,41):
            c4 = f'&euv&{c3}${vowelList[j]}'
            c2 = f'{c1}{vowelList[j]}'
            phonecopy = phonecopy.replace(c2, c4)

    phonecopy = rec_replace(phonecopy, '$', '')

    #//&q&w&eu& - CORRECTED TO 38 - CHECK
    for i in range(0,38):
        c1 = f'&q&{schwaList[i]}&euv&'
        c2 = f'&q&{schwaList[i]}&av&'
        phonecopy = phonecopy.replace(c1, c2)

    return phonecopy

# replacement for function in lines . //correct the geminate syllabification ,isReverse --reverse correction
def GeminateCorrection(phone : str, isReverse : int) -> str:
    geminateList = ["k","kh","lx","rx","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m","y",
    "r","l","w","sh","sx","zh","y","s","h","f","dxq"]

    phonecopy = phone
    for i in range(0, 39):
        c1 = f'&{geminateList[i]}&eu&{geminateList[i]}&'
        c2 = f'&{geminateList[i]}&{geminateList[i]}&'
        phonecopy = rec_replace(phonecopy, c2, c1) if isReverse != 0 else rec_replace(phonecopy, c1, c2)
    
    return phonecopy

# replacement for function in  lines 356 - 430.  //Syllabilfy the words
def Syllabilfy(phone : str) -> str:

    phonecopy = phone
    phonecopy = rec_replace(phonecopy, "&&","&")
    phonecopy = phonecopy.replace("&eu&","&eu&#&")
    phonecopy = phonecopy.replace("&euv&","&euv&#&")
    phonecopy = rec_replace(phonecopy, "&avq","&q&av")
    phonecopy = phonecopy.replace("&av&","&av&#&")
    phonecopy = phonecopy.replace("&q","&q&#")

    removeList = ["&nwv&","&nnv&","&rwv&","&lwv&","&lnv&","&aav&","&iiv&","&uuv&","&rqv&","&eev&",
                "&eiv&","&ouv&","&axv&","&oov&","&aiv&","&auv&","&aev&",
                "&nnx&","&nxx&","&rrx&","&llx&","&lxx&",
                "&aa&","&iv&","&ov&","&mq&","&aa&","&ii&","&uu&","&rq&","&au&","&ee&",
                "&ei&","&ou&","&oo&","&ax&","&ai&","&ev&","&uv&","&ae&",
                "&a&","&e&","&i&","&o&","&u&"]

    for i in range(0,45):
        c1 = removeList[i]
        c2 = c1 + '#&'
        phonecopy = phonecopy.replace(c1, c2)
    phonecopy = rec_replace(phonecopy, "&#&hq&","&hq&#&")

    # //for vowel in between correction
    pureVowelList = ["&a&","&e&","&i&","&o&","&u&"]
    for i in range(0,5):
        c1 = f'&#{pureVowelList[i]}'
        phonecopy = phonecopy.replace(pureVowelList[i], c1)
    
    consonantList = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh",
                    "nx","t","th","d","dh","n","p","ph","b","bh","m","y",
                    "r","l","w","sh","sx","zh","y","s","h","lx","rx","f","dxq"]

    # // &eu&#&r&eu&#& syllabification correction

    for i in range(0,39):
        c1 = f'&eu&#&{consonantList[i]}&euv&#&'
        c2 = f'&eu&{consonantList[i]}&av&#&'
        phonecopy = phonecopy.replace(c1, c2)

    for i in range(0,39):
        c1 = f'&euv&#&{consonantList[i]}&euv&#&'
        c2 = f'&euv&{consonantList[i]}&av&#&'
        phonecopy = phonecopy.replace(c1, c2)

    phonecopy = phonecopy.replace("&eu&","&eu&#&")
    return phonecopy

# replacement for function in lines 279 - 317. //check the word in Dict.
# REMOVED EXIT(1) ON ENGLISH. WAS USELESS
def CheckDictionary(g : GLOBALS, input : str) -> int:

    fileName = GetFile(g, g.langId, 1)
    if (g.flags.DEBUG):
        print(f'dict : {fileName}')
    try:
        with open(fileName, 'r') as output:
            cnts = output.readlines()
    except:
        if g.flags.DEBUG:
            print(f'Dict not found')
        if(g.langId == g.ENGLISH):
            exit(1)
        return 0

    if (g.langId == g.ENGLISH):
        input1 = ''
        for c in input:
            if ord(c) < 97:
                c = c.lower()
            input1 += c
        input = input1
    
    for l in cnts:
        l = l.strip().split('\t')
        assert(len(l) == 3)
        if g.flags.DEBUG:
            print(f"word : {l[0]}")
        if input == l[0]:
            if g.flags.DEBUG:
                print(f"match found")
                print(f'Syllables : {l[1]}')
                print(f'monophones : {l[2]}')
            if g.flags.writeFormat == 1:
                WriteFile(g, l[1])
            if g.flags.writeFormat == 0:
                WriteFile(g, l[2])
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
        phonecopy = rec_replace(phonecopy, c2, c1) if isReverse != 0 else rec_replace(phonecopy, c1, c2)
    return phonecopy

# replacement for function in lines 711 - 713.
def CountChars(s : str, c : str) -> int:
    count = 0
    for x in s:
        if x == c:
            count += 1
    return count

# replacement for function in lines 719 - 744.
def GenerateAllCombinations(g : GLOBALS, j : int, s : str, c : list, isRight : int):
    t = ''
    if (c[j][0][0] == '#'):
        if isRight == 1:
            g.combvars.rightStr[g.combvars.bi] = s + '&'
            g.combvars.bi += 1
        else:
            g.combvars.leftStr[g.combvars.bi] = s + '&'
            g.combvars.bi += 1
    else:
        i = 0
        while (c[j][i][0] != '#'):
            t = s + '&' + c[j][i]
            GenerateAllCombinations(g, j+1, t, c, isRight)
            i += 1

# replacement for function in lines 746 - 768.
def GenerateMatrix(g : GLOBALS, combMatrix : list, regex : str):
    row, col, item = 0, 0, 0
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
        if g.flags.DEBUG:
            print(f'{row} {col} {combMatrix[row][col]}')

    combMatrix[row][col+1] = '#'
    combMatrix[row+1][0] = '#'

# replacement for function in lines 770 - 799.
def CombinationCorrection(g : GLOBALS, phone : str, left : str, right : str, isReverse : int) -> str:
    leftComb = [['' for _ in range(256)] for _ in range(256)]
    rightComb = [['' for _ in range(256)] for _ in range(256)]
    GenerateMatrix(g, leftComb, left)
    GenerateMatrix(g, rightComb, right)

    g.combvars.bi = 0
    GenerateAllCombinations(g, 0, '', leftComb, 0)
    g.combvars.bi = 0
    GenerateAllCombinations(g, 0, '', rightComb, 1)

    i = 0
    phonecopy = phone
    while g.combvars.leftStr[i] != '':
        if isReverse != 0:
            phonecopy = phonecopy.replace(g.combvars.rightStr[i], g.combvars.leftStr[i])
        else:
            phonecopy = phonecopy.replace(g.combvars.leftStr[i], g.combvars.rightStr[i])

        if g.flags.DEBUG:
            print(f'{g.combvars.leftStr[i]} {g.combvars.rightStr[i]}')
        
        i += 1
    
    g.combvars.refresh()
    return phonecopy

# replacement for function in lines 825 - 930. //Language specific corrections
def LangSpecificCorrection(g : GLOBALS, phone : str, langSpecFlag : int) -> str:
    phonecopy = phone
    if g.isSouth:
        phonecopy = rec_replace(phonecopy,"&ei&","&ai&")
        phonecopy = rec_replace(phonecopy,"&eiv&","&aiv&")
    else:
        phonecopy = rec_replace(phonecopy,"&oo&","&o&")
        phonecopy = rec_replace(phonecopy,"&oov&","&ov&")

    phonecopy = phonecopy.replace("&q&","&av&q&")
    phonecopy = rec_replace(phonecopy, "&a&av&","&a&")
    phonecopy = rec_replace(phonecopy, "&e&av&","&e&")
    phonecopy = rec_replace(phonecopy, "&i&av&","&i&")
    phonecopy = rec_replace(phonecopy, "&o&av&","&o&")
    phonecopy = rec_replace(phonecopy, "&u&av&","&u&")
    phonecopy = rec_replace(phonecopy,"&a&rqv&","&rq&")
    phonecopy = rec_replace(phonecopy,"&aa&av&","&aa&")
    phonecopy = rec_replace(phonecopy,"&ae&av&","&ae&")
    phonecopy = rec_replace(phonecopy,"&ax&av&","&ax&")
    phonecopy = rec_replace(phonecopy,"&ee&av&","&ee&")
    phonecopy = rec_replace(phonecopy,"&ii&av&","&ii&")
    phonecopy = rec_replace(phonecopy,"&ai&av&","&ai&")
    phonecopy = rec_replace(phonecopy,"&au&av&","&au&")
    phonecopy = rec_replace(phonecopy,"&oo&av&","&oo&")
    phonecopy = rec_replace(phonecopy,"&uu&av&","&uu&")
    phonecopy = rec_replace(phonecopy,"&rq&av&","&rq&")
    phonecopy = rec_replace(phonecopy,"&av&av&","&av&")
    phonecopy = rec_replace(phonecopy,"&ev&av&","&ev&")
    phonecopy = rec_replace(phonecopy,"&iv&av&","&iv&")
    phonecopy = rec_replace(phonecopy,"&ov&av&","&ov&")
    phonecopy = rec_replace(phonecopy,"&uv&av&","&uv&")

    phonecopy = rec_replace(phonecopy, "&av&rqv&","&rqv&")
    phonecopy = rec_replace(phonecopy, "&aav&av&","&aav&")
    phonecopy = rec_replace(phonecopy, "&aev&av&","&aev&")
    phonecopy = rec_replace(phonecopy, "&auv&av&","&auv&")
    phonecopy = rec_replace(phonecopy, "&axv&av&","&axv&")
    phonecopy = rec_replace(phonecopy, "&aiv&av&","&aiv&")
    phonecopy = rec_replace(phonecopy, "&eev&av&","&eev&")
    phonecopy = rec_replace(phonecopy, "&eiv&av&","&eiv&")
    phonecopy = rec_replace(phonecopy, "&iiv&av&","&iiv&")
    phonecopy = rec_replace(phonecopy, "&oov&av&","&oov&")
    phonecopy = rec_replace(phonecopy, "&ouv&av&","&ouv&")
    phonecopy = rec_replace(phonecopy, "&uuv&av&","&uuv&")
    phonecopy = rec_replace(phonecopy, "&rqv&av&","&rqv&")

    if langSpecFlag == 0:
        return phonecopy
    
    fileName = GetFile(g, g.langId, 2)
    with open(fileName, 'r') as output:
        cnts = output.readlines()

    left = ''
    right = ''
    phonecopy = '^' + phonecopy + '$'

    if (g.flags.DEBUG):
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
            phonecopy = CombinationCorrection(g, phonecopy, a1, a2, 0)
            if g.flags.DEBUG:
                print(f'{a1}\t{a2}')
        elif left.find('@') != -1:
            phonecopy = PositionCorrection(phonecopy, left, right, 0)
        else:
            phonecopy = phonecopy.replace(left, right)

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
def SyllableReverseCorrection(g : GLOBALS, phone : str, langSpecFlag : int) -> str:
    phonecopy = phone

    if g.isSouth:
        phonecopy = rec_replace(phonecopy, "&ai&","&ei&")
        phonecopy = rec_replace(phonecopy, "&aiv&","&eiv&")
    else:
        phonecopy = rec_replace(phonecopy, "&o&","&oo&")
        phonecopy = rec_replace(phonecopy, "&ov&","&oov&")
    
    if langSpecFlag == 0:
        return phonecopy

    fileName = GetFile(g, g.langId, 2)
    with open(fileName, 'r') as output:
        cnts = output.readlines()

    left = ''
    right = ''
    # //update head and tail in phone
    phonecopy = '^' + phonecopy + '$'

    if g.flags.DEBUG:
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
            phonecopy = CombinationCorrection(g, phonecopy, a1, a2, 1)
            if g.flags.DEBUG:
                print(f'{a1}\t{a2}')
        elif left.find('@') != -1:
            phonecopy = PositionCorrection(phonecopy, left, right, 1)
        else:
            phonecopy = phonecopy.replace(right, left)

    # //remove head and tail in phone
    phonecopy = phonecopy.replace('^', '')
    phonecopy = phonecopy.replace('$', '')
    # //end correction
    if (g.flags.DEBUG):
        print(f'after phone : {phonecopy}')
    return phonecopy

# //language specific syllable correction
def LangSyllableCorrection(input : str) -> int:
    if input == "&av&q&":
        return 1
    else:
        return 0

# replacement for function in lines 1000 - 1160. //split into syllable array
def SplitSyllables(g : GLOBALS, input : str) -> int:
    incopy = input

    if g.flags.writeFormat == 2:
        i = 0
        j = 0
        fullList = ["k","kh","lx","rx","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m","y","r","l","w","sh","sx","zh","y","s","h","f","dxq"]

        for i in range(0,39):
            for j in range(0,39):
                c1 = f'&{fullList[i]}&{fullList[j]}&'
                c2 = f'&{fullList[i]}&euv&#&{fullList[j]}&'
                incopy = incopy.replace(c1, c2)
        
    incopy = rec_replace(incopy, "&#&mq&","&mq&")
    incopy = rec_replace(incopy, "&#&q&","&q&")

    pch = incopy.split('#')
    g.syllableList = []
    for c in pch:
        if c != '&':
            g.syllableList.append(c)
    
    # ln -> len
    ln = len(g.syllableList)
    if (ln == 0):
        return 1
    
    if g.flags.DEBUG:
        for i in range(ln):
            print(f"initStack : {g.syllableList[i]}")
    
    # //south specific av addition
    if CheckVowel(g.syllableList[ln-1],1,0) == 0 and CheckChillu(g.syllableList[ln-1]) == 0:
        if g.isSouth:
            g.syllableList[ln-1] += '&av&'
        else:
            g.syllableList[ln-1] += '&euv&'

    # //round 2 correction
    if g.flags.writeFormat == 2:
        g.syllableCount = ln
        g.flags.writeFormat = 1
        return 1

    euFlag = 1
    if ln > 1:
        for i in range(ln-1,-1,-1):
            if LangSyllableCorrection(g.syllableList[i]) == 1:
                g.syllableList[i-1] += g.syllableList[i]
                g.syllableList[i] = ''

            if g.syllableList[i].find("&eu&") != -1:
                g.syllableList[i] = g.syllableList[i].replace("&eu&", "!")
                euFlag = 1

            if g.syllableList[i].find("&euv&") != -1:
                g.syllableList[i] = g.syllableList[i].replace("&euv&", "!")
                euFlag = 2
            
            if CheckVowel(g.syllableList[i],0,1) == 0:
                if i-1 >= 0:
                    g.syllableList[i-1] += g.syllableList[i]
                    g.syllableList[i] = ''
                else:
                    g.syllableList[i] += g.syllableList[i+1]
                    g.syllableList[i+1] = ''
            
            if i-1 > 0:
                if euFlag == 1:
                    g.syllableList[i-1] = g.syllableList[i-1].replace("!","&eu&")
                elif euFlag == 2:
                    g.syllableList[i-1] = g.syllableList[i-1].replace("!","&euv&")
                g.syllableList[i-1] = rec_replace(g.syllableList[i-1], "&&","&")
            
            if euFlag == 1:
                g.syllableList[i] = g.syllableList[i].replace("!","&eu&")
            elif euFlag == 2:
                g.syllableList[i] = g.syllableList[i].replace("!","&euv&")
    else:
        if (CheckVowel(g.syllableList[0],1,0) == 0 and g.flags.writeFormat != 3) or Checkeuv(g.syllableList[0]) != 0:
            g.syllableList[0] += '&av'

    if g.flags.DEBUG:
        for i in range(ln):
            print(f'syllablifiedStack : {g.syllableList[i]}')

    # //round 3 double syllable correction
    for i in range(ln):
        # //corrections
        g.syllableList[i] = g.syllableList[i].replace('1','')
        if g.flags.DEBUG:
            print(f'LenStack : {len(g.syllableList[i])}')
        
        if len(g.syllableList[i]) > 0:
            if g.syllableList[i].find("&eu&") != -1:
                g.syllableList[i] = g.syllableList[i].replace("&eu&", "!")
                euFlag = 1

            if g.syllableList[i].find("&euv&") != -1:
                g.syllableList[i] = g.syllableList[i].replace("&euv&", "!")
                euFlag = 2
            
            if CheckVowel(g.syllableList[i],0,1) == 0 and g.flags.writeFormat != 3:
                if g.flags.DEBUG:
                    print(f'Stack : {g.syllableList[i]}')
                g.syllableList[i] += '&av'
            
            if g.syllableList[i].find('!') != -1:
                if euFlag == 1:
                    g.syllableList[i] = g.syllableList[i].replace("!","&eu&")
                elif euFlag == 2:
                    g.syllableList[i] = g.syllableList[i].replace("!","&euv&")
                g.syllableList[i] = g.syllableList[i].replace('!', 'eu')
        
        g.syllableList[i] = rec_replace(g.syllableList[i], '&&', '&')
        g.syllableList[i] = GeminateCorrection(g.syllableList[i],1)
    
    if g.flags.DEBUG:
        for i in range(ln):
            print(f'syllablifiedStack1 : {g.syllableList[i]}')
        print(f'No of syllables : {ln}')

    g.syllableCount = ln
    if g.flags.writeFormat == 3:
        g.flags.writeFormat = 0
    return 1

# replacement for function in lines 1164 - 1275. //make to write format
def WritetoFiles(g : GLOBALS) -> int:
    if g.flags.DEBUG:
        for i in range(0,g.syllableCount):
            print(f'syllablifiedStackfinal : {g.syllableList[i]}')
    
    validSyllable = 0
    for i in range(0,g.syllableCount):
        if g.syllableList[i] != '':
            validSyllable += 1
    
    if g.flags.DEBUG:
        print(f'a correction {g.syllableList[0]}')
    
    g.words.outputText = ''

    # //phone
    j = 0
    if g.flags.writeFormat == 0:
        syllablesPrint = 0
        for i in range(g.syllableCount):
            g.words.outputText += '(( '
            l = g.syllableList[i].split('&')
            for pch in l:
                if pch == '':
                    continue
                if g.flags.DEBUG:
                    print(f'syl {pch}')
                j = 1
                g.words.outputText += f'"{pch}" '
            if j != 0:
                if g.flags.syllTagFlag != 0:
                    if syllablesPrint == 0:
                        g.words.outputText += '_beg'
                    elif syllablesPrint == validSyllable - 1:
                        g.words.outputText += '_end'
                    else:
                        g.words.outputText += '_mid'
                    syllablesPrint += 1
                g.words.outputText += ') 0) '
            else:
                g.words.outputText = g.words.outputText[:(len(g.words.outputText) - 3)]
            j = 0
    
        g.words.outputText = g.words.outputText.replace('v', '')
        g.words.outputText = g.words.outputText.replace(" \"eu\"","")
        g.words.outputText = g.words.outputText.replace('!', '')

    # //syllable
    elif g.flags.writeFormat == 1:
        syllablesPrint = 0
        for i in range(g.syllableCount):
            g.syllableList[i] = rec_replace(g.syllableList[i], 'euv', 'eu')
            g.syllableList[i] = SyllableReverseCorrection(g, g.syllableList[i], g.flags.LangSpecificCorrectionFlag)
            if g.flags.DEBUG:
                print(f'{g.syllableList[i]}')
            g.words.outputText += '(( "'
            l = g.syllableList[i].split('&')
            for pch in l:
                if pch == '':
                    continue
                if g.flags.DEBUG:
                    print(f'syl {pch}')
                j = 1
                if CheckSymbol(g, pch) != 0:
                    g.words.outputText += GetUTF(g, pch)
                    if pch == 'av' and g.flags.DEBUG:
                        print('av found')
            if j != 0:
                if g.flags.syllTagFlag != 0:
                    if syllablesPrint == 0:
                        g.words.outputText += '_beg'
                    elif syllablesPrint == validSyllable - 1:
                        g.words.outputText += '_end'
                    else:
                        g.words.outputText += '_mid'
                    syllablesPrint += 1
                g.words.outputText += '" ) 0) '
            else:
                g.words.outputText = g.words.outputText[:(len(g.words.outputText) - 4)]
            j = 0
    
    g.words.outputText = g.words.outputText.replace('#', '')
    g.words.outputText = g.words.outputText.replace('  ', ' ')
    if g.flags.DEBUG:
        print(f'Print text : {g.words.outputText}')
    
    WriteFile(g, g.words.outputText)
    return 1