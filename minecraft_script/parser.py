from .print_colors import print_error

# dictionary of names
names = {}

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)


def is_name(name: str) -> bool:
    return bool(names.get(name, False))


def is_const(name: str) -> bool:
    return names.get(name, {}).get('type') == 'const'


######################################################
#                   STATEMENTS/VARS                  #
######################################################

def p_statement_declare_value(p):
    '''statement : VAR_DEFINE NAME "=" expression
                 | CONST_DEFINE NAME "=" expression'''
    if is_name(p[2]) and is_const(p[2]):
        print_error(f'Type Error: Constant {p[2] !r} has already been declared')
        exit()

    names[p[2]] = {
        'type': p[1],
        'value': p[4],
    }


def p_statement_declare(p):
    '''statement : VAR_DEFINE NAME
                 | CONST_DEFINE NAME'''
    if is_const(p[1]):
        print_error('Syntax Error: Missing value in const declaration')
        exit()

    names[p[2]] = {
        'type': p[1],
        'value': 0,
    }


def p_statement_assign(p):
    'statement : NAME "=" expression'
    if is_name(p[1]) and not is_const(p[1]):
        names[p[1]]['value'] = p[3]

    elif is_const(p[1]):
        print_error(f'Type Error: Tried to assign new value to const {p[1] !r}')
        exit()

    else:
        print_error(f'KeyError: Undefined name {p[1] !r}')
        exit()


def p_statement_log(p):
    'statement : LOG expression'
    print(p[2])


def p_statement_log_type(p):
    '''statement : LOGTYPE NAME
                 | LOGTYPE NUMBER'''
    try:
        int(p[2])
    except ValueError:
        isNumber = False
    else:
        isNumber = True

    if isNumber:
        print('number')
    else:
        if names.get(p[2]) is None:
            print(f'KeyError: Undefined name {p[1]}')
        else:
            print(names.get(p[2])['type'])


def p_statement_expr(p):
    'statement : expression'
    print_error(p[1])


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
    p[0] = names.get(p[1])['value']
    if p[0] is None:
        print_error(f"Undefined name {p[1]}")
        exit()


######################################################
#                    MISCELLANEOUS                   #
######################################################

def p_error(p):
    if p:
        print_error(f"Syntax error at {p.value}")
        exit()
