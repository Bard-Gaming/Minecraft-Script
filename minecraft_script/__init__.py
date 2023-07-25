from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, Context, SymbolTable

version = "0.1.403"


def run(text: str):
    global_symbol_table = SymbolTable()

    run_lexer = Lexer(text)
    tokens = run_lexer.tokenize()

    run_parser = Parser(tokens)
    ast = run_parser.parse()

    run_interpreter = Interpreter()
    context = Context('main', global_symbol_table)
    print(run_interpreter.visit(ast, context))


def run_file(filepath: str):  # currently line-by-line
    with open(filepath, 'rt') as file:
        file_content = file.read()

    global_symbol_table = SymbolTable()

    for line in filter(lambda x: not (x.strip(' ') == ''), file_content.split('\n')):
        run_lexer = Lexer(line)
        tokens = run_lexer.tokenize()

        run_parser = Parser(tokens)
        ast = run_parser.parse()

        run_interpreter = Interpreter()
        context = Context('main', global_symbol_table)
        print(run_interpreter.visit(ast, context))


def run_shell():
    global_symbol_table = SymbolTable()

    while True:
        text = input('> ')
        while text.strip(' ') == '':
            text = input('> ')

        run_lexer = Lexer(text)
        tokens = run_lexer.tokenize()

        run_parser = Parser(tokens)
        ast = run_parser.parse()

        run_interpreter = Interpreter()
        context = Context('main', global_symbol_table)
        print(run_interpreter.visit(ast, context))
