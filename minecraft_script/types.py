from .errors import *

operation_lookup_table = {
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide",
    "%": "modulus",
    "&&": "logical_and",
    "||": "logical_or",
}


class MCSObject:
    def get_value(self):
        raise MCSInterpreterError('Failed getting value of unknown Object')

    def class_name(self) -> str:
        return self.__class__.__name__[2:]

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

    def operation_error(self, other, operation):
        return MCSTypeError(
            f"Unsupported operand types for {operation if operation != '//' else '/' !r}: "
            f"{self.class_name() !r} and {other.class_name() !r}"
        )


class MCSIterable:
    def get_key(self, key):
        return self[]


class MCSNumber(MCSObject):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise MCSInterpreterError(f"Expected type 'int', got {value.__class__.__name__ !r}")

        self.value = value

    def get_value(self) -> int:
        return self.value

    # ----------------- Miscellaneous ----------------- :
    def __repr__(self) -> str:
        return f'MCSNumber({self.value !r})'


class MCSNull(MCSObject):
    def get_value(self) -> None:
        return

    # ----------------- Operations ----------------- :
    def _binary_operation(self, other, operator: str):
        if isinstance(other, (MCSNumber, MCSNull)):
            return MCSNumber(eval(f"0 {operator} other.get_value()"))

        raise self.operation_error(other, f'"{operator}"')

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


class MCSList(MCSObject):
    pass


class MCSFunction:
    pass
