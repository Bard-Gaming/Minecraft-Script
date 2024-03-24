from .compile_types import *


def log(interpreter, args, context) -> tuple[tuple[str, ...], mcs_type]:
    max_length = 5

    values = list(map(lambda arg: (arg.get_storage(), arg.get_nbt()), args))
    values.extend(("", "none") for _ in range(max_length - len(args)))

    storage = " {" + ", ".join(f'"s{i}": "{values[i][0]}", "n{i}": "{values[i][1]}"' for i in range(max_length)) + '}'

    commands = (
        f'function {interpreter.datapack_id}:builtins/log' + storage,
    )

    return commands, MCSNull(context)


def command(interpreter, args, context) -> tuple[tuple[str, ...], mcs_type]:
    value = args[0]

    commands = (
        f"data modify storage {value.get_storage()} current set value " "{\"cmd\": 0}",
        f"data modify storage {value.get_storage()} current.cmd set from storage {value.get_storage()} {value.get_nbt()}",
        f"function {interpreter.datapack_id}:builtins/command with storage {value.get_storage()} current",
    )

    return commands, MCSNull(context)


def get_block(interpreter, args, context) -> tuple[tuple[str, ...], mcs_type]:
    x, y, z, *_ = args

    value = MCSString(context)

    # TODO: fix this method (generate it dynamically instead of having a fixed fnc?)

    commands = (
        f"data modify storage mcs_{context.uuid} current.storage set value \"mcs_{context.uuid}\"",
        f"execute store result storage mcs_{context.uuid} current.nbt int 1 run random value 10000000..99999999",
        f"data modify storage mcs_{context.uuid} current.x set from storage {x.get_storage()} {x.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.y set from storage {y.get_storage()} {y.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.z set from storage {z.get_storage()} {z.get_nbt()}",
        f"function {interpreter.datapack_id}:builtins/get_block with storage mcs_{context.uuid} current",
        # Current is now block id (str), so save its data in string value:
        f"data modify storage {value.get_storage()} {value.get_nbt()} set from storage mcs_{context.uuid} current",
    )

    return commands, value


builtin_functions = (
    log, command,
    get_block,
)
