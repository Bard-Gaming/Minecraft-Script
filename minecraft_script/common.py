version = "0.1.416"
module_folder = "/".join(__file__.split('\\')[:-1])


class DebugLogger:
    global_indent_level = 0
    indent_space = 2

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        return self.function_call

    @classmethod
    def indent_str(cls):
        return " " * cls.global_indent_level * cls.indent_space

    @classmethod
    def function_call(cls, function):
        def function_call_wrapper(*args, **kwargs):
            print(f'{cls.indent_str()}Calling "{function.__name__}"...')

            cls.global_indent_level += 1
            output = function(*args, **kwargs)
            print(f'{cls.indent_str()}"{function.__name__}" return: {output !r}') if output else None
            cls.global_indent_level -= 1

            print(f'{cls.indent_str()}Successfully called "{function.__name__}".')

        return function_call_wrapper


if __name__ == '__main__':
    @DebugLogger()
    def test():
        bob()


    @DebugLogger()
    def bob():
        return 2 + 2

    test()