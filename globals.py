# global CONSTANTs for languages. Uses the same values as the enum at 
# lines 11-13 of unified.y

class FLAGS:
    DEBUG = False
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

class STRINGS:
    bi = 0
    leftStr = ['' for _ in range(1100)]
    rightStr = ['' for _ in range(1100)]
    def refresh(self):
        self.leftStr = ['' for _ in range(1100)]
        self.rightStr = ['' for _ in range(1100)]
        self.bi = 0

def init():
    global flags, words, combvars
    flags = FLAGS()
    words = WORDS()
    combvars = STRINGS()

    global MALAYALAM, TAMIL, TELUGU, KANNADA, HINDI, BENGALI, GUJARATHI, ODIYA, ENGLISH
    MALAYALAM = 1
    TAMIL = 2
    TELUGU = 3
    KANNADA = 4
    HINDI = 5
    BENGALI = 6
    GUJARATHI = 7
    ODIYA = 8
    ENGLISH = 9

    global langId, isSouth, syllableCount
    langId = 0
    isSouth = False
    syllableCount = 0

    global rootPath, commonFile, outputFile, outputPruneFile, symbolTable, ROW, COL, syllableList
    # files and paths
    rootPath = "./"
    commonFile = "common"
    outputFile = ""
    outputPruneFile = "rag_pho"

    # mapping from utf8 language chars to the phoneme
    # implemented as list of lists [rows ~ 128, cols - 2]
    # mimics the construction in unified.y but may be replaced with a dictionary
    symbolTable = [['' for _ in range(2)] for _ in range(128)]
    ROW = 128
    COL = 2
    syllableList = []

    global VOWELSSIZE, CONSONANTSSIZE, SEMIVOWELSSIZE, VOWELS, CONSONANTS, SEMIVOWELS, currLang
    VOWELSSIZE=18
    CONSONANTSSIZE=25
    SEMIVOWELSSIZE=13

    VOWELS = ["a","e","i","o","u","aa","mq","aa","ii", "uu","rq","au","ee","ei","ou","oo","ax","ai"]
    CONSONANTS = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m"]
    SEMIVOWELS = ["y","r","l","w","sh","sx","zh","s","h","lx","rx","f","dxq"]


    # variable to indicate current language being parsed.
    currLang = ENGLISH