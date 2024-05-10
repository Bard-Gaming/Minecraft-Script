from .shell_commands import handle_arguments
from sys import argv

arguments = argv[1:]  # argv[0] is path of the file executing __main__
handle_arguments(arguments)
