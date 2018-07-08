import yaml
from pathlib2 import Path
from typing import Union, Dict


class Config(object):

    @staticmethod
    def load_config_yaml(config_filepath: Union[Path, str]) -> Dict:
        with open(str(config_filepath), 'r') as infile:
            config = yaml.load(infile)
            config = Config.freeze_admins(config)
            return config

    @staticmethod
    def freeze_admins(config: Dict) -> Dict:
        if 'admins' in config:
            config['admins'] = frozenset(config['admins'])
        return config
