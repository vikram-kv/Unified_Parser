# combined lexical analyzer and parser

from ply.lex import Lexer
from ply.yacc import yacc
from globals import *
from helpers import *
import sys

# tokens used
tokens = ('kaki_c', 'conjsyll2_c', 'fullvowel_b', 'kaki_a', 'kaki_b',  'conjsyll2_b', 'conjsyll2_a',
        'conjsyll1', 'nukchan_b','nukchan_a', 'yarule', 'fullvowel_a', 'vowel')

# parser part

def p_sentence(p):
    '''
    sentence : words
    '''
    if p.parser.g.flags.parseLevel == 0:
        p.parser.g.words.syllabifiedWordOut = p[1]

        if p.parser.g.words.syllabifiedWordOut.find('&&') != -1:
            p.parser.g.words.syllabifiedWordOut = p.parser.g.words.syllabifiedWordOut.replace("&&","&")
        
        p.parser.g.flags.parseLevel += 1
    else:
        p.parser.g.words.phonifiedWord = p[1]

def p_words_syltoken(p):
    '''
    words : syltoken
    '''
    if(p.parser.g.flags.DEBUG):
        print(f"Syll:\t{p[1]}")
    p[0] = p[1]

def p_words_wordsandsyltoken(p):
    '''
    words : words syltoken
    '''
    if(p.parser.g.flags.DEBUG):
        print(f"Syll:\t{p[2]}")
    p[0] = p[1] + p[2]

def p_syltoken(p):
    '''
    syltoken : fullvowel_b
             | fullvowel_a
             | conjsyll2_c
             | conjsyll2_b
             | conjsyll2_a
             | conjsyll1 
             | nukchan_b
             | nukchan_a
             | yarule
             | vowel
    '''
    p[0] = p[1]

def p_syltoken1(p):
    '''
    syltoken :
             | kaki_c
             | kaki_a
             | kaki_b
    '''
    if (p.parser.g.flags.DEBUG):
        print(f'kaki : {p[1]}')
    p[0] = p[1]

def p_error(p):
    print('parse error')
    exit(1)

# //print the help of syntax
def printHelp():

    print("UnifiedParser : v3.0")
    print("Usage : ./unified-parser word LangSpecificCorrection WriteFormat ForSylldict IsPruning DirectParse LangId timestamp")
    print("LangSpecificCorrection : \n\t0-No\n\t1-Yes")
    print("WriteFormat : \n\t0-Phone\n\t1-Syllable")
    print("ForSylldict : writes output to wordpronunciationsyldict\n\t0-No\n\t1-Yes")
    print("IsPruning : writes output for pruning format\n\t0-No\n\t1-Yes")
    print("DirectParse : No UTF-8 to CLS conversion\n\t0-No\n\t1-Yes")
    print("LangId : lang id for direct parsing\t0-8")
    print("timestamp : append this to wordpronunciation\tstring")

    print("Example: ./unified-parser 1 0 0 0 - Monophone parser")
    print("Example: ./unified-parser 1 1 0 0 - Syllable parser")
    print("Example: ./unified-parser 1 2 0 0 - Aksharas parser")
    print("Example: ./unified-parser 1 3 0 0 - Direct parser for USS fallback")
    print("Example: ./unified-parser 1 4 0 0 - Syllable parser with beg mid end")

