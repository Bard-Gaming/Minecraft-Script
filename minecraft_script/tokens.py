class Token:
    def __init__(self, value: any, tt_type: str):
        self.value = value
        self.tt_type = tt_type

    def __repr__(self):
        return f'Token({self.value !r}, {self.tt_type !r})'