from .lexer.lexer import Lexer
from .parser.parser import Parser
from .interpreter.interpreter import Interpreter, InterpreterContext, SymbolTable


def debug_code(code_input: str, *, print_variables: bool = False) -> None:
    lexer = Lexer(code_input)
    parser = Parser(lexer.tokenize())

    interpreter = Interpreter()
    context = InterpreterContext(top_level=True)
    interpreter.visit(parser.parse(), context)

    if print_variables:
        print(context.symbol_table.symbols)

    print("\n\nCode ended with no errors.")


def run_shell():
    context = InterpreterContext(top_level=True)

    while True:
        text = input('> ')
        while text.strip(' ') == '':
            text = input('> ')

        run_lexer = Lexer(text)
        tokens = run_lexer.tokenize()

        run_parser = Parser(tokens)
        ast = run_parser.parse()

        run_interpreter = Interpreter()
        print(run_interpreter.visit(ast, context))


def parse_code(code: str):
    run_lexer = Lexer(code + "\n")
    tokens = run_lexer.tokenize()

    run_parser = Parser(tokens)
    ast = run_parser.parse()

    return ast
