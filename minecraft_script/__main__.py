from .shell_commands import shell_functions, sh_default
from sys import argv

arguments = argv[1:]  # argv[0] is path of the file executing __main__

if not arguments:
    sh_default()

function_name = arguments.pop(0)
function = shell_functions.get(function_name)

if function is not None:
    function(*arguments)

else:
    print(f'Unknown MCS command: "{function_name}"')
