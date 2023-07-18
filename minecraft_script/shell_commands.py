from . import parse_cmd
import os


shell_function_names = ['sh_build', 'sh_run', 'sh_help']

def sh_build(mcs_file: str, parentFolder: str = None, *args) -> None:
    parentFolder = parentFolder if parentFolder else os.getcwd()
    mcs_file = f'{mcs_file}.mcs' if '.' not in mcs_file else mcs_file  # check for existing extension
    try:
        build_file = open(mcs_file, 'rt')
    except FileNotFoundError:
        print(f'File {mcs_file} not found.')
        return
    print(f'{build_file = }\n{parentFolder = }')  # placeholder; put build code here :)


def sh_run_file_iteration(filename: str, *args) -> None:
    parse_confirm = input(f'Do you wish to parse {filename}? [y/n]: ')
    if parse_confirm.lower() in ['y', 'yes']:
        parse_cmd(open(filename, 'rt').read())

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
            try:
                parse_cmd(open(file, 'rt').read())
            except FileNotFoundError:
                print(f"Couldn't find \"{file}\".")


def sh_help(*args):
    help_message = """
#-------------------------------HELP PAGE-------------------------------#
    
    
- help: display this help page!
    
- run *[file(s): optional]: run file(s) and output result to terminal.
If filename is omitted, a prompt will ask you to choose between mcs
files in work directory (if there are any).
    
- build [file] [destination: optional]: build the mcs file
into a functional datapack! 
    
    
#-----------------------------------------------------------------------#
    """
    print(help_message)


def check_extension(filename: str) -> bool:
    return filename.split('.')[-1] == 'mcs'
