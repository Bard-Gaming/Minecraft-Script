from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, Context, SymbolTable

version = "0.1.401"


def run_string(text: str):
    global_symbol_table = SymbolTable()

    lexer = Lexer(text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    context = Context('main', global_symbol_table)
    print(interpreter.visit(ast, context))
