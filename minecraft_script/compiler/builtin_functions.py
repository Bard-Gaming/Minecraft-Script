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
    from .compile_interpreter import CompileContext
    x, y, z, *_ = args

    local_context = CompileContext(f":cb_{generate_uuid()}", context)

    mcs_obj = MCSString(context)

    fnc_commands = (
        "summon armor_stand ~ ~5 ~ {Invisible:1b, NoBasePlate:1b, NoGravity:1b, Tags:[\"mcs_get_block_temp\"]}",
        "$loot replace entity @e[type=armor_stand, limit=1, sort=nearest, tag=mcs_get_block_temp] armor.head mine $(x) $(y) $(z) netherite_pickaxe{Enchantments:[{id:\"minecraft:silk_touch\", lvl:1s}]}",  # NOQA
        f"data modify storage {mcs_obj.get_storage()} {mcs_obj.get_nbt()} set from entity @e[type=minecraft:armor_stand, limit=1] ArmorItems[3].id",  # NOQA
        "kill @e[type=armor_stand, tag=mcs_get_block_temp]"
    )
    interpreter.add_commands(local_context.mcfunction_name, fnc_commands)

    setup_commands = (
        f"data modify storage mcs_{context.uuid} current.x set from storage {x.get_storage()} {x.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.y set from storage {y.get_storage()} {y.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.z set from storage {z.get_storage()} {z.get_nbt()}",
        f"function {interpreter.datapack_id}:code_blocks/{local_context.mcfunction_name[1:]} with storage mcs_{context.uuid} current",
    )

    return setup_commands, mcs_obj


builtin_functions = (
    log, command,
    get_block,
)
