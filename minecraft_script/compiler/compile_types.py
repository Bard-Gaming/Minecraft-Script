from ..common import generate_uuid


class MCSObject:
    def __init__(self, context_id):
        self.context_id = context_id
        self.uuid = generate_uuid()

    def save_to_storage_cmd(self, storage_compartment: str, value: any) -> str:
        return f"data modify storage mcs_{self.context_id} {storage_compartment}.{self.uuid} set value {value}"

    def set_to_current_cmd(self, storage_compartment: str, output_context) -> str:
        return f"data modify storage mcs_{output_context.uuid} current set from storage mcs_{self.context_id} {storage_compartment}.{self.uuid}"  # NOQA


class MCSVariable:
    def __init__(self, name: str, context_id):
        self.name = name
        self.context_id = context_id

    def set_to_current_cmd(self, output_context) -> str:
        return f"data modify storage mcs_{output_context.uuid} current set from storage mcs_{self.context_id} variable.{self.name}"  # NOQA


class MCSNull(MCSObject):
    def __init__(self, context_id):
        super().__init__(context_id)

    @staticmethod
    def save_to_storage_cmd():  # NOQA
        return ""

    def set_to_current_cmd(self) -> str:  # NOQA
        return f"data modify storage mcs_{self.context_id} current set value \":null:\""


class MCSNumber(MCSObject):
    def __init__(self, context_id):
        super().__init__(context_id)

    def save_to_storage_cmd(self, value: int) -> str:  # NOQA
        return super().save_to_storage_cmd("number", value)

    def set_to_current_cmd(self, output_context) -> str:  # NOQA
        return super().set_to_current_cmd("number", output_context)

    def __repr__(self) -> str:
        return f"MCSNumber({self.uuid !r})"


class MCSFunction:
    def __init__(self, name: str, body):
        self.name = name
        self.body = body

    def generate_function(self, interpreter, context) -> None:
        from .compile_interpreter import CompileContext, CompileResult
        local_context = CompileContext(self.name, context)

        interpreter.visit(self.body, local_context)  # generate all commands inside body

    def call(self, interpreter) -> str:
        return f"function {interpreter.datapack_id}:user_functions/{self.name}"


mcs_type = MCSNull | MCSNumber | MCSFunction | MCSVariable
