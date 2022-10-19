# combined lexical analyzer and parser

from ply.lex import lex
from ply.yacc import yacc
from helpers import *
import sys

# tokens identified by the lexer
tokens = ('fullvowel_a', 'fullvowel_b', 'kaki_a', 'kaki_b', 'kaki_c', 'conjsyll2_a', 'conjsyll2_b', 'conjsyll2_c',
'conjsyll1', 'nukchan_a','nukchan_b', 'yarule', 'consonant', 'vowel', 'halant', 'matra')

# lexical analyzer part
t_fullvowel_a = r'.'
t_fullvowel_b = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|lx|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(a|aa|i|ii|u|uu|rq|ee|ei|o|ou|ax|a&mq|a&q|a&hq|aa&mq|aa&q|aa&hq|i&mq|ii&q|ii&hq|i&q|i&hq|ii&mq|u&mq|u&q|u&hq|uu&mq|uu&q|uu&hq|rq&mq|rq&q|rq&hq|ee&mq|ee&q|ee&hq|ei&mq|ei&q|ei&hq|o&mq|o&q|o&hq|ou&mq|ou&q|ou&hq)'
t_kaki_a = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|lx|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(aav|iv|iiv|uv|uuv|rqv|aev|eev|eiv|ax|ov|ouv|q|hq|mq)(&)(mq|q|hq)*'
t_kaki_b = r'(&)*(dxq&aav|dxq&iv|dxq&iiv|dxq&uv|dxq&uuv|dxq&rqv|dxq|dxq&eev|dxq&eiv|dxq&ov|dxq&ouv|dxq&mq|dxq&q|dxq&hq)'
t_conjsyll2_a = r'(&)*(kq|khq|gq|z|dxq|dxhq|f|y)(&)eu'
t_conjsyll2_b = r'(&)*(k&eu|kh&eu|g&eu|gh&eu|c&eu|ch&eu|j&eu|jh&eu|ng&eu|nj&eu|tx&eu|txh&eu|dx&eu|dxh&eu|nx&eu|t&eu|th&eu|d&eu|dh&eu|n&eu|p&eu|ph&eu|b&eu|bh&eu|m&eu|y&eu|r&eu|l&eu|lx&eu|w&eu|sh&eu|sx&eu|s&eu|h&eu)'
t_conjsyll1 = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|lx|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(aa|i|ii|u|uu|rq|ee|ei|o|ou|ax)(&)(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|aa|i|ii|u|uu|rq|ee|ei|o|ou|aav|iv|iiv|uv|uuv|rqv|aev|eev|eiv|ax|ov|ouv|mq|q|hq)(&)eu(&)(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|h|kq|khq|gq|z|dxq|dxhq|f|y)'
t_nukchan_a = r'(&)*(kq|khq|gq|z|dxq|dxhq|f|y)(&)(mq|q|hq)'
t_nukchan_b = r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|lx|w|sh|sx|s|h)(&)(mq|q|hq)'
t_yarule = r'(&)*(iv|iiv|uv|uuv|rqv)(&)(y)'
t_vowel = r'(&)*(a|aa|i|ii|u|uu|rq|ee|ei|o|ou|ax|a&mq|a&q|a&hq|aa&mq|aa&q|aa&hq|i&mq|ii&q|ii&hq|i&q|i&hq|ii&mq|u&mq|u&q|u&hq|uu&mq|uu&q|uu&hq|rq&mq|rq&q|rq&hq|ee&mq|ee&q|ee&hq|ei&mq|ei&q|ei&hq|o&mq|o&q|o&hq|ou&mq|ou&q|ou&hq)'

def t_conjsyll2_c(t):
    r'(eu)'
    t.value = 'eu&#'
    return t

def t_kaki_c(t):
    r'(\&)*(k|kh|lx|rx|g|gh|ng|c|ch|j|jh|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|r|l|w|sh|sx|zh|y|s|h|f|dxq|z|kq|khq|gq|dxhq)((&)(lx|k|kh|g|gh|ng|c|ch|j|jh|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|zh|y|s|h|ex|rx|f|dxq|z|kq|khq|gq|dxhq))*'
    s = t.value
    ans = ''
    i = 1
    if s[0] == '&':
        ans += '&'
    l = s.split('&')
    for pch in l:
        ans += f'{pch}&av&#&&'
        i += 1
    ans = ans[:(len(ans) - 7)]
    t.value = ans
    return t

