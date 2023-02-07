# global CONSTANTs for languages. Uses the same values as the enum at 
# lines 11-13 of unified.y

import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class FLAGS:
    DEBUG = False
    parseLevel = 0
    syllTagFlag = 0
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

class GLOBALS:
    def __init__(self):
        self.flags = FLAGS()
        self.words = WORDS()
        self.combvars = STRINGS()

        self.MALAYALAM = 1
        self.TAMIL = 2
        self.TELUGU = 3
        self.KANNADA = 4
        self.HINDI = 5
        self.BENGALI = 6
        self.GUJARATHI = 7
        self.ODIYA = 8
        self.PUNJABI = 9
        self.ENGLISH = 10 # new value from 9 to 10

        self.langId = 0
        self.isSouth = False
        self.syllableCount = 0

        self.rootPath = SCRIPT_DIR+'/'
        self.commonFile = "common.map"
        self.outputFile = ""

        self.symbolTable = [['' for _ in range(2)] for _ in range(128)]
        self.ROW = 128
        self.COL = 2
        self.syllableList = []

        self.VOWELSSIZE=18
        self.CONSONANTSSIZE=25
        self.SEMIVOWELSSIZE=13

        self.VOWELS = ["a","e","i","o","u","aa","mq","aa","ii", "uu","rq","au","ee","ei","ou","oo","ax","ai"]
        self.CONSONANTS = ["k","kh","g","gh","ng","c","ch","j","jh","nj","tx","txh","dx","dxh","nx","t","th","d","dh","n","p","ph","b","bh","m"]
        self.SEMIVOWELS = ["y","r","l","w","sh","sx","zh","s","h","lx","rx","f","dxq"]

        # variable to indicate current language being parsed.
        self.currLang = self.ENGLISH
        self.answer = ''