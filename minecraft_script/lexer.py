from json import loads
from .tokens import Token
from .common import module_folder

with open(f'{module_folder}/grammar/LANG_TOKENS.json') as file:
    LANG_TOKENS = loads(file.read())

with open(f'{module_folder}/grammar/LANG_KEYWORDS.json') as file:
    LANG_KEYWORDS = loads(file.read())

token_lookup_table = {}
for tt_type, tt_char_list in LANG_TOKENS.items():
    if tt_type[0] == '_':  # ignored token types
        continue

    char_count = tt_char_list[0]
    char_list = tt_char_list[1:]
    for i in range(0, len(char_list), char_count):
        token_lookup_table["".join(char_list[i:i + char_count])] = tt_type


class Lexer:
    def __init__(self, code_input: str):
        self.code_input = code_input
        self.current_index = -1
        self.current_char = None
        self.position_x = 0
        self.position_y = 1

        self.advance()  # initialize current_char and current_index to correct values

    def advance(self):
        if self.current_index >= len(self.code_input):
            self.current_char = None
            return

        self.current_index += 1
        self.current_char = self.code_input[self.current_index]

        # Keep track of position
        if self.current_char == '\n':
            self.position_x = 1
            self.position_y += 1
        else:
            self.position_x += 1

    def default_tokenize_treatment(self):
        pass

    def tokenize(self) -> tuple[Token, ...]:
        token_list = []

        while self.current_char is not None:
            pass

        return tuple(token_list)


