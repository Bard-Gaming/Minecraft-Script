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

        elif self.current_token.tt_type == 'TT_PARENTHESIS' and self.current_token.value == '(':
            return self.atom(self.call_function(atom))

        return atom

    def factor(self):
        return self.binary_operation(self.atom, ['*', '/', '%'])

    def term(self):
        return self.binary_operation(self.factor, ['+', '-'])

    def expression(self):
        return self.term()

    def code_block_statement(self):
        if self.current_token.tt_type == 'TT_BRACE' and self.current_token.value == '{':
            return self.code_block()

        return self.expression()

    def statement(self):
        if self.current_token.tt_type == 'TT_VAR_DEFINE':
            return self.declare_variable()

        elif self.current_token.tt_type == 'TT_FUNC_DEFINE':
            return self.define_function()

        elif self.current_token.tt_type == 'TT_RETURN':
            return self.return_statement()

        return self.code_block_statement()

    def multiline_code(self, *, expect_end: bool = False) -> MultilineCodeNode:
        position = self.current_token.get_position()

        while self.current_token.tt_type == 'TT_NEWLINE':
            self.advance()  # skip all leading newlines

        node_list = [self.statement()]  # self.advance() call already in self.statement()

        while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
            while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()

            if self.current_token is None or self.current_token.value == '}':
                return MultilineCodeNode(tuple(node_list), position)  # end parsing

            node_list.append(self.statement())  # self.advance() already called

        if not expect_end and self.current_token is not None:
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

    def return_statement(self) -> ReturnNode:
        position = self.current_token.get_position()

        if self.current_token.tt_type != 'TT_RETURN':
            self.raise_error(f'Expected "return" keyword, got {self.current_token.value !r}')
        self.advance()

        if self.current_token.tt_type == 'TT_NEWLINE':
            return ReturnNode(None, position)  # don't advance since newline is part of statement
        else:
            return ReturnNode(self.expression(), position)

    def code_block(self) -> CodeBlockNode:
        position = self.current_token.get_position()
        self.advance()  # skip left brace

        if self.current_token.value == '}':
            self.advance()
            return CodeBlockNode(NullNode(), position)

        body = self.multiline_code(expect_end=True)

        if self.current_token.value != '}':
            self.raise_error(f"Expected '{'}'}', got {self.current_token.value !r}")
        self.advance()

        return CodeBlockNode(body, position)

    def define_function(self) -> DefineFunctionNode:
        position = self.current_token.get_position()
        self.advance()  # skip "function" token

        if not self.current_token.tt_type in ('TT_NAME', 'TT_EQUALS'):
            self.raise_error(f"Expected name or '=', got {self.current_token.value !r}")

        name = None

        if self.current_token.tt_type == 'TT_NAME':
            name = self.current_token
            self.advance()

            if self.current_token.tt_type != 'TT_EQUALS':
                self.raise_error(f"Expected '=', got {self.current_token.value !r}")
        self.advance()  # skip '=' token

        parameter_names = []

        if self.current_token.value != '(':
            self.raise_error(f"Expected '(', got {self.current_token.value !r}")
        self.advance()

        if self.current_token.value != ')':
            if self.current_token.tt_type == 'TT_NAME':
                parameter_names.append(self.current_token)
                self.advance()
            else:
                self.raise_error(f"Expected ')' or parameter name, got {self.current_token.value !r}")

        while self.current_token.tt_type == 'TT_COMMA':
            self.advance()

            if self.current_token.tt_type == ')':
                break  # go out of loop if right parenthesis (treated after)

            if self.current_token.tt_type != 'TT_NAME':
                self.raise_error(f"Expected ')' or parameter name, got {self.current_token.value !r}")

            parameter_names.append(self.current_token)
            self.advance()

        self.advance()  # skip right parenthesis (self.current_token has to be ')' here)

        if self.current_token.tt_type != 'TT_FUNCTION_ARROW':
            self.raise_error(f"Expected '=>', got {self.current_token.value !r}")
        self.advance()

        body = self.code_block_statement()

        return DefineFunctionNode(name, body, parameter_names, position)

    def call_function(self, atom) -> FunctionCallNode:
        call_position = self.current_token.get_position()
        self.advance()  # skip opening left parenthesis

        arguments = []

        if self.current_token.tt_type == 'TT_PARENTHESIS' and self.current_token.value == ')':
            self.advance()
            return FunctionCallNode(atom, arguments, call_position)

        arguments.append(self.expression())

        while self.current_token is not None and self.current_token.tt_type == 'TT_COMMA':
            self.advance()

            if self.current_token.value == ')':
                self.advance()  # skip parenthesis
                return FunctionCallNode(atom, arguments, call_position)

            arguments.append(self.expression())

        if self.current_token.value != ')':
            self.raise_error(f"Expected ')', got {self.current_token.value !r}")
        self.advance()  # skip parenthesis

        return FunctionCallNode(atom, arguments, call_position)
