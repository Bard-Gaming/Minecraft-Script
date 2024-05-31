from json import loads
from .tokens import Token
from ..errors import MCSIllegalCharacterError, MCSSyntaxError
from ..common import module_folder

with open(f'{module_folder}/lexer/grammar/LANG_TOKENS.json') as file:
    LANG_TOKENS = loads(file.read())

with open(f'{module_folder}/lexer/grammar/LANG_KEYWORDS.json') as file:
    LANG_KEYWORDS = loads(file.read())

token_lookup_table = {}
for token_type, char_list in LANG_TOKENS.items():
    if token_type[0] == '_':
        continue  # ignore "private" token types

    for char_obj in char_list:
        char = char_obj.get("char")
        token_lookup_table[char] = token_type

token_type_chars = {
    token_type: [char["char"] for char in chars] for (token_type, chars) in LANG_TOKENS.items() if token_type[0] != '_'
}


class Lexer:
    def __init__(self, code_input: str):
        self.code_input = code_input
        self.current_index = -1
        self.current_char = None
        self.position_x = 0
        self.position_y = 1
        self.__token_list = []

        self.advance()  # initialize current_char and current_index to correct values

    def advance(self):
        if self.current_index >= len(self.code_input) - 1:  # if index is equal to len - 1, don't advance
            self.current_char = None
            return

        self.current_index += 1
        self.current_char = self.code_input[self.current_index]

        # Keep track of position
        if self.current_char == '\n':
            self.position_x = 0
            self.position_y += 1
        else:
            self.position_x += 1

    @property
    def next_char(self) -> str | None:
        return self.code_input[self.current_index + 1] if self.current_index < len(self.code_input) - 2 else None

    # ---------------- Special cases ---------------- :
    def make_number(self) -> Token:
        number = self.current_char
        position = (self.position_x, self.position_y)
        self.advance()

        while self.current_char in token_type_chars['TT_NUMBER']:
            number += self.current_char
            self.advance()

        return Token(number, 'TT_NUMBER', position)

    def make_name(self) -> Token:
        name = self.current_char
        position = (self.position_x, self.position_y)
        self.advance()

        while self.current_char in token_type_chars['TT_NAME'] + LANG_TOKENS['_TT_NAME_extend']:
            name += self.current_char
            self.advance()

        reserved_name = LANG_KEYWORDS.get(name)
        if reserved_name is not None:  # if a name is reserved, update
            return Token(name, reserved_name, position)

        return Token(name, 'TT_NAME', position)  # generic variable name

    def make_string(self) -> Token:
        string_quote = self.current_char  # store quote type to know when to stop string
        string = ""
        position = (self.position_x, self.position_y)  # store position since token gets starting pos of string
        self.advance()

        while self.current_char is not None and self.current_char != string_quote:
            string += self.current_char
            self.advance()

        if self.current_char is None:
            raise MCSSyntaxError(f'Unmatched string starting at line {position[1]}, {position[0]}')
        self.advance()  # skip closing string quote

        return Token(string, 'TT_STRING', position)

    def make_entity_selector(self) -> Token:
        selector = self.current_char  # should be "@" char
        self.advance()

        position = self.position_x, self.position_y
        depth = 0

        while self.current_char is not None and not (depth == 0 and self.current_char == ' '):
            if self.current_char == '[':
                depth += 1
            elif self.current_char == ']':
                depth -= 1

            if depth < 0:
                raise MCSSyntaxError(f'Malformed entity selector at line {position[1]}, {position[0]}')

            selector += self.current_char
            self.advance()

        if self.current_char is None:
            raise MCSSyntaxError(f'Malformed entity selector at line {position[1]}, {position[0]}')
        self.advance()  # skip space (is going to get skipped anyway)

        return Token(selector, 'TT_SELECTOR', position)

    # ---------------- Main implementation (turning code into tokens) ---------------- :
    def default_tokenize_treatment(self) -> None:
        position = (self.position_x, self.position_y)

        advance_needed = True if self.next_char is not None else False  # If token is composed, advance is needed
        token_value = self.current_char + self.next_char if self.next_char is not None else self.current_char
        token_type = token_lookup_table.get(token_value)  # try with composed token first (priority to composed tokens)

        if token_type is None:  # check if composed token exists
            advance_needed = False  # only 1 char, no advance needed
            token_value = self.current_char
            token_type = token_lookup_table.get(token_value)

            if token_type is None:  # no composed token and no simple token
                raise MCSIllegalCharacterError(token_value, position)

        if advance_needed:
            self.advance()

        # Check for variants (to add information to token):
        variant = None
        for char_dict in LANG_TOKENS[token_type]:
            if char_dict.get("char") == token_value:
                variant = char_dict.get("variant")  # if no variant, default to None
                break  # if you get a match, don't need to continue searching

        token = Token(token_value, token_type, position, variant)
        self.__token_list.append(token)
        self.advance()

    def tokenize(self) -> tuple[Token, ...]:
        if self.__token_list:
            return tuple(self.__token_list)

        while self.current_char is not None:
            if self.current_char in token_type_chars['TT_IGNORE']:
                self.advance()

            elif self.current_char in token_type_chars['TT_NUMBER']:
                self.__token_list.append(self.make_number())

            elif self.current_char in token_type_chars['TT_NAME']:
                self.__token_list.append(self.make_name())

            elif self.current_char in token_type_chars['TT_QUOTE']:
                self.__token_list.append(self.make_string())

            elif self.current_char in token_type_chars['TT_AT']:
                self.__token_list.append(self.make_entity_selector())

            elif self.next_char is not None and self.current_char + self.next_char in token_type_chars['TT_COMMENT']:
                self.advance()  # skip second "/" (self.next_char)
                while self.current_char is not None and self.current_char != "\n":
                    self.advance()  # skip everything until newline (it's a comment)

            else:
                self.default_tokenize_treatment()

        return tuple(self.__token_list)
