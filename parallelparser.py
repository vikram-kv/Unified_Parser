# combined lexical analyzer and parser

from ply.lex import lex
from ply.yacc import yacc
from globals import *
from helpers import *

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
    ans = ans[:(len(ans) - 7)]
    t.value = ans
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
    g.flags.DEBUG = True
    lexer = lex()
    parser = yacc()
    parser.g = g

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
    
    if g.flags.directParseFlag != 1:
        word = RemoveUnwanted(word)
    
    if SetlanguageFeat(g, word) == 0:
        return 0
    if g.flags.directParseFlag == 1:
        g.langId = int(argv[7])
    
    if CheckDictionary(g, word) != 0:
        return 0
    word = ConvertToSymbols(g, word)
    if g.flags.directParseFlag == 1:
        g.words.syllabifiedWord = argv[1]
        print(f'{word}')

    parser.parse(g.words.syllabifiedWord)
    g.words.syllabifiedWordOut = g.words.syllabifiedWordOut.replace("&#&","&") + '&'
    g.words.syllabifiedWordOut = LangSpecificCorrection(g, g.words.syllabifiedWordOut, g.flags.LangSpecificCorrectionFlag)
    g.words.syllabifiedWordOut = CleanseWord(g.words.syllabifiedWordOut)

    if not g.isSouth:
        count = 0
        for i in range(len(g.words.syllabifiedWordOut)):
            if i == '&':
                count += 1
        splitPosition = 2
        if GetPhoneType(g, g.words.syllabifiedWord, 1) == 1:
            if count > 2:
                tpe = GetPhoneType(g, g.words.syllabifiedWord, 2)
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

        end = SchwaSpecificCorrection(g, end)
        g.words.syllabifiedWordOut = start + end
        g.words.syllabifiedWordOut = CleanseWord(g.words.syllabifiedWordOut)
        g.words.syllabifiedWordOut = SchwaDoubleConsonent(g.words.syllabifiedWordOut)
    
    g.words.syllabifiedWordOut = GeminateCorrection(g.words.syllabifiedWordOut, 0)
    
    g.words.syllabifiedWordOut = MiddleVowel(g, g.words.syllabifiedWordOut)

    g.words.syllabifiedWordOut = Syllabilfy(g.words.syllabifiedWordOut)
    
    SplitSyllables(g,g.words.syllabifiedWordOut)
    
    WritetoFiles(g)
    return g.answer

if __name__ == '__main__':
    ans = wordparse('कबाड़')
    print(ans)
    pass