from .errors import MCSTypeError, MCSZeroDivisionError, MCSValueError, MCSIndexError
from .text_additions import text_underline


# -------- Abstract Types --------

class MCSObject:
    value = None

    def get_value(self):
        return self.value

    def raise_operation_error(self, value: any, operator: str):
        MCSTypeError(f'Unsupported operand type(s) for {operator}: "{self.__class__.__name__}" and "{value.__class__.__name__}"')
        exit()

    def add(self, value):
        self.raise_operation_error(value, '+')

    def subtract(self, value):
        self.raise_operation_error(value, '-')

    def multiply(self, value):
        self.raise_operation_error(value, '*')

    def divide(self, value):
        self.raise_operation_error(value, '/')

    def modulus(self, value):
        self.raise_operation_error(value, '%')


class Iterable(MCSObject):
    def get_index(self, index):
        index: int = index.get_value()
        output = None

        try:
            output = self.get_value()[index]
        except IndexError:
            MCSIndexError(str(index), type=self.__class__.__name__)
            exit()

        return output

    def set_index(self, index, value: any):
        index = index.get_value()
        try:
            self.get_value()[index] = value
        except IndexError:
            MCSIndexError(str(index), type=self.__class__.__name__)
            exit()

    @classmethod
    def types(cls):
        return tuple(cls.__subclasses__())


class Return:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Return({self.value !r})'


# -------- Data Types --------

class Number(MCSObject):
    def __init__(self, value: str | int | object):
        self.supported_operations = (Number, Boolean)

        match value:
            case int():
                self.value = value

            case str():
                try:
                    self.value = int(value)
                except ValueError:
                    MCSValueError(f'{value !r} is not a number')
                    exit()

            case String():
                MCSTypeError(f'Expected Number, got String: "{value.get_value()}"')
                exit()

            case List():
                MCSTypeError(f'Expected Number, got List: "{value}"')
                exit()

            case Number():
                self.value = value.get_value()

            case Boolean():
                self.value = value.get_value()

            case _:
                MCSValueError(f'"{value !s}" is not a number')
                exit()

    def add(self, number):
        if isinstance(number, self.supported_operations):
            self.value = self.get_value() + number.get_value()
            return Number(self.get_value())
        else:
            super().add(number)

    def subtract(self, number):
        if isinstance(number, self.supported_operations):
            self.value = self.get_value() - number.value
            return Number(self.get_value())
        else:
            super().subtract(number)

    def multiply(self, number):
        if isinstance(number, self.supported_operations):
            self.value = self.get_value() * number.value
            return Number(self.get_value())
        else:
            super().multiply(number)

    def divide(self, number):
        if isinstance(number, self.supported_operations):
            if number.value == 0:
                MCSZeroDivisionError(f"Can't divide by zero")
            self.value = self.get_value() // number.value
            return Number(self.get_value())
        else:
            super().divide(number)

    def modulus(self, number):
        if isinstance(number, self.supported_operations):
            self.value = self.get_value() % number.value
            return Number(self.get_value())
        else:
            super().modulus(number)

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return f'Number({self.get_value()})'


class String(Iterable, MCSObject):
    def __init__(self, value):
        match value:
            case str():
                self.value = value

            case int():
                self.value = str(value)

            case list():
                self.value = str(value)

            case bool():
                self.value = str(value)

            case Number():
                self.value = str(value.get_value())

            case String():
                self.value = value.get_value()

            case List():
                self.value = str(value.get_value())

            case Boolean():
                self.value = str(value.get_value())

            case _:
                MCSValueError(f'"{value}" could not be parsed to String.')
                exit()

    def get_index(self, index):
        value = super().get_index(index)
        return String(value)

    def set_index(self, index, value: any):
        MCSTypeError('String does not support item assignment')
        exit()

    def add(self, value):
        if isinstance(value, String):
            output = self.get_value() + value.get_value()
            return String(output)
        else:
            MCSTypeError(f'Failed to concatenate {self !s} (String) with operand {value !s} ({value.__class__.__name__})')
            exit()

    def subtract(self, value):
        if isinstance(value, String):
            characters = set(value.get_value())
            output = self.get_value()
            for char in characters:
                output = output.replace(char, "", value.get_value().count(char))

            return String(output)

        else:
            MCSTypeError(f'Failed to subtract {self !s} (String) with operand {value !s} ({value.__class__.__name__})')
            exit()

    def multiply(self, value):
        if isinstance(value, Number):
            output = self.get_value() * value.get_value()
            return String(output)

        else:
            MCSTypeError(f'Can\'t multiply String by non-number of type "{value.__class__.__name__}"')
            exit()

    def __str__(self):
        return repr(self.get_value())

    def __repr__(self):
        return f'String({self.get_value() !r})'


class List(Iterable, MCSObject):
    def __init__(self, value: list):
        self.value = value

    def __str__(self):
        return str([str(element) for element in self.get_value()]).replace("'", "")

    def __repr__(self):
        return f'List({self.get_value()})'


class Boolean(MCSObject):
    def __init__(self, value):
        match value:
            case bool():
                self.value = value

            case Boolean():
                self.value = value.get_value()

            case Number():
                self.value = bool(value.get_value())

            case String():
                self.value = bool(value.get_value())

            case List():
                self.value = bool(value.get_value())

            case Function():
                self.value = True

            case BuiltinFunction():
                self.value = True

            case _:
                MCSValueError(f'{value !r} could not be parsed to boolean')
                exit()

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


class Function(MCSObject):
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
    names = ['log', 'append', 'extend', 'range', 'any', 'parseNumber', 'parseString']

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
        if len(arguments) > 3:
            MCSTypeError(f'range() takes a maximum of 3 arguments ({len(arguments)} given)')
            exit()

        arguments = map(lambda element: element.get_value(), arguments)

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

    @staticmethod
    def call_parseNumber(arguments: list):
        if len(arguments) > 1:
            MCSTypeError(f'parseNumber() only takes 1 argument ({len(arguments)} given)')
            exit()

        value = arguments[0]
        try:
            value = int(value.get_value())
        except TypeError:
            MCSTypeError(f'Expected String or Boolean, got {type(value).__name__} instead.')
            exit()
        except ValueError:
            MCSValueError(f'Couldn\'t parse "{value.get_value()}" to a valid Number.')
            exit()

        return Number(value)

    @staticmethod
    def call_parseString(arguments: list):
        if len(arguments) > 1:
            MCSTypeError(f'parseString() only takes 1 argument ({len(arguments)} given)')
            exit()

        return String(arguments[0].get_value())

    def unknown_name(self, arguments: list):
        print(f'Interpreter built-in error ({self.name !r})')
        exit()

    def __str__(self):
        return f'<builtin function {self.name}>'

    def __repr__(self):
        return f'BuiltinFunction({self.name !r})'
