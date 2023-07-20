from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

version = "0.1.401"


def interpret_text(text: str):
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    print(interpreter.visit(ast))
