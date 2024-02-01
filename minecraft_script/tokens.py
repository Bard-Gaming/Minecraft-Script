class Token:
    def __init__(self, value: any, tt_type: str, position: tuple[int, int] = None, variant: str = None):
        self.value = value
        self.tt_type = tt_type
        self.position = position
        self.variant = variant

    def get_position(self):
        return self.position

    def __repr__(self):
        return f'Token({self.value !r}, {self.tt_type !r}, {self.position !r})'