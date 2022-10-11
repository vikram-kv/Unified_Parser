# combined lexical analyzer and parser


# global CONSTANTs for languages. Uses the same values as the enum at 
# lines 11-13 of unified.y

MALAYALAM=1
TAMIL = 2
TELUGU = 3
KANNADA = 4
HINDI = 5
BENGALI = 6
GUJARATHI = 7
ODIYA = 8
ENGLISH = 9

# variable to indicate current language being parsed.
currLang = ENGLISH




from ply.lex import lex
from ply.yacc import yacc

# tokens identified by the lexer
tokens = ('space', 'fullvowel', 'kaki', 'conjsyll2', 'conjsyll1', 'nukchan', 'yarule', 'consonant', 'vowel', 'halant', 'matra')


