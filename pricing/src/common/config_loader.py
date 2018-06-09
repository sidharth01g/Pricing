import yaml
from pathlib2 import Path
from typing import Union, Dict


class Config(object):

    @staticmethod
    def load_config_yaml(config_filepath: Union[Path, str]) -> Dict:
        with open(str(config_filepath), 'r') as infile:
            return yaml.load(infile)
