import ply.lex as lex

literals = ['=', '+', '-', '*', '/', '(', ')', ';']

keywords = {
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT'
}

tokens = list(keywords.values()) + [
    'INUMBER',
    'FNUMBER',
    'ID'
]

t_ignore = " \t"

t_INUMBER = r'\d+'
t_FNUMBER = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'

def t_ID(t):
    r'[a-zA-Z_][\w]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Build Lexer
lexer = lex.lex()