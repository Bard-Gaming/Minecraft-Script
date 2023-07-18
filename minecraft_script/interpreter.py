from ply import lex, yacc
from .tokens import *
from .parser import *

lexer = lex.lex()
parser = yacc.yacc()

if __name__ == "__main__":
    inp = '5 + 5\n+1'
    print(parser.parse(inp))