def t_error(t):
    print('Lexer error')
    exit(1)

# parser part

def p_sentence(p):
    '''
    sentence : words
    '''
    global flags, words
    if flags.parseLevel == 0:
        words.syllabifiedWordOut = p[1]

        if words.syllabifiedWordOut.find('&&') != -1:
            words.syllabifiedWordOut = words.syllabifiedWordOut.replace("&&","&")
        
        flags.parseLevel += 1
    else:
        words.phonifiedWord = p[1]


def p_words_syltoken(p):
    '''
    words : syltoken
    '''
    global flags
    if flags.DEBUG:
        print(f'\nSyll:\t{p[1]}')
    p[0] = p[1]

def p_words_wordsandsyltoken(p):
    '''
    words : words syltoken
    '''
    p[0] = p[1] + p[2]

def p_syltoken(p):
    '''
    syltoken : fullvowel_a
             | fullvowel_b
             | kaki_a
             | kaki_b
             | kaki_c
             | conjsyll2_a
             | conjsyll2_b
             | conjsyll2_c
             | conjsyll1 
             | nukchan_a
             | nukchan_b
             | yarule
             | consonant
             | vowel
             | halant
             | matra
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

def main():
    global flags, words, outputFile, langId
    lexer = lex()
    parser = yacc()

    argc = len(sys.argv)
    argv = sys.argv

    if argc <= 5:
        print('READ HELP!!')
        exit(1)
    
    if argv[2] != '1':
        flags.LangSpecificCorrectionFlag = 0
    
    flags.writeFormat = int(argv[3])
    if argv[3] == '4':
        flags.writeFormat = 1
        flags.syllTagFlag = 1
    
    if argv[4] == '1':
        outputFile = 'wordpronunciationsyldict'
    
    if argv[5] == '1':
        flags.pruiningFlag = 1
        outputFile = 'wordpronunciation'
        flags.writeFormat = 3
    
    if argc > 6 and argv[6] == '1':
        flags.directParseFlag = 1
        langId = int(argv[7])
    
    if argc > 8:
        outputFile = 'wordpronunciation' + argv[8]
    else:
        outputFile = 'wordpronunciation'
        if argv[4] == '1':
            outputFile = 'wordpronunciationsyldict'
    
    word = argv[1]
    if flags.DEBUG:
        print(f'Word {word}')
    
    if flags.directParseFlag != 1:
        word = RemoveUnwanted(word)
    if flags.DEBUG:
        print(f'Cleared Word : {word}')
    
    if SetlanguageFeat(word) == 0:
        return 0
    if flags.directParseFlag == 1:
        langId = int(argv[7])
    
    if CheckDictionary(word) != 0:
        return 0
    if flags.DEBUG:
        print(f'langId : {langId}')
    word = ConvertToSymbols(word)
    if flags.directParseFlag == 1:
        words.syllabifiedWord = argv[1]
        print(f'{word}')
    
    if flags.DEBUG:
        print(f"Symbols code : {words.unicodeWord}");
        print(f"Symbols syllables : {words.syllabifiedWord}");

    parser.parse(words.syllabifiedWord)

    if flags.DEBUG:
        print(f'Syllabified Word : {words.syllabifiedWordOut}')
    
    words.syllabifiedWordOut = words.syllabifiedWordOut.replace("&#&","&") + '&'
    if flags.DEBUG:
        print(f'Syllabified Word out : {words.syllabifiedWordOut}')

    words.syllabifiedWordOut = LangSpecificCorrection(words.syllabifiedWordOut, flags.LangSpecificCorrectionFlag)
    if flags.DEBUG:
        print(f'Syllabified Word langCorr : {words.syllabifiedWordOut}')
    words.syllabifiedWordOut = CleanseWord(words.syllabifiedWordOut)
    if flags.DEBUG:
        print(f'Syllabified Word memCorr : {words.syllabifiedWordOut}')
   

if __name__ == '__main__':
    main()
    pass