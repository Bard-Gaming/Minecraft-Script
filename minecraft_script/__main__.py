from . import parse_cmd
import os
from sys import argv

arguments = argv[1:]

if arguments:
    for filename in arguments:
        print(f'Attempting to parse {filename}...')
        try:
            parse_cmd(open(filename, 'rt').read())
        except FileNotFoundError:
            print(f"Couldn't find {filename}")
    exit()

current_workdir = os.getcwd()


def file_extension(filename: str):
    return filename.split('.')[-1]

def confirm_parse_operation(filename: str):
    parse_confirm = input(f'Do you wish to parse {filename}? [y/n]: ')
    if parse_confirm.lower() in ['y', 'yes']:
        parse_cmd(open(filename, 'rt').read())

    elif parse_confirm.lower() in ['n', 'no']:
        pass

    else:
        confirm_parse_operation(filename)


valid_files = filter(lambda filename: (file_extension(filename) == 'mcs'), os.listdir(current_workdir))

for file in valid_files:
    confirm_parse_operation(file)