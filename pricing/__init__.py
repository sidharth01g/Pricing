from pathlib2 import Path
from pricing.src.common.config_loader import Config
from pricing.src.common.logging_base import Logging
from pricing.src.common.database import Database
import os

# Load config
directory = Path(os.path.dirname(os.path.realpath(__file__)))
config_filepath = directory / 'config' / 'config.yaml'
configuration = Config.load_config_yaml(config_filepath=config_filepath)
logger = Logging.create_rotating_log(module_name=__name__, logging_directory=configuration['logging_directory'])
logger.info('Config file: {}'.format(config_filepath))

print(configuration)

db_name = configuration['database_name']
uri = configuration['database_uri']
db = Database(db_name=db_name, uri=uri)
