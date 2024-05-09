from .compile_types import *
from ..common import COMMON_CONFIG

function_output = tuple[tuple[str, ...], mcs_type]  # [commands, return value]


def log(interpreter, args, context) -> function_output:
    max_length = 5

    values = list(map(lambda arg: (arg.get_storage(), arg.get_nbt()), args))
    values.extend(("", "none") for _ in range(max_length - len(args)))

    storage = " {" + ", ".join(f'"s{i}": "{values[i][0]}", "n{i}": "{values[i][1]}"' for i in range(max_length)) + '}'

    commands = (
        f'function {interpreter.datapack_id}:builtins/log' + storage,
    )

    return commands, MCSNull(context)


def command(interpreter, args, context) -> function_output:
    value = args[0]

    commands = (
        f"data modify storage {value.get_storage()} current set value " "{}",  # set current to object to store values
        f"data modify storage {value.get_storage()} current.cmd set from storage {value.get_storage()} {value.get_nbt()}",
        f"function {interpreter.datapack_id}:builtins/command with storage {value.get_storage()} current",
    )

    return commands, MCSNull(context)


def get_block(interpreter, args, context) -> function_output:
    from .compile_interpreter import CompileContext
    x, y, z, *_ = args

    local_context = CompileContext(parent=context)

    mcs_obj = MCSString(context)

    fnc_commands = (
        f"data modify storage {mcs_obj.get_storage()} {mcs_obj.get_nbt()} set value \"\"",
        "summon armor_stand ~ ~5 ~ {Invisible:1b, NoBasePlate:1b, NoGravity:1b, Tags:[\"mcs_get_block_temp\"]}",
        "$loot replace entity @e[type=armor_stand, limit=1, sort=nearest, tag=mcs_get_block_temp] armor.head mine $(x) $(y) $(z) netherite_pickaxe[minecraft:enchantments={levels:{\"minecraft:silk_touch\":1}}]",
        # NOQA
        f"data modify storage {mcs_obj.get_storage()} {mcs_obj.get_nbt()} set from entity @e[type=minecraft:armor_stand, tag=mcs_get_block_temp, limit=1, sort=nearest] ArmorItems[3].id",
        # NOQA
        "kill @e[type=armor_stand, tag=mcs_get_block_temp]"
    )
    interpreter.add_commands(local_context.mcfunction_name, fnc_commands)

    setup_commands = (
        f"data modify storage mcs_{context.uuid} current set value " "{}",  # set current to an object to store values
        f"data modify storage mcs_{context.uuid} current.x set from storage {x.get_storage()} {x.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.y set from storage {y.get_storage()} {y.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.z set from storage {z.get_storage()} {z.get_nbt()}",
        f"function {interpreter.datapack_id}:{local_context.mcfunction_name} with storage mcs_{context.uuid} current",
    )

    return setup_commands, mcs_obj


def set_block(interpreter, args, context) -> function_output:
    x, y, z, block_name, *_ = args

    commands = (
        f"data modify storage mcs_{context.uuid} current set value " "{}",  # set current to an object to store values
        f"data modify storage mcs_{context.uuid} current.x set from storage {x.get_storage()} {x.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.y set from storage {y.get_storage()} {y.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.z set from storage {z.get_storage()} {z.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.block set from storage {block_name.get_storage()} {block_name.get_nbt()}",
        f"function {interpreter.datapack_id}:builtins/set_block with storage mcs_{context.uuid} current",
    )

    return commands, MCSNull(context)


