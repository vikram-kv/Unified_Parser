# combined lexical analyzer and parser

from ply.lex import lex
from ply.yacc import yacc

# tokens identified by the lexer
tokens = ('space', 'fullvowel', 'kaki', 'conjsyll2', 'conjsyll1', 'nukchan', 'yarule', 'consonant', 'vowel', 'halant', 'matra')


