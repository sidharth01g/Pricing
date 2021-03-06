import logging
from pathlib2 import Path
from typing import Union, SupportsInt, Any
from logging.handlers import TimedRotatingFileHandler
import os


class Logging(object):
    """
    Logging class for web blog application
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_rotating_log(module_name: str, logging_directory: Union[Path, str],
                            level: SupportsInt = logging.DEBUG) -> Any:
        """
        Creates and returns a logger instance for a module

        Args:
            module_name: name of the python module
            logging_directory: directory where logs are to be placed
            level: logging level
        Returns:
            A logger instance
        """

        logger = logging.getLogger(name=module_name)
        logger.setLevel(level=level)
        os.makedirs(logging_directory, exist_ok=True)

        log_file = Path(logging_directory) / '{}.log'.format(module_name)
        handler = TimedRotatingFileHandler(filename=str(log_file), when='d', interval=1, backupCount=5)
        formatter = logging.Formatter('[%(asctime)s - %(name)s - {%(funcName)s} - %(levelname)s]: %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger


if __name__ == '__main__':
    lgr = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp', level=logging.DEBUG)
    lgr.debug('test')
    lgr.info('test')
    lgr.warning('test')
    lgr.error('test')
    lgr.critical('test')
