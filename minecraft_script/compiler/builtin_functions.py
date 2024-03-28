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
        f"data modify storage {mcs_obj.get_storage()} {mcs_obj.get_nbt()} set value \"\"",
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


def raycast_block(interpreter, args, context) -> tuple[tuple[str, ...], mcs_type]:
    from .compile_interpreter import CompileContext
    local_context = CompileContext(f":cb_{generate_uuid()}", context)
    raycast_id = generate_uuid()
    raycast_function: MCSFunction = args[0]  # get function to play on block (at raycast end)
    raycast_range: mcs_type = args[1]  # get raycast range
    raycast_loop_function: MCSFunction | None = args[2] if len(args) > 2 else None  # get function to play on each loop

    fnc_commands = (
        # Check if not colliding with block
        f"execute unless block ~ ~ ~ minecraft:air run scoreboard players operation .raycast_iter_{raycast_id} mcs_math = .raycast_end_{raycast_id} mcs_math",  # NOQA

        # Call function if at end of raycast
        f"execute if score .raycast_iter_{raycast_id} mcs_math >= .raycast_end_{raycast_id} mcs_math run function {interpreter.datapack_id}:user_functions/{raycast_function.name}",  # NOQA

        # Call loop function if it exists
        f"function {interpreter.datapack_id}:user_functions/{raycast_loop_function.name}" if raycast_loop_function is not None else "",  # NOQA

        # Start next loop
        f"scoreboard players add .raycast_iter_{raycast_id} mcs_math 1",
        f"execute if score .raycast_iter_{raycast_id} mcs_math < .raycast_end_{raycast_id} mcs_math positioned ^ ^ ^0.5 run function {interpreter.datapack_id}:code_blocks/{local_context.mcfunction_name[1:]}",  # NOQA
    )
    interpreter.add_commands(local_context.mcfunction_name, fnc_commands)

    setup_commands = (
        # Initialize values
        raycast_range.set_to_current_cmd(context),
        f"execute store result score .raycast_end_{raycast_id} mcs_math run data get storage mcs_{context.uuid} current 2",  # NOQA
        f"scoreboard players set .raycast_iter_{raycast_id} mcs_math 0",

        # Call raycast
        f"execute anchored eyes positioned ^ ^ ^.00001 run function {interpreter.datapack_id}:code_blocks/{local_context.mcfunction_name[1:]}",

        # Reset used scoreboards
        f"scoreboard players reset .raycast_iter_{raycast_id} mcs_math",
        f"scoreboard players reset .raycast_end_{raycast_id} mcs_math",
    )

    return setup_commands, MCSNull(context)


def raycast_entity(interpreter, args, context) -> tuple[tuple[str, ...], mcs_type]:
    from .compile_interpreter import CompileContext
    local_context = CompileContext(f":cb_{generate_uuid()}", context)
    raycast_id = generate_uuid()
    raycast_function: MCSFunction = args[0]
    raycast_range: mcs_type = args[1]  # get raycast range
    raycast_loop_function: MCSFunction | None = args[2] if len(args) > 2 else None  # get function to play on each loop

    fnc_commands = (
        # Check if entity is found
        f"execute positioned ~-0.1 ~-0.1 ~-0.1 as @e[tag=!raycast_{raycast_id}, dx=0] positioned ~-0.7 ~-0.7 ~-0.7 if entity @s[dx=0] run scoreboard players operation .raycast_iter_{raycast_id} mcs_math = .raycast_end_{raycast_id} mcs_math",  # NOQA

        # Call function if at end of raycast
        f"execute if score .raycast_iter_{raycast_id} mcs_math >= .raycast_end_{raycast_id} mcs_math positioned ~-0.1 ~-0.1 ~-0.1 as @e[tag=!raycast_{raycast_id}, dx=0] positioned ~-0.7 ~-0.7 ~-0.7 at @s run function {interpreter.datapack_id}:user_functions/{raycast_function.name}",  # NOQA

        # Call loop function if it exists
        f"function {interpreter.datapack_id}:user_functions/{raycast_loop_function.name}" if raycast_loop_function is not None else "", # NOQA

        # Start next loop
        f"scoreboard players add .raycast_iter_{raycast_id} mcs_math 1",
        f"execute if block ~ ~ ~ minecraft:air if score .raycast_iter_{raycast_id} mcs_math < .raycast_end_{raycast_id} mcs_math positioned ^ ^ ^0.5 run function {interpreter.datapack_id}:code_blocks/{local_context.mcfunction_name[1:]}",  # NOQA
    )
    interpreter.add_commands(local_context.mcfunction_name, fnc_commands)

    setup_commands = (
        # Initialize values
        raycast_range.set_to_current_cmd(context),
        f"execute store result score .raycast_end_{raycast_id} mcs_math run data get storage mcs_{context.uuid} current 2",  # NOQA
        f"scoreboard players set .raycast_iter_{raycast_id} mcs_math 0",
        f"tag @s add raycast_{raycast_id}",

        # Call raycast
        f"execute anchored eyes positioned ^ ^ ^.00001 run function {interpreter.datapack_id}:code_blocks/{local_context.mcfunction_name[1:]}",

        # Reset used scoreboards
        f"tag @s remove raycast_{raycast_id}",
        f"scoreboard players reset .raycast_iter_{raycast_id} mcs_math",
        f"scoreboard players reset .raycast_end_{raycast_id} mcs_math",
    )

    return setup_commands, MCSNull(context)


builtin_functions = (
    log, command, get_block,
    raycast_block, raycast_entity
)
