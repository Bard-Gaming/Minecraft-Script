from json import JSONDecoder
from minecraft_script.tokens import Token
from minecraft_script.errors import IllegalCharException, NameErrorException
from minecraft_script.parser import Parser

module_folder = '/'.join(__file__.split('\\')[:-1])

with open(f'{module_folder}/data/LANG_TOKENS.json', 'rt') as file:
    LANG_TOKENS = JSONDecoder().decode(file.read())

with open(f'{module_folder}/data/LANG_KEYWORDS.json', 'rt') as file:
    LANG_KEYWORDS = JSONDecoder().decode(file.read())


DIGITS = 'data/0123456789'


class Lexer:
    tokens_ignored = [' ', '\t']

    def __init__(self, text: str):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self) -> (list, int):
        tokens = []

        while self.current_char is not None:
            if self.current_char in self.tokens_ignored:
                pass

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            elif self.current_char in LANG_TOKENS:
                tokens.append(Token(LANG_TOKENS[self.current_char]))

            elif self.current_char not in LANG_TOKENS:
                return [], IllegalCharException(f"'{self.current_char}'")

            self.advance()

        return tokens, 0

    def make_number(self):
        number: str = ''
        while self.current_char is not None and self.current_char in DIGITS:
            number += self.current_char
            self.advance()

        return Token(LANG_TOKENS['int'], number)


def main():
    lexer = Lexer('5 + 5')
    tokens, exit_code = lexer.make_tokens()
    print(tokens)

    parser = Parser(tokens)
    abstract_syntax_tree = parser.parse()
    # print(abstract_syntax_tree)


if __name__ == '__main__':
    main()