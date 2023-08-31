from .build_types import BuildString, BuildNumber, BuildList, BuildVariable, BuildFunction
from secrets import token_hex


class BuildSymbol:
    def __init__(self, parent = None):
        self.__symbol_table = {}
        if isinstance(parent, BuildContext):
            parent = parent.symbol_table
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
    def __init__(self, name: str, function_name = 'init', parent = None, symbol_table = None):
        self.name = name
        self.parent = parent
        self.id = f'mcs_{name.lower()}'
        self.symbol_table = symbol_table if symbol_table is not None else BuildSymbol(parent)
        self.function_name = function_name


class BuildInterpreter:
    def __init__(self, datapack_id: str, parent = None):
        self.datapack_id = datapack_id
        self.commands = {}
        self.parent: BuildInterpreter = parent

    def add_command(self, command: str, function: str = None):
        if function is None:
            self.add_command(command, 'init')
            return

        if self.parent and self.parent.commands.get(function) is not None:
            self.parent.add_command(command, function)
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

        self.add_command(f'data modify storage {string_obj.get_full_storage_location()} set value {string_obj.get_value()}', context.function_name)

        return string_obj

    def visit_NumberNode(self, node, context):
        number_obj = BuildNumber(node.get_value(), self.datapack_id)

        self.add_command(f'data modify storage {number_obj.get_full_storage_location()} set value {number_obj.get_value()}', context.function_name)

        return number_obj

    def visit_ListNode(self, node, context):
        value_array = [self.visit(element, context) for element in node.array]
        list_obj = BuildList(value_array, self.datapack_id)

        self.add_commands(list_obj.list_commands(), context.function_name)

        return list_obj

    def visit_IterableGetNode(self, node, context):
        current_iterable = self.visit(node.atom, context)
        index = self.visit(node.index, context).get_value()

        self.add_command(current_iterable.get_index_cmd(index), context.function_name)

        return current_iterable.get_index(index)

    def visit_VariableAccessNode(self, node, context) -> any:
        var_name = f'{node.get_name()}'
        var_value = context.symbol_table.get(var_name)

        if var_value:
            return BuildVariable(var_name, var_value, self.datapack_id)

    def visit_VariableAssignNode(self, node, context):
        var_name: str = node.get_name()
        var_value = self.visit(node.value_node, context)

        context.symbol_table.set(var_name, var_value)

        self.add_command(var_value.set_temporary(), context.function_name)
        self.add_command(f'data modify storage mcs_{self.datapack_id} variables.{var_name} set from storage mcs_{self.datapack_id} temporary', context.function_name)

    def visit_FunctionAssignNode(self, node, context):
        func_name = node.name_token.value if node.name_token else None
        parameter_names = [param_token.value for param_token in node.parameter_name_tokens]
        body_node = node.body_node

        function = BuildFunction(name=func_name, parameter_names=parameter_names, body_node=body_node,
                                 datapack_id=self.datapack_id, context=context, interpreter=self)

        if func_name:
            context.symbol_table.set(func_name, function)

        return function

    def visit_FunctionCallNode(self, node, context):
        function: BuildFunction = self.visit(node.atom, context)
        arguments = BuildList([self.visit(arg_token, context) for arg_token in node.argument_nodes], self.datapack_id)

        self.add_command(function.call_command(arguments))

    def visit_CodeBlockNode(self, node, context):
        local_context = BuildContext('code_block', f'code_blocks/cb_{token_hex(16)}', context)
        self.add_command(f'function {self.datapack_id}:{local_context.function_name}', context.function_name)

        visit_list = []
        for statement in node.statements:
            visit_statement = self.visit(statement, local_context)
            visit_list.append(visit_statement)

        return visit_list

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
