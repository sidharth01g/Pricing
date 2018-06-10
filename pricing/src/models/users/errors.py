from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')


class UserError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        logger.exception(self.__repr__())


class UserNotExistsError(UserError):

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __repr__(self) -> str:
        return '<UserNotExistsError: {}>'.format(self.message)


class IncorrectPasswordError(UserError):

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __repr__(self) -> str:
        return '<IncorrectPasswordError: {}>'.format(self.message)
