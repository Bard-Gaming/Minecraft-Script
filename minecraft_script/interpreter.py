import ply.lex as lex
import ply.yacc as yacc
from .tokens import *
from .parser import *

lexer = lex.lex()
parser = yacc.yacc()


def parse_line(line: str) -> None:
    yacc.parse(line)

def manage_multiline(multiline_text: str) -> list[str]:
    multiline_text.replace('\n', ' ')  # turn newlines to spaces
    return multiline_text.split(';')

def parse_text(multiline_text: str) -> None:
    for line in manage_multiline(multiline_text):
        parse_line(line)