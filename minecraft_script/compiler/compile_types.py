class MCSObject:
    def __init__(self, name: str, context_id):
        self.name = name
        self.context_id = context_id

    def set_value_cmd(self, value: any) -> str:
        return f"data modify storage mcs_{self.context_id} variables.{self.name} set value {value}"

    def set_to_current_cmd(self, output_context) -> str:
        return f"data modify storage mcs_{output_context.uuid} current set from storage mcs_{self.context_id} variables.{self.name}"  # NOQA


class MCSValue:
    def __init__(self, value: any):
        self.value = value

    def set_to_currend_cmd(self, output_context) -> str:
        return f"data modify storage mcs_{output_context.uuid} current set value {self.value}"


class MCSFunction:
    def __init__(self, name: str, body):
        self.name = name
        self.body = body

    def call(self, interpreter, context):
        from .compile_interpreter import CompileContext, CompileResult
        local_context = CompileContext(self.name, context)

        command = f"function {interpreter.datapack_id}:user_functions/{self.name}"
        interpreter.add_command(context.mcfunction_name, command)

        function_result: CompileResult = interpreter.visit(self.body, local_context)
        return CompileResult(function_result.get_return())  # return value as normal value


mcs_type = MCSObject | MCSValue
