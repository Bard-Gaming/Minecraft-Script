class Token:
    def __init__(self, type: str, value: any = None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({repr(self.type)}, {repr(self.value)})'