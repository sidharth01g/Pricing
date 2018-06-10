from pathlib2 import Path
from pricing.src.common.config_loader import Config
from pricing.src.common.logging_base import Logging
import os

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')


# Load config
directory = Path(os.path.dirname(os.path.realpath(__file__)))
config_filepath = directory / 'config' / 'config.yaml'
logger.debug('Config file: {}'. format(config_filepath))
configuration = Config.load_config_yaml(config_filepath=config_filepath)
print(configuration)