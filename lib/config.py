import sys
import yaml
from lib.logManager import m_LogManager

class Config:
    def __init__(self, config_file):
        try:
            with open(config_file, 'r') as f:
                self.config_dict = yaml.safe_load(f)            
        except Exception as e:
            print("[CONFIG] config init failed, config_file: {}, error: {}".format(config_file, e))
            sys.exit(0)

    def get(self, key):
        try:
            value = self.config_dict[key]
        except Exception as e:
            print("[CONFIG] config failed, key error, key: {}".format(key))
            sys.exit(0)
        else:
            return value

m_config = Config("config_file/auto_anime.yaml")