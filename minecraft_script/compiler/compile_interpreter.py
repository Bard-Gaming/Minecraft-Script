from .builtin_functions import builtin_functions
from .compile_types import *


class CompileSymbols:
    def __init__(self, parent: "CompileSymbols" = None, *, load_builtins: bool = False):
        self.symbols: dict[str, mcs_type] = {}
        self.parent = parent

        if load_builtins:
            self.load_builtins()

    def load_builtins(self) -> None:
        # Lookup table to change function names
        function_name_lookup = {
            "mcs_range": "range"
        }

        for fnc in builtin_functions:
            mcs_fnc = MCSFunction(None, None, None, None)
            mcs_fnc.call = fnc

            self.declare(
                function_name_lookup.get(fnc.__name__, fnc.__name__),  # get name in dict, otherwise just use fnc name
                mcs_fnc
            )

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
        self.parent: CompileContext = parent
        self.symbols = CompileSymbols(parent.symbols if parent is not None else None, load_builtins=top_level)  # NOQA
        self.top_level = top_level
        self._mcfunction_name = mcfunction_name
        self.uuid = generate_uuid()

    @property
    def mcfunction_name(self) -> str:
        return (
            f"user_functions/{self._mcfunction_name}"
            if self._mcfunction_name[0] != ":" else
            f"code_blocks/{self._mcfunction_name[1:]}"
        )

    def get(self, name: str) -> mcs_type:
        return self.symbols.get(name)

    def set(self, name: str, value: mcs_type):
        return self.symbols.set(name, value)

    def declare(self, name: str, value: mcs_type) -> None:
        self.symbols.declare(name, value)

    def get_context_ownership(self, var_name: str) -> "CompileContext":
        if self.symbols.symbols.get(var_name, None) is not None:
            return self

        if self.parent is not None:
            return self.parent.get_context_ownership(var_name)

        raise NameError(f"name {var_name} is not defined")

    def __repr__(self) -> str:
        return f'CompileContext({self._mcfunction_name !r}, {self.parent !r}, {self.top_level !r})'


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
        self.used_context_ids = set()
        self.functions_to_generate = set()

    def add_command(self, mcfunction: str, command: str | None) -> None:
        if command is not None:  # only add command if it's not nothing (makes it easier for dynamic commands)
            self.commands.add_command(mcfunction, command)

    def add_commands(self, mcfunction: str, commands: iter) -> None:
        multiline_command = "\n".join(commands)  # wrap all commands into a single string
        self.add_command(mcfunction, multiline_command)

    def get_file_content(self, mcfunction):
        return self.commands.get_file_content(mcfunction)

    def get_mcs_functions(self) -> tuple[str, ...]:
        return self.commands.get_mcs_functions()

    def visit(self, node, context: CompileContext) -> CompileResult:
        if context.uuid not in self.used_context_ids:
            self.used_context_ids.add(context.uuid)

        method = getattr(self, f"visit_{type(node).__name__}", self.visit_unknown)
        return method(node, context)

    # ------------------ value nodes ------------------ :
    def visit_NumberNode(self, node, context: CompileContext) -> CompileResult:
        value = int(node.get_value())
        obj = MCSNumber(context)

        # add value creation command to compiled commands
        self.add_command(context.mcfunction_name, obj.save_to_storage_cmd(value))

        result = CompileResult(obj)
        return result

    def visit_StringNode(self, node, context: CompileContext) -> CompileResult:
        value = repr(node.get_value())  # repr to turn double quotes into single quotes if double quotes are used in str
        mcs_obj = MCSString(context)

        # add value creation command to compiled commands
        self.add_command(context.mcfunction_name, mcs_obj.save_to_storage_cmd(value))

        result = CompileResult(mcs_obj)
        return result

    def visit_ListNode(self, node, context: CompileContext) -> CompileResult:
        value_list: list[mcs_type] = list(map(lambda x: self.visit(x, context).get_value(), node.get_node_list()))
        mcs_obj = MCSList(context)

        # add value creation commands to compiled commands
        self.add_commands(context.mcfunction_name, mcs_obj.save_to_storage_cmd(value_list))

        result = CompileResult(mcs_obj)
        return result

    def visit_BooleanNode(self, node, context: CompileContext) -> CompileResult:
        boolean: bool = node.get_value()
        mcs_obj = MCSBoolean(context)
        value = "1b" if boolean is True else "0b"

        # add value creation command to compiled commands
        self.add_command(context.mcfunction_name, mcs_obj.save_to_storage_cmd(value))

        result = CompileResult(mcs_obj)
        return result

    @staticmethod
    def visit_NullNode(node, context: CompileContext) -> CompileResult:
        mcs_obj = MCSNull(context)
        # Don't add any commands since null node is always 0b
        return CompileResult(mcs_obj)

    def visit_DefineFunctionNode(self, node, context: CompileContext) -> CompileResult:
        fnc_name = node.get_name()
        fnc_body = node.get_body()
        fnc_parameter_names: list[str, ...] = node.get_parameter_names()

        function = MCSFunction(fnc_name, fnc_body, fnc_parameter_names, context)
        self.functions_to_generate.add(function)  # save function to generate for later
        context.declare(fnc_name, function)

        return CompileResult(function)

    # ------------------ variables ------------------ :
    def visit_VariableDeclareNode(self, node, context: CompileContext) -> CompileResult:
        variable_name: str = node.get_name()
        variable_value: mcs_type = node.get_value()
        if variable_value is None:
            context.declare(variable_name, MCSNull(context))
            return CompileResult()

        variable_value = self.visit(variable_value, context).get_value()

        commands = [
            variable_value.set_to_current_cmd(context),
            f"data modify storage mcs_{context.uuid} variable.{variable_name} set from storage mcs_{context.uuid} current"  # NOQA
        ]
        # garbage collect variable_value if it's not a variable (was only used to define current variable):
        if not isinstance(variable_value, MCSVariable):
            commands.append(variable_value.delete_from_storage_cmd())
        self.add_commands(context.mcfunction_name, commands)  # actually put the commands in the context file

        variable = MCSVariable(variable_name, context)  # create variable object to save in context
        context.declare(variable_name, variable)  # declare variable in local context

        return CompileResult()

    @staticmethod
    def visit_VariableAccessNode(node, context: CompileContext) -> CompileResult:
        variable_name: str = node.get_name()
        value: MCSVariable = context.get(variable_name)

        return CompileResult(value)

    def visit_VariableSetNode(self, node, context: CompileContext) -> CompileResult:
        var_name = node.get_name()
        new_value: mcs_type = self.visit(node.get_value(), context).get_value()

        owner_context = context.get_context_ownership(var_name)

        commands = (
            new_value.set_to_current_cmd(context),
            f"data modify storage mcs_{owner_context.uuid} variable.{var_name} set from storage mcs_{context.uuid} current",  # NOQA
        )
        self.add_commands(context.mcfunction_name, commands)

        return CompileResult()

    def visit_GetKeyNode(self, node, context: CompileContext) -> CompileResult:
        atom: mcs_type = self.visit(node.get_atom(), context).get_value()
        key: MCSNumber = self.visit(node.get_key(), context).get_value()

        result = MCSUnknown(context)

        local_context = CompileContext(f":cb_{generate_uuid()}")  # context for function that retrieves value at index
        self.add_command(
            local_context.mcfunction_name,
            f"$data modify storage {result.get_storage()} {result.get_nbt()} set from storage {atom.get_storage()} {atom.get_nbt()}.$(index)"
        )

        commands = (
            f"data modify storage mcs_{context.uuid} current set value " "{}",
            f"data modify storage mcs_{context.uuid} current.index set from storage {key.get_storage()} {key.get_nbt()}",
            f"function {self.datapack_id}:{local_context.mcfunction_name} with storage mcs_{context.uuid} current"
        )
        self.add_commands(context.mcfunction_name, commands)

        return CompileResult(result)

    # ------------------ conditions & loops ------------------ :
    def visit_IfConditionNode(self, node, context: CompileContext) -> CompileResult:
        conditions: list[dict] = node.get_conditions()

        for condition in conditions:
            if condition.get('type') == 'if':
                # create local context with all parent variables and create all body commands there
                local_context = CompileContext(f':cb_{generate_uuid()}', context)
                out: CompileResult = self.visit(condition.get('body'), local_context)

                expression: MCSNumber = self.visit(condition.get('expression'), context).get_value()
                commands = (
                    expression.set_to_current_cmd(context),
                    f"execute store result score .out mcs_math run data get storage mcs_{context.uuid} current 1",
                    f"data modify storage mcs_{local_context.uuid} variable set from storage mcs_{context.uuid} variable",
                    f"execute if score .out mcs_math matches 1 run function {self.datapack_id}:{local_context.mcfunction_name}"  # NOQA
                )
                self.add_commands(context.mcfunction_name, commands)

                if out.get_return() is not None:
                    return out

            else:
                out: CompileResult = self.visit(condition.get('body'), context)
                if out.get_return() is not None:
                    return out

        return CompileResult()

    def visit_ForLoopNode(self, node, context: CompileContext) -> CompileResult:
        iterable: MCSList = self.visit(node.get_iterable(), context).get_value()
        element_name: str = node.get_child_name()
        body = node.get_body()

        local_context = CompileContext(f':cb_{generate_uuid()}', context)
        macro_context = CompileContext(f':cb_{generate_uuid()}', context)
        loop_id = f"{generate_uuid()}"

        init_commands = (
            f"scoreboard players set .loop_iter_{loop_id} mcs_math 0",
            iterable.set_to_current_cmd(context),
            f"execute store result score .loop_end_{loop_id} mcs_math run data get storage mcs_{context.uuid} current.length 1",  # NOQA
            f"function {self.datapack_id}:{local_context.mcfunction_name}",
            f"scoreboard players reset .loop_iter_{loop_id} mcs_math",  # remove to avoid clutter
            f"scoreboard players reset .loop_end_{loop_id} mcs_math",
        )
        self.add_commands(context.mcfunction_name, init_commands)

        macro_cmd = f"$data modify storage mcs_{local_context.uuid} variable.{element_name} set from storage {iterable.get_storage()} {iterable.get_nbt()}.$(index)"  # NOQA
        self.add_command(macro_context.mcfunction_name, macro_cmd)

        loop_init_commands = (
            f"execute store result storage mcs_{local_context.uuid} current.index int 1 run scoreboard players get .loop_iter_{loop_id} mcs_math",  # NOQA
            f"function {self.datapack_id}:{macro_context.mcfunction_name} with storage mcs_{local_context.uuid} current",  # NOQA
        )
        self.add_commands(local_context.mcfunction_name, loop_init_commands)
        local_context.declare(element_name, MCSVariable(element_name, local_context))

        out: CompileResult = self.visit(body, local_context)  # add commands to code block

        loop_end_commands = (
            f"scoreboard players add .loop_iter_{loop_id} mcs_math 1",
            f"execute if score .loop_iter_{loop_id} mcs_math < .loop_end_{loop_id} mcs_math run function {self.datapack_id}:{local_context.mcfunction_name}",
        )
        self.add_commands(local_context.mcfunction_name, loop_end_commands)

        if out.get_return() is not None:
            return out

        return CompileResult()

    def visit_WhileLoopNode(self, node, context: CompileContext) -> CompileResult:
        loop_context = CompileContext(f':cb_{generate_uuid()}', context)

        out: CompileResult = self.visit(node.get_body(), loop_context)  # add commands to loop context file

        condition: mcs_type = self.visit(node.get_condition(), loop_context).get_value()
        loop_commands = (
            condition.set_to_current_cmd(loop_context),
            f"execute store result score .out mcs_math run data get storage mcs_{loop_context.uuid} current 1",
            f"execute if score .out mcs_math matches 1 run function {self.datapack_id}:{loop_context.mcfunction_name}",  # NOQA
        )
        self.add_commands(loop_context.mcfunction_name, loop_commands)

        self.add_command(context.mcfunction_name, f"function {self.datapack_id}:{loop_context.mcfunction_name}")  # NOQA

        return out if out.get_return() is not None else CompileResult()

    # ------------------ scope nodes ------------------ :
    def visit_MultilineCodeNode(self, node, context: CompileContext) -> CompileResult:
        for statement in node.get_nodes():
            return_value: CompileResult = self.visit(statement, context)

            # if a "return" statement is encountered:
            if return_value.get_return() is not None:
                return return_value

        return CompileResult(MCSNull(context))  # if no return statement is encountered

    def visit_CodeBlockNode(self, node, context: CompileContext) -> CompileResult:
        local_context = CompileContext(f':cb_{generate_uuid()}', context)
        return_value: CompileResult = self.visit(node.get_body(), local_context)

        # import parent context's variables and execute code block:
        commands = (
            f"data modify storage mcs_{local_context.uuid} variable set from storage mcs_{context.uuid} variable",
            f"function {self.datapack_id}:{local_context.mcfunction_name}"
        )
        self.add_commands(context.mcfunction_name, commands)  # add commands to parent context

        return return_value

    def visit_FunctionCallNode(self, node, context: CompileContext) -> CompileResult:
        fnc: MCSFunction = self.visit(node.get_root(), context).get_value()
        arguments: tuple[mcs_type, ...] = tuple(map(lambda x: self.visit(x, context).get_value(), node.get_arguments()))

        commands, return_value = fnc.call(self, arguments, context)

        if commands is not None:
            self.add_commands(context.mcfunction_name, commands)

        return CompileResult(return_value)

    # ------------------ minecraft stuff ------------------ :
    def visit_EntitySelectorNode(self, node, context: CompileContext) -> CompileResult:
        selector: str = node.get_selector()
        local_context = CompileContext(f":cb_{generate_uuid()}", context)

        out: CompileResult = self.visit(node.get_statement(), local_context)  # add commands to local context

        setup_commands = (
            f"data modify storage mcs_{local_context.uuid} variable set from storage mcs_{context.uuid} variable",
            f"execute as @{selector} at @s run function {self.datapack_id}:{local_context.mcfunction_name}",  # NOQA
        )
        self.add_commands(context.mcfunction_name, setup_commands)

        return out if out.get_return() is not None else CompileResult()

    # ------------------ miscellaneous ------------------ :
    def visit_BinaryOperationNode(self, node, context: CompileContext) -> CompileResult:
        left_value: mcs_type = self.visit(node.get_left_node(), context).get_value()
        right_value: mcs_type = self.visit(node.get_right_node(), context).get_value()
        operation: str = node.get_operator().variant.lower()  # 'add', 'subtract', etc...
        result: mcs_type = MCSNumber(context)

        commands = (
            left_value.set_to_current_cmd(context),
            f"execute store result score .a mcs_math run data get storage mcs_{context.uuid} current",
            right_value.set_to_current_cmd(context),
            f"execute store result score .b mcs_math run data get storage mcs_{context.uuid} current",
            f"function {self.datapack_id}:math/{operation}",
            f"execute store result storage mcs_{context.uuid} {result.get_nbt()} int 1 run scoreboard players get .out mcs_math",  # NOQA
        )
        self.add_commands(context.mcfunction_name, commands)

        return CompileResult(result)

    @staticmethod
    def visit_unknown(node, context):
        raise ValueError(f'Unknown node {node !r}')

    def __repr__(self) -> str:
        return "CompileInterpreter()"


