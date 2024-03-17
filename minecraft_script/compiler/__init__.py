from .. import get_ast_from_file
from .compiler import Compiler


def build_datapack_from_file(filename: str, datapack_name: str, verbose: bool = False):
    ast = None
    try:
        ast = get_ast_from_file(filename)
    except FileNotFoundError:
        print(f'Error: File "{filename}" not found.')
        return

    Compiler(ast, datapack_name).build(verbose)
