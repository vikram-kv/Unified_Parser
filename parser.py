# combined lexical analyzer and parser

from ply.lex import lex
from ply.yacc import yacc
import globals
from helpers import *
import sys

# tokens identified by the lexer
tokens = ('kaki_c', 'conjsyll2_c', 'fullvowel_b', 'kaki_a', 'kaki_b',  'conjsyll2_b', 'conjsyll2_a',
'conjsyll1', 'nukchan_b','nukchan_a', 'yarule', 'fullvowel_a', 'consonant', 'vowel', 'halant', 'matra')

# lexical analyzer part

def t_kaki_c(t):
    r'(\&)*(k|kh|lx|rx|g|gh|ng|c|ch|j|jh|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|r|l|w|sh|sx|zh|y|s|h|f|dxq|z|kq|khq|gq|dxhq)((&)(lx|k|kh|g|gh|ng|c|ch|j|jh|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|zh|y|s|h|ex|rx|f|dxq|z|kq|khq|gq|dxhq))*'
    s = t.value
    ans = ''
    i = 1
    if s[0] == '&':
        ans += '&'
    l = s.split('&')
    for pch in l:
        if pch == '':
            continue
        ans += f'{pch}&av&#&&'
        i += 1
    print(f'doubt - {ans}')
    ans = ans[:(len(ans) - 7)]
    t.value = ans
    print(f'doubt - {t.value}')
    return t

def t_conjsyll2_c(t):
    r'(eu)'
    t.value = 'eu&#'
    return t

t_fullvowel_b = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|lx|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(a|aa|i|ii|u|uu|rq|ee|ei|o|ou|ax|a&mq|a&q|a&hq|aa&mq|aa&q|aa&hq|i&mq|ii&q|ii&hq|i&q|i&hq|ii&mq|u&mq|u&q|u&hq|uu&mq|uu&q|uu&hq|rq&mq|rq&q|rq&hq|ee&mq|ee&q|ee&hq|ei&mq|ei&q|ei&hq|o&mq|o&q|o&hq|ou&mq|ou&q|ou&hq)'
t_kaki_a = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|lx|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(aav|iv|iiv|uv|uuv|rqv|aev|eev|eiv|ax|ov|ouv|q|hq|mq)(&)(mq|q|hq)*'
t_kaki_b = r'(&)*(dxq&aav|dxq&iv|dxq&iiv|dxq&uv|dxq&uuv|dxq&rqv|dxq|dxq&eev|dxq&eiv|dxq&ov|dxq&ouv|dxq&mq|dxq&q|dxq&hq)'
t_conjsyll2_b = r'(&)*(k&eu|kh&eu|g&eu|gh&eu|c&eu|ch&eu|j&eu|jh&eu|ng&eu|nj&eu|tx&eu|txh&eu|dx&eu|dxh&eu|nx&eu|t&eu|th&eu|d&eu|dh&eu|n&eu|p&eu|ph&eu|b&eu|bh&eu|m&eu|y&eu|r&eu|l&eu|lx&eu|w&eu|sh&eu|sx&eu|s&eu|h&eu)'
t_conjsyll2_a = r'(&)*(kq|khq|gq|z|dxq|dxhq|f|y)(&)eu'
t_conjsyll1 = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|lx|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(aa|i|ii|u|uu|rq|ee|ei|o|ou|ax)(&)(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|aa|i|ii|u|uu|rq|ee|ei|o|ou|aav|iv|iiv|uv|uuv|rqv|aev|eev|eiv|ax|ov|ouv|mq|q|hq)(&)eu(&)(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|y)'
t_nukchan_b = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|lx|w|sh|sx|s|h)(&)(mq|q|hq)'
t_nukchan_a = r'(&)*(kq|khq|gq|z|dxq|dxhq|f|y)(&)(mq|q|hq)'
t_yarule = r'(&)*(iv|iiv|uv|uuv|rqv)(&)(y)'
t_vowel = r'(&)*(a|aa|i|ii|u|uu|rq|ee|ei|o|ou|ax|a&mq|a&q|a&hq|aa&mq|aa&q|aa&hq|i&mq|ii&q|ii&hq|i&q|i&hq|ii&mq|u&mq|u&q|u&hq|uu&mq|uu&q|uu&hq|rq&mq|rq&q|rq&hq|ee&mq|ee&q|ee&hq|ei&mq|ei&q|ei&hq|o&mq|o&q|o&hq|ou&mq|ou&q|ou&hq)'
t_fullvowel_a = r'.'

def t_error(t):
    print('Lexer error')
    exit(1)

# parser part

def p_sentence(p):
    '''
    sentence : words
    '''
    if globals.flags.parseLevel == 0:
        globals.words.syllabifiedWordOut = p[1]

        if globals.words.syllabifiedWordOut.find('&&') != -1:
            globals.words.syllabifiedWordOut = globals.words.syllabifiedWordOut.replace("&&","&")
        
        globals.flags.parseLevel += 1
    else:
        globals.words.phonifiedWord = p[1]


def p_words_syltoken(p):
    '''
    words : syltoken
    '''
    if globals.flags.DEBUG:
        print(f'\nSyll:\t{p[1]}')
    p[0] = p[1]

