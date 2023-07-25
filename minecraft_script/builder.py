from os import mkdir
from .common import module_folder
from .text_additions import text_error


class Builder:
    def __init__(self, ast, datapack_name: str):
        self.datapack_name = datapack_name
        self.datapack_id = datapack_name.lower().replace(' ', '_')

    def build(self):
        try:
            mkdir(self.datapack_name)  # main folder
        except FileExistsError:
            print(text_error(f"Can't build file: {self.datapack_name !r} folder exists already!"))
            exit()
        mkdir(f'{self.datapack_name}/data')
        # minecraft folders:
        mkdir(f'{self.datapack_name}/data/minecraft')
        mkdir(f'{self.datapack_name}/data/minecraft/tags')
        mkdir(f'{self.datapack_name}/data/minecraft/tags/functions')

        # datapack folders:
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}')
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions')

        # minecraft function tags

        with (
            open(f'{module_folder}/build_templates/pack.mcmeta', 'rt') as template_file,
            open(f'{self.datapack_name}/pack.mcmeta', 'xt') as output_file
        ):
            output_file.write(template_file.read())

        with (
            open(f'{module_folder}/build_templates/function_tags.json', 'rt') as template_file,
            open(f'{self.datapack_name}/data/minecraft/tags/functions/tick.json', 'xt') as tick_file,
            open(f'{self.datapack_name}/data/minecraft/tags/functions/load.json', 'xt') as load_file
        ):
            template_content = template_file.read()
            tick_file.write(template_content.replace('NAME', self.datapack_id).replace('FILETYPE', 'main'))
            load_file.write(template_content.replace('NAME', self.datapack_id).replace('FILETYPE', 'init'))

        with (
            open(f'{self.datapack_name}/data/{self.datapack_id}/functions/main.mcfunction', 'xt') as main_file,
            open(f'{self.datapack_name}/data/{self.datapack_id}/functions/init.mcfunction', 'xt') as init_file
        ):
            main_file.write('# main file. This mcfunction file is run every tick.')
            init_file.write('# init file. This mcfunction file is run when the game loads.')
