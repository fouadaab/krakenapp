import configparser
from typing import Dict, Any
import enum
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(str, enum.Enum):
    SECRET_KEY = "random key"
    SERVER_NAME = "localhost:5500"


class AppConfig:

    def __init__(self, f_name: str):
        self.config = self.read_config(f_name)
    
    def read_config(self, name: str) -> Dict[str, Dict[Any]]:
        """_summary_

        Args:
            name (str): _description_

        Returns:
            Dict[str, Dict[Any]]: _description_
        """
        print("   Loading configuration from: " + name)
        config = configparser.ConfigParser()
        conf = {}
        config.read(name)

        conf["db_type"] = config['default']['db']
        conf["db_connect"] = dict(config.items(conf["db_type"]))

        conf["cache_type"] = config['default']['cache']
        conf["cache_connect"] = dict(config.items(conf["cache_type"]))

        conf["host"] = config['default']['host']
        conf["port"] = config['default']['port']
        
        return conf
