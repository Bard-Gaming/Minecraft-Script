from .types import MCSFunction, MCSNull, MCSString, MCSNumber, MCSList
from .errors import MCSValueError


def custom_log(args, context) -> MCSNull:
    print(*[arg.print_value() for arg in args])
    return MCSNull()


builtin_function_log = MCSFunction('log', None, None)
builtin_function_log.call = custom_log
builtin_function_log.print_value = lambda: '<builtin-log>'


def custom_repr(args, context) -> MCSString:
    if len(args) > 1:
        raise MCSValueError(f"Function <builtin-repr> takes 1 argument, got {len(args)}")
    value = args[0]

    return MCSString(value.repr_value())


builtin_function_repr = MCSFunction('repr', None, None)
builtin_function_repr.call = custom_repr
builtin_function_repr.print_value = lambda: '<builtin-repr>'


def custom_range(args, context) -> MCSList:
    if len(args) > 1:
        raise MCSValueError(f"Function <builtin-range> takes 1 argument, got {len(args)}")
    range_length = args[0]

    return MCSList(list(
        map(lambda num: MCSNumber(num), range(range_length.get_value()))
    ))


builtin_function_range = MCSFunction('range', None, None)
builtin_function_range.call = custom_range
builtin_function_range.print_value = lambda: '<builtin-range>'

builtin_functions = [
    builtin_function_log,
    builtin_function_repr,
    builtin_function_range,
]
