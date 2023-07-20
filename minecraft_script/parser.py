from tokens import Token
from operations import NumberNode, BinaryOperationNode, UnaryOperationNode


class Parser:
    def __init__(self, token_list: list[Token]):
        self.token_list = token_list
        self.current_index = -1
        self.current_token = None

        self.advance()

    def advance(self):
        self.current_index += 1
        if self.current_index < len(self.token_list):
            self.current_token = self.token_list[self.current_index]

    def parse(self):
        result = self.expression()
        return result

    def factor(self) -> NumberNode | UnaryOperationNode | BinaryOperationNode:
        token = self.current_token

        if token.value in ['+', '-']:
            self.advance()
            factor = self.factor()
            return UnaryOperationNode(token, factor)

        elif token.tt_type == 'TT_LEFT_PARENTHESIS':
            self.advance()
            expression = self.expression()
            if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
                self.advance()
                return expression

        elif token.tt_type == 'TT_NUMBER':
            self.advance()
            return NumberNode(token)

    def term(self) -> BinaryOperationNode:
        return self.binary_operation(self.factor, ['*', '/', '%'])

    def expression(self) -> BinaryOperationNode:
        return self.binary_operation(self.term, ['+', '-'])

    def binary_operation(self, function, operators) -> BinaryOperationNode:
        left_node = function()
        # self.current_token is now the operator

        while self.current_token.value in operators:
            operator = self.current_token
            self.advance()
            right_node = function()
            left_node = BinaryOperationNode(left_node, operator, right_node)
        return left_node


if __name__ == '__main__':
    tokens = [Token(5, 'TT_NUMBER'), Token('+', 'TT_BINARY_OPERATOR'), Token(5, 'TT_NUMBER'), Token('*', 'TT_BINARY_OPERATOR'), Token('(', 'TT_LEFT_PARENTHESIS'), Token(3, 'TT_NUMBER'), Token('+', 'TT_BINARY_OPERATOR'), Token('-', 'TT_BINARY_OPERATOR'), Token(5, 'TT_NUMBER'), Token(')', 'TT_RIGHT_PARENTHESIS')]
    print(Parser(tokens).parse())
