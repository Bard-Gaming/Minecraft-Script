class BuildContext:
    def __init__(self, name: str, function_folder: str):
        self.name = name
        self.id = f'mcs_{name.lower()}'
        self.function_folder = function_folder

    def generate(self):
        return f'scoreboard objectives add {self.id} dummy ' '{"text":"MCS Context", "color":"green"}'


class BuildInterpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, 'no_visit_node')
        return method(node, context)

    @staticmethod
    def visit_NumberNode(node, context):
        return node.get_value()

    def visit_VariableAssignNode(self, node, context):
        var_name = f'.{node.get_name()}'
        value = self.visit(node.value_node, context)
        return f'scoreboard players set {var_name} {context.id} {value}'

    def visit_FunctionAssignNode(self, node, context):
        func_name = node.name_token.value
        parameter_names = [param_token.value for param_token in node.parameter_name_tokens]

    @staticmethod
    def no_visit_node(node, context):
        print('Error here')
        exit()
