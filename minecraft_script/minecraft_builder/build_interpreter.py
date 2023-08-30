from .build_types import BuildList, BuildNumber


class BuildContext:
    def __init__(self, name: str):
        self.name = name
        self.id = f'mcs_{name.lower()}'
        self.symbols = {}


def operation_add(left_value, right_value, only_value: bool = False):
    full_text = f"""
scoreboard players set .left_expr mcs_math {left_value}
scoreboard players set .right_expr mcs_math {right_value}
scoreboard players operation .result mcs_math = .left_expr mcs_math
scoreboard players operation .result mcs_math += .right_expr mcs_math
"""[1:]
    return full_text


class BuildInterpreter:
    def visit(self, node, context, command_position: str = None):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, 'no_visit_node')
        return method(node, context, command_position)

    @staticmethod
    def visit_NumberNode(node, context, command_position):
        num_element = BuildNumber(node.get_value())
        if command_position:
            return num_element
        else:
            return num_element.command()

    def visit_ListNode(self, node, context, command_position):
        list_contents = map(lambda element: self.visit(element, context, True), node.array)
        list_element = BuildList(list_contents, context)

        if command_position:
            return list_element
        else:
            return list_element.command()

    def visit_ListGetNode(self, node, context, command_position):
        current_list: BuildList = self.visit(node.atom, context)
        index = self.visit(node.index, context, command_position).mc_value()

        return f'data get storage {context.id} {current_list.list_name}.{index}'

    def visit_VariableAccessNode(self, node, context, command_position) -> any:
        var_name = f'{node.get_name()}'
        var_value = context.symbols.get(var_name)

        if var_value:
            return var_value

    def visit_VariableAssignNode(self, node, context, command_position):
        var_name = f'{node.get_name()}'
        value = self.visit(node.value_node, context, command_position)

        if isinstance(value, BuildList):
            value.list_name = f'variables.{var_name}'
        context.symbols[var_name] = value

        if command_position == 'start':
            return f'execute store result storage {context.id} variables.{var_name} int 1 run {value.mc_value()}'

        elif command_position == 'end':
            return value

        else:
            return f'data modify storage {context.id} variables.{var_name} set value {value.mc_value()}'

    def visit_MultipleStatementsNode(self, node, context, command_position):
        statement_map = map(lambda statement: self.visit(statement, context, command_position), node.statements)
        statement_filter = filter(lambda x: x != '', statement_map)
        return '\n'.join(statement_filter)

    def visit_BinaryOperationNode(self, node, context, command_position):
        left_value = self.visit(node.left_node, context, True)
        right_value = self.visit(node.right_node, context, True)

        if node.operator.value == '+':
            return operation_add(left_value, right_value, command_position)

    @staticmethod
    def no_visit_node(node, context, only_value):
        print('Error here')
        exit()


def build(ast: list, parent_folder):
    if parent_folder.strip(' ') != '' and parent_folder[-1] not in ['/', '\\']:
        parent_folder += '/'

    build_interpreter = BuildInterpreter()
    main_context = BuildContext('main')
    full_text = build_interpreter.visit(ast, main_context)

    with open(f'{parent_folder}init.mcfunction', 'at', encoding='utf-8') as file:
        if full_text != '':
            file.write(full_text)
