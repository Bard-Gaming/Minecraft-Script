class MCSSyntaxError(SyntaxError):
    def __init__(self, details: str):
        super().__init__(details)


class MCSIllegalCharacterError(Exception):
    def __init__(self, value: str, position: tuple[int, int]):
        super().__init__(f"Illegal Character: {value} (line {position[1]}, {position[0]})")


class MCSTypeError(TypeError):
    pass


class MCSZeroDivisionError(ZeroDivisionError):
    pass


class MCSValueError(ValueError):
    pass


class MCSIndexError(IndexError):
    pass


class MCSNameError(NameError):
    pass
