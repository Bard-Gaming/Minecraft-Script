# dictionary to store variables
names = {}


######################################################
#                  BINARY OPERATIONS                 #
######################################################

def p_sum(t):
    "expression : expression PLUS expression"
    t[0] = t[1] + t[3]  # t[2] = '+'


def p_subtract(t):
    "expression : expression MINUS expression"
    t[0] = t[1] - t[3]  # t[2] = '-'


def p_multiply(t):
    "expression : expression MULTIPLY expression"
    t[0] = t[1] * t[3]  # t[2] = '*'


def p_divide(t):
    "expression : expression DIVIDE expression"
    t[0] = t[1] // t[3]  # t[2] = '/'


######################################################
#                  NUMBERS & EXPRESSIONS             #
######################################################

def p_expression_group(t):
    "expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS"
    t[0] = t[2]


def p_expression_number(t):
    "expression : NUMBER"
    t[0] = t[1]


def p_expression_name(t):
    "expression : NAME"
    t[0] = names.get(t[1])
    if t[0] is None:
        print(f'Undefined name {t[1]}')
        t[0] = 0


######################################################
#                       VARIABLES                    #
######################################################

def p_statement_var_define(t):
    "statement : VAR_DEFINE NAME EQUALS expression"
    names[t[2]] = t[4]
    t[0] = t[4]


def p_statement_log(t):
    "expression : LOG expression"
    print(f'[ * ] {t[2]}')


def p_statement_expression(t):
    "statement : expression"
    t[0] = t[1]


######################################################
#                       MISC.                        #
######################################################

def p_error(t):
    if t is None:  # lexer error
        return
    print(f"Syntax Error: {t.value !r} at line {t.lineno}, position {t.lexpos}")
