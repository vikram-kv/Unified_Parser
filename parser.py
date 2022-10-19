# combined lexical analyzer and parser

from re import I
from ply.lex import lex
from ply.yacc import yacc
from helpers import *

# tokens identified by the lexer
tokens = ('space', 'fullvowel', 'kaki', 'conjsyll2', 'conjsyll1', 'nukchan', 'yarule', 'consonant', 'vowel', 'halant', 'matra')




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
    syltoken : fullvowel
             | kaki
             | conjsyll2
             | conjsyll1 
             | nukchan
             | yarule
             | consonant
             | vowel
             | halant
             | matra
    '''
    p[0] = p[1]

if __name__ == '__main__':
    parser = yacc()
    pass