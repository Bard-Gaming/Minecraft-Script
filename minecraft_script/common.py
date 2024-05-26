import json
from uuid import uuid4 as get_uuid
from .config_utils import config_value_wrapper as _config_value_wrapper

version = "0.2.0"
module_folder = "/".join(__file__.split('\\')[:-1])

# load Minecraft-Script configuration
with open(f"{module_folder}/config.json", "rt", encoding="utf-8") as file:
    COMMON_CONFIG: dict = json.loads(file.read())


def generate_uuid() -> str:
    return str(get_uuid())


def update_config(setting: str, value: str) -> None:
    value_wrapper_fnc = _config_value_wrapper[setting]
    py_value = value_wrapper_fnc(value)
    COMMON_CONFIG[setting] = py_value

    with open(f"{module_folder}/config.json", "wt", encoding="utf-8") as file:
        file.write(json.dumps(COMMON_CONFIG))

    print(f"Updated setting {setting !r} to value {py_value !r}")
