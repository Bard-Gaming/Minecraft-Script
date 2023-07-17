from minecraft_script.tokens import Token


class NumberNode:
    def __init__(self, token: Token):
        self.token = token

    def __repr__(self):
        return f'NumberNode({self.token})'


class BinaryOperationNode:
    def __init__(self, left_node: NumberNode, operator: Token, right_node: NumberNode):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'BinaryOperationNode({self.left_node}, {self.operator}, {self.right_node})'


class Parser:
    term_types = ['TT_MULTIPLY', 'TT_DIVIDE']
    expression_types = ['TT_PLUS', 'TT_MINUS']

    def __init__(self, tokens: [Token]):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.next_token()

    def next_token(self) -> Token:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self) -> NumberNode:
        current_token = self.current_token
        if current_token.type == 'TT_INTEGER':
            self.next_token()
            return NumberNode(current_token)

    def binary_operation(self, function, operation_types: [str]) -> BinaryOperationNode:
        left_number = function()
        operation_node = None

        print(left_number)

        while self.current_token.type in operation_types:
            operator_token = self.current_token
            self.next_token()
            right_number = function()
            operation_node = BinaryOperationNode(left_number, operator_token, right_number)
            print(operation_node, left_number, operator_token, right_number)

        return operation_node

    def term(self) -> BinaryOperationNode:
        return self.binary_operation(self.factor, self.term_types)

    def expression(self) -> BinaryOperationNode:
        return self.binary_operation(self.term, self.expression_types)

    def parse(self):
        return self.expression()

if __name__ == '__main__':
    parser = Parser([Token('TT_INTEGER', '5'), Token('TT_PLUS', None), Token('TT_INTEGER', '5')])
    print(parser.parse())