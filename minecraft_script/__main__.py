from .shell_commands import *
from sys import argv

arguments = argv[1:]
if not arguments:
    exit()

function = f'sh_{arguments[0]}'
if function in shell_function_names:
    eval(function)(*arguments[1:])