from uuid import uuid4 as get_uuid

version = "0.2.0"
module_folder = "/".join(__file__.split('\\')[:-1])


def generate_uuid():
    return str(get_uuid())


# Minecraft-Script Configuration. If a type is specified, DO NOT DEVIATE OR ERRORS WILL OCCUR
COMMON_CONFIG = {
    "pack_format": "41",  # Specifies pack_format version for datapack (str)
}
