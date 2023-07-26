from .text_additions import text_error, text_underline
from .types import Number, Function, BuiltinFunction
from .errors import MCSNameError


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

    def visit_NumberNode(self, node, context: Context) -> int:
        return node.get_value()

    def visit_VariableAccessNode(self, node, context: Context) -> any:
        var_name: str = node.get_name()
        var_value = context.symbol_table.get(var_name)

        if var_value is None:
            MCSNameError(var_name)
            exit()

        return var_value

    def visit_VariableAssignNode(self, node, context: Context) -> any:
        var_name: str = node.get_name()
        var_new_value = self.visit(node.value_node, context)

        context.symbol_table.set(var_name, var_new_value)
        return var_new_value

    def visit_FunctionAssignNode(self, node, context: Context) -> Function:
        func_name = node.name_token.value if node.name_token else None
        parameter_names = [param_token.value for param_token in node.parameter_name_tokens]
        body_node = node.body_node

        function = Function(func_name, parameter_names, body_node, context)

        if func_name:
            context.symbol_table.set(func_name, function)

        return function

    def visit_FunctionCallNode(self, node, context: Context) -> any:
        func_name = node.name_token.value
        arguments = [self.visit(arg_token, context) for arg_token in node.argument_nodes]

        function = context.symbol_table.get(func_name)
        result = function.call(arguments)

        return result

    def visit_BinaryOperationNode(self, node, context: Context) -> int:
        operator = node.operator.value
        left_expression = Number(self.visit(node.left_node, context))
        right_expression = Number(self.visit(node.right_node, context))
        result = 0

        if operator == '+':
            result = left_expression.add(right_expression)
        elif operator == '-':
            result = left_expression.subtract(right_expression)
        elif operator == '*':
            result = left_expression.multiply(right_expression)
        elif operator == '/':
            result = left_expression.divide(right_expression)
        elif operator == '%':
            result = left_expression.modulus(right_expression)

        return result

    def visit_UnaryOperationNode(self, node, context: Context) -> int:
        operator = node.operator.value
        right_node = Number(self.visit(node.right_node, context))
        result = 0

        if operator == '+':
            result = Number(0).add(right_node)
        elif operator == '-':
            result = Number(0).subtract(right_node)

        return result

    def visit_MultipleStatementsNode(self, node, context):
        return [self.visit(statement, context) for statement in node.statements]

    def no_visit_node(self, node, context: Context):
        print(text_error(f'No visit method defined for {text_underline(type(node).__name__)}'))


if __name__ == '__main__':
    Interpreter()
