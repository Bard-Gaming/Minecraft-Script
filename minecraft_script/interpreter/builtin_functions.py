from .types import MCSFunction, MCSNull, MCSString, MCSNumber, MCSList
from ..errors import MCSValueError, MCSTypeError


def custom_log(args, context):
    from .interpreter import RuntimeResult
    if len(args) > 5:
        raise MCSTypeError(f"Function <builtin-log> takes up to 5 arguments, got {len(args)}")

    print(*[arg.print_value() for arg in args])
    return RuntimeResult(return_value=MCSNull())


def custom_concatenate(args, context):
    from .interpreter import RuntimeResult
    if len(args) > 2:
        raise MCSTypeError(f"Function <builtin-concatenate> takes 2 arguments, got {len(args)}")

    string_1 = args[0]
    string_2 = args[1]

    if not isinstance(string_1, MCSString) or not isinstance(string_2, MCSString):
        raise MCSTypeError(
            f"Function <builtin-concatenate> takes 2 strings as arguments, got {string_1.class_name() !r} and {string_2.class_name() !r}")

    return RuntimeResult(return_value=MCSString(string_1.get_value() + string_2.get_value()))


def custom_command(args, context):
    from .interpreter import RuntimeResult

    # Check if argument count is correct
    if len(args) != 1:
        raise MCSTypeError(f"Function <builtin-command> takes 1 argument, got {len(args)}")

    command: MCSString = args[0]

    # Type check command
    if not isinstance(command, MCSString):
        raise MCSTypeError(f"Command must be string, got {command.class_name() !r}")

    return RuntimeResult(return_value=MCSNull())


