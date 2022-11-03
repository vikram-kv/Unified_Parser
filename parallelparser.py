# combined lexical analyzer and parser

from ply.lex import lex
from ply.yacc import yacc
from globals import *
from helpers import *
import sys

# tokens identified by the lexer
tokens = ('kaki_c', 'conjsyll2_c', 'fullvowel_b', 'kaki_a', 'kaki_b',  'conjsyll2_b', 'conjsyll2_a',
'conjsyll1', 'nukchan_b','nukchan_a', 'yarule', 'fullvowel_a', 'consonant', 'vowel', 'halant', 'matra')

# lexical analyzer part
# r'(&)*(k|kh|lx|rx|g|gh|ng|c|ch|j|jh|nj|tx|txh|dx|dxh|nx|t|th|dh|d|n|p|ph|b|bh|m|y|r|l|w|sh|sx|zh|y|s|h|f|dxq|z|kq|khq|gq|dxhq)((&)(lx|k|kh|g|gh|ng|c|ch|j|jh|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|zh|y|s|h|ex|rx|f|dxq|z|kq|khq|gq|dxhq))*'
def t_kaki_c(t):
    r'(&)*(dxhq|txh|khq|dxq|dxh|zh|tx|th|sx|sh|rx|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)((&)(dxhq|txh|khq|dxq|dxh|zh|tx|th|sx|sh|rx|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|ex|dx|dh|ch|bh|z|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b))*'
    s = t.value
    print('c - '+s)
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
    ans = ans[:(len(ans) - 7)]
    t.value = ans
    return t

def t_conjsyll2_c(t):
    r'(eu)'
    t.value = 'eu&#'
    return t

t_fullvowel_b = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|lx|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(uu&mq|uu&hq|rq&mq|rq&hq|ou&mq|ou&hq|ii&mq|ii&hq|ei&mq|ei&hq|ee&mq|ee&hq|aa&mq|aa&hq|uu&q|u&mq|u&hq|rq&q|ou&q|o&mq|o&hq|ii&q|i&mq|i&hq|ei&q|ee&q|aa&q|a&mq|a&hq|u&q|o&q|i&q|a&q|uu|rq|ou|ii|ei|ee|ax|aa|u|o|i|a)'
t_kaki_a = r'(&)*(dxhq|txh|khq|dxq|dxh|tx|th|sx|sh|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)(&)(uuv|rqv|ouv|iiv|eiv|eev|aev|aav|uv|ov|mq|iv|hq|ax|q)(&)(mq|hq|q)*'
t_kaki_b = r'(&)*(dxq&uuv|dxq&rqv|dxq&ouv|dxq&iiv|dxq&eiv|dxq&eev|dxq&aav|dxq&uv|dxq&ov|dxq&mq|dxq&iv|dxq&hq|dxq&q|dxq)'
t_conjsyll2_b = r'(&)*(txh&eu|dxh&eu|tx&eu|th&eu|sx&eu|sh&eu|ph&eu|nx&eu|nj&eu|ng&eu|lx&eu|kh&eu|jh&eu|gh&eu|dx&eu|dh&eu|ch&eu|bh&eu|y&eu|w&eu|t&eu|s&eu|r&eu|p&eu|n&eu|m&eu|l&eu|k&eu|j&eu|h&eu|g&eu|d&eu|c&eu|b&eu)'
t_conjsyll2_a = r'(&)*(dxhq|khq|dxq|kq|gq|z|y|f)(&)eu'
t_conjsyll1 = r'(&)*(dxhq|txh|khq|dxq|dxh|tx|th|sx|sh|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)(&)(uu|rq|ou|ii|ei|ee|ax|aa|u|o|i)(&)(dxhq|uuv|txh|rqv|ouv|khq|iiv|eiv|eev|dxq|dxh|aev|aav|uv|uu|tx|th|sx|sh|rq|ph|ov|ou|nx|nj|ng|mq|kq|kh|jh|iv|ii|hq|gq|gh|ei|ee|dx|dh|ch|bh|ax|aa|z|y|w|u|t|s|r|q|p|o|n|m|l|k|j|i|h|g|f|d|c|b)(&)eu(&)(dxhq|txh|khq|dxq|dxh|tx|th|sx|sh|ph|nx|nj|ng|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)'
t_nukchan_b = r'(&)*(txh|dxh|tx|th|sx|sh|ph|nx|nj|ng|lx|kh|jh|gh|dx|dh|ch|bh|y|w|t|s|r|p|n|m|l|k|j|h|g|d|c|b)(&)(mq|hq|q)'
t_nukchan_a = r'(&)*(dxhq|khq|dxq|kq|gq|z|y|f)(&)(mq|hq|q)'
t_yarule = r'(&)*(uuv|rqv|iiv|uv|iv)(&)(y)'
t_vowel = r'(&)*(uu&mq|uu&hq|rq&mq|rq&hq|ou&mq|ou&hq|ii&mq|ii&hq|ei&mq|ei&hq|ee&mq|ee&hq|aa&mq|aa&hq|uu&q|u&mq|u&hq|rq&q|ou&q|o&mq|o&hq|ii&q|i&mq|i&hq|ei&q|ee&q|aa&q|a&mq|a&hq|u&q|o&q|i&q|a&q|uu|rq|ou|ii|ei|ee|ax|aa|u|o|i|a)'
t_fullvowel_a = r'.'

def t_error(t):
    print('Lexer error')
    exit(1)

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
    lexer = lex()
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

    parser.parse(g.words.syllabifiedWord)
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

def debug_lexer(wd):
    g = GLOBALS()
    lexer = lex()
    lexer.g = g
    g.flags.DEBUG = True
    lexer.input(wd)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


if __name__ == '__main__':

    if (len(sys.argv) != 2):
        print('Incorrect Usage')
        exit(-1)

    # ans = wordparse(sys.argv[1])
    # print(ans)

    debug_lexer('&a&dh&hq&s&aav&q&w&eev&d&n&iv&k')
    pass