class ApiError(Exception):
    code = 500
    message = 'error base'

    def __init__(self, code, message):
        self.code = code or self.code
        self.message = message or self.message