def log(interpreter, args) -> tuple[str]:
    value = args[0]

    return (
        f'function {interpreter.datapack_id}:builtins/log' ' {'
        f'"storage":"{value.get_storage()}", "nbt":"{value.get_nbt()}"' '}',
    )


builtin_functions = (
    log,
)
