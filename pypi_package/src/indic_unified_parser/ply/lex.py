from typing import NamedTuple
import re

def t_kaki_c(t):
    r'(&)*(dxhq|txh|khq|dxq|dxh|zh|tx|th|sx|sh|rx|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)((&)(dxhq|txh|khq|dxq|dxh|zh|tx|th|sx|sh|rx|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|ex|dx|dh|ch|bh|z|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b))*'
    s = t
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
    return ans

def t_conjsyll2_c(t):
    r'(eu)'
    return 'eu&#'

def t_fullvowel_b(t):
    r'(&)*(k|kh|g|gh|c|ch|j|jh|ng|nj|tx|txh|dx|dxh|nx|t|th|d|dh|n|p|ph|b|bh|m|y|r|l|w|sh|sx|s|lx|h|kq|khq|gq|z|dxq|dxhq|f|y)(&)(uu&mq|uu&hq|rq&mq|rq&hq|ou&mq|ou&hq|ii&mq|ii&hq|ei&mq|ei&hq|ee&mq|ee&hq|aa&mq|aa&hq|uu&q|u&mq|u&hq|rq&q|ou&q|o&mq|o&hq|ii&q|i&mq|i&hq|ei&q|ee&q|aa&q|a&mq|a&hq|u&q|o&q|i&q|a&q|uu|rq|ou|ii|ei|ee|ax|aa|u|o|i|a)'
    return t

def t_kaki_a(t):
    r'(&)*(dxhq|txh|khq|dxq|dxh|tx|th|sx|sh|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)(&)(uuv|rqv|ouv|iiv|eiv|eev|aev|aav|uv|ov|mq|iv|hq|ax|q)(&)(mq|hq|q)*'
    return t

def t_kaki_b(t):
    r'(&)*(dxq&uuv|dxq&rqv|dxq&ouv|dxq&iiv|dxq&eiv|dxq&eev|dxq&aav|dxq&uv|dxq&ov|dxq&mq|dxq&iv|dxq&hq|dxq&q|dxq)'
    return t

def t_conjsyll2_b(t):
    r'(&)*(txh&eu|dxh&eu|tx&eu|th&eu|sx&eu|sh&eu|ph&eu|nx&eu|nj&eu|ng&eu|lx&eu|kh&eu|jh&eu|gh&eu|dx&eu|dh&eu|ch&eu|bh&eu|y&eu|w&eu|t&eu|s&eu|r&eu|p&eu|n&eu|m&eu|l&eu|k&eu|j&eu|h&eu|g&eu|d&eu|c&eu|b&eu)'
    return t

def t_conjsyll2_a(t):
    r'(&)*(dxhq|khq|dxq|kq|gq|z|y|f)(&)eu'
    return t

def t_conjsyll1(t):
    r'(&)*(dxhq|txh|khq|dxq|dxh|tx|th|sx|sh|ph|nx|nj|ng|lx|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)(&)(uu|rq|ou|ii|ei|ee|ax|aa|u|o|i)(&)(dxhq|uuv|txh|rqv|ouv|khq|iiv|eiv|eev|dxq|dxh|aev|aav|uv|uu|tx|th|sx|sh|rq|ph|ov|ou|nx|nj|ng|mq|kq|kh|jh|iv|ii|hq|gq|gh|ei|ee|dx|dh|ch|bh|ax|aa|z|y|w|u|t|s|r|q|p|o|n|m|l|k|j|i|h|g|f|d|c|b)(&)eu(&)(dxhq|txh|khq|dxq|dxh|tx|th|sx|sh|ph|nx|nj|ng|kq|kh|jh|gq|gh|dx|dh|ch|bh|z|y|y|w|t|s|r|p|n|m|l|k|j|h|g|f|d|c|b)'
    return t

def t_nukchan_b(t):
    r'(&)*(txh|dxh|tx|th|sx|sh|ph|nx|nj|ng|lx|kh|jh|gh|dx|dh|ch|bh|y|w|t|s|r|p|n|m|l|k|j|h|g|d|c|b)(&)(mq|hq|q)'
    return t

def t_nukchan_a(t):
    r'(&)*(dxhq|khq|dxq|kq|gq|z|y|f)(&)(mq|hq|q)'
    return t

def t_yarule(t):
    r'(&)*(uuv|rqv|iiv|uv|iv)(&)(y)'
    return t

def t_vowel(t):
    r'(&)*(uu&mq|uu&hq|rq&mq|rq&hq|ou&mq|ou&hq|ii&mq|ii&hq|ei&mq|ei&hq|ee&mq|ee&hq|aa&mq|aa&hq|uu&q|u&mq|u&hq|rq&q|ou&q|o&mq|o&hq|ii&q|i&mq|i&hq|ei&q|ee&q|aa&q|a&mq|a&hq|u&q|o&q|i&q|a&q|uu|rq|ou|ii|ei|ee|ax|aa|u|o|i|a)'
    return t

def t_fullvowel_a(t):
    r'.'
    return t

class Token(NamedTuple):
    type: str
    value: str

class Lexer:
    def __init__(self):
        # tokens identified by the lexer
        self.tokens = ('kaki_c', 'conjsyll2_c', 'fullvowel_b', 'kaki_a', 'kaki_b',  'conjsyll2_b', 'conjsyll2_a',
        'conjsyll1', 'nukchan_b','nukchan_a', 'yarule', 'fullvowel_a', 'vowel')
        self.token_specification = []
        for tkn in self.tokens:
            self.token_specification += [(tkn, r'{}'.format(eval('t_'+tkn).__doc__), eval('t_'+tkn))]

        self.patterns = []
        for pr in self.token_specification:
            pn = re.compile(pr[1])
            self.patterns += [pn]
        self.tokencount = len(self.token_specification)
        self.data = ''
        self.idx = 0
    
    def input(self,data):
        self.data = data
        self.idx = 0

    def token(self):
        maxlen = 0
        maxidx = -1
        maxmo = None
        for i in range(self.tokencount):
            mo = self.patterns[i].match(self.data, self.idx)
            if mo != None:
                molen = mo.end() - mo.start()
                if molen > maxlen:
                    maxlen = molen
                    maxidx = i
                    maxmo = mo
        
        if maxlen == 0:
            return None
        self.idx += maxlen
        tok = self.token_specification[maxidx][2](maxmo.group())
        return Token(type = self.tokens[maxidx], value=tok)