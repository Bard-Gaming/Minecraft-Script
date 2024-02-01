from .types import MCSFunction, MCSNull, MCSString, MCSNumber


def log(args, context) -> MCSNull:
    print(*[arg.print_value() for arg in args])
    return MCSNull()


builtin_function_log = MCSFunction('log', None, None)
builtin_function_log.call = log
builtin_function_log.print_value = lambda: 'builtin-log'

builtin_functions = [
    builtin_function_log
]
