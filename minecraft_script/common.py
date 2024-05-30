import json
from uuid import uuid4 as get_uuid

version = "0.2.0"
module_folder = "/".join(__file__.split('\\')[:-1])

# load Minecraft-Script configuration
with open(f"{module_folder}/config.json", "rt", encoding="utf-8") as file:
    COMMON_CONFIG: dict = json.loads(file.read())


def generate_uuid() -> str:
    return str(get_uuid())
