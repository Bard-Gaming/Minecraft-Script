from .interpreter import parse_text

version = "0.1.3"


def parse_file(filename: str):
    filename = filename if '.' in filename else f'{filename}.mcs'  # add extension if missing
    try:
        with open(filename, 'rt') as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f'Failed to start process: Couldn\'t find file {filename !r}.')

    parse_text(file_contents)