from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')


class UserNotExistsError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        logger.exception(self.__repr__())

    def __repr__(self) -> str:
        return '<UserNotExistsError: {}>'.format(self.message)


class IncorrectPasswordError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        logger.exception(self.__repr__())

    def __repr__(self) -> str:
        return '<IncorrectPasswordError: {}>'.format(self.message)
