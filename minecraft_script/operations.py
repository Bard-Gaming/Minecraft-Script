from tokens import Token


class NumberNode:
    def __init__(self, number_token: Token):
        self.token = number_token

    def __str__(self):
        return f'{self.token.tt_type}:{self.token.value}'

    def __repr__(self):
        return f'NumberNode({self.token !r})'


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
