from . import version
from .shell_commands import *
from sys import argv

arguments = argv[1:]
if not arguments:
    print(f"Minecraft Script version {version}\nType \"mcs help\" for more information.")
    exit()

function = f'sh_{arguments[0]}'
if function in shell_function_names:
    eval(function)(*arguments[1:])