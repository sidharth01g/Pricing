from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')


class StoreError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        logger.exception(self.__repr__())


class StoreNotFoundError(StoreError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message)

    def __repr__(self):
        return '<StoreNotFoundError: {}>'.format(self.message)
