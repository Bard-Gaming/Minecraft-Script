from .tokens import Token


class _InterpreterNode:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def get_value(self):
        return self.value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value !r})'


class NumberNode(_InterpreterNode):
    def __init__(self, token):
        super().__init__(token, token.get_position())


class StringNode(_InterpreterNode):
    def __init__(self, token):
        super().__init__(token, token.get_position())


class ListNode(_InterpreterNode):
    def __init__(self, node_list, position):
        super().__init__(node_list, position)


class VariableAccessNode(_InterpreterNode):
    def __init__(self, token):
        super().__init__(token, token.get_position())


class BinaryOperationNode(_InterpreterNode):
    def __init__(self, left_value, operator, right_value):
        self.left_value = left_value  # is Node
        self.operator: Token = operator
        self.right_value = right_value  # is Node

        super().__init__(self.operator, self.operator.get_position())

    def get_left_node(self):
        return self.left_value

    def get_right_node(self):
        return self.right_value

    def __repr__(self) -> str:
        return f'BinaryOperationNode({self.left_value !r}, {self.operator !r}, {self.right_value !r})'

