from .tokens import Token
from .errors import MCSSyntaxError
from .text_additions import text_underline
from .nodes import NumberNode, BinaryOperationNode, UnaryOperationNode, VariableAssignNode, VariableAccessNode, \
    FunctionAssignNode, FunctionCallNode, MultipleStatementsNode, ListNode, IterableGetNode, CodeBlockNode, BooleanNode, \
    ReturnNode, UnaryBooleanNode, StringNode, IterableSetNode, IfConditionNode


class Parser:
    def __init__(self, token_list: list[Token]):
        self.token_list = token_list
        self.current_index = -1
        self.current_token = None

        self.advance()

    def advance(self):
        if self.current_index < len(self.token_list) - 1:
            self.current_index += 1
            self.current_token = self.token_list[self.current_index]

    def parse(self):
        result = self.statement_list()
        return result

    # ---------------------------- Grammar ---------------------------- :

    def atom(self):
        token = self.current_token

        if token.tt_type == 'TT_NAME':
            self.advance()
            return VariableAccessNode(token)

        elif token.tt_type == 'TT_TEXT_STRING':
            self.advance()
            return StringNode(token)

        elif token.tt_type == 'TT_NUMBER':
            self.advance()
            return NumberNode(token)

        elif token.value in ['+', '-']:
            self.advance()
            atom = self.atom()
            return UnaryOperationNode(token, atom)

        elif token.tt_type == 'TT_BOOLEAN':
            self.advance()
            return BooleanNode(token)

        elif token.tt_type == 'TT_LOGICAL_NOT':
            self.advance()
            atom = self.atom()
            return UnaryBooleanNode(token, atom)

        elif token.tt_type == 'TT_LEFT_BRACKET':
            return self.array()

        elif token.tt_type == 'TT_LEFT_PARENTHESIS':
            self.advance()
            expression = self.expression()
            if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
                self.advance()
                return expression

    def factor(self, atom=None):
        atom = atom if atom else self.atom()
        token = self.current_token

        if token.tt_type == 'TT_LEFT_PARENTHESIS':
            atom = self.function_call(atom)
            return self.factor(atom)

        elif token.tt_type == 'TT_LEFT_BRACKET':
            atom = self.iterable_get(atom)
            return self.factor(atom)

        else:
            return atom

    def term(self) -> BinaryOperationNode:
        return self.binary_operation(self.factor, ['*', '/', '%'])

    def boolean_operation(self) -> BinaryOperationNode:
        return self.binary_operation(self.term, ['+', '-'])

    def compare_operation(self) -> BinaryOperationNode:
        return self.binary_operation(self.boolean_operation, ['&&', '||'])

    def expression(self) -> BinaryOperationNode | VariableAssignNode | FunctionAssignNode | CodeBlockNode | ReturnNode:
        if self.current_token.tt_type == 'FUNC_DEFINE':
            return self.function_define()

        elif self.current_token.tt_type == 'TT_RETURN':
            self.advance()
            if self.current_token.tt_type in ['TT_NEWLINE', 'TT_RIGHT_BRACE']:
                return ReturnNode()

            return ReturnNode(self.expression())

        return self.binary_operation(self.compare_operation, ['==', '>', '>=', '<', '<='])

    def statement(self):
        if self.current_token.tt_type == 'VAR_DEFINE':
            return self.var_define()

        elif self.current_token.tt_type == 'TT_LEFT_BRACE':
            return self.code_block()

        elif self.current_token.tt_type == 'SET_DEFINE':
            return self.set_define()

        elif self.current_token.tt_type == 'IF_CONDITIONAL':
            return self.if_conditional()

        else:
            return self.expression()

    def statement_list(self) -> MultipleStatementsNode:
        statements = []
        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()
        statements.append(self.statement())

        more_statements = True
        while self.current_token.tt_type == 'TT_NEWLINE' and more_statements:
            while self.current_token.tt_type == 'TT_NEWLINE' and more_statements:
                index = self.current_index
                self.advance()
                if index == self.current_index:
                    more_statements = False

            if more_statements:
                statements.append(self.statement())

        return MultipleStatementsNode(statements)

    # ---------------------------- Nodes ---------------------------- :

    def binary_operation(self, function, operators) -> BinaryOperationNode:
        left_node = function()
        # self.current_token is now the operator

        while self.current_token.value in operators:
            operator = self.current_token
            self.advance()
            right_node = function()
            left_node = BinaryOperationNode(left_node, operator, right_node)
        return left_node

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

        function_body = self.statement()

        return FunctionAssignNode(function_name_token, function_parameters, function_body)

    def function_call(self, atom) -> FunctionCallNode:
        self.advance()

        argument_tokens = []

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
            self.advance()
            return FunctionCallNode(atom, argument_tokens)

        argument_tokens.append(self.expression())

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()
            argument_tokens.append(self.expression())

        if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
            self.advance()
            return FunctionCallNode(atom, argument_tokens)

        else:
            MCSSyntaxError(f'Expected ")". Got {self.current_token.value !r} instead')
            exit()

    def array(self) -> ListNode:
        if self.current_token.tt_type != 'TT_LEFT_BRACKET':
            MCSSyntaxError(f'Expected "[". Got {self.current_token.value} instead')
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
            MCSSyntaxError(f'Expected "]". Got {self.current_token.value} instead')
            exit()

    def iterable_get(self, atom) -> IterableGetNode:
        if self.current_token.tt_type != 'TT_LEFT_BRACKET':
            MCSSyntaxError(f'Expected "[". Got {self.current_token.value} instead')
            exit()
        self.advance()

        index = self.term()

        if self.current_token.tt_type == 'TT_RIGHT_BRACKET':
            self.advance()
            return IterableGetNode(atom, index)

        else:
            MCSSyntaxError(f'Expected "]". Got {self.current_token.value} instead')
            exit()

    def var_define(self) -> VariableAssignNode:
        self.advance()
        if self.current_token.tt_type != 'TT_NAME':
            MCSSyntaxError(f'Expected name. Got {text_underline(f"{self.current_token.value !r}")} instead')
            exit()

        var_name_token = self.current_token
        self.advance()

        if self.current_token.tt_type != 'TT_EQUALS':
            MCSSyntaxError(f'Expected "=". Got {text_underline(f"{self.current_token.value !r}")} instead')
            exit()

        self.advance()
        return VariableAssignNode(var_name_token, self.expression())

    def set_define(self) -> IterableSetNode:
        self.advance()  # skip "set" keyword

        if self.current_token.tt_type != 'TT_NAME':
            MCSSyntaxError(f'Expected Variable Name. Got "{self.current_token.value}" instead')
            exit()

        set_name_token = self.current_token
        self.advance()

        index = None
        if self.current_token.tt_type == 'TT_LEFT_BRACKET':
            self.advance()

            index = self.term()

            if self.current_token.tt_type != 'TT_RIGHT_BRACKET':
                MCSSyntaxError(f'Expected "]". Got "{self.current_token.value}" instead')
                exit()
            self.advance()

        if self.current_token.tt_type != 'TT_EQUALS':
            MCSSyntaxError(f'Expected "=". Got "{self.current_token.value}" instead')
            exit()
        self.advance()

        set_value_expression = self.expression()

        return IterableSetNode(set_name_token, index, set_value_expression)

    def if_conditional_main(self, condition_type: str):
        self.advance()

        if self.current_token.tt_type != 'TT_LEFT_PARENTHESIS':
            MCSSyntaxError(f'Expected "(". Got "{self.current_token.value}" instead')
            exit()
        self.advance()

        condition = self.expression()

        if self.current_token.tt_type != 'TT_RIGHT_PARENTHESIS':
            MCSSyntaxError(f'Expected ")". Got "{self.current_token.value}" instead')
            exit()
        self.advance()

        statement = self.statement()
        return {
            "type": condition_type,
            "condition": condition,
            "statement": statement
        }

    def if_conditional(self) -> IfConditionNode:
        condition_list = [self.if_conditional_main('if')]

        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()

        if self.current_token.tt_type == 'ELSE_CONDITIONAL':
            self.advance()  # skip "else" token

            ended_on_else = False
            while self.current_token.tt_type == 'IF_CONDITIONAL':
                ended_on_else = False
                condition_list.append(self.if_conditional_main('else if'))

                while self.current_token.tt_type == 'TT_NEWLINE':
                    self.advance()

                if self.current_token.tt_type == 'ELSE_CONDITIONAL':
                    self.advance()
                    ended_on_else = True

            if ended_on_else:  # "else" without "if" after
                else_statement = self.statement()

                condition_list.append({
                    "type": "else",
                    "statement": else_statement
                })

            else:  # temporary fix ig; artificially adds newline that was removed in the while loop
                self.current_token = Token('\n', 'TT_NEWLINE')

        else:  # temporary fix ig; artificially adds newline that was removed in the while loop
            self.current_token = Token('\n', 'TT_NEWLINE')

        return IfConditionNode(condition_list)

    def code_block(self):
        if self.current_token.tt_type != 'TT_LEFT_BRACE':
            MCSSyntaxError('Expected "{". Got "%s" instead' % self.current_token.value)
            exit()
        self.advance()

        statements = []

        if self.current_token.tt_type == 'TT_RIGHT_BRACE':
            self.advance()
            return CodeBlockNode(statements)

        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()

        statements.append(self.statement())

        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()
            while self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()

            if self.current_token.tt_type == 'TT_RIGHT_BRACE':
                self.advance()
                return CodeBlockNode(statements)

            statements.append(self.statement())

        if self.current_token.tt_type == 'TT_RIGHT_BRACE':
            self.advance()
            return CodeBlockNode(statements)
        else:
            MCSSyntaxError('Expected "}". Got "%s" instead.' % self.current_token.value)
            exit()
