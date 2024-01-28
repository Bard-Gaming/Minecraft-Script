from .tokens import Token
from .errors import *
from .nodes import *


class Parser:
    def __init__(self, token_input: tuple[Token, ...]):
        self.token_input = token_input
        self.__current_token: Token = None  # NOQA (Only None until the self.advance() call)
        self.current_index = -1

        self.advance()  # initialize token & index

    @property
    def current_token(self) -> Token:
        return self.__current_token if self.__current_token is not None else Token("", "NONE")

    def advance(self) -> None:
        if self.current_index >= len(self.token_input) - 1:
            self.__current_token = None
            return

        self.current_index += 1
        self.__current_token = self.token_input[self.current_index]

    def parse(self) -> tuple:
        return self.program()

    # --------------- Grammar --------------- :

    def sub_atom(self):
        if self.current_token.tt_type == 'TT_NUMBER':
            node = NumberNode(self.current_token)
            self.advance()
            return node

        elif self.current_token.tt_type == 'TT_STRING':
            node = StringNode(self.current_token)
            self.advance()
            return node

        elif self.current_token.tt_type == 'TT_BRACKET':
            return self.make_list()

        elif self.current_token.tt_type == 'TT_NAME':
            node = VariableAccessNode(self.current_token)
            self.advance()
            return node

        elif self.current_token.tt_type == 'TT_PARENTHESIS':
            if self.current_token.value != '(':
                position = self.current_token.get_position()
                raise MCSSyntaxError(f"Unmatched closing parenthesis at line {position[1]}, {position[0]}")
            self.advance()  # skip opening parenthesis

            expression = self.expression()

            if self.current_token.value != ')':
                position = self.current_token.get_position()
                raise MCSSyntaxError(f"Unclosed parenthesis at line {position[1]}, {position[0]}")
            self.advance()  # skip closing parenthesis

            return expression

    def atom(self, atom=None):
        atom = self.sub_atom() if atom is None else atom

        return atom

    def factor(self):
        return self.binary_operation(self.atom, ['*', '/', '%'])

    def term(self):
        return self.binary_operation(self.factor, ['+', '-'])

    def expression(self):
        return self.term()

    def statement(self):
        return self.expression()

    def program(self):
        pass

    # --------------- Implementation  --------------- :

    def binary_operation(self, operation_function, operators):
        left = operation_function()

        while self.current_token is not None and self.current_token.value in operators:
            operator = self.current_token
            self.advance()  # skip operator token

            right = operation_function()

            left = BinaryOperationNode(left, operator, right)

        return left

    def make_list(self) -> ListNode:
        pos = self.current_token.get_position()  # use starting __position for whole node
        list_nodes = []

        if self.current_token.value != '[':  # has to be a bracket (otherwise function can't be called)
            raise MCSSyntaxError(f"Expected '[', got {self.current_token.value !r} instead (line {pos[1]}, {pos[0]}")
        self.advance()

        if self.current_token.tt_type == 'TT_BRACKET' and self.current_token.value == ']':
            self.advance()
            return ListNode(list_nodes, pos)

        list_nodes.append(self.expression())

        while self.current_token is not None and self.current_token.tt_type == 'TT_COMMA':  # check if null
            self.advance()  # skip comma

            if self.current_token.tt_type == 'TT_BRACKET' and self.current_token.value == ']':
                self.advance()
                return ListNode(list_nodes, pos)

            list_nodes.append(self.expression())

        if self.current_token.tt_type != 'TT_BRACKET' or self.current_token.value != ']':
            current_pos = self.current_token.get_position()
            raise MCSSyntaxError(f'Unclosed list bracket at line {current_pos[1]}, {current_pos[0]}')
        self.advance()

        return ListNode(list_nodes, pos)
