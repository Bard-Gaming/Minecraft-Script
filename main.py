from minecraft_script import parse

with open('test.mcs', 'rt') as file:
    parse(file.read())