def raycast_block(interpreter, args, context) -> function_output:
    from .compile_interpreter import CompileContext
    local_context = CompileContext(parent=context)
    raycast_id = generate_uuid()
    raycast_function: MCSFunction = args[0]  # get function to play on block (at raycast end)
    raycast_range: mcs_type = args[1]  # get raycast range
    raycast_loop_function: MCSFunction | None = args[2] if len(args) > 2 else None  # get function to play on each loop

    fnc_commands = (
        # Check if not colliding with block
        f"execute unless block ~ ~ ~ #{interpreter.datapack_id}:no_collision run scoreboard players operation .raycast_iter_{raycast_id} mcs_math = .raycast_end_{raycast_id} mcs_math",

        # Call function if at end of raycast
        f"execute if score .raycast_iter_{raycast_id} mcs_math >= .raycast_end_{raycast_id} mcs_math run function {interpreter.datapack_id}:user_functions/{raycast_function.name}",

        # Call loop function if it exists
        f"function {interpreter.datapack_id}:user_functions/{raycast_loop_function.name}" if raycast_loop_function is not None else "# No loop function",

        # Start next loop
        f"scoreboard players add .raycast_iter_{raycast_id} mcs_math 1",
        f"execute if score .raycast_iter_{raycast_id} mcs_math < .raycast_end_{raycast_id} mcs_math positioned ^ ^ ^0.5 run function {interpreter.datapack_id}:{local_context.mcfunction_name}",
    )
    interpreter.add_commands(local_context.mcfunction_name, fnc_commands)

    setup_commands = (
        # Initialize values
        raycast_range.set_to_current_cmd(context),
        f"execute store result score .raycast_end_{raycast_id} mcs_math run data get storage mcs_{context.uuid} current 2",
        f"scoreboard players set .raycast_iter_{raycast_id} mcs_math 0",

        # Call raycast
        f"execute anchored eyes positioned ^ ^ ^.00001 run function {interpreter.datapack_id}:{local_context.mcfunction_name}",

        # Reset used scoreboards
        f"scoreboard players reset .raycast_iter_{raycast_id} mcs_math",
        f"scoreboard players reset .raycast_end_{raycast_id} mcs_math",
    )

    return setup_commands, MCSNull(context)


def raycast_entity(interpreter, args, context) -> function_output:
    from .compile_interpreter import CompileContext
    local_context = CompileContext(parent=context)
    raycast_id = generate_uuid()
    raycast_function: MCSFunction = args[0]
    raycast_range: mcs_type = args[1]  # get raycast range
    raycast_loop_function: MCSFunction | None = args[2] if len(args) > 2 else None  # get function to play on each loop

    fnc_commands = (
        # Check if entity is found
        f"execute positioned ~-0.1 ~-0.1 ~-0.1 as @e[tag=!raycast_{raycast_id}, dx=0] positioned ~-0.7 ~-0.7 ~-0.7 if entity @s[dx=0] run scoreboard players operation .raycast_iter_{raycast_id} mcs_math = .raycast_end_{raycast_id} mcs_math",

        # Call function if at end of raycast
        f"execute if score .raycast_iter_{raycast_id} mcs_math >= .raycast_end_{raycast_id} mcs_math positioned ~-0.1 ~-0.1 ~-0.1 as @e[tag=!raycast_{raycast_id}, dx=0] positioned ~-0.7 ~-0.7 ~-0.7 at @s run function {interpreter.datapack_id}:user_functions/{raycast_function.name}",

        # Call loop function if it exists
        f"function {interpreter.datapack_id}:user_functions/{raycast_loop_function.name}" if raycast_loop_function is not None else "# No loop function",

        # Start next loop
        f"scoreboard players add .raycast_iter_{raycast_id} mcs_math 1",
        f"execute if block ~ ~ ~ #{interpreter.datapack_id}:no_collision if score .raycast_iter_{raycast_id} mcs_math < .raycast_end_{raycast_id} mcs_math positioned ^ ^ ^0.5 run function {interpreter.datapack_id}:{local_context.mcfunction_name}",
    )
    interpreter.add_commands(local_context.mcfunction_name, fnc_commands)

    setup_commands = (
        # Initialize values
        raycast_range.set_to_current_cmd(context),
        f"execute store result score .raycast_end_{raycast_id} mcs_math run data get storage mcs_{context.uuid} current 2",
        f"scoreboard players set .raycast_iter_{raycast_id} mcs_math 0",
        f"tag @s add raycast_{raycast_id}",

        # Call raycast
        f"execute anchored eyes positioned ^ ^ ^.00001 run function {interpreter.datapack_id}:{local_context.mcfunction_name}",

        # Reset used scoreboards
        f"tag @s remove raycast_{raycast_id}",
        f"scoreboard players reset .raycast_iter_{raycast_id} mcs_math",
        f"scoreboard players reset .raycast_end_{raycast_id} mcs_math",
    )

    return setup_commands, MCSNull(context)


