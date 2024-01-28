from .tokens import Token
from .errors import *
from .nodes import *


class Parser:
    def __init__(self, token_input: tuple[Token, ...]):
        self.token_input = token_input + (Token(';', 'TT_NEWLINE'),)  # add a newline at the end
        self.__current_token: Token = None  # NOQA (Only None until the self.advance() call)
        self.current_index = -1

        self.parse_result = None

        self.advance()  # initialize token & index

    @property
    def current_token(self) -> Token:
        return self.__current_token

    def advance(self) -> None:
        if self.current_index >= len(self.token_input) - 1:
            self.__current_token = None
            return

        self.current_index += 1
        self.__current_token = self.token_input[self.current_index]

    def raise_error(self, details: str, *, error=MCSSyntaxError, token: Token = None, include_pos: bool = True) -> None:
        token = self.current_token if token is None else token

        if include_pos:
            pos_x, pos_y = token.get_position()
            details = f"{details} (line {pos_y}, {pos_x})"

        raise error(details)

    def parse(self) -> tuple[ParserNode, ...]:
        if self.parse_result is None:
            self.parse_result = self.multiline_code()

        return self.parse_result  # reuse old parse result if it exists

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

        elif self.current_token.tt_type == 'TT_NULL':
            self.advance()
            return NullNode()

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

        raise MCSParserError(f'Unknown token: {self.current_token !r}')

    def atom(self, atom=None):
        atom = self.sub_atom() if atom is None else atom

        if self.current_token.tt_type == 'TT_BRACKET' and self.current_token.value == '[':
            return self.atom(self.get_key(atom))

        return atom

    def factor(self):
        return self.binary_operation(self.atom, ['*', '/', '%'])

    def term(self):
        return self.binary_operation(self.factor, ['+', '-'])

    def expression(self):
        return self.term()

    def statement(self):
        if self.current_token.tt_type == 'TT_VAR_DEFINE':
            return self.declare_variable()

        return self.expression()

    def multiline_code(self) -> MultilineCodeNode:
        position = self.current_token.get_position()

        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()  # skip all leading newlines

        node_list = [self.statement()]  # self.advance() call already in self.statement()

        while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
            while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()

            if self.current_token is None:
                return MultilineCodeNode(tuple(node_list), position)  # end parsing

            node_list.append(self.statement())  # self.advance() already called

        if self.current_token is not None:
            self.raise_error("Unexpected end of statement. Did you perhaps forget a ';'?")

        return MultilineCodeNode(tuple(node_list), position)

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
        pos = self.current_token.get_position()  # use starting position for whole node
        list_nodes = []

        if self.current_token.value != '[':  # has to be a bracket (otherwise function can't be called)
            self.raise_error(f"Expected '[', got {self.current_token.value !r}")
        self.advance()

        if self.current_token.tt_type == 'TT_BRACKET' and self.current_token.value == ']':
            self.advance()
            return ListNode(list_nodes, pos)

        list_nodes.append(self.expression())

        while self.current_token is not None and self.current_token.tt_type == 'TT_COMMA':  # check if None in loop
            self.advance()  # skip comma

            if self.current_token.tt_type == 'TT_BRACKET' and self.current_token.value == ']':
                self.advance()
                return ListNode(list_nodes, pos)

            list_nodes.append(self.expression())

        if self.current_token.tt_type != 'TT_BRACKET' or self.current_token.value != ']':
            self.raise_error('Unclosed list bracket')
        self.advance()

        return ListNode(list_nodes, pos)

    def declare_variable(self) -> VariableDeclareNode:
        if self.current_token.tt_type != "TT_VAR_DEFINE":
            self.raise_error(f'Expected "var" keyword, got {self.current_token.value !r}')
        self.advance()

        if self.current_token.tt_type != 'TT_NAME':
            self.raise_error(f'Expected name, got {self.current_token.value !r}')
        name = self.current_token
        self.advance()

        if self.current_token.tt_type == 'TT_NEWLINE':
            return VariableDeclareNode(name)
        elif self.current_token.tt_type != 'TT_EQUALS':
            self.raise_error(f"Expected ';' or '=', got {self.current_token.value !r}")
        self.advance()  # skip '=' Token

        value = self.expression()  # self.advance() call already in self.expression()
        return VariableDeclareNode(name, value)

    def get_key(self, atom: ParserNode) -> GetKeyNode:
        if self.current_token.tt_type == 'TT_BRACKET' and self.current_token.value != '[':
            self.raise_error(f"Expected '[', got {self.current_token.value !r}")
        self.advance()

        key = self.expression()  # includes advance() call

        if self.current_token.tt_type != 'TT_BRACKET' and self.current_token.value != ']':
            self.raise_error(f"Expected ']', got {self.current_token.value !r}")
        self.advance()

        return GetKeyNode(atom, key)
