from .common import version
from .shell_commands import shell_functions
from sys import argv
from os import getcwd

arguments = argv[1:]
if not arguments:
    print(f"Minecraft Script version {version}; currently in {getcwd()}\nUse \"help\" for more information.")
    exit()

function = shell_functions.get(arguments[0])
if function is not None:
    function(*arguments[1:])
else:
    print(f'Unknown MCS command: "{arguments[0]}"')