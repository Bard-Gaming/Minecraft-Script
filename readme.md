# Minecraft Script

Minecraft script is primarily a tool to make Minecraft Datapack creation easier.
Minecraft Script is an interpreted programming language which goes through the Python interpreter for output.
However, interpretation is not its main feature, and is rather more of a debugging tool, as its sole
purpose is to allow you to validate your code before building it into a full datapack.

Be sure to check out the [documentation](https://github.com/Bard-Gaming/Minecraft-Script/tree/main/documentation) and the provided [examples](https://github.com/Bard-Gaming/Minecraft-Script/tree/main/examples)!

## Installation
MCS can be installed using [Python's pip module](https://pip.pypa.io/en/stable/installation/).

```commandline
pip install minecraft-script
```
or
```commandline
python -m pip install minecraft-script
```
_Note: The package's name in pip is written with a hyphen ``-``,
whilst the actual Python package is written with an underscore ``_``._


## Using Minecraft Script to make Datapacks
### Debugging your program
To debug your program, you can first run your file like any other programming language.
To do this, use the following command:
```commandline
python -m minecraft_script debug [file]
```
_where [file] is a relative or absolute path to your mcs file_

### Building your datapack
To actually build your minecraft datapack, which you can then simply drag & drop into your
minecraft worlds, use the following command:
```commandline
python -m minecraft_script compile [file]
```
_where [file] is a relative or absolute path to your mcs file_

### More info
For a list of all shell commands, you can use the following command:
```commandline
python -m minecraft_script help
```
If you want to simplify the usage of shell commands, you can check out [the installations page in the documentation](https://github.com/Bard-Gaming/Minecraft-Script/blob/main/documentation/custom-installations.md).

## GitHub
[**Link to GitHub Repository**](https://github.com/Bard-Gaming/Minecraft-Script)

Source code, documentation, and examples, can all be found on the GitHub.

## Compatibility
This python package **does not work on Linux / macOS**.
