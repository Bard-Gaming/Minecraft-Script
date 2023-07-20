from tokens import Token


class Parser:
    def __init__(self, token_list: list[Token]):
        self.token_list = token_list
        self.current_index = -1
        self.current_token = None

        self.advance()

    def advance(self):
        self.current_index += 1
        self.current_token = self.token_list[self.current_index] if self.current_index < len(self.token_list) else None

    def factor(self):
        token = self.current_token

        if token.tt_type == 'TT_NUMBER':
            self.advance()
            return NumberNode(token)

    # def binary_operation(self, function, ops):


# ----------------------- Operations ----------------------- :

class NumberNode:
    def __init__(self, number_token: Token):
        self.token = number_token

    def __str__(self):
        return f'{self.token.tt_type}: {self.token.value}'

    def __repr__(self):
        return f'NumberNode({self.token !r})'


class BinaryOperationNode:
    def __init__(self, left_node: NumberNode, operator: Token, right_node: NumberNode):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __str__(self):
        return f'([{self.left_node !s}] {self.operator.value !s} [{self.right_node !s}])'

    def __repr__(self):
        return f'BinaryOperationNode({self.left_node !r}, {self.operator !r}, {self.right_node !r})'


class UnaryOperationNode:
    def __init__(self, operator: Token, right_node: NumberNode):
        self.operator = operator
        self.right_node = right_node

    def __str__(self):
        return f'[{str(self.right_node)[:-1]}{self.operator.value !s}{self.right_node.token.value !s}]'

    def __repr__(self):
        return f'UnaryOperationNode({self.operator !r}, {self.right_node !r})'


if __name__ == '__main__':
    a = BinaryOperationNode(NumberNode(Token(5, 'TT_NUMBER')), Token('+', 'TT_BINARY_OPERATOR'),
                            NumberNode(Token(7, 'TT_NUMBER')))
    b = UnaryOperationNode(Token('-', 'TT_BINARY_OPERATOR'), NumberNode(Token(7, 'TT_NUMBER')))
    print(b)
