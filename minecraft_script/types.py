from .errors import *

operation_lookup_table = {
    "&&": "logical_and",
    "||": "logical_or",
}


class MCSObject:
    def get_value(self):
        raise MCSInterpreterError('Failed getting value of unknown Object')

    def get_key(self, key):
        raise MCSTypeError(f'{self.class_name() !r} is not subscriptable')

    def call(self, *args):
        raise MCSTypeError(f'{self.class_name() !r} is not callable')

    def class_name(self) -> str:
        return self.__class__.__name__[3:]

    def print_value(self) -> str:
        return str(self.get_value())

    def repr_value(self) -> str:
        return repr(self.get_value())

    # ----------------- Operations  ----------------- :
    def _binary_operation(self, other, operator: str):
        if isinstance(other, self.__class__):
            return MCSNumber(eval(f"self.value {operator} other.get_value()"))

        raise self.operation_error(other, f'"{operator}"')

    def add(self, other):
        return self._binary_operation(other, '+')

    def subtract(self, other):
        return self._binary_operation(other, '-')

    def multiply(self, other):
        return self._binary_operation(other, '*')

    def divide(self, other):
        return self._binary_operation(other, '//')

    def modulus(self, other):
        return self._binary_operation(other, '%')

    def unary_operation(self, operator: str):
        if operator == 'not':
            return MCSBool(not bool(self.get_value()))

        raise MCSTypeError(f'Unsupported unary operand {operator !r} for type {self.class_name() !r}')

    def operation_error(self, other, operation):
        return MCSTypeError(
            f"Unsupported operand types for {operation if operation != '//' else '/' !r}: "
            f"{self.class_name() !r} and {other.class_name() !r}"
        )

    # ----------------- Comparisons ----------------- :
    def _comparison_operation(self, other, comparator: str):
        try:
            result = eval(f"self.get_value() {comparator} other.get_value()")
        except TypeError as err:
            raise self.comparison_error(other, comparator) from err
        else:
            return MCSBool(result)

    def equals(self, other):
        return self._comparison_operation(other, '==')

    def lesser_than(self, other):
        return self._comparison_operation(other, '<')

    def greater_than(self, other):
        return self._comparison_operation(other, '>')

    def lesser_equals_than(self, other):
        return self._comparison_operation(other, '<=')

    def greater_equals_than(self, other):
        return self._comparison_operation(other, '>=')

    def comparison_error(self, other, comparator: str):
        return MCSTypeError(
            f"{comparator !r} not supported between instances of "
            f"{self.class_name() !r} and {other.class_name() !r}"
        )

    # ----------------- Miscellaneous  ----------------- :
    def __bool__(self):
        return bool(self.get_value())


class MCSIterable(MCSObject):
    def get_key(self, key: str):
        try:
            index = int(key)
        except ValueError as err:
            raise MCSTypeError(f'{self.class_name()} indices must be integers') from err

        return self.get_value()[index]


class MCSNumber(MCSObject):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise MCSInterpreterError(f"Expected type 'int', got {value.__class__.__name__ !r}")

        self.value = value

    def get_value(self) -> int:
        return self.value

    def unary_operation(self, operator: str):
        if operator == 'add':
            return self
        elif operator == 'subtract':
            return MCSNumber(-self.value)  # Number with opposite value

        return super().unary_operation(operator)

    # ----------------- Miscellaneous ----------------- :
    def __repr__(self) -> str:
        return f'MCSNumber({self.value !r})'


class MCSBool(MCSObject):
    def __init__(self, value: bool):
        if not isinstance(value, bool):
            raise MCSInterpreterError(f"Expected type 'bool', got {value.__class__.__name__ !r}")

        self.value = value

    def get_value(self) -> bool:
        return self.value

    def print_value(self) -> str:
        return "true" if self.value else "false"

    def repr_value(self) -> str:
        return self.print_value()  # same as print value


class MCSNull(MCSObject):
    def get_value(self) -> None:
        return

    # ----------------- Operations ----------------- :
    def _binary_operation(self, other, operator: str):
        if isinstance(other, (MCSNumber, MCSNull)):
            return MCSNumber(eval(f"0 {operator} other.get_value()"))

        raise self.operation_error(other, repr(operator))

    # ----------------- Miscellaneous ----------------- :
    def __repr__(self) -> str:
        return f'MCSNull()'


class MCSString(MCSIterable, MCSObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise MCSInterpreterError(f"Expected type 'str', got {value.__class__.__name__ !r}")
        self.value = value

    def get_value(self) -> str:
        return self.value

    def get_key(self, key: str) -> "MCSString":
        return MCSString(super().get_key(key))

    # ----------------- Operations ----------------- :
    def _binary_operation(self, other, operator: str):
        if operator in ('//', '%'):  # invalid operations
            raise self.operation_error(other, operator)

        if isinstance(other, MCSString if operator in ('+', '-') else (MCSNumber, MCSNull)):
            return MCSString(eval(f"self.value {operator} other.get_value()"))

        raise self.operation_error(other, operator)

    # ----------------- Miscellaneous ----------------- :
    def __repr__(self) -> str:
        return f"MCSString({self.value !r})"


class MCSList(MCSIterable, MCSObject):
    def __init__(self, value: list | tuple):
        if not isinstance(value, (list, tuple)):
            raise MCSInterpreterError(f"Expected type 'list' or 'tuple', got {value.__class__.__name__ !r}")

        self.value = list(value)

    def get_value(self) -> list:
        return self.value

    def print_value(self) -> str:
        return f"[{', '.join(value.repr_value() for value in self.value)}]"

    # ----------------- Operations ----------------- :
    def _binary_operation(self, other, operator: str):
        if operator in ('//', '%', '-'):  # invalid operations
            raise self.operation_error(other, operator)

        if isinstance(other, MCSList):
            return MCSList(self.value + other.get_value())

        raise self.operation_error(other, operator)

    # ----------------- Miscellaneous ----------------- :
    def __repr__(self) -> str:
        return f'MCSList({self.value !r})'


class MCSFunction(MCSObject):
    def __init__(self, name: str, body, parameter_names: tuple[str, ...]):
        self.name = name if name is not None else "anonymous function"
        self.body = body
        self.parameter_names = parameter_names

    def get_value(self):
        raise MCSInterpreterError("Can't get value of function")

    def print_value(self) -> str:
        return f'<{self.name}>'

    def repr_value(self) -> str:
        return self.print_value()

    def call(self, arg_list: list | None, context):
        from .interpreter import Interpreter, InterpreterContext
        local_interpreter = Interpreter()
        local_context = InterpreterContext(parent=context)  # top level always false here

        if len(arg_list) != len(self.parameter_names):
            raise MCSValueError(f"Function {self.print_value()} takes {len(self.parameter_names)} arguments, got {len(arg_list)}")

        # Add argument values to parameter names in local context (to make arguments work)
        for i in range(len(self.parameter_names)):
            local_context.declare(self.parameter_names[i], arg_list[i])

        result = local_interpreter.visit(self.body, local_context)

        return result if result is not None else MCSNull()

    def __repr__(self) -> str:
        return f"MCSFunction({self.name !r}, {self.parameter_names !r})"
