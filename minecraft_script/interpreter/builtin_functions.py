from .types import MCSFunction, MCSNull, MCSString, MCSNumber, MCSList
from ..errors import MCSValueError, MCSTypeError


def custom_log(args, context):
    from .interpreter import RuntimeResult

    print(*[arg.print_value() for arg in args])
    return RuntimeResult(return_value=MCSNull())


def custom_get_block(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 3:
        raise MCSValueError(f"Function <builtin-get_block> takes 3 arguments, got {len(args)}")

    return RuntimeResult(return_value=MCSString("<Minecraft block ID>"))


def custom_command(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 1:
        raise MCSValueError(f"Function <builtin-command> takes 1 argument, got {len(args)}")

    return RuntimeResult(return_value=MCSNull())


def custom_repr(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 1:
        raise MCSValueError(f"Function <builtin-repr> takes 1 argument, got {len(args)}")
    value = args[0]

    return RuntimeResult(return_value=MCSString(value.repr_value()))


def custom_range(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 1:
        raise MCSValueError(f"Function <builtin-range> takes 1 argument, got {len(args)}")
    range_length = args[0]

    if not isinstance(range_length, MCSNumber):
        raise MCSTypeError(f"{range_length.class_name() !r} object cannot be interpreted as an integer")

    return RuntimeResult(return_value=MCSList(list(
        map(lambda num: MCSNumber(num), range(range_length.get_value()))
    )))


builtin_functions = [
    custom_log, custom_get_block, custom_command,
    custom_repr, custom_range,
]
