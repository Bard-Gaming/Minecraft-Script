import ply.lex as lex
import ply.yacc as yacc
from .tokens import *
from .parser import *
from .print_colors import print_error

lexer = lex.lex()
parser = yacc.yacc()


def parse_line(line: str) -> None:
    yacc.parse(line)


def parse_text(multiline_text: str) -> None:
    for line in manage_multiline(multiline_text):
        print(line)
        parse_line(line)


def manage_multiline(multiline_text: str) -> list[str]:
    bracket_depth, previous_bracket_depth = 0, 0
    line_list = []
    for line in filter(lambda x: not x.strip(' ') == '', multiline_text.split('\n')):  # remove unnecessary lines
        bracket_depth += line.count('{') - line.count('}')
        if bracket_depth < 0:
            bracket_mismatch_index = list(reversed(line)).index('}')
            line_snippet = (
                bracket_mismatch_index - 5 if bracket_mismatch_index - 5 >= 0 else 0,
                bracket_mismatch_index + 5 if bracket_mismatch_index + 5 <= len(line) else len(line)
            )
            print_error(f'Syntax: Unmatched bracket at {line[line_snippet[0]:line_snippet[1]] !r}')
            exit()

        elif bracket_depth == 0:
            if previous_bracket_depth > 0:
                line_list[-1] += f'¤{line}'
            else:
                line_list.append(line)

            previous_bracket_depth = bracket_depth

        elif bracket_depth > 0:
            try:
                line_list[-1] += f'¤{line}'
            except IndexError:
                line_list.append(line)
            finally:
                previous_bracket_depth = bracket_depth

    return line_list
