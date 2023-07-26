from .tokens import Token
from .errors import MCSSyntaxError
from .text_additions import text_underline
from .nodes import NumberNode, BinaryOperationNode, UnaryOperationNode, VariableAssignNode, VariableAccessNode, \
    FunctionAssignNode, FunctionCallNode, MultipleStatementsNode, ListNode, ListGetNode


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
        result = self.statement()
        return result

    def factor(self) -> NumberNode | UnaryOperationNode | BinaryOperationNode | VariableAccessNode | FunctionCallNode | ListNode:
        token = self.current_token

        if token.value in ['+', '-']:
            self.advance()
            factor = self.factor()
            return UnaryOperationNode(token, factor)

        elif token.tt_type == 'TT_NAME':
            self.advance()

            if self.current_token.tt_type == 'TT_LEFT_PARENTHESIS':
                return self.function_call(token)

            elif self.current_token.tt_type == 'TT_LEFT_BRACKET':
                return self.array_get(token)

            return VariableAccessNode(token)

        elif token.tt_type == 'TT_LEFT_PARENTHESIS':
            self.advance()
            expression = self.expression()
            if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
                self.advance()
                return expression

        elif token.tt_type == 'TT_LEFT_BRACKET':
            return self.array()

        elif token.tt_type == 'TT_NUMBER':
            self.advance()
            return NumberNode(token)

    def term(self) -> BinaryOperationNode:
        return self.binary_operation(self.factor, ['*', '/', '%'])

    def expression(self) -> BinaryOperationNode | VariableAssignNode | FunctionAssignNode:
        if self.current_token.tt_type == 'VAR_DEFINE':
            self.advance()
            if self.current_token.tt_type != 'TT_NAME':
                MCSSyntaxError(f'Expected name. Got {text_underline(f"{self.current_token.value !r}")} instead.')
                exit()

            var_name_token = self.current_token
            self.advance()

            if self.current_token.tt_type != 'TT_EQUALS':
                MCSSyntaxError(f'Expected "=". Got {text_underline(f"{self.current_token.value !r}")} instead')
                exit()

            self.advance()
            return VariableAssignNode(var_name_token, self.expression())

        elif self.current_token.tt_type == 'FUNC_DEFINE':
            return self.function_define()

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

    def statement(self) -> MultipleStatementsNode:
        statements = []
        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()
        statements.append(self.expression())

        while self.current_token.tt_type == 'TT_NEWLINE':
            while self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()
            statements.append(self.expression())

        return MultipleStatementsNode(statements)

    def function_define(self) -> FunctionAssignNode:
        self.advance()

        function_name_token = None
        if self.current_token.tt_type == 'TT_NAME':
            function_name_token = self.current_token
            self.advance()

        if self.current_token.tt_type != 'TT_EQUALS':
            MCSSyntaxError(f'Expected "=". Got {text_underline(f"{self.current_token.value !r}")} instead')
            exit()
        self.advance()

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            MCSSyntaxError(f'Expected "(". Got {text_underline(f"{self.current_token.value !r}")} instead')
            exit()
        self.advance()

        function_parameters = []
        if self.current_token.tt_type == 'TT_NAME':
            function_parameters.append(self.current_token)
            self.advance()

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()
            function_parameters.append(self.current_token)
            self.advance()

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            MCSSyntaxError(f'Expected ")". Got {text_underline(f"{self.current_token.value !r}")} instead')
            exit()
        self.advance()

        if self.current_token.tt_type != 'TT_FUNCTION_ARROW':
            MCSSyntaxError(f'Expected "=>". Got {text_underline(f"{self.current_token.value !r}")} instead')
            exit()
        self.advance()

        function_body = self.expression()

        return FunctionAssignNode(function_name_token, function_parameters, function_body)

    def function_call(self, name_token: Token) -> FunctionCallNode:
        self.advance()

        argument_tokens = []

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
            return FunctionCallNode(name_token, argument_tokens)

        argument_tokens.append(self.factor())

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()
            argument_tokens.append(self.factor())

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
            self.advance()
            return FunctionCallNode(name_token, argument_tokens)

    def array(self) -> ListNode:
        if self.current_token.tt_type != 'TT_LEFT_BRACKET':
            MCSSyntaxError(f'Expected "[". Got {self.current_token.value} instead.')
            exit()
        self.advance()

        array_contents = []

        if self.current_token.tt_type != 'TT_RIGHT_BRACKET':
            array_contents.append(self.expression())
        else:
            self.advance()
            return ListNode(array_contents)

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()
            if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
                self.advance()
                return ListNode(array_contents)

            array_contents.append(self.expression())

        if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
            self.advance()
            return ListNode(array_contents)

        else:
            MCSSyntaxError(f'Expected "]". Got {self.current_token.value} instead.')
            exit()

    def array_get(self, name_token) -> ListGetNode:
        if self.current_token.tt_type != 'TT_LEFT_BRACKET':
            MCSSyntaxError(f'Expected "[". Got {self.current_token.value} instead.')
            exit()
        self.advance()

        index = self.term()

        if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
            self.advance()
            return ListGetNode(name_token, index)





if __name__ == '__main__':
    tokens = [Token(5, 'TT_NUMBER'), Token('+', 'TT_BINARY_OPERATOR'), Token(5, 'TT_NUMBER'),
              Token('*', 'TT_BINARY_OPERATOR'), Token('(', 'TT_LEFT_PARENTHESIS'), Token(3, 'TT_NUMBER'),
              Token('+', 'TT_BINARY_OPERATOR'), Token('-', 'TT_BINARY_OPERATOR'), Token(5, 'TT_NUMBER'),
              Token(')', 'TT_RIGHT_PARENTHESIS')]
    print(Parser(tokens).parse())