def p_words_wordsandsyltoken(p):
    '''
    words : words syltoken
    '''
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
             | consonant
             | vowel
             | halant
             | matra
    '''
    p[0] = p[1]

def p_syltoken1(p):
    '''
    syltoken :
             | kaki_c
             | kaki_a
             | kaki_b
    '''
    if globals.flags.DEBUG:
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

def main():
    
    globals.init()
    lexer = lex()
    parser = yacc()

    argc = len(sys.argv)
    argv = sys.argv
    globals.flags.DEBUG = True
    if argc <= 5:
        printHelp()
        exit(1)
    
    if argv[2] != '1':
        globals.flags.LangSpecificCorrectionFlag = 0
    
    globals.flags.writeFormat = int(argv[3])
    if argv[3] == '4':
        globals.flags.writeFormat = 1
        globals.flags.syllTagFlag = 1
    
    if argv[4] == '1':
        globals.outputFile = 'wordpronunciationsyldict'
    
    if argv[5] == '1':
        globals.flags.pruiningFlag = 1
        globals.outputFile = 'wordpronunciation'
        globals.flags.writeFormat = 3
    
    if argc > 6 and argv[6] == '1':
        globals.flags.directParseFlag = 1
        globals.langId = int(argv[7])
    
    if argc > 8:
        globals.outputFile = 'wordpronunciation' + argv[8]
    else:
        globals.outputFile = 'wordpronunciation'
        if argv[4] == '1':
            globals.outputFile = 'wordpronunciationsyldict'
    
    word = argv[1]
    if globals.flags.DEBUG:
        print(f'Word {word}')
    
    if globals.flags.directParseFlag != 1:
        word = RemoveUnwanted(word)
    if globals.flags.DEBUG:
        print(f'Cleared Word : {word}')
    
    if SetlanguageFeat(word) == 0:
        return 0
    if globals.flags.directParseFlag == 1:
        globals.langId = int(argv[7])
    
    if CheckDictionary(word) != 0:
        return 0
    if globals.flags.DEBUG:
        print(f'langId : {globals.langId}')
    word = ConvertToSymbols(word)
    if globals.flags.directParseFlag == 1:
        globals.words.syllabifiedWord = argv[1]
        print(f'{word}')
    
    if globals.flags.DEBUG:
        print(f"Symbols code : {globals.words.unicodeWord}");
        print(f"Symbols syllables : {globals.words.syllabifiedWord}");

    parser.parse(globals.words.syllabifiedWord)

    if globals.flags.DEBUG:
        print(f'Syllabified Word : {globals.words.syllabifiedWordOut}')
    
    globals.words.syllabifiedWordOut = globals.words.syllabifiedWordOut.replace("&#&","&") + '&'
    if globals.flags.DEBUG:
        print(f'Syllabified Word out : {globals.words.syllabifiedWordOut}')

    globals.words.syllabifiedWordOut = LangSpecificCorrection(globals.words.syllabifiedWordOut, globals.flags.LangSpecificCorrectionFlag)
    if globals.flags.DEBUG:
        print(f'Syllabified Word langCorr : {globals.words.syllabifiedWordOut}')
    globals.words.syllabifiedWordOut = CleanseWord(globals.words.syllabifiedWordOut)
    if globals.flags.DEBUG:
        print(f'Syllabified Word memCorr : {globals.words.syllabifiedWordOut}')

    if not globals.isSouth:
        count = 0
        for i in range(len(globals.words.syllabifiedWordOut)):
            if i == '&':
                count += 1
        splitPosition = 2
        if GetPhoneType(globals.words.syllabifiedWord, 1) == 1:
            if count > 2:
                tpe = GetPhoneType(globals.words.syllabifiedWord, 2)
                if tpe == 2:
                    splitPosition = 1
                elif tpe == 3:
                    splitPosition = 3
            else:
                splitPosition = 1
        count = 0
        for i in range(len(globals.words.syllabifiedWordOut)):
            if globals.words.syllabifiedWordOut[i] == '&':
                count += 1
            if count > splitPosition:
                count = i
                break
        start, end = globals.words.syllabifiedWordOut, globals.words.syllabifiedWordOut
        end = end[count:]
        start = start[:count]

        if globals.flags.DEBUG:
            print(f'posi  {count} {start} {end}')
        end = SchwaSpecificCorrection(end)
        if globals.flags.DEBUG:
            print(f'prefinal : {globals.words.syllabifiedWordOut}\n')
        globals.words.syllabifiedWordOut = start + end
        if globals.flags.DEBUG:
            print(f'prefinal1 : {globals.words.syllabifiedWordOut}')
        globals.words.syllabifiedWordOut = CleanseWord(globals.words.syllabifiedWordOut)
        if globals.flags.DEBUG:
            print(f'final : {globals.words.syllabifiedWord}')
        globals.words.syllabifiedWordOut = SchwaDoubleConsonent(globals.words.syllabifiedWordOut)
        if globals.flags.DEBUG:
            print(f'final0 : {globals.words.syllabifiedWordOut}')
    
    globals.words.syllabifiedWordOut = GeminateCorrection(globals.words.syllabifiedWordOut, 0)
    if globals.flags.DEBUG:
        print(f'Syllabified Word gemCorr : {globals.words.syllabifiedWordOut}')
    
    globals.words.syllabifiedWordOut = MiddleVowel(globals.words.syllabifiedWordOut)
    if globals.flags.DEBUG:
        print(f'Syllabified Word gemCorr : {globals.words.syllabifiedWordOut}')

    globals.words.syllabifiedWordOut = Syllabilfy(globals.words.syllabifiedWordOut)
    if globals.flags.DEBUG:
        print(f'Syllabified Word final : {globals.words.syllabifiedWordOut}')
    
    SplitSyllables(globals.words.syllabifiedWordOut)
    if globals.flags.DEBUG:
        print('Splitted to Syllables')
    
    WritetoFiles()
    if globals.flags.DEBUG:
        print(f'Files created {globals.words.outputText}')

if __name__ == '__main__':
    main()
    pass