from ..common import generate_uuid


class MCSObject:
    def __init__(self, context_id):
        self.context_id = context_id
        self.uuid = generate_uuid()

    def save_to_storage_cmd(self, storage_compartment: str, value: any) -> str:
        return f"data modify storage mcs_{self.context_id} {storage_compartment}.{self.uuid} set value {value}"

    def set_to_current_cmd(self, storage_compartment: str) -> str:
        return (
            f"data modify storage mcs_{self.context_id} current "
            f"set from storage mcs_{self.context_id} {storage_compartment}.{self.uuid}"
        )


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

    def set_to_current_cmd(self) -> str:  # NOQA
        return super().set_to_current_cmd("number")

    def __repr__(self) -> str:
        return f"MCSNumber({self.uuid !r})"


mcs_type = MCSNull | MCSNumber
