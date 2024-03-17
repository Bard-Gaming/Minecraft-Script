from uuid import uuid4 as get_uuid

version = "0.2.0"
module_folder = "/".join(__file__.split('\\')[:-1])


def generate_uuid():
    return str(get_uuid())
