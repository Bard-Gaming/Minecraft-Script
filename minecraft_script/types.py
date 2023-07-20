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
