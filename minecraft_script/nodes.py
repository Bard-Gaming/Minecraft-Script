from .tokens import Token


class _InterpreterNode:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def get_value(self):
        return self.value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value})'


class NumberNode(_InterpreterNode):
    def __init__(self, token):
        super().__init__(token, token.get_position())


class VariableAccessNode(_InterpreterNode):
    def __init__(self, token):
        super().__init__(token, token.get_position())
