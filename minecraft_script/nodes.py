from .tokens import Token
from .errors import MCSValueError


class NumberNode:
    def __init__(self, number_token: Token):
        self.token = number_token

    def get_value(self):
        return self.token.value

    def __str__(self):
        return f'{self.token.tt_type}:{self.token.value}'

    def __repr__(self):
        return f'NumberNode({self.token !r})'


class VariableAccessNode:
    def __init__(self, name_token: Token):
        self.name_token = name_token

    def get_name(self) -> str:
        return self.name_token.value

    def __str__(self):
        return f'Var access:{self.name_token.value !r}'

    def __repr__(self):
        return f'VariableAccessNode({self.name_token !r})'


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
