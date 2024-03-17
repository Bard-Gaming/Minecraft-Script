from .compile_types import *


class CompileSymbols:
    def __init__(self, parent: "CompileSymbols" = None):
        self.symbols: dict[str, mcs_type] = {}
        self.parent = parent

    def get(self, name: str, *, raise_error=True) -> mcs_type:
        value = self.symbols.get(name, None)
        if value is not None:
            return value  # NOQA since value is not None but PyCharm seems to think it is

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(f"name {name !r} is not defined")

    def set(self, name: str, value: mcs_type) -> None:
        if self.symbols.get(name, None) is not None:
            self.symbols[name] = value
            return

        if self.parent is not None:
            self.parent.set(name, value)
            return

        raise NameError(f"name {name !r} has not been declared")

    def declare(self, name: str, value: mcs_type) -> None:
        # declare in own symbols regardless if parent already defines variable
        self.symbols[name] = value

    def __repr__(self) -> str:
        return f'CompileSymbols({self.parent !r})'


class CompileContext:
    def __init__(self, mcfunction_name: str = 'init', parent: "CompileContext" = None, *, top_level: bool = False):
        self.parent = parent
        self.symbols = CompileSymbols(parent.symbols if parent is not None else None)  # NOQA
        self.top_level = top_level
        self.mcfunction_name = mcfunction_name
        self.uuid = generate_uuid()

    def get(self, name: str) -> mcs_type:
        return self.symbols.get(name)

    def set(self, name: str, value: mcs_type):
        return self.symbols.set(name, value)

    def declare(self, name: str, value: mcs_type) -> tuple[str, str]:
        self.symbols.declare(name, value)

    def __repr__(self) -> str:
        return f'CompileContext({self.mcfunction_name !r}, {self.parent !r}, {self.top_level !r})'


class CompileCommands:
    def __init__(self):
        self.commands: dict[str, list[str]] = {}

    def add_command(self, mcfunction, command) -> None:
        current_commands = self.commands.get(mcfunction, None)
        if current_commands is not None:
            current_commands.append(command)
            return

        self.commands[mcfunction] = [command]  # create list if it doesn't already exist

    def get_file_content(self, mcfunction_file_name: str) -> str:
        return "\n".join(self.commands.get(mcfunction_file_name, []))

    def get_mcs_functions(self) -> tuple[str, ...]:
        return tuple(self.commands.keys())

    def __repr__(self) -> str:
        return "CompileCommands()"


class CompileResult:
    def __init__(self, value: mcs_type = None, return_value: mcs_type = None):
        self.value = value
        self.return_value = return_value

    def get_value(self) -> mcs_type | None:
        return self.value

    def get_return(self) -> mcs_type | None:
        return self.return_value

    def __repr__(self) -> str:
        return f"CompileResult({self.value}, {self.return_value})"


class CompileInterpreter:
    def __init__(self, datapack_id):
        self.datapack_id = datapack_id
        self.commands = CompileCommands()

    def add_command(self, mcfunction: str, command: str) -> None:
        self.commands.add_command(mcfunction, command)

    def add_commands(self, mcfunction: str, commands: iter) -> None:
        for command in commands:
            self.add_command(mcfunction, command)

    def get_file_content(self, mcfunction):
        return self.commands.get_file_content(mcfunction)

    def get_mcs_functions(self) -> tuple[str, ...]:
        return self.commands.get_mcs_functions()

    def visit(self, node, context: CompileContext) -> CompileResult:
        method = getattr(self, f"visit_{type(node).__name__}", self.visit_unknown)
        return method(node, context)

    # ------------------ value nodes ------------------ :
    def visit_NumberNode(self, node, context: CompileContext) -> CompileResult:
        value = int(node.get_value())
        obj = MCSNumber(context.uuid)

        # add value creation command to compiled commands
        self.add_command(context.mcfunction_name, obj.save_to_storage_cmd(value))

        result = CompileResult(obj)
        return result

    # ------------------ variables ------------------ :
    def visit_VariableDeclareNode(self, node, context: CompileContext) -> CompileResult:
        variable_name = node.get_name()
        variable_value = node.get_value()
        if variable_value is not None:
            variable_value = self.visit(variable_value, context).get_value()

        context.declare(variable_name, variable_value)  # declare variable in local context
        if variable_value is None:
            return CompileResult()

        commands = (
            variable_value.set_to_current_cmd(),

            f"data modify storage mcs_{context.uuid} variables.{variable_name} "
            f"set from storage mcs_{context.uuid} current"
        )
        self.add_commands(context.mcfunction_name, commands)

        return CompileResult()

    @staticmethod
    def visit_VariableAccessNode(node, context: CompileContext) -> CompileResult:
        variable_name: str = node.get_name()
        value = context.get(variable_name)

        return CompileResult(value)

    # ------------------ miscellaneous ------------------ :
    def visit_BinaryOperationNode(self, node, context: CompileContext) -> CompileResult:
        left_value: mcs_type = self.visit(node.get_left_node(), context).get_value()
        right_value: mcs_type = self.visit(node.get_right_node(), context).get_value()
        operation: str = node.get_operator().variant.lower()  # 'add', 'subtract', etc...
        result: mcs_type = MCSNumber(context.uuid)

        commands = (
            left_value.set_to_current_cmd(),
            f"execute store result score .a mcs_math run data get storage mcs_{context.uuid} current",
            right_value.set_to_current_cmd(),
            f"execute store result score .b mcs_math run data get storage mcs_{context.uuid} current",
            f"function {self.datapack_id}:math/{operation}",

            f"execute store result storage mcs_{context.uuid} number.{result.uuid} int 1 "
            "run scoreboard players get .out mcs_math"
        )
        self.add_commands(context.mcfunction_name, commands)

        return CompileResult(result)

    def visit_MultilineCodeNode(self, node, context: CompileContext) -> CompileResult:
        for statement in node.get_nodes():
            return_value: CompileResult = self.visit(statement, context)

            # if a "return" statement is encountered:
            if return_value.get_return() is not None:
                return return_value

        return CompileResult(MCSNull(context.uuid))  # if no return statement is encountered

    @staticmethod
    def visit_unknown(node, context):
        raise ValueError(f'Unknown node {node !r}')

    def __repr__(self) -> str:
        return "CompileInterpreter()"


def mcs_compile(ast, user_function_dir: str, datapack_id):
    context = CompileContext(top_level=True)
    interpreter = CompileInterpreter(datapack_id)

    interpreter.visit(ast, context)
    for fnc_name in interpreter.get_mcs_functions():
        with open(f"{user_function_dir}/{fnc_name}.mcfunction", "xt") as mcfunction_file:
            mcfunction_file.write(interpreter.get_file_content(fnc_name))


