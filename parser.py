# combined lexical analyzer and parser

from ply.lex import lex
from ply.yacc import yacc
from helpers import *

# tokens identified by the lexer
tokens = ('space', 'fullvowel_a', 'fullvowel_b', 'kaki_a', 'kaki_b', 'conjsyll2_a', 'conjsyll2_b', 'conjsyll2_c'
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

if __name__ == '__main__':
    lexer = lex()
    parser = yacc()
    pass