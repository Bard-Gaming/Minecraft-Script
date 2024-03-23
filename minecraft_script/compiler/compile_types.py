from ..common import generate_uuid


class MCSObject:
    def __init__(self, context_id, storage_compartment: str):
        self.context_id = context_id
        self.uuid = generate_uuid()
        self.storage_compartment = storage_compartment

    def get_nbt(self) -> str:
        return f"{self.storage_compartment}.{self.uuid}"

    def get_storage(self) -> str:
        return f"mcs_{self.context_id}"

    def save_to_storage_cmd(self, value: any) -> str:
        return f"data modify storage {self.get_storage()} {self.get_nbt()} set value {value}"

    def set_to_current_cmd(self, output_context) -> str:
        return f"data modify storage mcs_{output_context.uuid} current set from storage {self.get_storage()} {self.get_nbt()}"  # NOQA


class MCSVariable:
    def __init__(self, name: str, context_id):
        self.name = name
        self.context_id = context_id

    def get_nbt(self) -> str:
        return f"variable.{self.name}"

    def get_storage(self) -> str:
        return f"mcs_{self.context_id}"

    def set_to_current_cmd(self, output_context) -> str:
        return f"data modify storage mcs_{output_context.uuid} current set from storage {self.get_storage()} {self.get_nbt()}"  # NOQA

    def __repr__(self) -> str:
        return f"MCSVariable({self.name !r}, {self.context_id !r})"


class MCSNull(MCSObject):
    def __init__(self, context_id):
        super().__init__(context_id, "")

    @staticmethod
    def save_to_storage_cmd(output_context):  # NOQA
        return ""

    def set_to_current_cmd(self, output_context) -> str:  # NOQA
        return f"data modify storage mcs_{self.context_id} current set value 0b"

    def __repr__(self) -> str:
        return "MCSNull()"


class MCSNumber(MCSObject):
    def __init__(self, context_id):
        super().__init__(context_id, "number")

    def __repr__(self) -> str:
        return f"MCSNumber({self.uuid !r})"


class MCSString(MCSObject):
    def __init__(self, context_id):
        super().__init__(context_id, "string")

    def __repr__(self) -> str:
        return f"MCSString({self.uuid !r})"


class MCSFunction:
    def __init__(self, name: str, body, parameter_names: list[str, ...], context):
        from .compile_interpreter import CompileContext

        self.name = name
        self.body = body
        self.parameter_names = parameter_names
        self.local_context = CompileContext(self.name, context)

    def generate_function(self, interpreter) -> None:
        for name in self.parameter_names:
            self.local_context.declare(name, MCSVariable(name, self.local_context.uuid))

        interpreter.visit(self.body, self.local_context)  # generate all commands inside body

    def call(self, interpreter, arguments) -> list[str, ...]:
        commands = []

        for name, argument in zip(self.parameter_names, arguments):
            commands.extend([
                argument.set_to_current_cmd(self.local_context),
                f"data modify storage mcs_{self.local_context.uuid} variable.{name} set from storage mcs_{self.local_context.uuid} current",  # NOQA
            ])

        commands.append(f"function {interpreter.datapack_id}:user_functions/{self.name}")

        return commands  # NOQA

    def __repr__(self) -> str:
        return f"MCSFunction({self.name !r})"


mcs_type = MCSNull | MCSNumber | MCSFunction | MCSVariable
