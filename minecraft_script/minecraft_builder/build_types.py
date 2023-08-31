from secrets import token_hex


class BuildType:
    __value = None
    datapack_id = None
    storage_location = None

    def get_value(self):
        return self.__value

    @staticmethod
    def generate_storage_location():
        return token_hex(16)

    def set_temporary(self):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.storage_location}'


class BuildVariable(BuildType):
    def __init__(self, name, value, datapack_id):
        self.name = name
        self.value = value
        self.datapack_id = datapack_id

    def get_value(self):
        return self.value.get_value()

    def call_command(self, arguments):
        return self.value.call_command(arguments)

    def set_temporary(self):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.value.storage_location}'


class BuildString(BuildType):
    def __init__(self, value, datapack_id):
        self.__value = value
        self.datapack_id = datapack_id
        self.storage_location = f'string.{self.generate_storage_location()}'

    def get_value(self):
        return self.__value

    def get_full_storage_location(self):
        return f'mcs_{self.datapack_id} {self.storage_location}'


class BuildNumber(BuildType):
    def __init__(self, value, datapack_id):
        self.__value = value
        self.datapack_id = datapack_id
        self.storage_location = f'number.{self.generate_storage_location()}'

    def get_value(self):
        return self.__value

    def get_full_storage_location(self):
        return f'mcs_{self.datapack_id} {self.storage_location}'


class BuildList(BuildType):
    def __init__(self, value, datapack_id):
        self.__value = value
        self.datapack_id = datapack_id
        self.storage_location = f'list.{self.generate_storage_location()}'

    def list_commands(self) -> iter:
        for index, element in enumerate(self.__value):
            yield element.set_temporary()
            yield f'data modify storage mcs_{self.datapack_id} {self.storage_location}.{index} set from storage mcs_{self.datapack_id} temporary'

    def set_temporary(self):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.storage_location}'


class BuildFunction(BuildType):
    def __init__(self, *, name: str = None, parameter_names, datapack_id, body_node, context, interpreter):
        self.name = name if name is not None else f'function_{self.generate_storage_location()}'
        self.datapack_id = datapack_id
        self.path = f'{self.datapack_id}:{self.name}'

        self.parameter_names = parameter_names if parameter_names else None
        self.body_node = body_node
        self.context = context
        self.interpreter = interpreter

        self.setup()

    def setup(self):
        from .build_interpreter import BuildContext
        local_context = BuildContext(self.name, self.name)
        self.interpreter.visit(self.body_node, local_context)

    def call_command(self, arguments: BuildList):
        if arguments.get_value() is not None:
            arguments.set_temporary()
            return f'function {self.datapack_id}:{self.name} with storage mcs_{self.datapack_id} temporary'
        else:
            return f'function {self.datapack_id}:{self.name}'