def mcs_compile(ast, functions_dir: str, datapack_id):
    context = CompileContext(top_level=True)
    interpreter = CompileInterpreter(datapack_id)

    interpreter.visit(ast, context)  # compile whole program to have a list of commands for each function

    for mcs_fnc in interpreter.functions_to_generate:
        mcs_fnc.generate_function(interpreter)  # generate user-defined functions (not done when compiling over program)

    for context_id in interpreter.used_context_ids:  # remove all used storages in user_functions/kill.mcfunction
        commands = (
            f"data remove storage mcs_{context_id} current",
            f"data remove storage mcs_{context_id} variable",
            f"data remove storage mcs_{context_id} number",
            f"data remove storage mcs_{context_id} string",
            f"data remove storage mcs_{context_id} list",
            f"data remove storage mcs_{context_id} boolean",
            f"data remove storage mcs_{context_id} unknown",
            ""  # add newline to separate contexts (only visual)
        )
        interpreter.add_commands('kill', commands)

    for fnc_name in interpreter.get_mcs_functions():  # create the files for all functions
        mcfunction_path = f"{functions_dir}/{fnc_name}.mcfunction"

        with open(mcfunction_path, "xt") as mcfunction_file:
            mcfunction_file.write(interpreter.get_file_content(fnc_name))
