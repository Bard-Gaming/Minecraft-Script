from .common import version
from .shell_commands import *
from sys import argv
from os import getcwd

arguments = argv[1:]
if not arguments:
    print(f"Minecraft Script version {version}; currently in {getcwd()}\nUse \"help\" for more information.")
    exit()

function = f'sh_{arguments[0]}'
if function in shell_function_names:
    eval(function)(*arguments[1:])
else:
    print(f'Unknown MCS command: "{arguments[0]}"')