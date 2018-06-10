class UserNotExistsError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return '<UserNotExistsError: {}>'.format(self.message)


class IncorrectPasswordError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return '<IncorrectPasswordError: {}>'.format(self.message)
