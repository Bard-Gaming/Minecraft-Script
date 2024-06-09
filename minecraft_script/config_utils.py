import json
import os.path
from .common import COMMON_CONFIG, module_folder


def config_boolean_check(value: str, setting: str) -> bool:
    py_value = value.lower().capitalize()

    if py_value not in ('True', 'False'):
        print(f"Error: incorrect value {value !r} for setting {setting !r}")
        exit(-1)

    return eval(py_value)  # safe to eval here


def config_path_check(value: str, setting: str) -> str:
    path = value.replace("\\", "/")
    if not os.path.exists(path):
        print(f"Error: path {value !r} doesn't exist for setting {setting !r}")
        exit(-1)

    return path


def update_config(setting: str, value: str) -> None:
    value_wrapper_fnc = config_value_wrapper[setting]
    py_value = value_wrapper_fnc(value)
    COMMON_CONFIG[setting] = py_value

    json_file_content: str = (
        json.dumps(COMMON_CONFIG)
        .replace("{", "{\n\t")
        .replace("}", "\n}")
        .replace(", ", ",\n\t")
    )

    with open(f"{module_folder}/config.json", "wt", encoding="utf-8") as file:
        file.write(json_file_content)


config_value_wrapper = {
    "pack_format": lambda x: x,  # don't check (it's just text anyway, it can be whatever)
    "debug_comments": lambda x: config_boolean_check(x, "debug_comments"),
    "verbose": lambda x: config_boolean_check(x, "verbose"),
    "default_output_path": lambda x: config_path_check(x, "default_output_path"),
}
