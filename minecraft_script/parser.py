from .print_colors import print_error


class AnonymousFunction:
    def __init__(self, parameters: str, instructions: str):
        parameters = [param_name.strip(' ') for param_name in parameters.lstrip('(').rstrip(')').split(',')]
        self.parameters = dict.fromkeys(parameters)
        self.instructions = instructions.replace('¤', '\n')[1:-1]

    def call(self, arguments: str):
        argument_list = [arg_name.strip(' ') for arg_name in arguments.lstrip('(').rstrip(')').split(',')]
        param_instructions = ''

        global_scope_names = {}
        # copy names (vars) that are used in the function call into global_scope_names
        for i in range(len(self.parameters.keys())):
            parameter = list(self.parameters.keys())[i]
            try:
                argument = argument_list[i]
            except IndexError:
                print_error(f'Invalid arguments: {arguments !r}')
            finally:
                if names.get(parameter, False):
                    global_scope_names[parameter] = names[parameter]
                param_instructions += f'var {parameter} = {argument}\n'

        from .interpreter import parse_line, parse_text
        print(param_instructions)
        print('CALLING')
        parse_line(param_instructions.split('\n')[0])
        print(names)
        parse_text(self.instructions)

    def __repr__(self):
        return f'AnonymousFunction("({",".join(self.parameters)})", {("{" + self.instructions + "}") !r})'


ignore_warnings = False

# memory
names = {}
functions = []

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
                 | CONST_DEFINE NAME "=" expression
                 | FUNCTION_DEFINE NAME "=" function'''
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
    "expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS"
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


def p_expression_repeat(p):
    '''expression_repeat :
                         | expression expression_repeat'''
    if p[1] and p[2]:
        expr_list = [p[1]]
        expr_list.extend(p[2])
        p[0] = expr_list

    elif p[1]:
        p[0] = [p[1]]

    else:
        p[0] = None


######################################################
#                     FUNCTIONS                      #
######################################################

def p_statement_function_call(p):
    'statement : function LEFT_PARENTHESIS expression_repeat RIGHT_PARENTHESIS'
    p[1].call(p[3])

def p_function_anonymous_define(p):
    'function : FUNCTION_PARAMETER FUNCTION_ARROW FUNCTION_BLOCK'
    anonymous_function = AnonymousFunction(p[1], p[3])
    print(anonymous_function)
    p[0] = anonymous_function


######################################################
#                    MISCELLANEOUS                   #
######################################################

def p_error(p):
    if p:
        print_error(f"Syntax error: {p.value !r}")
        exit()
