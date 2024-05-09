from .common import version
from .shell_commands import shell_functions
from sys import argv
from os import getcwd

arguments = argv[1:]  # argv[0] is path of the file executing __main__

if not arguments:
    print(
        f"Minecraft Script version {version}; currently in \"{getcwd()}\" \n"
        "Use the \"help\" command for more information."
    )
    exit()

function_name = arguments.pop(0)
function = shell_functions.get(function_name)

if function is not None:
    function(*arguments)

else:
    print(f'Unknown MCS command: "{function_name}"')
