# dictionary of names
names = {}

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)


######################################################
#                   STATEMENTS/VARS                  #
######################################################

def p_statement_define_value(p):
    'statement : VAR_DEFINE NAME "=" expression'
    names[p[2]] = p[4]


def p_statement_define(p):
    'statement : VAR_DEFINE NAME'
    names[p[2]] = 0


def p_statement_assign(p):
    'statement : NAME "=" expression'
    if names.get(p[1]) is not None:
        names[p[1]] = p[3]
    else:
        print(f'Undefined name {p[1]}')

def p_statement_log(p):
    'statement : LOG expression'
    print(p[2])

def p_statement_expr(p):
    'statement : expression'
    print(p[1])


######################################################
#                  BINARY OPERATIONS                 #
######################################################

def p_expression_add(p):
    "expression : expression '+' expression"
    p[0] = p[1] + p[3]


def p_expression_subtract(p):
    "expression : expression '-' expression"
    p[0] = p[1] - p[3]


def p_expression_multiply(p):
    "expression : expression '*' expression"
    p[0] = p[1] * p[3]


def p_expression_divide(p):
    "expression : expression '/' expression"
    p[0] = p[1] // p[3]


######################################################
#                    EXPRESSIONS                     #
######################################################

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    p[0] = names.get(p[1])
    if p[0] is None:
        print(f"Undefined name {p[1]}")
        exit()


######################################################
#                    MISCELLANEOUS                   #
######################################################

def p_error(p):
    if p:
        print(f"Syntax error at {p.value}")
    else:
        print("Syntax error at EOF")
