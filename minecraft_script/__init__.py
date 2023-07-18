from .interpreter import parser


def parse(text: str):
    for line in text.split('\n'):
        print(parser.parse(line))

def parse_cmd(text: str):
    print('\n#-----------------OUTPUT-----------------#\n')
    parse(text)
    print('\n#----------------------------------------#\n')
