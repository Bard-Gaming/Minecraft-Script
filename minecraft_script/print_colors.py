from os import system

system('color')  # enable colors

colors = {
    'header': '\033[95m',

    'okblue': '\033[94m',
    'okcyan': '\033[96m',
    'okgreen': '\033[92m',

    'warning': '\033[93m',
    'error': '\033[91m',

    'bold': '\033[1m',
    'underline': '\033[4m',

    'endc': '\033[0m',
}


def print_warning(*text: str) -> None:
    print(f'{colors["warning"]}{" ".join(text)}{colors["endc"]}')


def print_error(*text: str) -> None:
    print(f'{colors["error"]}{" ".join(text)}{colors["endc"]}')


if __name__ == '__main__':
    print_warning('This is a warning')
    print_error('This is an error')
