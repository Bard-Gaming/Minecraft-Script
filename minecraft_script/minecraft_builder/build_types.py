from random import randint


class BuildNumber:
    def __init__(self, value: int | str):
        self.value = int(value)

    def mc_value(self) -> str:
        return str(self.value)

    @staticmethod
    def command() -> str:
        return ''


class BuildList:
    def __init__(self, list_contents: list | map, context):
        self.list_contents = list_contents
        self.context = context

        self.list_name = f'lists.{randint(100000, 999999)}'

    def get_contents(self) -> list:
        return list(self.list_contents)

    def mc_value(self) -> str:
        current_index = 0
        list_text = '{'
        for value in self.list_contents:
            value = value.mc_value()
            list_text += f'{current_index}: {value}, '
            current_index += 1
        list_text = list_text[:-2] + '}'
        return list_text

    def command(self) -> str:
        return f'data modify storage {self.context.id} {self.list_name} set value {self.mc_value}\n'
