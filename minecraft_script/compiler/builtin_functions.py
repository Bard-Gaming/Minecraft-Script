def log(args, context) -> str:
    return 'tellraw @a {' f'"storage":"{context.uuid}", "nbt":"{args[0].uuid}"' '}'


builtin_functions = (
    log,
)
