from .tokens import Token


class ParserNode:
    def __init__(self, determinant_value, position=None):
        self.__determinant_value: ParserNode | Token = determinant_value
        self.__position = position if position is not None else self.__determinant_value.get_position()

    def get_determinant_value(self):
        return self.__determinant_value

    def get_position(self):
        return self.__position

    def repr_gen(self, *values) -> str:
        return f'{self.__class__.__name__}({", ".join(repr(value) for value in values)})'

    def __repr__(self) -> str:
        return self.repr_gen(self.__determinant_value)


class NumberNode(ParserNode):
    def __init__(self, value: Token):
        super().__init__(value)

    def get_value(self) -> str:
        value_token: Token = self.get_determinant_value()
        return value_token.value  # extract value of token


class StringNode(ParserNode):
    def __init__(self, value: Token):
        super().__init__(value)

    def get_value(self) -> str:
        value_token: Token = self.get_determinant_value()
        return value_token.value  # extract value of token


class ListNode(ParserNode):
    def __init__(self, node_list, position):
        super().__init__(node_list, position)

    def get_node_list(self) -> list[ParserNode, ...]:
        return self.get_determinant_value()  # NOQA needed since there is no problem with det_val here


class NullNode(ParserNode):
    def __init__(self):  # NOQA override ParserNode's init
        pass

    def __repr__(self):
        return f'NullNode()'


class VariableAccessNode(ParserNode):
    def __init__(self, name: Token):
        super().__init__(name)

    def get_name(self) -> str:
        name_token = self.get_determinant_value()
        return name_token.value  # extract value from token


class VariableDeclareNode(ParserNode):
    def __init__(self, name: Token, value: any = None):
        super().__init__(name)  # set name to determinant value
        self.value = value  # Node or None

    def get_name(self) -> str:
        name_token = self.get_determinant_value()
        return name_token.value  # extract value from token

    def get_value(self) -> any:
        return self.value  # is a node or none

    def __repr__(self):
        return self.repr_gen(self.get_determinant_value(), self.value)


class BinaryOperationNode(ParserNode):
    def __init__(self, left_value, operator, right_value):
        super().__init__(operator)

        self.left_value = left_value  # Node
        self.right_value = right_value  # Node

    def get_left_node(self):
        return self.left_value

    def get_right_node(self):
        return self.right_value

    def get_operator(self) -> Token:
        return self.get_determinant_value()  # don't extract token value (can be used to determine type of operator)

    def __repr__(self):
        return self.repr_gen(self.left_value, self.get_determinant_value(), self.right_value)


class GetKeyNode(ParserNode):
    def __init__(self, atom, key):
        super().__init__(atom)
        self.key = key

    def get_atom(self) -> ParserNode:
        return self.get_determinant_value()

    def get_key(self) -> ParserNode:
        return self.key

    def __repr__(self):
        return self.repr_gen(self.get_determinant_value(), self.key)


class CodeBlockNode(ParserNode):
    def __init__(self, body, position):
        super().__init__(body, position)

    def get_body(self):
        return self.get_determinant_value()


class MultilineCodeNode(ParserNode):
    def __init__(self, statements: tuple, position: tuple):
        super().__init__(statements, position)

    def get_nodes(self) -> tuple[ParserNode, ...]:
        return self.get_determinant_value()


class ReturnNode(ParserNode):
    def __init__(self, value: any, position: tuple):
        super().__init__(value, position)

    def get_value(self):
        return self.get_determinant_value()


class DefineFunctionNode(ParserNode):
    def __init__(self, name: Token, body: ParserNode, parameter_names, position):
        super().__init__(name, position)
        self.body = body
        self.parameter_names = parameter_names

    def get_name(self) -> str:
        return self.get_determinant_value().value  # extract string from token

    def get_body(self) -> ParserNode:
        return self.body

    def get_parameter_names(self) -> list:
        return [token.value for token in self.parameter_names]


class FunctionCallNode(ParserNode):
    def __init__(self, root_node, arguments, position):
        super().__init__(root_node, position)
        self.arguments: list = arguments  # list of nodes

    def get_root(self):
        return self.get_determinant_value()

    def get_arguments(self) -> tuple[ParserNode, ...]:
        return tuple(self.arguments)


class IfConditionNode(ParserNode):
    def __init__(self, condition_list, position):
        super().__init__(condition_list, position)

    def get_conditions(self) -> list[dict, ...]:
        return self.get_determinant_value()

