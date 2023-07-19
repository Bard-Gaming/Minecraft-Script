reserved = {
    'var': 'VAR_DEFINE',
    'const': 'CONST_DEFINE',
    'log': 'LOG',
    'logtype': 'LOGTYPE'
}

tokens = [
    'NAME', 'NUMBER',
] + list(reserved.values())

literals = ['=', '+', '-', '*', '/', '(', ')']


# Tokens

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_COMMENT(t):
    r'\/\/.*'
    pass

def t_error(t):
    print(f"Lexer Error: Illegal character {t.value[0] !r}")
    t.lexer.skip(1)
