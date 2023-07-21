from json import loads
from .tokens import Token
from .errors import MCSIllegalCharError
from .common import module_folder

with open(f'{module_folder}/grammar/LANG_TOKENS.json') as file:
    LANG_TOKENS = loads(file.read())

with open(f'{module_folder}/grammar/LANG_KEYWORDS.json') as file:
    LANG_KEYWORDS = loads(file.read())


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.current_index = -1
        self.current_char = None
        self.current_line = 0

        self.advance()

    def advance(self) -> None:
        self.current_index += 1
        self.current_char = self.text[self.current_index] if self.current_index < len(self.text) else None

        if self.current_char == '\n':
            self.current_line += 1
            self.advance()

    def make_name(self):
        name_str = ''
        # allow numbers after first character
        while self.current_char and (self.current_char in LANG_TOKENS['TT_NAME'] or self.current_char in LANG_TOKENS['TT_NUMBER']):
            name_str += self.current_char
            self.advance()

        return name_str

    def make_number(self):
        number_str = ''

        while self.current_char and self.current_char in LANG_TOKENS['TT_NUMBER']:
            number_str += self.current_char
            self.advance()

        return int(number_str)

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.current_char is not None:
            if self.current_char in LANG_TOKENS['TT_IGNORE']:
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_LEFT_PARENTHESIS']:
                tokens.append(Token(self.current_char, 'TT_LEFT_PARENTHESIS'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_RIGHT_PARENTHESIS']:
                tokens.append(Token(self.current_char, 'TT_RIGHT_PARENTHESIS'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_EQUALS']:
                tokens.append(Token(self.current_char, 'TT_EQUALS'))
                self.advance()

            elif self.current_char in LANG_TOKENS['TT_NUMBER']:
                number = self.make_number()
                tokens.append(Token(number, 'TT_NUMBER'))

            elif self.current_char in LANG_TOKENS['TT_BINARY_OPERATOR']:
                tokens.append(Token(self.current_char, 'TT_BINARY_OPERATOR'))
                self.advance()

            elif self.current_char in LANG_TOKENS['TT_NAME']:
                name = self.make_name()
                if LANG_KEYWORDS.get(name, False):
                    tokens.append(Token(name, LANG_KEYWORDS[name]))
                else:
                    tokens.append(Token(name, "TT_NAME"))

            else:
                MCSIllegalCharError(self.current_char, self.current_line)
                exit()

        return tokens
