import ply.lex as lex
import ply.yacc as yacc
from .tokens import *
from .parser import *

lexer = lex.lex()
parser = yacc.yacc()


def parse_line(line: str):
    yacc.parse(line)
