from .interpreter import parser


def parse(text: str):
    parser.parse(text)


def parse_cmd(text: str):
    print('\n#--------------------------------OUTPUT---------------------------------#\n')
    parse(text)
    print('\n#-----------------------------------------------------------------------#\n')
