from .types import MCSFunction, MCSNull, MCSString, MCSNumber
from .errors import MCSValueError


def log(args, context) -> MCSNull:
    print(*[arg.print_value() for arg in args])
    return MCSNull()


builtin_function_log = MCSFunction('log', None, None)
builtin_function_log.call = log
builtin_function_log.print_value = lambda: '<builtin-log>'


def repr(args, context) -> MCSString:
    if len(args) > 1:
        raise MCSValueError(f"Function <builtin-repr> takes 1 argument, got {len(args)}")
    value = args[0]

    return MCSString(value.repr_value())


builtin_function_repr = MCSFunction('repr', None, None)
builtin_function_repr.call = repr
builtin_function_repr.print_value = lambda: '<builtin-repr>'


builtin_functions = [
    builtin_function_log,
    builtin_function_repr
]
