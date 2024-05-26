def config_boolean_check(value: str, setting: str) -> bool:
    py_value = value.lower().capitalize()

    if py_value not in ('True', 'False'):
        print(f"Error: incorrect value {value !r} for setting {setting !r}")
        exit()

    return eval(py_value)  # safe to eval here


config_value_wrapper = {
    "pack_format": lambda x: x,  # don't check (it's just text anyway, it can be whatever)
    "debug_comments": lambda x: config_boolean_check(x, "debug_comments")
}