from minecraft_script import parse

with open('test2.mcs', 'rt') as file:
    print(parse(file.read()))