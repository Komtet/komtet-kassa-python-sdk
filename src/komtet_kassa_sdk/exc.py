class Error(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CheckError(Error):

    pass


class FormatError(Error):

    def __init__(self, message, schema):
        self.message = message
        self.schema = schema


class TaskError(Error):

    def __init__(self, message, description):
        self.message = message
        self.description = description


class ServerError(Error):

    def __init__(self, message, code):
        self.message = message
        self.code = code
