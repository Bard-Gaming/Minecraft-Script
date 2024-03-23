def log(interpreter, args) -> tuple[str, ...]:
    max_length = 5

    values = list(map(lambda arg: (arg.get_storage(), arg.get_nbt()), args))
    values.extend(("", "none") for _ in range(max_length - len(args)))

    storage = " {" + ", ".join(f'"s{i}": "{values[i][0]}", "n{i}": "{values[i][1]}"' for i in range(max_length)) + '}'

    return f'function {interpreter.datapack_id}:builtins/log' + storage,


def command(interpreter, args) -> tuple[str, ...]:
    value = args[0]

    return (
        f"data modify storage {value.get_storage()} current set value " "{\"cmd\": 0}",
        f"data modify storage {value.get_storage()} current.cmd set from storage {value.get_storage()} {value.get_nbt()}",  # NOQA
        f"function {interpreter.datapack_id}:builtins/command with storage {value.get_storage()} current",
    )


builtin_functions = (
    log, command,
)
