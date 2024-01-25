from . import run_file
from .minecraft_builder import build_file
from .text_additions import text_error
import os

shell_function_names = [
    'sh_help',
    'sh_run', 'sh_build',
]


def sh_build(mcs_file: str, datapack_name: str = None, verbose: str | bool = True, *args) -> None:
    if isinstance(verbose, str):
        verbose = eval(verbose.capitalize())  # "true" or "True" --> True (bool)

    datapack_name = datapack_name if datapack_name else mcs_file.split('/')[-1].split('.')[0].replace('_', ' ').replace('-', ' ').title()
    mcs_file = f'{mcs_file}.mcs' if '.' not in mcs_file else mcs_file  # check for existing extension

    build_file(mcs_file, datapack_name, verbose)


def sh_run_file_iteration(filename: str, *args) -> None:
    parse_confirm = input(f'Do you wish to parse {filename}? [y/n]: ')
    if parse_confirm.lower() in ['y', 'yes']:
        run_file(filename)

    elif parse_confirm.lower() in ['n', 'no']:
        pass
    else:
        sh_run_file_iteration(filename)


def sh_run(*filenames) -> None:
    if not filenames:
        valid_files = filter(check_extension, os.listdir(os.getcwd()))
        for file in valid_files:
            sh_run_file_iteration(file)
    else:
        for file in filenames:
            run_file(file)


def sh_help(*args) -> None:
    help_message = """
#-------------------------------HELP PAGE-------------------------------#
    
- help: display this help page!
    
- run *[file(s): optional]: run file(s) and output result to terminal.
If filename is omitted, a prompt will ask you to choose between mcs
files in work directory (if there are any).
    
- build [mcs file] [datapack name: optional] [verbose: optional]: build the mcs file
into a functional datapack! If the datapack name is left empty,
a matching name will be generated based on the file name.    
Example: "example/test_file.mcs" turns to "Test File".
    
#-----------------------------------------------------------------------#
    """
    print(help_message)


def check_extension(filename: str) -> bool:
    return filename.split('.')[-1] == 'mcs'
