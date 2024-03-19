from ..errors import *
from .types import *
from .builtin_functions import builtin_functions


class SymbolTable:
    def __init__(self, parent: "SymbolTable" = None, *, load_builtins=False):
        self.symbols: dict = {}
        self.parent = parent

        if load_builtins:
            self.load_builtins()

    def load_builtins(self) -> None:
        for py_function in builtin_functions:
            function_name = py_function.__name__[7:]  # skip "custom_" part of name
            mcs_function = MCSFunction(function_name, None, None)

            # Update custom function call method
            mcs_function.call = py_function

            # Update function name (looks cooler having "builtin-" before function name)
            mcs_function.print_value = lambda: f"<builtin-{function_name}>"

            # Save function in local context's names
            self.declare(function_name, mcs_function)

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


class RuntimeResult:
    def __init__(self, *, value: any = None, return_value: any = None):
        self.value = value
        self.return_value = return_value

    def get_value(self) -> any:
        return self.value

    def get_return_value(self) -> any:
        return self.return_value

    def __repr__(self) -> str:
        return f'RuntimeResult({self.value !r}, {self.return_value !r})'


class Interpreter:

    def visit(self, node, context: InterpreterContext) -> RuntimeResult:
        method_name = f'visit_{node.__class__.__name__}'
        method = getattr(self, method_name, self.visit_unknown)

        return method(node, context)

    # --------------- Builtin Types --------------- :
    def visit_NumberNode(self, node, context: InterpreterContext) -> RuntimeResult:
        node_value: str = node.get_value()
        value = MCSNumber(int(node_value))
        return RuntimeResult(value=value)

    def visit_BooleanNode(self, node, context: InterpreterContext) -> RuntimeResult:
        node_value: bool = node.get_value()
        value = MCSBool(node_value)
        return RuntimeResult(value=value)

    def visit_StringNode(self, node, context: InterpreterContext) -> RuntimeResult:
        node_value: str = node.get_value()
        value = MCSString(node_value)
        return RuntimeResult(value=value)

    def visit_ListNode(self, node, context: InterpreterContext) -> RuntimeResult:
        value_nodes: list = node.get_node_list()
        value_list = [self.visit(value_node, context).get_value() for value_node in value_nodes]
        end_value = MCSList(value_list)
        return RuntimeResult(value=end_value)

    def visit_NullNode(self, node, context: InterpreterContext) -> RuntimeResult:
        value = MCSNull()
        return RuntimeResult(value=value)

    # --------------- Type Manipulation --------------- :
    def visit_GetKeyNode(self, node, context: InterpreterContext) -> RuntimeResult:
        root_object = self.visit(node.get_atom(), context).get_value()
        key = self.visit(node.get_key(), context).get_value()

        return RuntimeResult(value=root_object.get_key(key))

    # --------------- Variables --------------- :
    def visit_VariableAccessNode(self, node, context: InterpreterContext) -> RuntimeResult:
        name = node.get_name()
        return RuntimeResult(value=context.get(name))

    def visit_VariableDeclareNode(self, node, context: InterpreterContext) -> RuntimeResult:
        name = node.get_name()
        value = self.visit(node.get_value(), context).get_value()

        context.declare(name, value)
        return RuntimeResult()

    def visit_VariableSetNode(self, node, context: InterpreterContext) -> RuntimeResult:
        name = node.get_name()
        value = self.visit(node.get_value(), context).get_value()

        context.set(name, value)
        return RuntimeResult()

    # --------------- Functions --------------- :
    def visit_DefineFunctionNode(self, node, context: InterpreterContext) -> RuntimeResult:
        name: str = node.get_name()
        body = node.get_body()
        parameter_names: list[str, ...] = node.get_parameter_names()

        function = MCSFunction(name, body, tuple(parameter_names))

        if name is not None:
            context.declare(name, function)

        return RuntimeResult()

    def visit_FunctionCallNode(self, node, context: InterpreterContext) -> RuntimeResult:
        root: RuntimeResult = self.visit(node.get_root(), context)
        root: MCSFunction = root.get_value()  # turn root into function; if it isn't a function, an error will be raised

        args = [self.visit(arg_node, context).get_value() for arg_node in node.get_arguments()]

        call_result: RuntimeResult = root.call(args, context)  # has no value, but return value

        # functions as converters of return values into values
        return RuntimeResult(value=call_result.get_return_value())

    # --------------- Conditionals --------------- :
    def visit_IfConditionNode(self, node, context: InterpreterContext) -> RuntimeResult:
        conditions: list[dict, ...] = node.get_conditions()
        local_context = InterpreterContext(parent=context, top_level=context.is_top_level())

        for condition in conditions:
            if condition.get('type') == 'if':  # condition is 'if' or 'else if' -> expression needs to be evaluated
                if bool(self.visit(condition.get('expression'), context).get_value()) is True:
                    return self.visit(condition.get('body'), local_context)  # already RuntimeResult

            else:  # final 'else' statement (not 'else if') -> no expression to evaluate
                return self.visit(condition.get('body'), local_context)  # already RuntimeResult, don't need to convert

    # --------------- Loops --------------- :
    def visit_WhileLoopNode(self, node, context: InterpreterContext) -> RuntimeResult:
        condition = node.get_condition()
        body = node.get_body()

        local_context = InterpreterContext(parent=context, top_level=context.top_level)
        while bool(self.visit(condition, local_context).get_value()) is True:
            visit_value: RuntimeResult = self.visit(body, local_context)
            if visit_value.get_return_value() is not None:
                return visit_value  # already RuntimeResult, don't need to convert

    def visit_ForLoopNode(self, node, context: InterpreterContext) -> RuntimeResult:
        iterable = self.visit(node.get_iterable(), context).get_value()
        child_name = node.get_child_name()
        body = node.get_body()

        if iterable.is_iterable() is False:
            raise MCSTypeError(f"{iterable.class_name() !r} object is not iterable")

        local_context = InterpreterContext(parent=context, top_level=context.top_level)

        for py_value in iterable.get_value():
            local_context.declare(child_name, py_value)

            visit_value: RuntimeResult = self.visit(body, local_context)
            if visit_value.get_return_value() is not None:
                return visit_value  # already RuntimeResult, don't need to convert

    # --------------- Operations --------------- :
    def visit_BinaryOperationNode(self, node, context: InterpreterContext) -> RuntimeResult:
        left_operand = self.visit(node.get_left_node(), context).get_value()
        right_operand = self.visit(node.get_right_node(), context).get_value()
        operator = node.get_operator()  # Token

        value_method = getattr(left_operand, operator.variant.lower())
        return RuntimeResult(value=value_method(right_operand))

    def visit_UnaryOperationNode(self, node, context: InterpreterContext) -> RuntimeResult:
        root = self.visit(node.get_root(), context).get_value()
        operator = node.get_operator()

        return RuntimeResult(value=root.unary_operation(operator))

    # --------------- Miscellaneous --------------- :
    def visit_CodeBlockNode(self, node, context: InterpreterContext) -> RuntimeResult:
        body = node.get_body()
        local_context = InterpreterContext(parent=context, top_level=context.top_level)

        # Only need to visit one node, since body of code block is only one node
        return_value: RuntimeResult = self.visit(body, local_context)

        return return_value  # already RuntimeResult, so don't need to convert

    def visit_MultilineCodeNode(self, node, context: InterpreterContext) -> RuntimeResult:
        for statement in node.get_nodes():
            return_value: RuntimeResult | None = self.visit(statement, context)

            # if a "return" statement is encountered:
            if return_value is not None and return_value.get_return_value() is not None:
                return return_value

        return RuntimeResult()  # if no return statement is encountered

    def visit_ReturnNode(self, node, context: InterpreterContext) -> RuntimeResult:
        if context.is_top_level():
            pos_x, pos_y = node.get_position()
            raise MCSSyntaxError(f"Illegal return statement (line {pos_y}, {pos_x})")

        if node.get_value() is None:
            return RuntimeResult(return_value=MCSNull())

        return_value: RuntimeResult = self.visit(node.get_value(), context)
        return RuntimeResult(return_value=return_value.get_value())  # turn value into return value

    # --------------- Error --------------- :
    def visit_unknown(self, node, context: InterpreterContext):
        raise MCSInterpreterError(f"Unknown node {node.__class__.__name__ !r}")
