# Python_Unified_Parser


Yacc file - unified.y - Contains grammar rules and associated actions for each rule. Has a lot of helper functions. Need to figure out the purpose of each one.

Lex file - unified.l - Contains regexs for every token in our grammar.

utf8.c / utf8.h - Contains 2 replace functions that find and replace one / more occurrences of a supplied subtring with a new string in a given string.

Our python parser - parser.py - Combines lex and yacc functionality in a single python script using the PLY framework.

ply folder - contains the code files for the PLY framework.

yply folder - contains code for conversion of .l and .y files to ply's .py scripts. Doesn't work! :)
