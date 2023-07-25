from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, Context, SymbolTable

version = "0.1.401"


def run(text: str):
    global_symbol_table = SymbolTable()

    run_lexer = Lexer(text)
    tokens = run_lexer.tokenize()

    run_parser = Parser(tokens)
    ast = run_parser.parse()

    run_interpreter = Interpreter()
    context = Context('main', global_symbol_table)
    print(run_interpreter.visit(ast, context))
