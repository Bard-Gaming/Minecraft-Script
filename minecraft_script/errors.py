class Error:
    def __init__(self, error_name: str, details: str):
        self.error_name = error_name
        self.details = details

    def __str__(self):
        return f'{self.error_name}: {self.details}'


class IllegalCharException(Error):
    def __init__(self, details: str):
        super().__init__('Illegal Character Exception', details)

class NameErrorException(Error):
    def __init__(self, details: str):
        super().__init__('NameError', f"'{details}' is not defined.")
