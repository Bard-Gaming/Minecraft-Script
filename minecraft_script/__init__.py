from .interpreter import parse_line

version = "0.1.0"


def parse_file(filename: str):
    filename = filename if '.' in filename else f'{filename}.mcs'  # add extension if missing
    try:
        with open(filename, 'rt') as file:
            file_contents = file.readlines()
    except FileNotFoundError:
        print(f'Failed to start process: Couldn\'t find file {filename !r}.')

    for line in file_contents:
        parse_line(line)

    print('\nProcess finished with exit code 0')


def run_file_terminal(filename: str):
    print('\n#--------------------------------OUTPUT---------------------------------#\n')
    parse_file(filename)
    print('\n#-----------------------------------------------------------------------#\n')
