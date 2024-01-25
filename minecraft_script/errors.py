from .text_additions import text_error, text_underline


class MCSError:
    def __init__(self, details: str, error_type: str = "Unknown Error", line_number: int = None):
        self.details = details
        self.error_type = error_type
        self.line_number = line_number

        print(self)

    def __str__(self):
        if self.line_number:
            return text_error(f'{self.error_type}: {self.details} at line {self.line_number}')
        else:
            return text_error(f'{self.error_type}: {self.details}')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.error_type !r}, {self.details !r}, {self.line_number !r})'


class MCSSyntaxError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Syntax Error", line_number)


class MCSValueError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Value Error", line_number)


class MCSIllegalCharacterError(Exception):
    def __init__(self, value: str, position: tuple[int, int]):
        super().__init__(f"Illegal Character: {value} (line {position[1]}, {position[0]})")


class MCSTypeError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Type Error", line_number)


class MCSZeroDivisionError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Zero Division Error", line_number)


class MCSNameError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        details = f'Name {text_underline(f"{details !r}")} is not defined'
        super().__init__(details, "Name Error", line_number)


class MCSIndexError(MCSError):
    def __init__(self, details: str, *, type = None, line_number: int = None):
        if type:
            details = f'{type} index {text_underline(f"{details}")} out of range'
        else:
            details = f'Index {text_underline(f"{details}")} out of range'
        super().__init__(details, "Index Error", line_number)


if __name__ == '__main__':
    a = MCSTypeError('const')
    print(a)
