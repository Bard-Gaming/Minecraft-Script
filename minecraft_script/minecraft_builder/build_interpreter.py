from .build_types import BuildString, BuildNumber, BuildList, BuildVariable


class BuildSymbol:
    def __init__(self, parent = None):
        self.__symbol_table = {}
        self.parent: BuildSymbol = parent

    def set(self, name, value):
        if self.parent and self.parent.get(name) is not None:
            self.parent.set(name, value)
            return

        self.__symbol_table[name] = value

    def get(self, name):
        value = self.__symbol_table.get(name)

        if value is None and self.parent:
            return self.parent.get(name)

        return value


class BuildContext:
    def __init__(self, name: str, parent = None, symbol_table = None):
        self.name = name
        self.parent = parent
        self.id = f'mcs_{name.lower()}'
        self.symbol_table = symbol_table if symbol_table is not None else BuildSymbol(parent)


class BuildInterpreter:
    def __init__(self, datapack_id: str):
        self.datapack_id = datapack_id
        self.commands = {}

    def add_command(self, command: str, function: str = None):
        if function is None:
            self.add_command(command, 'init')
            return

        if self.commands.get(function) is None:
            self.commands[function] = [f'\n{command}']
            return

        else:
            self.commands[function].append(f'\n{command}')
            return

    def add_commands(self, iterable, function: str = None):
        for command in iterable:
            self.add_command(command, function)

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, 'no_visit_node')
        return method(node, context)

    def visit_StringNode(self, node, context):
        string_obj = BuildString(node.get_value(), self.datapack_id)

        self.add_command(f'data modify storage {string_obj.get_full_storage_location()} set value {string_obj.get_value()}')

        return string_obj

    def visit_NumberNode(self, node, context):
        number_obj = BuildNumber(node.get_value(), self.datapack_id)

        self.add_command(f'data modify storage {number_obj.get_full_storage_location()} set value {number_obj.get_value()}')

        return number_obj

    def visit_ListNode(self, node, context):
        value_array = [self.visit(element, context) for element in node.array]
        list = BuildList(value_array, self.datapack_id)

        self.add_commands(list.list_commands())

        return list

    def visit_VariableAccessNode(self, node, context) -> any:
        var_name = f'{node.get_name()}'
        var_value = context.symbol_table.get(var_name)

        if var_value:
            return BuildVariable(var_name, var_value, self.datapack_id)

    def visit_VariableAssignNode(self, node, context):
        var_name: str = node.get_name()
        var_value = self.visit(node.value_node, context)

        context.symbol_table.set(var_name, var_value)

        self.add_command(var_value.set_temporary())
        self.add_command(f'data modify storage mcs_{self.datapack_id} variables.{var_name} set from storage mcs_{self.datapack_id} temporary')

    def visit_MultipleStatementsNode(self, node, context):
        for statement in node.statements:
            self.visit(statement, context)

    @staticmethod
    def no_visit_node(node, context):
        print(f'Error with {node}')
        exit()


def build(ast: list, parent_folder, datapack_id):
    if parent_folder.strip(' ') != '' and parent_folder[-1] not in ['/', '\\']:
        parent_folder += '/'

    build_interpreter = BuildInterpreter(datapack_id)
    main_context = BuildContext('main')
    build_interpreter.visit(ast, main_context)

    for function, command_list in build_interpreter.commands.items():
        with open(f'{parent_folder}{function}.mcfunction', 'at', encoding='utf-8') as current_file:
            current_file.writelines(command_list)