def give_item(interpreter, args, context) -> function_output:
    item: MCSString = args[0]  # item name
    components: MCSString = args[1] if len(args) > 1 else None  # item nbt (optional)
    count: MCSString = args[2] if len(args) > 2 else None

    commands = (
        # ------ Setup ------
        f"data modify storage mcs_{context.uuid} current set value " "{}",

        # --- Item ---
        f"data modify storage mcs_{context.uuid} current.item set from storage {item.get_storage()} {item.get_nbt()}",

        # --- Components ---
        f"data modify storage mcs_{context.uuid} current.components set from storage {components.get_storage()} {components.get_nbt()}"
        if components is not None else
        f"data modify storage mcs_{context.uuid} current.components set value ''",  # set value to default

        # --- Count ---
        f"data modify storage mcs_{context.uuid} current.count set from storage {count.get_storage()} {count.get_nbt()}"
        if count is not None else
        f"data modify storage mcs_{context.uuid} current.count set value 1",  # set value to default

        # ------ Call Function ------
        f"function {interpreter.datapack_id}:builtins/give_item with storage mcs_{context.uuid} current",
    )

    return commands, MCSNull(context)


def concatenate(interpreter, args, context) -> function_output:
    from .compile_interpreter import CompileContext
    string_1: MCSString = args[0]
    string_2: MCSString = args[1]

    string_concat_context = CompileContext(parent=context)

    output_string = MCSString(context)

    setup_commands = (
        f"data modify storage mcs_{context.uuid} current set value " "{}",
        f"data modify storage mcs_{context.uuid} current.string_1 set from storage {string_1.get_storage()} {string_1.get_nbt()}",
        f"data modify storage mcs_{context.uuid} current.string_2 set from storage {string_2.get_storage()} {string_2.get_nbt()}",
        f"function {interpreter.datapack_id}:{string_concat_context.mcfunction_name} with storage mcs_{context.uuid} current",
    )

    interpreter.add_command(
        string_concat_context.mcfunction_name,
        f"$data modify storage {output_string.get_storage()} {output_string.get_nbt()} set value \"$(string_1)$(string_2)\""
    )

    return setup_commands, output_string


def append(interpreter, args, context) -> function_output:
    from .compile_interpreter import CompileContext
    list_arg: MCSList = args[0]
    value: mcs_type = args[1]

    set_key_context = CompileContext(parent=context)

    commands = (
        # Add element to list
        f"data modify storage mcs_{context.uuid} current set value " "{}",
        f"data modify storage mcs_{context.uuid} current.index set from storage {list_arg.get_storage()} {list_arg.get_nbt()}.length",
        f"function {interpreter.datapack_id}:{set_key_context.mcfunction_name} with storage mcs_{context.uuid} current",

        # Increment list length
        f"execute store result score .temp mcs_math run data get storage {list_arg.get_storage()} {list_arg.get_nbt()}.length",
        f"scoreboard players set .1 mcs_math 1",
        f"scoreboard players operation .temp mcs_math += .1 mcs_math",
        f"execute store result storage {list_arg.get_storage()} {list_arg.get_nbt()}.length int 1 run scoreboard players get .temp mcs_math",
        f"scoreboard players reset .1 mcs_math",
    )

    interpreter.add_command(
        set_key_context.mcfunction_name,
        f"$data modify storage {list_arg.get_storage()} {list_arg.get_nbt()}.$(index) set from storage {value.get_storage()} {value.get_nbt()}"
    )

    return commands, MCSNull(context)


def mcs_range(interpreter, args, context) -> function_output:  # TODO: Implement range fnc
    pass
    # from .compile_interpreter import CompileContext
    # range_bound: MCSNumber = args[0]


builtin_functions = (
    log, command, concatenate,
    get_block, set_block, give_item,
    raycast_block, raycast_entity,
    append, mcs_range
)
