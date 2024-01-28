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
    def operation_error(self, other, operation):
        return MCSTypeError(
            f"Unsupported operand types for {operation}: {self.__class__.__name__ !r} and {other.__class__.__name__ !r}")


class MCSNumber(MCSObject):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f'Expected integer, got {value !r}')

        self.value = value

    def get_value(self) -> int:
        return self.value

    # ---------------- Operations ---------------- :
    def add(self, other):
        if isinstance(other, (MCSNumber,)):
            return MCSNumber(self.value + other.get_value())

        raise self.operation_error(other, '"+"')

    def subtract(self, other):
        if isinstance(other, (MCSNumber,)):
            return MCSNumber(self.value - other.get_value())

        raise self.operation_error(other, '"-"')

    def multiply(self, other):
        if isinstance(other, (MCSNumber,)):
            return MCSNumber(self.value * other.get_value())

        raise self.operation_error(other, '"*"')

    def __repr__(self) -> str:
        return f'MCSNumber({self.value !r})'


class MCSNull:
    def __repr__(self) -> str:
        return f'MCSNull()'


class MCSString(MCSObject):
    pass


class MCSList(MCSObject):
    pass


class MCSFunction:
    pass