def custom_get_block(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 3:
        raise MCSTypeError(f"Function <builtin-get_block> takes 3 arguments, got {len(args)}")

    x, y, z = args[:3]

    # Type check x, y, and z
    if not all(isinstance(coord, (MCSString, MCSNumber)) for coord in (x, y, z)):
        raise MCSTypeError(
            f"X, Y and Z coordinates must be numbers or strings, got {x.class_name() !r}, {y.class_name() !r}, {z.class_name() !r}")

    return RuntimeResult(return_value=MCSString("<Minecraft block ID>"))


def custom_set_block(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 4:
        raise MCSTypeError(f"Function <builtin-set_block> takes 4 arguments, got {len(args)}")

    block = args[0]
    x, y, z = args[1:4]

    if not isinstance(block, MCSString):
        raise MCSTypeError(f"Block must be a string, got {block.class_name() !r}")
    elif not all(isinstance(coord, (MCSString, MCSNumber)) for coord in (x, y, z)):
        raise MCSTypeError(
            f"X, Y and Z coordinates must be numbers or strings, got {x.class_name() !r}, {y.class_name() !r}, {z.class_name() !r}")

    return RuntimeResult(return_value=MCSNull())


def custom_give_item(args, context):
    from .interpreter import RuntimeResult

    if not (1 <= len(args) <= 3):
        raise MCSTypeError(f"Function <builtin-give_item> takes between 1 and 3 arguments, got {len(args)}")

    item: MCSString = args[0]
    components: MCSString = args[1] if len(args) > 1 else None
    count: MCSNumber = args[2] if len(args) > 2 else None

    # Type check:
    if not isinstance(item, MCSString):
        raise MCSTypeError(f"Item must be a string, got {item.class_name() !r}")
    if components is not None and not isinstance(components, MCSString):
        raise MCSTypeError(f"Components must be a string, got {components.class_name() !r}")
    if count is not None and not isinstance(count, MCSNumber):
        raise MCSTypeError(f"Item count must be a number, got {count.class_name() !r}")

    # Check for quotes in components:
    if "'" in components.get_value() or '"' in components.get_value():
        raise MCSValueError("Components String contains quotes (this leads to errors if compiled)")

    return RuntimeResult(return_value=MCSNull())


def custom_give_clickable_item(args, context):
    from .interpreter import RuntimeResult

    if not (1 <= len(args) <= 3):
        raise MCSTypeError(f"Function <builtin-give_clickable_item> takes between 1 and 3 arguments, got {len(args)}")

    click_function: MCSFunction = args[0]
    item_name: MCSString = args[1] if len(args) > 1 else None
    custom_model_data: MCSString | MCSNumber = args[2] if len(args) > 2 else None

    # Type check:
    if not isinstance(click_function, MCSFunction):
        raise MCSTypeError(f"Click function must be a Function, got {click_function.class_name() !r}")
    if item_name is not None and not isinstance(item_name, MCSString):
        raise MCSTypeError(f"Item name must be a String, got {item_name.class_name() !r}")
    if custom_model_data is not None and not isinstance(custom_model_data, (MCSString, MCSNumber)):
        raise MCSTypeError(f"Item count must be a String or Number, got {custom_model_data.class_name() !r}")

    if "'" in item_name.get_value() or '"' in item_name.get_value():
        raise MCSValueError("Item name contains quotes (this leads to errors if compiled)")

    return RuntimeResult(return_value=MCSNull())


def custom_raycast_block(args, context):
    from .interpreter import RuntimeResult

    if not 2 <= len(args) <= 3:
        raise MCSTypeError(f"Function <builtin-raycast_block> takes between 2 and 3 arguments, got {len(args)}")

    end_function: MCSFunction = args[0]
    travel_distance: MCSNumber = args[1]
    ray_function: MCSFunction = args[2] if len(args) > 2 else None

    # Type check:
    if not isinstance(end_function, MCSFunction):
        raise MCSTypeError(f"End function must be a Function, got {end_function.class_name() !r}")
    if not isinstance(travel_distance, MCSNumber):
        raise MCSTypeError(f"Travel distance must be a Number, got {travel_distance.class_name() !r}")
    if ray_function is not None and not isinstance(ray_function, MCSFunction):
        raise MCSTypeError(f"Ray function must be a Function, got {ray_function.class_name() !r}")

    # Check if travel distance is positive:
    if travel_distance.get_value() < 1:  # 0 leads to weird behavior and is useless anyway
        raise MCSValueError(f"Travel distance must be over 0 (otherwise this leads to errors if compiled)")

    return RuntimeResult(return_value=MCSNull())


def custom_raycast_entity(args, context):
    from .interpreter import RuntimeResult

    if not 2 <= len(args) <= 3:
        raise MCSTypeError(f"Function <builtin-raycast_entity> takes between 2 and 3 arguments, got {len(args)}")

    end_function: MCSFunction = args[0]
    travel_distance: MCSNumber = args[1]
    ray_function: MCSFunction = args[2] if len(args) > 2 else None

    # Type check:
    if not isinstance(end_function, MCSFunction):
        raise MCSTypeError(f"End function must be a Function, got {end_function.class_name() !r}")
    if not isinstance(travel_distance, MCSNumber):
        raise MCSTypeError(f"Travel distance must be a Number, got {travel_distance.class_name() !r}")
    if ray_function is not None and not isinstance(ray_function, MCSFunction):
        raise MCSTypeError(f"Ray function must be a Function, got {ray_function.class_name() !r}")

    # Check if travel distance is positive:
    if travel_distance.get_value() < 1:  # 0 leads to weird behavior and is useless anyway
        raise MCSValueError(f"Travel distance must be over 0, got {travel_distance.get_value()}")

    return RuntimeResult(return_value=MCSNull())


def custom_append(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 2:
        raise MCSTypeError(f"Function <builtin-append> takes 2 arguments, got {len(args)}")

    append_list: MCSList = args[0]
    value = args[1]

    if not isinstance(append_list, MCSList):
        raise MCSTypeError(f"Append list must be a List, got {append_list.class_name() !r}")
    if isinstance(value, (MCSFunction, MCSList)):
        raise MCSTypeError(f"Value can't be of type Function or List, got {value.class_name() !r}")

    return RuntimeResult(return_value=MCSNull())


def custom_range(args, context):
    from .interpreter import RuntimeResult

    if len(args) != 1:
        raise MCSTypeError(f"Function <builtin-range> takes 1 argument, got {len(args)}")

    bounding_value = args[0]

    if not isinstance(bounding_value, MCSNumber):
        raise MCSTypeError(f"Bounding value must be a Number, got {bounding_value.class_name()}")

    if bounding_value.get_value() < 1:
        raise MCSValueError(f"Bounding value has to be over 0, got {bounding_value.get_value()}")

    return RuntimeResult(return_value=MCSList(list(
        map(lambda num: MCSNumber(num), range(bounding_value.get_value()))
    )))


builtin_functions = [
    custom_log, custom_concatenate, custom_command,
    custom_get_block, custom_set_block,
    custom_give_item, custom_give_clickable_item,
    custom_raycast_block, custom_raycast_entity,
    custom_append, custom_range,
]
