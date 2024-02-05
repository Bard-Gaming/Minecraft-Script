from .errors import *
from .types import *
from .builtin_functions import builtin_functions


class SymbolTable:
    def __init__(self, parent: "SymbolTable" = None, *, load_builtins=False):
        self.symbols: dict = {}
        self.parent = parent

        if load_builtins:
            self.load_builtins()

    def load_builtins(self) -> None:
        for function in builtin_functions:
            self.declare(function.name, function)

    def get(self, name, *, generate_error: bool = True) -> any:
        # Search for value in self
        value = self.symbols.get(name)
        if value is not None:
            return value

        # Check if parent is present
        if self.parent is None:
            if not generate_error:
                return None

            raise MCSNameError(f"Name {name !r} is not defined.")

        # Search for value in parent
        value = self.parent.get(name, generate_error=False)
        if generate_error and value is None:
            raise MCSNameError(f"Name {name !r} is not defined.")

        return value  # return value even if it is None since no error is to be generated

    def set(self, name, new_value: any) -> None:
        if self.symbols.get(name) is not None:
            self.symbols[name] = new_value
            return

        if self.parent is None:
            raise MCSNameError(f"Name {name !r} is not defined.")

        self.parent.set(name, new_value)

    def declare(self, name, value: any = None) -> None:
        value = value if value is not None else MCSNull()
        self.symbols[name] = value


class InterpreterContext:
    def __init__(self, *, parent: "InterpreterContext" = None, top_level: bool = False):
        self.parent = parent
        self.top_level = top_level
        self.symbol_table = SymbolTable(
            parent.symbol_table if parent is not None else None,  # NOQA
            load_builtins=top_level
        )

    def is_top_level(self) -> bool:
        return self.top_level

    def get(self, name) -> any:
        return self.symbol_table.get(name)

    def set(self, name, new_value) -> None:
        return self.symbol_table.set(name, new_value)

    def declare(self, name, value=None) -> None:
        self.symbol_table.declare(name, value)

    def __repr__(self) -> str:
        return f'InterpreterContext({self.parent !r}, {self.top_level !r})'


class Interpreter:

    def visit(self, node, context: InterpreterContext):
        method_name = f'visit_{node.__class__.__name__}'
        method = getattr(self, method_name, self.visit_unknown)

        return method(node, context)

    # --------------- Builtin Types --------------- :
    def visit_NumberNode(self, node, context):
        value: str = node.get_value()
        return MCSNumber(int(value))

    def visit_StringNode(self, node, context):
        value: str = node.get_value()
        return MCSString(value)

    def visit_ListNode(self, node, context):
        value_nodes: list = node.get_node_list()
        value_list = [self.visit(value_node, context) for value_node in value_nodes]
        return MCSList(value_list)

    def visit_NullNode(self, node, context):
        return MCSNull()

    def visit_DefineFunctionNode(self, node, context: InterpreterContext):
        name: str = node.get_name()
        body = node.get_body()
        parameter_names: list[str, ...] = node.get_parameter_names()

        function = MCSFunction(name, body, tuple(parameter_names))

        if name is not None:
            context.declare(name, function)

    # --------------- Builtin Type Manipulation --------------- :
    def visit_GetKeyNode(self, node, context):
        root_object = self.visit(node.get_atom(), context)
        key = node.get_key()

        return root_object.get_key(key.get_value())

    def visit_FunctionCallNode(self, node, context: InterpreterContext):
        root = self.visit(node.get_root(), context)
        args = [self.visit(arg_node, context) for arg_node in node.get_arguments()]

        return root.call(args, context)

    # --------------- Variables --------------- :
    def visit_VariableAccessNode(self, node, context):
        name = node.get_name()
        return context.get(name)

    def visit_VariableDeclareNode(self, node, context):
        name = node.get_name()
        value = self.visit(node.get_value(), context)

        context.declare(name, value)

    # --------------- Conditionals --------------- :
    def visit_IfConditionNode(self, node, context: InterpreterContext):
        conditions: list[dict, ...] = node.get_conditions()
        local_context = InterpreterContext(parent=context, top_level=context.is_top_level())

        for condition in conditions:
            if condition.get('type') == 'if':  # condition is 'if' or 'else if'
                if bool(self.visit(condition.get('expression'), context)) is True:
                    return self.visit(condition.get('body'), local_context)

            else:  # final 'else' statement (not 'else if'
                return self.visit(condition.get('body'), local_context)


    # --------------- Miscellaneous --------------- :
    def visit_BinaryOperationNode(self, node, context):
        left_operand = self.visit(node.get_left_node(), context)
        right_operand = self.visit(node.get_right_node(), context)
        operator = node.get_operator()  # Token

        value_method = getattr(left_operand, operator.variant.lower())
        return value_method(right_operand)

    def visit_CodeBlockNode(self, node, context: InterpreterContext):
        body = node.get_body()
        local_context = InterpreterContext(parent=context, top_level=context.top_level)

        return self.visit(body, local_context)  # return in case of "return" statement

    def visit_MultilineCodeNode(self, node, context: InterpreterContext):
        for statement in node.get_nodes():
            if statement.__class__.__name__ == 'ReturnNode':
                return self.visit(statement, context)  # return statement and don't continue iterating

            self.visit(statement, context)

        return MCSNull()

    def visit_ReturnNode(self, node, context: InterpreterContext):
        if context.is_top_level():
            pos_x, pos_y = node.get_position()
            raise MCSSyntaxError(f"Illegal return statement (line {pos_y}, {pos_x})")

        return_value = self.visit(node.get_value(), context) if node.get_value() is not None else MCSNull()
        return return_value

    # --------------- Error --------------- :
    def visit_unknown(self, node, context):
        raise MCSInterpreterError(f"Unknown node {node !r}")
