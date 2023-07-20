from os import system

system('color')  # enable colors

colors = {
    'ok': '\033[92m',
    'warning': '\033[93m',
    'error': '\033[91m',

    'bold': '\033[1m',
    'underline': '\033[4m',

    'endc': '\033[0m',
}


def text_ok(*text: str) -> str:
    return " ".join(f'{colors["ok"]}{word}{colors["endc"]}' for word in " ".join(text).split(' '))


def text_bold(*text: str) -> str:
    return " ".join(f'{colors["bold"]}{word}{colors["endc"]}' for word in " ".join(text).split(' '))


def text_underline(*text: str) -> str:
    return " ".join(f'{colors["underline"]}{word}{colors["endc"]}' for word in " ".join(text).split(' '))


def text_warning(*text: str) -> str:
    return " ".join(f'{colors["warning"]}{word}{colors["endc"]}' for word in " ".join(text).split(' '))


def text_error(*text: str) -> str:
    return " ".join(f'{colors["error"]}{word}{colors["endc"]}' for word in " ".join(text).split(' '))


if __name__ == '__main__':
    print(text_ok(f'This is {text_underline("error")} good'))
    print(text_warning('This is a warning'))
    print(text_error(f'This is an eaihfiaefe'))
