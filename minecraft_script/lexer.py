from json import loads
from .tokens import Token
from .errors import MCSIllegalCharError, MCSSyntaxError
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
        self.current_line = 1

        self.advance()

    def advance(self) -> None:
        self.current_index += 1
        self.current_char = self.text[self.current_index] if self.current_index < len(self.text) else None

        if self.current_char == '\n':
            self.current_line += 1

    def make_name(self):
        name_str = ''
        # allow numbers after first character
        while (self.current_char and
               (self.current_char in LANG_TOKENS['TT_NAME'] or self.current_char in LANG_TOKENS['TT_NAME__extend'])):
            name_str += self.current_char
            self.advance()

        return name_str

    def make_string(self):
        quote_char = self.current_char
        full_text = ''
        self.advance()

        while self.current_char not in (quote_char, '\n', None):
            full_text += self.current_char
            self.advance()

        if self.current_char in ('\n', None):
            MCSSyntaxError(f'Unmatched string {quote_char}{full_text} at line {self.current_line}')
            exit()

        self.advance()  # skip quote at the end
        return full_text

    def make_number(self):
        number_str = ''

        while self.current_char and self.current_char in LANG_TOKENS['TT_NUMBER']:
            number_str += self.current_char
            self.advance()

        return int(number_str)

    def make_equals(self):
        token_value = self.current_char
        self.advance()
        if f"{token_value}{self.current_char}" == LANG_TOKENS['TT_FUNCTION_ARROW']:
            token_value = f"{token_value}{self.current_char}"
            self.advance()
            return token_value

        elif f"{token_value}{self.current_char}" == LANG_TOKENS['TT_COMPARE_EQUALS']:
            token_value = f"{token_value}{self.current_char}"
            self.advance()
            return token_value

        else:
            return token_value

    def make_comparator(self):
        comparator_char = self.current_char
        if comparator_char == LANG_TOKENS['TT_COMPARE_LESSER']:
            self.advance()

            if self.current_char == LANG_TOKENS['TT_EQUALS']:
                comparator_char += self.current_char
                self.advance()
                return comparator_char, 'TT_COMPARE_LESSER_EQUALS'

            return comparator_char, 'TT_COMPARE_LESSER'

        elif comparator_char == LANG_TOKENS['TT_COMPARE_GREATER']:
            self.advance()

            if self.current_char == LANG_TOKENS['TT_EQUALS']:
                comparator_char += self.current_char
                self.advance()
                return comparator_char, 'TT_COMPARE_GREATER_EQUALS'

            return comparator_char, 'TT_COMPARE_GREATER'


    def make_logical_and(self):
        token_value = self.current_char
        self.advance()
        if self.current_char == LANG_TOKENS['TT_LOGICAL_AND'][1]:
            token_value += self.current_char
            self.advance()
            return token_value
        else:
            return token_value

    def make_logical_or(self):
        token_value = self.current_char
        self.advance()
        if self.current_char == LANG_TOKENS['TT_LOGICAL_OR'][1]:
            token_value += self.current_char
            self.advance()
            return token_value
        else:
            return token_value

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

            elif self.current_char == LANG_TOKENS['TT_LEFT_BRACKET']:
                tokens.append(Token(self.current_char, 'TT_LEFT_BRACKET'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_RIGHT_BRACKET']:
                tokens.append(Token(self.current_char, 'TT_RIGHT_BRACKET'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_COMMA']:
                tokens.append(Token(self.current_char, 'TT_COMMA'))
                self.advance()

            elif self.current_char in LANG_TOKENS['TT_NEWLINE']:
                tokens.append(Token(self.current_char, 'TT_NEWLINE'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_LEFT_BRACE']:
                tokens.append(Token(self.current_char, 'TT_LEFT_BRACE'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_RIGHT_BRACE']:
                tokens.append(Token(self.current_char, 'TT_RIGHT_BRACE'))
                self.advance()

            elif self.current_char in LANG_TOKENS['TT_QUOTE']:
                text = self.make_string()
                tokens.append(Token(text, 'TT_TEXT_STRING'))
                # already advanced in .make_string()

            elif self.current_char == LANG_TOKENS['TT_EQUALS']:
                token_value = self.make_equals()

                if token_value == LANG_TOKENS['TT_FUNCTION_ARROW']:
                    tokens.append(Token(token_value, 'TT_FUNCTION_ARROW'))

                elif token_value == LANG_TOKENS['TT_COMPARE_EQUALS']:
                    tokens.append(Token(token_value, 'TT_COMPARE_EQUALS'))

                else:
                    tokens.append(Token(token_value, 'TT_EQUALS'))

                # don't self.advance() since that is already done in self.make_equals()

            elif self.current_char in (LANG_TOKENS['TT_COMPARE_LESSER'], LANG_TOKENS['TT_COMPARE_GREATER']):
                value, type = self.make_comparator()
                tokens.append(Token(value, type))

            elif self.current_char == LANG_TOKENS['TT_LOGICAL_NOT']:
                tokens.append(Token(self.current_char, 'TT_LOGICAL_NOT'))
                self.advance()

            elif self.current_char == LANG_TOKENS['TT_LOGICAL_AND'][0]:
                token_value = self.make_logical_and()
                tokens.append(Token(token_value, 'TT_LOGICAL_AND'))

            elif self.current_char == LANG_TOKENS['TT_LOGICAL_OR'][0]:
                token_value = self.make_logical_or()
                tokens.append(Token(token_value, 'TT_LOGICAL_OR'))

            elif self.current_char in LANG_TOKENS['TT_NUMBER']:
                number = self.make_number()
                tokens.append(Token(number, 'TT_NUMBER'))

            elif self.current_char in LANG_TOKENS['TT_BINARY_OPERATOR']:
                current_char = self.current_char
                self.advance()

                if f'{current_char}{self.current_char}' == LANG_TOKENS['TT_COMMENT']:
                    while self.current_char != '\n':
                        self.advance()

                else:
                    tokens.append(Token(current_char, 'TT_BINARY_OPERATOR'))

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
