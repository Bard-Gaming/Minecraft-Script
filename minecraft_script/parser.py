from .tokens import Token
from .nodes import *


class Parser:
    def __init__(self, token_input: tuple[Token, ...]):
        self.token_input = token_input
        self.current_token = None
        self.current_index = -1

    def advance(self) -> None:
        if self.current_index >= len(self.token_input) - 1:
            self.current_token = None
            return

        self.current_index += 1
        self.current_token = self.token_input[self.current_index]

    def parse(self) -> tuple:
        return ()

    # --------------- Grammar --------------- :

    def sub_atom(self):
        if self.current_token.tt_type == 'TT_NUMBER':
            node = NumberNode(self.current_token)
            self.advance()
            return node

        elif self.current_token.tt_type == 'TT_NAME':
            node = VariableAccessNode(self.current_token)
            self.advance()
            return node

    def atom(self, atom=None):
        atom = self.sub_atom() if atom is None else atom

        return atom

    # --------------- Implementation  --------------- :

