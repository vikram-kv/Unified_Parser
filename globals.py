# global CONSTANTs for languages. Uses the same values as the enum at 
# lines 11-13 of unified.y

class FLAGS:
    DEBUG = False
    parseLevel = 0
    # pruningFlag = 0
    syllTagFlag = 0
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
        self.ENGLISH = 9

        self.langId = 0
        self.isSouth = False
        self.syllableCount = 0

        self.rootPath = "./"
        self.commonFile = "common"
        self.outputFile = ""
        self.outputPruneFile = "rag_pho"

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