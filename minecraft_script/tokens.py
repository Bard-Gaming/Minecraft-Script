reserved = {
    "var": "VAR_DEFINE",
    "log": "LOG",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
}

tokens = [
    'NUMBER',
    'PLUS', 'MINUS',
    'MULTIPLY', 'DIVIDE',
    'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS',
    'NAME',
]
tokens += list(reserved.values())

literals = ['=']

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'

t_ignore = ' \t'


def t_NUMBER(t):
    r"\d+"
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Failed to parse to integer: {t.value}")
        t.value = 0
    return t


def t_COMMENT(t):
    r"\/\/.*"  # JS comments B)
    return None


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')  # check for reserved keywords

    return t


def t_error(t):
    print(f"Illegal character {t.value[0]!r} on line {t.lexer.lineno}")
    t.lexer.skip(1)
