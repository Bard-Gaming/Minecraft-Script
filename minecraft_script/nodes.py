from .tokens import Token
from .errors import MCSValueError, MCSSyntaxError


class NumberNode:
    def __init__(self, number_token: Token):
        self.token = number_token

    def get_value(self):
        return self.token.value

    def __str__(self):
        return f'{self.token.tt_type}:{self.token.value}'

    def __repr__(self):
        return f'NumberNode({self.token !r})'


class StringNode:
    def __init__(self, token):
        self.token = token

    def get_value(self):
        return self.token.value

    def __str__(self):
        return f'String: {self.get_value()}'

    def __repr__(self):
        return f'StringNode({self.token !r})'


class ListNode:
    def __init__(self, array: list):
        self.array = array

    def get_index(self, index: int):
        return self.array[index]

    def __str__(self):
        return f'array node: {self.array}'

    def __repr__(self):
        return f'ListNode({self.array !r})'


class ListGetNode:
    def __init__(self, atom, index):
        self.atom = atom
        self.index = index

    def __str__(self):
        return f'array get: {self.atom} {self.index}'

    def __repr__(self):
        return f'ListGetNode({self.atom !r}, {self.index !r})'


class BooleanNode:
    def __init__(self, token: Token):
        self.value = True if token.value == 'true' else False

    def __str__(self):
        return f'boolean: {str(self.value).lower()}'

    def __repr__(self):
        return f'BooleanNode({str(self.value).lower()})'


class UnaryBooleanNode:
    def __init__(self, unary_token, atom):
        self.unary_token = unary_token
        self.atom = atom

    def get_unary_value(self):
        return self.unary_token.value

    def get_unary_type(self):
        return self.unary_token.tt_type

    def get_atom(self):
        return self.atom

    def __str__(self):
        return f'Unary Bool Node: {self.unary_token}, {self.atom}'

    def __repr__(self):
        return f'UnaryBooleanNode({self.unary_token !r}, {self.atom !r})'


class VariableAssignNode:
    def __init__(self, name_token: Token, value_node):
        self.name_token = name_token
        self.value_node = value_node

    def get_name(self) -> str:
        return self.name_token.value

    def __str__(self):
        return f'Var assign:{self.name_token.value !r} <- {self.value_node}'

    def __repr__(self):
        return f'VariableAssignNode({self.name_token !r}, {self.value_node !r})'


class VariableAccessNode:
    def __init__(self, name_token: Token):
        self.name_token = name_token

    def get_name(self) -> str:
        return self.name_token.value

    def __str__(self):
        return f'Var access:{self.name_token.value !r}'

    def __repr__(self):
        return f'VariableAccessNode({self.name_token !r})'


class FunctionAssignNode:
    def __init__(self, name_token: Token, parameter_name_tokens: list[Token], body_node):
        self.name_token = name_token
        self.parameter_name_tokens = parameter_name_tokens
        self.body_node = body_node

    def __str__(self):
        return f'Func assign:{self.name_token.value !r}'

    def __repr__(self):
        return f'FunctionAssignNode({self.name_token !r}, {self.parameter_name_tokens !r}, {self.body_node !r})'


class FunctionCallNode:
    def __init__(self, atom, argument_nodes: list):
        self.atom = atom
        self.argument_nodes = argument_nodes

    def __str__(self):
        return f'Func call:{self.atom.value !r}'

    def __repr__(self):
        return f'FunctionCallNode({self.atom !r}, {self.argument_nodes !r})'


class BinaryOperationNode:
    def __init__(self, left_node: NumberNode, operator: Token, right_node: NumberNode):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __str__(self):
        return f'({self.left_node !s}, {self.operator.value !s}, {self.right_node !s})'

    def __repr__(self):
        return f'BinaryOperationNode({self.left_node !r}, {self.operator !r}, {self.right_node !r})'


class UnaryOperationNode:
    def __init__(self, operator: Token, right_node: NumberNode):
        self.operator = operator
        self.right_node = right_node

    def __str__(self):
        return f'{str(self.right_node)[:-1]}{self.operator.value !s}{self.right_node.token.value !s}'

    def __repr__(self):
        return f'UnaryOperationNode({self.operator !r}, {self.right_node !r})'


class MultipleStatementsNode:
    def __init__(self, statements: list):
        self.statements = statements
        if any(isinstance(element, ReturnNode) for element in self.statements):
            MCSSyntaxError('Illegal return statement')
            exit()

    def __str__(self):
        return f'statements: {self.statements}'

    def __repr__(self):
        return f'MultipleStatementsNode({self.statements})'


class CodeBlockNode:
    def __init__(self, statements: list):
        self.statements = statements

    def __str__(self):
        return f'Code Block: {self.statements}'

    def __repr__(self):
        return f'CodeBlockNode({self.statements})'


class ReturnNode:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f'return: {self.value}'

    def __repr__(self):
        return f'ReturnNode({self.value})'
