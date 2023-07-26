from .errors import MCSTypeError, MCSZeroDivisionError, MCSValueError


class Number:
    def __init__(self, value: str | int):
        try:
            self.value = int(value)
        except ValueError:
            MCSValueError(f'{value !r} is not a number')
            exit()

    def add(self, number) -> int:
        if isinstance(number, Number):
            self.value = self.value + number.value
            return self.value
        else:
            MCSTypeError(f'{number !s} is not a number')
            exit()

    def subtract(self, number) -> int:
        if isinstance(number, Number):
            self.value = self.value - number.value
            return self.value
        else:
            MCSTypeError(f'{number !s} is not a number')
            exit()

    def multiply(self, number) -> int:
        if isinstance(number, Number):
            self.value = self.value * number.value
            return self.value
        else:
            MCSTypeError(f'{number !s} is not a number')
            exit()

    def divide(self, number) -> int:
        if isinstance(number, Number):
            if number.value == 0:
                MCSZeroDivisionError(f"Can't divide by zero")
            self.value = self.value // number.value
            return self.value
        else:
            MCSTypeError(f'{number !s} is not a number')
            exit()

    def modulus(self, number) -> int:
        if isinstance(number, Number):
            self.value = self.value % number.value
            return self.value
        else:
            MCSTypeError(f'{number !s} is not a number')
            exit()

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Number({self.value})'


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

        return local_interpreter.visit(self.body_node, local_context)

    def __repr__(self):
        return f'Function({self.name !r}, {self.parameter_names !r}, {self.body_node !r}, {self.context !r})'

    def __str__(self):
        return f'{self.name}'


class BuiltinFunction:
    def __init__(self, name):
        self.name = name

    def call(self, arguments: list):
        method = getattr(self, f'call_{self.name}', 'unknown_name')
        method(arguments)

    @staticmethod
    def call_log(arguments: list):
        print(', '.join([str(argument) for argument in arguments]))
        return Number(0)

    def unknown_name(self, arguments: list):
        print(f'Interpreter built-in error ({self.name !r})')
        exit()
