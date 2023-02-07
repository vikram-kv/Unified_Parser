import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

# combined lexical analyzer and parser

from ply.lex import Lexer
from ply.yacc import yacc
from globals import *
from helpers import *
import sys
from sys import exit

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
            p.parser.g.words.syllabifiedWordOut = rec_replace(p.parser.g.words.syllabifiedWordOut,'&&','&')
        
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

# print the help of syntax
def printHelp():

    print("UnifiedParser - Usage Instructions")
    print("Run python3 parser.py wd lsflag wfflag clearflag")
    print("wd - word to parse in unicode.")
    print("lsflag - always 0. we are not using this.")
    print("wfflag - 0 for Monophone parsing, 1 for syllable parsing, 2 for Akshara Parsing")
    print("clearflag - 1 for removing the lisp like format of output and to just produce space separated output. Otherwise, 0.")


def wordparse(wd : str, lsflag : int, wfflag : int, clearflag : int):
    g = GLOBALS()
    lexer = Lexer()
    parser = yacc()
    parser.g = g
    g.flags.DEBUG = False
    wd = wd.strip('  ') # hidden characters

    if lsflag not in [0,1] or wfflag not in [0,1,2]:
        print("Invalid input")
        exit(1)
    
    g.flags.LangSpecificCorrectionFlag = lsflag
    
    g.flags.writeFormat = wfflag
    if wfflag == 4:
        g.flags.writeFormat = 1
        g.flags.syllTagFlag = 1
    
    word = wd
    if g.flags.DEBUG:
        print(f'Word : {word}')

    word = RemoveUnwanted(word)
    if g.flags.DEBUG:
        print(f'Cleared Word : {word}')

    if SetlanguageFeat(g, word) == 0:
        return 0
    
    if CheckDictionary(g, word) != 0:
        return 0

    if g.flags.DEBUG:
        print(f'langId : {g.langId}')
    
    word = ConvertToSymbols(g, word)

    if g.flags.DEBUG:
        print(f"Symbols code : {g.words.unicodeWord}")
        print(f"Symbols syllables : {g.words.syllabifiedWord}")

    parser.parse(g.words.syllabifiedWord, lexer=lexer)
    if(g.flags.DEBUG):
        print(f"Syllabified Word : {g.words.syllabifiedWordOut}")
    g.words.syllabifiedWordOut = rec_replace(g.words.syllabifiedWordOut, '&#&','&') + '&'
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
    if clearflag == 1:
        t = g.words.outputText
        t = t.split('"')
        ln = len(t)
        i = 1
        g.answer = ''
        while i < ln:
            g.answer += t[i] + ' '
            i += 2
        g.answer.strip()
    return g.answer

if __name__ == '__main__':

    if (len(sys.argv) != 5):
        printHelp()
        exit(-1)
    
    ans = wordparse(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    print(ans)
