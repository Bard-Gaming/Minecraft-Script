from text_additions import text_error, text_underline


class MCSError:
    def __init__(self, details: str, error_type: str = "Unknown Error", line_number: int = None):
        self.details = details
        self.error_type = error_type
        self.line_number = line_number

        print(self)

    def __str__(self):
        if self.line_number:
            return text_error(f'{self.error_type}: {text_underline(f"{self.details !r}")} at line {self.line_number}')
        else:
            return text_error(f'{self.error_type}: {text_underline(f"{self.details !r}")}')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.error_type !r}, {self.details !r}, {self.line_number !r})'


class MCSSyntaxError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Syntax Error", line_number)


class MCSIllegalCharError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Illegal Character", line_number)


class MCSTypeError(MCSError):
    def __init__(self, details: str, line_number: int = None):
        super().__init__(details, "Type Error", line_number)


if __name__ == '__main__':
    a = MCSTypeError('const')
    print(a)
