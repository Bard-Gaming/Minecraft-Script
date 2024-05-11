from .compile_interpreter import mcs_compile
from ..common import module_folder, COMMON_CONFIG
from ..text_additions import text_error
from os import mkdir, listdir
from time import time
from shutil import copyfile


class Compiler:
    def __init__(self, ast: list, datapack_name: str):
        self.ast = ast
        self.datapack_name = datapack_name
        self.datapack_id = datapack_name.lower().replace(' ', '_')

    def make_init_file(self):
        text = (
            "################################################################\n"
            "#                                                              #\n"
            "#  default init.mcfunction file generated by Minecraft-Script  #\n"
            "#                                                              #\n"
            "################################################################\n"
            "\n"
            "scoreboard objectives add mcs_math dummy \"Minecraft-Script Math\"\n"
            "scoreboard objectives add mcs_click minecraft.used:minecraft.carrot_on_a_stick \"Minecraft-Script Click\"\n"
            "\n"
            f"function {self.datapack_id}:user_functions/init\n"  # call user-defined init
        )

        with open(f'{self.datapack_name}/data/{self.datapack_id}/functions/init.mcfunction', 'xt') as init_file:
            init_file.write(text)

    def make_main_file(self):
        text = (
            "################################################################\n"
            "#                                                              #\n"
            "#  default main.mcfunction file generated by Minecraft-Script  #\n"
            "#                                                              #\n"
            "################################################################\n"
            "\n"  # check for clickable item activation:
            f"execute as @a at @s if score @s mcs_click matches 1.. run function {self.datapack_id}:clickable_items/check\n"  
            "\n"
            f"function {self.datapack_id}:user_functions/main\n"  # call user-defined main
        )

        with open(f'{self.datapack_name}/data/{self.datapack_id}/functions/main.mcfunction', 'xt') as main_file:
            main_file.write(text)

    def make_kill_file(self):
        text = (
            "################################################################\n"
            "#                                                              #\n"
            "#  default kill.mcfunction file generated by Minecraft-Script  #\n"
            "#                                                              #\n"
            "################################################################\n"
            "\n"
            f"function {self.datapack_id}:user_functions/kill\n"  # call user-defined kill first (everything still there)
            "\n"
            "scoreboard objectives remove mcs_math\n"
            "scoreboard objectives remove mcs_click\n"
            "data remove storage mcs_click id\n"
            "\n"
            f"datapack disable \"file/{self.datapack_name}\"\n"
        )

        with open(f'{self.datapack_name}/data/{self.datapack_id}/functions/kill.mcfunction', 'xt') as kill_file:
            kill_file.write(text)

    def make_click_item_check_file(self):
        check_text = (
            "scoreboard players set @s mcs_click 0\n"
            "\n"
            "data modify storage mcs_click id set from entity @s SelectedItem.components.\"minecraft:custom_data\".mcs_click\n"
            f"function {self.datapack_id}:clickable_items/run with storage mcs_click\n"
        )

        click_path = f'{self.datapack_name}/data/{self.datapack_id}/functions/clickable_items'
        mkdir(click_path)  # create clickable_items directory

        with open(f'{click_path}/check.mcfunction', 'xt') as check_file:
            check_file.write(check_text)

        with open(f'{click_path}/run.mcfunction', 'xt') as run_file:
            run_file.write(f"$function {self.datapack_id}:clickable_items/$(id)\n")

    def import_math_files(self):
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions/math')
        for filename in listdir(f'{module_folder}/compiler/build_templates/math'):
            copyfile(
                f'{module_folder}/compiler/build_templates/math/{filename}',
                f'{self.datapack_name}/data/{self.datapack_id}/functions/math/{filename}'
            )

    def import_builtins_files(self):
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions/builtins')
        for filename in listdir(f'{module_folder}/compiler/build_templates/builtins'):
            copyfile(
                f'{module_folder}/compiler/build_templates/builtins/{filename}',
                f'{self.datapack_name}/data/{self.datapack_id}/functions/builtins/{filename}'
            )

    def import_tags_folder(self):
        module_tags_folder = f'{module_folder}/compiler/build_templates/tags'
        datapack_tags_folder = f'{self.datapack_name}/data/{self.datapack_id}/tags'

        mkdir(datapack_tags_folder)
        for directory_name in listdir(module_tags_folder):
            current_module_folder = f'{module_tags_folder}/{directory_name}'
            current_datapack_folder = f'{datapack_tags_folder}/{directory_name}'

            mkdir(current_datapack_folder)
            for file_name in listdir(current_module_folder):
                copyfile(
                    f'{current_module_folder}/{file_name}',
                    f'{current_datapack_folder}/{file_name}'
                )

    def generate_builtin_functions(self, verbose: bool):
        if verbose:
            print('\rBuilding built-in functions...', end="")

        self.make_init_file()
        if verbose:
            print('\rBuilding built-in functions... 17%', end="")

        self.make_main_file()
        if verbose:
            print('\rBuilding built-in functions... 33%', end="")

        self.make_kill_file()
        if verbose:
            print('\rBuilding built-in functions... 50%', end="")

        self.import_math_files()
        if verbose:
            print('\rBuilding built-in functions... 67%', end="")

        self.import_builtins_files()
        if verbose:
            print('\rBuilding built-in functions... 83%', end="")

        self.make_click_item_check_file()
        if verbose:
            print('\rBuilding builtin-in functions... Done!', end="")

    def build(self, verbose: bool = True):
        start_time = time()  # keep track of start time

        if verbose:
            print(f'Building with name "{self.datapack_name}" (id: "{self.datapack_id}")')

        try:
            mkdir(self.datapack_name)  # main folder
        except FileExistsError:
            print(text_error(f"Can't build file: {self.datapack_name !r} folder exists already!"))
            exit()

        mkdir(f'{self.datapack_name}/data')

        # minecraft folders:
        if verbose:
            print('Creating default folders...', end=" ")

        mkdir(f'{self.datapack_name}/data/minecraft')
        mkdir(f'{self.datapack_name}/data/minecraft/tags')
        mkdir(f'{self.datapack_name}/data/minecraft/tags/functions')

        # datapack folders:
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}')
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions')
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions/code_blocks')
        mkdir(f'{self.datapack_name}/data/{self.datapack_id}/functions/user_functions')

        # default stuff
        if verbose:
            print('Done!')
            print('Building Templates...', end=" ")

        with (
            open(f'{module_folder}/compiler/build_templates/pack.mcmeta', 'rt') as template_file,
            open(f'{self.datapack_name}/pack.mcmeta', 'xt') as output_file
        ):
            template_text = template_file.read()
            # copy pack.mcmeta template to datapack with correct pack_format version:
            output_file.write(template_text.replace("PACK_FORMAT", COMMON_CONFIG["pack_format"]))

        # Copy datapack icon img:
        copyfile(f'{module_folder}/compiler/build_templates/pack.png', f'{self.datapack_name}/pack.png')

        # Minecraft function tags

        with (
            open(f'{module_folder}/compiler/build_templates/function_tags.json', 'rt') as template_file,
            open(f'{self.datapack_name}/data/minecraft/tags/functions/tick.json', 'xt') as tick_file,
            open(f'{self.datapack_name}/data/minecraft/tags/functions/load.json', 'xt') as load_file
        ):
            template_content = template_file.read()
            tick_file.write(template_content.replace('NAME', self.datapack_id).replace('FILETYPE', 'main'))
            load_file.write(template_content.replace('NAME', self.datapack_id).replace('FILETYPE', 'init'))

        if verbose:
            print("Done!")

        self.generate_builtin_functions(verbose)

        if verbose:
            print("Generating datapack tags...", end=" ")
        self.import_tags_folder()
        if verbose:
            print("Done!")

        if verbose:
            print("Compiling program...", end=" ")
        mcs_compile(
            self.ast,
            f'{self.datapack_name}/data/{self.datapack_id}/functions',
            self.datapack_id
        )
        if verbose:
            print("Done!")

        elapsed_time = time() - start_time

        if verbose:
            print(f'Finished compiling {self.datapack_name}! Time Elapsed: {elapsed_time: 0.3f}s')
