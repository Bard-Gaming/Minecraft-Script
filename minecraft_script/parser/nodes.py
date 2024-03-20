from ..lexer.tokens import Token


class ParserNode:
    """
    ParserNode class that implements all parser nodes.
    Purely used for encapsulation/categorising.
    """
    pass


class NumberNode(ParserNode):
    def __init__(self, value: Token):
        self.value = value

    def get_value(self) -> str:
        return self.value.value  # extract value of token

    def get_position(self) -> tuple[int, int]:
        return self.value.get_position()

    def __repr__(self) -> str:
        return f"NumberNode({self.value !r})"


class StringNode(ParserNode):
    def __init__(self, value: Token):
        self.value = value

    def get_value(self) -> str:
        return self.value.value  # extract value of token

    def get_position(self) -> tuple[int, int]:
        return self.value.get_position()

    def __repr__(self) -> str:
        return f"StringNode({self.value !r})"


class ListNode(ParserNode):
    def __init__(self, node_list: list[ParserNode, ...], position: tuple[int, int]):
        self.node_list = node_list
        self.position = position

    def get_node_list(self) -> list[ParserNode, ...]:
        return self.node_list

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"ListNode({self.node_list !r}, {self.position !r})"


class BooleanNode(ParserNode):
    def __init__(self, value: Token):
        self.value = value

    def get_value(self) -> bool:
        return self.value.value == 'true'

    def get_position(self) -> tuple[int, int]:
        return self.value.get_position()

    def __repr__(self) -> str:
        return f"BooleanNode({self.value !r})"


class NullNode(ParserNode):
    def __init__(self):
        pass

    def __repr__(self):
        return f'NullNode()'


class VariableAccessNode(ParserNode):
    def __init__(self, name: Token):
        self.name = name

    def get_name(self) -> str:
        return self.name.value  # extract value from token

    def get_position(self) -> tuple[int, int]:
        return self.name.get_position()

    def __repr__(self) -> str:
        return f"VariableAccessNode({self.name !r})"


class VariableDeclareNode(ParserNode):
    def __init__(self, name: Token, value: ParserNode = None):
        self.name = name
        self.value = value  # Node or None

    def get_name(self) -> str:
        return self.name.value  # extract value from token

    def get_value(self) -> ParserNode | None:
        return self.value  # is a node or none

    def __repr__(self) -> str:
        return f"VariableDeclareNode({self.name !r}, {self.value !r})"


class VariableSetNode(ParserNode):
    def __init__(self, name: Token, value: ParserNode, position: tuple[int, int]):
        self.name = name
        self.position = position
        self.value = value

    def get_name(self) -> str:
        return self.name.value  # extract value out of name

    def get_value(self) -> ParserNode:
        return self.value

    def get_position(self) -> tuple[int, int]:
        return self.name.get_position()

    def __repr__(self) -> str:
        return f"VariableSetNode({self.name !r}, {self.value !r})"


class BinaryOperationNode(ParserNode):
    def __init__(self, left_value: ParserNode, operator: Token, right_value: ParserNode):
        self.left_value = left_value  # Node
        self.operator = operator  # Token
        self.right_value = right_value  # Node

    def get_left_node(self) -> ParserNode:
        return self.left_value

    def get_right_node(self) -> ParserNode:
        return self.right_value

    def get_operator(self) -> Token:
        return self.operator  # don't extract token value (type can be used to determine type of operator)

    def get_position(self) -> tuple[int, int]:
        return self.operator.get_position()

    def __repr__(self):
        return f"BinaryOperationNode({self.left_value !r}, {self.operator !r}, {self.right_value !r})"


class GetKeyNode(ParserNode):
    def __init__(self, atom: ParserNode, key: ParserNode):
        self.atom = atom
        self.key = key

    def get_atom(self) -> ParserNode:
        return self.atom

    def get_key(self) -> ParserNode:
        return self.key

    def __repr__(self):
        return f"GetKeyNode({self.atom !r}, {self.key !r})"


class SetKeyNode(ParserNode):
    def __init__(self, name: Token, key: ParserNode, value: ParserNode):
        self.name = name  # Token
        self.key = key  # Node
        self.value = value  # Node

    def get_name(self) -> str:
        return self.name.value

    def get_key(self) -> ParserNode:
        return self.key

    def get_value(self) -> ParserNode:
        return self.value

    def get_position(self) -> tuple[int, int]:
        return self.name.get_position()

    def __repr__(self) -> str:
        return f"SetKeyNode({self.name !r}, {self.key !r}, {self.value !r})"


