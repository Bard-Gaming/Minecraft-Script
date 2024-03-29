class Token:
    def __init__(self, value: any, tt_type: str, position: tuple[int, int] = None, variant: str = None):
        self.value = value
        self.tt_type = tt_type
        self.position = position
        self.variant = variant

    def get_position(self):
        return self.position

    def matches(self, token_type: str, variant: str = None) -> bool:
        return self.tt_type == token_type and (self.variant == variant if variant is not None else True)

    def matches_variants(self, token_type: str, variants: iter) -> bool:
        return self.tt_type == token_type and any(self.variant == variant for variant in variants)

    def __repr__(self):
        return (
            f'Token({self.value !r}, {self.tt_type !r}'
            f'{f", {self.position !r}" if self.position is not None else ""}'
            f'{f", {self.variant !r}" if self.variant is not None else ""})'
        )