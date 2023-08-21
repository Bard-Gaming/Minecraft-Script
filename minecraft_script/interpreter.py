from .text_additions import text_error, text_underline
from .types import Number, String, List, Boolean, Function, BuiltinFunction, Return, Iterable
from .errors import MCSNameError, MCSTypeError, MCSIndexError, MCSSyntaxError


class Context:
    def __init__(self, display_name: str, symbol_table, parent=None):
        self.display_name = display_name
        self.parent: None | Context = parent
        self.symbol_table: SymbolTable = symbol_table

    def display(self):
        return f'<{self.display_name}>'

    def __repr__(self):
        return f'Context({self.display_name}, {self.symbol_table}, {self.parent})'


class SymbolTable:
    def __init__(self, parent=None, *, load_builtins=True):
        self.symbols: dict = {}
        self.parent = parent

        if load_builtins:
            for name in BuiltinFunction.names:
                self.set(name, BuiltinFunction(name))

    def get(self, variable_name):
        value = self.symbols.get(variable_name, None)

        if value is None and self.parent:
            return self.parent.get(variable_name)

        return value

    def set(self, variable_name: str, variable_value: any):
        self.symbols[variable_name] = variable_value

    def remove(self, variable_name):
        del self.symbols[variable_name]

    def __repr__(self):
        return f'SymbolTable({self.parent})'

    def __str__(self):
        return f'{self.symbols}'


class Interpreter:
    def visit(self, node, context: Context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_node)
        return method(node, context)

    def visit_NumberNode(self, node, context) -> Number:
        return Number(node.get_value())

    def visit_StringNode(self, node, context) -> String:
        return String(node.get_value())

    def visit_ListNode(self, node, context):
        value_array = [self.visit(element, context) for element in node.array]
        return List(value_array)

    def visit_BooleanNode(self, node, context):
        return Boolean(node.value)

    def visit_UnaryBooleanNode(self, node, context):
        operator_type = node.get_unary_type()
        boolean = self.visit(node.get_atom(), context)

        if operator_type == 'TT_LOGICAL_NOT':
            return boolean.logical_not()

        else:
            MCSSyntaxError(node.get_unary_value())
            exit()

    def visit_IterableGetNode(self, node, context):
        current_iterable = self.visit(node.atom, context)
        index = self.visit(node.index, context)

        if isinstance(current_iterable, Iterable.types()):
            return current_iterable.get_index(index)

        else:
            MCSTypeError(f'{type(current_iterable).__name__} {current_iterable} is not iterable')
            exit()

    def visit_IterableSetNode(self, node, context):
        variable: Iterable = self.visit(node.variable_node, context)
        index: Number | None = self.visit(node.index, context)
        new_value = self.visit(node.value_expression, context)

        variable.set_index(index, new_value)


    def visit_VariableAccessNode(self, node, context) -> any:
        var_name: str = node.get_name()
        var_value = context.symbol_table.get(var_name)

        if var_value is None:
            MCSNameError(var_name)
            exit()

        return var_value

    def visit_VariableSetNode(self, node, context):
        var_name: str = node.get_name()
        var_new_value = self.visit(node.value_node, context)
        var_current_value = context.symbol_table.get(var_name)

        if var_current_value is None:
            MCSNameError(var_name)
            exit()

        context.symbol_table.set(var_name, var_new_value)
        return var_new_value

    def visit_VariableAssignNode(self, node, context) -> any:
        var_name: str = node.get_name()
        var_new_value = self.visit(node.value_node, context)

        context.symbol_table.set(var_name, var_new_value)
        return var_new_value

    def visit_FunctionAssignNode(self, node, context) -> Function:
        func_name = node.name_token.value if node.name_token else None
        parameter_names = [param_token.value for param_token in node.parameter_name_tokens]
        body_node = node.body_node

        function = Function(func_name, parameter_names, body_node, context)

        if func_name:
            context.symbol_table.set(func_name, function)

        return function

    def visit_FunctionCallNode(self, node, context) -> any:
        function = self.visit(node.atom, context)
        arguments = [self.visit(arg_token, context) for arg_token in node.argument_nodes]

        if isinstance(function, (Function, BuiltinFunction)):
            result = function.call(arguments)
            return result
        else:
            MCSTypeError(f'"{function}" is not a function')
            exit()

    def visit_BinaryOperationNode(self, node, context) -> Number | Boolean:
        operator = node.operator.value
        left_expression: Number | Boolean = self.visit(node.left_node, context)
        right_expression: Number | Boolean = self.visit(node.right_node, context)
        result = 0

        if operator == '+':
            right_expression = Number(right_expression)
            result = Number(left_expression).add(right_expression)

        elif operator == '-':
            right_expression = Number(right_expression)
            result = Number(left_expression).subtract(right_expression)

        elif operator == '*':
            right_expression = Number(right_expression)
            result = Number(left_expression).multiply(right_expression)

        elif operator == '/':
            right_expression = Number(right_expression)
            result = Number(left_expression).divide(right_expression)

        elif operator == '%':
            right_expression = Number(right_expression)
            result = Number(left_expression).modulus(right_expression)

        elif operator == '&&':
            right_expression = Boolean(right_expression)
            result = Boolean(left_expression).logical_and(right_expression)

        elif operator == '||':
            right_expression = Boolean(right_expression)
            result = Boolean(left_expression).logical_or(right_expression)

        return result

    def visit_UnaryOperationNode(self, node, context) -> Number:
        operator = node.operator.value
        right_node = Number(self.visit(node.right_node, context))
        result = Number(0)

        if operator == '+':
            result = result.add(right_node)
        elif operator == '-':
            result = result.subtract(right_node)

        return result

    def visit_MultipleStatementsNode(self, node, context):
        return [self.visit(statement, context) for statement in node.statements]

    def visit_CodeBlockNode(self, node, context):
        local_symbol_table = SymbolTable(context.symbol_table, load_builtins=False)
        local_context = Context(f'code_block at {id(node)}', local_symbol_table)

        visit_list = []
        for statement in node.statements:
            if type(statement).__name__ == 'ReturnNode':
                visit_list.append(self.visit(statement, local_context))
                break
            visit_list.append(self.visit(statement, local_context))

        return visit_list

    def visit_ReturnNode(self, node, context):
        if node.value:
            return Return(self.visit(node.value, context))

    def no_visit_node(self, node, context):
        print(text_error(f'No visit method defined for {text_underline(type(node).__name__)}'))


if __name__ == '__main__':
    Interpreter()
