from .build_interpreter import build
from ..common import module_folder
from ..text_additions import text_error
from os import mkdir
from time import time
from shutil import copyfile


class Builder:
    def __init__(self, ast: list, datapack_name: str):
        self.ast = ast
        self.datapack_name = datapack_name
        self.datapack_id = datapack_name.lower().replace(' ', '_')

    def make_init_file(self):
        with open(f'{self.datapack_name}/data/{self.datapack_id}/functions/init.mcfunction', 'xt') as init_file:
            init_file.write('# init file. This mcfunction file is run when the game loads.')
            init_file.write('\nscoreboard objectives add mcs_math dummy {"text":"MCS Math"}')

    def make_main_file(self):
        with open(f'{self.datapack_name}/data/{self.datapack_id}/functions/main.mcfunction', 'xt') as main_file:
            main_file.write('# main file. This mcfunction file is run every tick.')

    def make_kill_file(self):
        with open(f'{self.datapack_name}/data/{self.datapack_id}/functions/kill.mcfunction', 'xt') as kill_file:
            kill_file.write('# kill file. This mcfunction file is used to disable the datapack.')
            kill_file.write(f'\ndata remove storage minecraft:mcs_{self.datapack_id} variables')
            kill_file.write(f'\ndata remove storage minecraft:mcs_{self.datapack_id} string')
            kill_file.write(f'\ndata remove storage minecraft:mcs_{self.datapack_id} number')
            kill_file.write(f'\ndata remove storage minecraft:mcs_{self.datapack_id} list')
            kill_file.write(f'\ndata remove storage minecraft:mcs_{self.datapack_id} temporary')
            kill_file.write(f'\nscoreboard objectives remove mcs_math\ndatapack disable "file/{self.datapack_name}"')

    def build(self, verbose: bool = True):
        start_time = time()
        if verbose: print(f'Building with name "{self.datapack_name}" (id: "{self.datapack_id}")')

        try:
            mkdir(self.datapack_name)  # main folder
        except FileExistsError:
            print(text_error(f"Can't build file: {self.datapack_name !r} folder exists already!"))
            exit()

        mkdir(f'{self.datapack_name}/data')

        # minecraft folders:
        if verbose:
            print('Creating Folders...', end=" ")

        mkdir(f'{self.datapack_name}/data/minecraft')
        mkdir(f'{self.datapack_name}/data/minecraft/tags')
        mkdir(f'{self.datapack_name}/data/minecraft/tags/functions')

        # datapack folders:
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}')
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions')
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions/code_blocks')

        # default stuff
        if verbose:
            print('Done!')
            print('Building Templates...', end=" ")

        with (
            open(f'{module_folder}/build_templates/pack.mcmeta', 'rt') as template_file,
            open(f'{self.datapack_name}/pack.mcmeta', 'xt') as output_file
        ):
            output_file.write(template_file.read())
        copyfile(f'{module_folder}/build_templates/pack.png', f'{self.datapack_name}/pack.png')

        # minecraft function tags

        with (
            open(f'{module_folder}/build_templates/function_tags.json', 'rt') as template_file,
            open(f'{self.datapack_name}/data/minecraft/tags/functions/tick.json', 'xt') as tick_file,
            open(f'{self.datapack_name}/data/minecraft/tags/functions/load.json', 'xt') as load_file
        ):
            template_content = template_file.read()
            tick_file.write(template_content.replace('NAME', self.datapack_id).replace('FILETYPE', 'main'))
            load_file.write(template_content.replace('NAME', self.datapack_id).replace('FILETYPE', 'init'))

        if verbose:
            print('Done!')
            print('Building Functions...', end=" ")

        self.make_init_file()
        self.make_main_file()
        self.make_kill_file()

        build(self.ast, f'{self.datapack_name}/data/{self.datapack_id}/functions/', self.datapack_id)

        elapsed_time = time() - start_time

        if verbose:
            print('Done!')
            print(f'Finished Building {self.datapack_name}! Time Elapsed:{elapsed_time: 0.3f}s')
