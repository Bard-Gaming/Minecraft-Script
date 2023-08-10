from .errors import MCSTypeError, MCSZeroDivisionError, MCSValueError
from .text_additions import text_underline


class Number:
    def __init__(self, value: str | int | object):
        match value:
            case int():
                self.value = value

            case str():
                try:
                    self.value = int(value)
                except ValueError:
                    MCSValueError(f'{value !r} is not a number')
                    exit()

            case Number():
                self.value = value.get_value()

            case Boolean():
                self.value = value.get_value()

            case _:
                MCSValueError(f'"{value !s}" is not a number')
                exit()

    def get_value(self):
        return self.value

    def add(self, number):
        if isinstance(number, Number):
            self.value = self.get_value() + number.get_value()
            return Number(self.get_value())
        else:
            MCSTypeError(f'"{number !s}" is not a number')
            exit()

    def subtract(self, number):
        if isinstance(number, Number):
            self.value = self.get_value() - number.value
            return Number(self.get_value())
        else:
            MCSTypeError(f'"{number !s}" is not a number')
            exit()

    def multiply(self, number):
        if isinstance(number, Number):
            self.value = self.get_value() * number.value
            return Number(self.get_value())
        else:
            MCSTypeError(f'"{number !s}" is not a number')
            exit()

    def divide(self, number):
        if isinstance(number, Number):
            if number.value == 0:
                MCSZeroDivisionError(f"Can't divide by zero")
            self.value = self.get_value() // number.value
            return Number(self.get_value())
        else:
            MCSTypeError(f'"{number !s}" is not a number')
            exit()

    def modulus(self, number):
        if isinstance(number, Number):
            self.value = self.get_value() % number.value
            return Number(self.get_value())
        else:
            MCSTypeError(f'"{number !s}" is not a number')
            exit()

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Number({self.value})'


class List:
    def __init__(self, array: list):
        self.array = array

    def get_value(self):
        return self.array

    def get_index(self, index: Number, fallback: any = None):
        output = None
        index: int = index.get_value()

        try:
            output = self.array[index]
        except IndexError:
            output = fallback

        return output

    def __str__(self):
        return str([str(element) for element in self.array]).replace("'", "")

    def __repr__(self):
        return f'List({self.array})'


class Boolean:
    def __init__(self, value):
        match value:
            case bool():
                self.value = value

            case Boolean():
                self.value = value.get_value()

            case Number():
                self.value = bool(value.get_value())

            case _:
                MCSValueError(f'{value !r} could not be parsed to boolean')
                exit()

    def get_value(self) -> bool:
        return self.value

    def logical_not(self):
        return Boolean(not self.get_value())

    def logical_and(self, other):
        return Boolean(self.get_value() and other)

    def logical_or(self, other):
        return Boolean(self.get_value() or other)

    def __str__(self):
        return str(self.value).lower()

    def __repr__(self):
        return f'Boolean({self.value})'


class Function:
    def __init__(self, name: str, parameter_names: list[str], body_node, context):
        self.name = f'<function {name}>' if name else "<function anonymous>"
        self.parameter_names = parameter_names
        self.body_node = body_node
        self.context = context

    def call(self, arguments: list):
        from .interpreter import Interpreter, Context, SymbolTable
        local_interpreter = Interpreter()

        local_symbol_table = SymbolTable(self.context.symbol_table, load_builtins=False)
        local_context = Context(self.name, local_symbol_table)

        for i in range(len(arguments)):
            arg_name = self.parameter_names[i]
            arg_value = arguments[i]
            local_context.symbol_table.set(arg_name, arg_value)

        output = local_interpreter.visit(self.body_node, local_context)
        if isinstance(output, list):
            try:
                return next(element for element in output if isinstance(element, Return)).value
            except StopIteration:
                return Boolean(False)

        else:
            return output

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Function({self.name !r}, {self.parameter_names !r}, {self.body_node !r}, {self.context !r})'


class BuiltinFunction:
    names = ['log', 'append', 'extend', 'range', 'any']

    def __init__(self, name):
        self.name = name

    def call(self, arguments: list):
        method = getattr(self, f'call_{self.name}', 'unknown_name')
        return method(arguments)

    @staticmethod
    def call_log(arguments: list):
        print(', '.join([str(argument) for argument in arguments]))
        return Boolean(False)

    @staticmethod
    def call_append(arguments: list):
        if len(arguments) > 2:
            MCSTypeError(f'append() takes 2 arguments ({len(arguments)} given)')
            exit()
        base_list: List = arguments[0]
        value = arguments[1]

        if isinstance(base_list, List):
            MCSTypeError(f'{text_underline(f"{base_list}")} is not a list')
            exit()

        base_list.array.append(value)

        return base_list

    @staticmethod
    def call_extend(arguments: list):
        if len(arguments) > 2:
            MCSTypeError(f'extend() takes 2 arguments ({len(arguments)} given)')
            exit()
        base_list: List = arguments[0]
        extend_list: List = arguments[1]

        if not isinstance(base_list, List):
            MCSTypeError(f'{text_underline(f"{base_list}")} is not a list')
            exit()

        if not isinstance(extend_list, List):
            MCSTypeError(f'{text_underline(f"{extend_list}")} is not a list')
            exit()

        base_list.array.extend(extend_list.array)

        return base_list

    @staticmethod
    def call_range(arguments: list):
        if len(arguments) > 1:
            MCSTypeError(f'range() only takes 1 argument ({len(arguments)} given)')
            exit()

        return List(list(range(*arguments)))

    @staticmethod
    def call_any(arguments: list):
        if len(arguments) > 1:
            MCSTypeError(f'any() only takes 1 argument ({len(arguments)} given)')
            exit()

        list_arg: List = arguments[0]

        if isinstance(list_arg, List):
            value_list: map[bool] = map(lambda element: bool(element.get_value()), list_arg.get_value())
            return Boolean(any(value_list))

        else:
            return MCSTypeError(f'')



    def unknown_name(self, arguments: list):
        print(f'Interpreter built-in error ({self.name !r})')
        exit()

    def __str__(self):
        return f'<builtin function {self.name}>'

    def __repr__(self):
        return f'BuiltinFunction({self.name !r})'


class Return:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Return({self.value !r})'