def wordparse(wd : str):
    g = GLOBALS()
    lexer = Lexer()
    parser = yacc()
    parser.g = g
    g.flags.DEBUG = True

    argv = ['parallelparser.py', wd, '0', '1', '1', '1', '0']
    argc = len(argv)
    if argc <= 5:
        printHelp()
        exit(1)
    
    if argv[2] != '1':
        g.flags.LangSpecificCorrectionFlag = 0
    
    g.flags.writeFormat = int(argv[3])
    if argv[3] == '4':
        g.flags.writeFormat = 1
        g.flags.syllTagFlag = 1
    
    if argv[4] == '1':
        g.outputFile = 'wordpronunciationsyldict'
    
    if argv[5] == '1':
        g.flags.pruiningFlag = 1
        g.outputFile = 'wordpronunciation'
        g.flags.writeFormat = 3
    
    if argc > 6 and argv[6] == '1':
        g.flags.directParseFlag = 1
        g.langId = int(argv[7])
    
    if argc > 8:
        g.outputFile = 'wordpronunciation' + argv[8]
    else:
        g.outputFile = 'wordpronunciation'
        if argv[4] == '1':
            g.outputFile = 'wordpronunciationsyldict'
    
    word = argv[1]
    
    if g.flags.DEBUG:
        print(f'Word : {word}')

    if g.flags.directParseFlag != 1:
        word = RemoveUnwanted(word)

    if g.flags.DEBUG:
        print(f'Cleared Word : {word}')

    if SetlanguageFeat(g, word) == 0:
        return 0
    if g.flags.directParseFlag == 1:
        g.langId = int(argv[7])
    
    if CheckDictionary(g, word) != 0:
        return 0
    if g.flags.DEBUG:
        print(f'langId : {g.langId}')
    
    word = ConvertToSymbols(g, word)
    if g.flags.directParseFlag == 1:
        g.words.syllabifiedWord = argv[1]
        print(f'{word}')

    if g.flags.DEBUG:
        print(f"Symbols code : {g.words.unicodeWord}")
        print(f"Symbols syllables : {g.words.syllabifiedWord}")

    parser.parse(g.words.syllabifiedWord, lexer=lexer)
    if(g.flags.DEBUG):
        print(f"Syllabified Word : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = g.words.syllabifiedWordOut.replace("&#&","&") + '&'
    if(g.flags.DEBUG):
        print(f"Syllabified Word out : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = LangSpecificCorrection(g, g.words.syllabifiedWordOut, g.flags.LangSpecificCorrectionFlag)
    if(g.flags.DEBUG):
        print(f"Syllabified Word langCorr : {g.words.syllabifiedWordOut}")
    if(g.flags.DEBUG):
        print(f"Syllabified Word gemCorr : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = CleanseWord(g.words.syllabifiedWordOut)
    if(g.flags.DEBUG):
        print(f"Syllabified Word memCorr : {g.words.syllabifiedWordOut}")

    if not g.isSouth:
        if g.flags.DEBUG:
            print('NOT SOUTH')
        count = 0
        for i in range(len(g.words.syllabifiedWordOut)):
            if g.words.syllabifiedWordOut[i] == '&':
                count += 1
        splitPosition = 2
        if GetPhoneType(g, g.words.syllabifiedWordOut, 1) == 1:
            if count > 2:
                tpe = GetPhoneType(g, g.words.syllabifiedWordOut, 2)
                if tpe == 2:
                    splitPosition = 1
                elif tpe == 3:
                    splitPosition = 3
            else:
                splitPosition = 1
        count = 0
        for i in range(len(g.words.syllabifiedWordOut)):
            if g.words.syllabifiedWordOut[i] == '&':
                count += 1
            if count > splitPosition:
                count = i
                break
        start, end = g.words.syllabifiedWordOut, g.words.syllabifiedWordOut
        end = end[count:]
        start = start[:count]
        if(g.flags.DEBUG):
            print(f"posi {count} {start} {end}")
        end = SchwaSpecificCorrection(g, end)
        if(g.flags.DEBUG):
            print(f"prefinal : {g.words.syllabifiedWordOut}")
        g.words.syllabifiedWordOut = start + end
        if(g.flags.DEBUG):
            print(f"prefinal1 : {g.words.syllabifiedWordOut}")
        g.words.syllabifiedWordOut = CleanseWord(g.words.syllabifiedWordOut)
        if(g.flags.DEBUG):
            print(f"final : {g.words.syllabifiedWordOut}")
        g.words.syllabifiedWordOut = SchwaDoubleConsonent(g.words.syllabifiedWordOut)
        if(g.flags.DEBUG):
            print(f"final0 : {g.words.syllabifiedWordOut}")
    
    g.words.syllabifiedWordOut = GeminateCorrection(g.words.syllabifiedWordOut, 0)
    
    g.words.syllabifiedWordOut = MiddleVowel(g, g.words.syllabifiedWordOut)

    g.words.syllabifiedWordOut = Syllabilfy(g.words.syllabifiedWordOut)
    
    SplitSyllables(g,g.words.syllabifiedWordOut)
    
    WritetoFiles(g)
    return g.answer

if __name__ == '__main__':

    if (len(sys.argv) != 2):
        print('Incorrect Usage')
        exit(-1)

    ans = wordparse(sys.argv[1])
    print(ans)