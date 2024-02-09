from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter, InterpreterContext, SymbolTable


def run_code(code_input: str, *, print_variables: bool = False) -> None:
    lexer = Lexer(code_input)
    parser = Parser(lexer.tokenize())

    interpreter = Interpreter()
    context = InterpreterContext(top_level=True)
    interpreter.visit(parser.parse(), context)

    if print_variables:
        print(context.symbol_table.symbols)


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
        print(run_interpreter.visit(ast, context)[0])


def get_ast_from_file(filepath: str):
    with open(filepath, 'rt', encoding='utf-8') as file:
        file_content = file.read()

    run_lexer = Lexer(file_content + "\n")
    tokens = run_lexer.tokenize()

    run_parser = Parser(tokens)
    ast = run_parser.parse()

    return ast
