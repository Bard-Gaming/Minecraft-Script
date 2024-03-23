def log(interpreter, args) -> tuple[str]:
    max_length = 5

    values = list(map(lambda arg: (arg.get_storage(), arg.get_nbt()), args))
    values.extend(("", "none") for _ in range(max_length - len(args)))
    
    storage = " {" + ", ".join(f'"s{i}": "{values[i][0]}", "n{i}": "{values[i][1]}"' for i in range(max_length)) + '}'

    return (f'function {interpreter.datapack_id}:builtins/log' + storage,)


builtin_functions = (
    log,
)
