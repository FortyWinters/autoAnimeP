import yaml
import logging
from logging.handlers import RotatingFileHandler

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

class LogManager:
    def __init__(self, prog):
        self.prog = prog
        self.logLevel = self.getLogLevel()
        self.logDir = self.getLogDir()
        self.max_file_size = 10 * 1024 * 1024
        self.logMap = []

    def getLogLevel(self):
        try:
            with open('config_file/log_config.yaml', 'r') as config_file:
                logLevel = yaml.safe_load(config_file)['logging']['level']
        except Exception as e:
                logLevel = "INFO"
        
        if logLevel == "DEBUG":
            return 10
        elif logLevel == "WARNING":
            return 30
        elif logLevel == "ERROR":
            return 40
        elif logLevel == "CRITICAL":
            return 50
        else:
            return 20
        
    def getLogDir(self):
        return "log/autoAnimeApp.log"
    
    def getLogObj(self):
        logger = logging.getLogger(self.prog)
        logger.setLevel(logging.DEBUG)
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(self.logDir, maxBytes=self.max_file_size, backupCount=5)
        file_handler.setLevel(self.logLevel)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.propagate = False

        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(self.logLevel)
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)

        return logger