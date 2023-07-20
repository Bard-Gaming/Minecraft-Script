reserved = {
    'var': 'VAR_DEFINE',
    'const': 'CONST_DEFINE',
    'function': 'FUNCTION_DEFINE',
    'log': 'LOG',
    'logtype': 'LOGTYPE',
}

tokens = [
    'NAME', 'NUMBER',
    'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS',
    'FUNCTION_ARROW', 'FUNCTION_BLOCK', 'FUNCTION_PARAMETER',
] + list(reserved.values())

literals = ['=', '+', '-', '*', '/', '{', '}']

t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_FUNCTION_ARROW = r'\=\>'
t_FUNCTION_BLOCK = r'{(.|\n)*}'
t_FUNCTION_PARAMETER = r'\(([a-zA-Z_][a-zA-Z_0-9]*)(,\s?[a-zA-Z_][a-zA-Z_0-9]*)*\)'
t_ignore = " \t"


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT(t):
    r'\/\/.*'
    pass


def t_error(t):
    print(f"Lexer Error: Illegal character {t.value[0] !r}")
    t.lexer.skip(1)