class CodeBlockNode(ParserNode):
    def __init__(self, body: ParserNode, position: tuple[int, int]):
        self.body = body
        self.position = position

    def get_body(self):
        return self.body

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"CodeBlockNode({self.body !r}, {self.position !r})"


class MultilineCodeNode(ParserNode):
    def __init__(self, statements: tuple[ParserNode, ...], position: tuple[int, int]):
        self.statements = statements
        self.position = position

    def get_nodes(self) -> tuple[ParserNode, ...]:
        return self.statements

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"MultilineCodeNode({self.statements !r}, {self.position !r})"


class ReturnNode(ParserNode):
    def __init__(self, value: ParserNode, position: tuple[int, int]):
        self.value = value
        self.position = position

    def get_value(self) -> ParserNode:
        return self.value

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"ReturnNode({self.value !r}, {self.position !r})"


class DefineFunctionNode(ParserNode):
    def __init__(self, name: Token, body: ParserNode, parameter_names: list[Token, ...], position: tuple[int, int]):
        self.name = name
        self.body = body
        self.parameter_names = parameter_names
        self.position = position

    def get_name(self) -> str:
        return self.name.value  # extract string from token

    def get_body(self) -> ParserNode:
        return self.body

    def get_parameter_names(self) -> list[str, ...]:
        return list(map(lambda param: param.value, self.parameter_names))  # NOQA extract value out of parameter tokens

    def get_position(self) -> tuple[int, int]:
        return self.name.get_position()

    def __repr__(self) -> str:
        return f"DefineFunctionNode({self.name !r}, {self.body !r}, {self.parameter_names !r}, {self.position !r})"


class FunctionCallNode(ParserNode):
    def __init__(self, root_node: ParserNode, arguments: list[ParserNode, ...], position: tuple[int, int]):
        self.root_node = root_node
        self.arguments = arguments
        self.position = position

    def get_root(self) -> ParserNode:
        return self.root_node

    def get_arguments(self) -> tuple[ParserNode, ...]:
        return tuple(self.arguments)

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"FunctionCallNode({self.root_node !r}, {self.arguments !r}, {self.position !r})"


class IfConditionNode(ParserNode):
    def __init__(self, condition_list: list[dict, ...], position: tuple[int, int]):
        self.condition_list = condition_list
        self.position = position

    def get_conditions(self) -> list[dict, ...]:
        return self.condition_list

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"IfConditionNode({self.condition_list !r}, {self.position !r})"


class UnaryOperationNode(ParserNode):
    def __init__(self, operator: str, root: ParserNode, position: tuple[int, int]):
        self.operator: str = operator
        self.root = root
        self.position = position

    def get_root(self) -> ParserNode:
        return self.root

    def get_operator(self) -> str:
        return self.operator

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"UnaryOperationNode({self.operator !r}, {self.root !r}, {self.position !r})"


class WhileLoopNode(ParserNode):
    def __init__(self, condition: ParserNode, body: ParserNode, position: tuple[int, int]):
        self.condition = condition
        self.body = body
        self.position = position

    def get_condition(self) -> ParserNode:
        return self.condition

    def get_body(self) -> ParserNode:
        return self.body

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"WhileLoopNode({self.condition !r}, {self.body !r}, {self.position !r})"


class ForLoopNode(ParserNode):
    def __init__(self, iterable: ParserNode, child_name: Token, body: ParserNode, position: tuple[int, int]):
        self.iterable = iterable
        self.child_name = child_name
        self.body = body
        self.position = position

    def get_iterable(self) -> ParserNode:
        return self.iterable

    def get_child_name(self) -> str:
        return self.child_name.value  # extract value of token

    def get_body(self) -> ParserNode:
        return self.body

    def get_position(self) -> tuple[int, int]:
        return self.position

    def __repr__(self) -> str:
        return f"ForLoopNode({self.iterable !r}, {self.child_name !r}, {self.body !r}, {self.position !r})"


class AttributeGetNode(ParserNode):
    def __init__(self, root: ParserNode, name: Token):
        self.root = root
        self.name = name

    def get_root(self) -> ParserNode:
        return self.root

    def get_name(self) -> str:
        return self.name.value

    def get_position(self) -> tuple[int, int]:
        return self.name.get_position()

    def __repr__(self) -> str:
        return f"AttributeGetNode({self.root !r}, {self.name !r})"
