from random import randint

"""
variable dict structure:
{
    var_name: {"type": var_type, "value": var_value},
    var2_name: {"type": var2_type, "value": var2_value},
    ...
}
"""

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
        for variable_name, value in self.variables.items():
            variable_name = f'{self.dm_char}{variable_name}'
            value = value['value']
            command = f"scoreboard players set {variable_name} {self.scoreboard_id} {value}"
            self.parse_add_line(command)
        return f'{self.parse_result}\n'
