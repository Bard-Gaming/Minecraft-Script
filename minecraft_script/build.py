from random import randint


class BuildFile:
    def __init__(self, filename: str, variables: dict, *, debug_mode: bool = True):
        self.filename = filename if '.' in filename else f'{filename}.mcfunction'  # add extension if missing
        self.scoreboard = VariableScoreboard(variables, debug_mode=debug_mode)
        self.build()

    def build(self):
        variable_section = self.scoreboard.parse_variables()
        with open(self.filename, 'xt') as file:
            file.write(variable_section)


class VariableScoreboard:
    def __init__(self, variables: dict, *, debug_mode: bool = True):
        self.variables = variables
        self.dm_char = '.' if debug_mode else '#'  # makes fake players if debug mode is on
        self.scoreboard_id = f'vars_{randint(10000, 99999)}'
        self.parse_result = f'scoreboard objectives add {self.scoreboard_id} dummy "Variables"\n'  # skip line for style

    def parse_add_line(self, content: str):
        self.parse_result += f'\n{content}'

    def parse_variables(self):
        for variable, value in self.variables.items():
            variable = f'{self.dm_char}{variable}'
            command = f"scoreboard players set {variable} {self.scoreboard_id} {value}"
            self.parse_add_line(command)
        return f'{self.parse_result}\n'

if __name__ == '__main__':
    test = {
        "test": 42,
        "x": 123
    }

    BuildFile('bob', test)