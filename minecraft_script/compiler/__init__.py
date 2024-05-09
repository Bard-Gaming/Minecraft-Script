from .. import parse_code
from .compiler import Compiler


def build_datapack(code: str, datapack_name: str, verbose: bool = False) -> None:
    ast = parse_code(code)
    Compiler(ast, datapack_name).build(verbose)
