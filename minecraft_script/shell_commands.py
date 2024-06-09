from . import debug_code
from .compiler import build_datapack
from .common import COMMON_CONFIG, version
from .config_utils import update_config, reset_config
import os.path


def handle_arguments(arguments: list):
    if not arguments:
        sh_default()

    function_name = arguments.pop(0)
    function = shell_functions.get(function_name)

    if function is not None:
        function(*arguments)

    else:
        print(f'Unknown MCS command: "{function_name}"')


sh_help_message = """
#-------------------------------HELP PAGE-------------------------------#
    
- help: displays this page!
    
- debug <path>: debug the minecraft script file found at the given path.
    
- compile <path> [<datapack name>] [<output path>]: compile the associated
mcs file into a datapack. The resulting datapack folder will be named after
the mcs file, unless a datapack name is specified. The output path argument
specifies where the datapack should be generated (default to current path).

- config set <setting> <value>: Overwrite specified setting in config
to the new value.

- config get [<setting>]: prints out specified settings' value. If no setting
is specified, all settings with their associated values will be shown.

- config default: Resets all config values to their default values.

#-----------------------------------------------------------------------#
"""


def sh_help(*args) -> None:
    print(sh_help_message)


def sh_default() -> None:
    print(
        f"Minecraft Script {version} (version {version}) \n"
        "Type \"help\" for more information."
    )
    exit()


def sh_debug(*args) -> None:
    if len(args) < 1:
        print("No path specified to debug.")
        exit()

    path: str = args[0]

    with open(path, 'rt', encoding='utf-8') as file:
        code = file.read()
    debug_code(code)  # run code only after closing file


def sh_compile(*args) -> None:
    # Manage args & parameters:
    arg_count = len(args)
    if arg_count < 1:
        print("No path specified to compile.")
        exit()

    path: str = args[0]
    datapack_name: str = (
        "-".join(args[0].split("\\")[-1].split("/")[-1].split(".")[:-1]).replace("_", " ").title()
        if arg_count < 2 else
        args[1]
    )
    output_path: str = (
        COMMON_CONFIG["default_output_path"]
        if arg_count < 3 else
        args[2].replace("\\", '/').rstrip("/")
    )

    verbose = COMMON_CONFIG["verbose"]

    # Check if given paths are valid:
    if not os.path.isfile(path):
        print(f"Error: Could not find file at {path !r}")
        exit(-1)

    if not os.path.isdir(output_path):
        print(f"Error: Output path is not a directory ({output_path !r})")
        exit(-1)

    # Build datapack
    with open(path, 'rt', encoding='utf-8') as mcs_file:
        code = mcs_file.read()

    build_datapack(code, datapack_name, output_path, verbose)


def sh_config(*args) -> None:
    arg_count = len(args)
    args = list(args)
    if arg_count < 1:
        print("Invalid arguments. Use the \"help\" command for more information.")
        exit()

    arg_literal = args.pop(0)

    if arg_literal in ("set", "get", "default"):
        eval(f"sh_config_{arg_literal}(args)")
    else:
        print(f"Invalid argument {arg_literal !r}. Use the \"help\" command for more information.")
        exit()


def sh_config_set(args: list) -> None:
    if len(args) < 2:
        print("Invalid arguments. Use the \"help\" command for more information.")
        exit()
    setting = args[0]
    value = args[1]

    if setting not in COMMON_CONFIG.keys():
        print(f"Unknown setting {setting !r}.")
        exit()

    update_config(setting, value)
    print(f"Updated setting {setting !r} to value {value !r}")


def sh_config_get(args: list) -> None:
    if len(args) < 1:
        print("Minecraft Script configuration:")
        for setting, value in COMMON_CONFIG.items():
            print(f"- {setting}: {value !r}")
        exit()

    setting = args[0]
    nonexistent = object()
    value: any = COMMON_CONFIG.get(setting, nonexistent)

    if value is nonexistent:
        print(f"Unknown setting {setting !r}.")
        exit()

    print(
        f"Setting {setting !r} has the following value: \n"
        f"{value !r}"
    )


def sh_config_default(args: list) -> None:
    confirm = input("Reset whole config to default values? (Y/N): ").lower().strip(" ")
    if confirm != "y":
        return

    reset_config()
    print("Successfully reset config to its default state")


shell_functions = {
    'help': sh_help,
    'debug': sh_debug,
    'compile': sh_compile,
    'config': sh_config,
}
