from secrets import token_hex


class BuildType:
    value = None
    datapack_id = None
    storage_location = None

    def get_value(self):
        return self.value

    @staticmethod
    def generate_storage_location():
        return token_hex(16)

    def set_temporary(self):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.storage_location}'

    def __str__(self):
        return f'{self.get_value}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value !r}, {self.datapack_id !r}, {self.storage_location !r})'


class BuildIterable(BuildType):
    def get_index_cmd(self, index: int):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.storage_location}.{index}'

    def get_index(self, index):
        return self.value[index]


class BuildVariable(BuildType):
    def __init__(self, name, value, datapack_id):
        self.name = name
        self.value = value
        self.datapack_id = datapack_id

    def get_value(self):
        return self.value.get_value()

    def call_command(self, arguments):
        return self.value.call_command(arguments)

    def get_index_cmd(self, index: int):
        return self.value.get_index_cmd(index)

    def get_index(self, index: int):
        return self.value.get_index(index)

    def set_temporary(self):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.value.storage_location}'

    def __str__(self):
        return str(self.value)


class BuildString(BuildIterable, BuildType):
    def __init__(self, value, datapack_id):
        self.value = value
        self.datapack_id = datapack_id
        self.storage_location = f'string.{self.generate_storage_location()}'

    def get_value(self):
        return self.value

    def get_index_cmd(self, index: int):
        return f'data modify storage mcs_{self.datapack_id} temporary set string storage {self.get_full_storage_location()} {index} {index + 1}'

    def get_index(self, index):
        return BuildString(self.value[index], self.datapack_id)

    def get_full_storage_location(self):
        return f'mcs_{self.datapack_id} {self.storage_location}'


class BuildNumber(BuildType):
    def __init__(self, value, datapack_id):
        self.value = value
        self.datapack_id = datapack_id
        self.storage_location = f'number.{self.generate_storage_location()}'

    def get_value(self):
        return self.value

    def get_full_storage_location(self):
        return f'mcs_{self.datapack_id} {self.storage_location}'


class BuildList(BuildIterable, BuildType):
    def __init__(self, value, datapack_id):
        self.value = value
        self.datapack_id = datapack_id
        self.storage_location = f'list.{self.generate_storage_location()}'

    def list_commands(self) -> iter:
        for index, element in enumerate(self.value):
            yield element.set_temporary()
            yield f'data modify storage mcs_{self.datapack_id} {self.storage_location}.{index} set from storage mcs_{self.datapack_id} temporary'

    def set_temporary(self):
        return f'data modify storage mcs_{self.datapack_id} temporary set from storage mcs_{self.datapack_id} {self.storage_location}'

    def __str__(self):
        return ', '.join([str(element) for element in self.get_value()])


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
        local_context = BuildContext(self.name, self.name, self.context)
        self.interpreter.visit(self.body_node, local_context)

    def call_command(self, arguments: BuildList):
        if arguments.get_value() is not None:
            arguments.set_temporary()
            return f'function {self.datapack_id}:{self.name} with storage mcs_{self.datapack_id} temporary'
        else:
            return f'function {self.datapack_id}:{self.name}'


class BuildBuiltinFunction(BuildType):
    functions = ['log']

    def __init__(self, name):
        self.name = name

    def call_command(self, arguments: BuildList):
        method = getattr(self, f'call_{self.name}')
        return method(arguments)

    @staticmethod
    def call_log(arguments: BuildList):
        if arguments.get_value() is None:
            return
        else:
            tellraw_string = '[""'
            previous = False
            for element in arguments.get_value():
                if previous:
                    tellraw_string += ', {"text":", "}'
                tellraw_string += ', {"text":' f'"{element.get_value()}"' '}'  # TODO: fix weird bug with BuildList
                previous = True

            tellraw_string += ']'
            print(tellraw_string)
            return f'tellraw @a {tellraw_string}'
