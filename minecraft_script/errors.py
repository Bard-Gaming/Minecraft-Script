# --------------- User Errors --------------- :

class MCSSyntaxError(SyntaxError):
    def __init__(self, details: str):
        super().__init__(details)


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


class MCSAttributeError(AttributeError):
    pass


# --------------- Language Errors --------------- :
class MCSIllegalCharacterError(Exception):
    def __init__(self, value: str, position: tuple[int, int]):
        super().__init__(f"Illegal Character: {value} (line {position[1]}, {position[0]})")


class MCSParserError(Exception):
    def __init__(self, details):
        super().__init__(details)


class MCSInterpreterError(NotImplementedError):
    def __init__(self, details):
        super().__init__(details)
