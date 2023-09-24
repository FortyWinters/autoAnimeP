import os
import sys
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
    def __init__(self):
        self.progs = dict()
        self.logConfig = dict()
        self.max_file_size = 10 * 1024 * 1024
        self.logMap = []

        self.getLogConfig()

    def getLogConfig(self):
        config_dir = 'config_file/log_config.yaml'
        try:
            with open(config_dir, 'r') as config_file:
                config = yaml.safe_load(config_file)['logging']
                self.logConfig['logLevel'] = config['level']
                self.logConfig['logDir'] = config['dir']

        except Exception as e:
                print(e)
                print("[Error] log initial filed. cant' read log config from %s", config_dir)
                sys.exit(0)

    def getLogLevel(self):
        logLevel = self.logConfig['logLevel']
        
        if logLevel == "DEBUG":
            return DEBUG
        elif logLevel == "WARNING":
            return WARNING
        elif logLevel == "ERROR":
            return ERROR
        elif logLevel == "CRITICAL":
            return CRITICAL
        else:
            return INFO
        
    def getLogDir(self):
        return self.logConfig["logDir"]
    
    def getLogObj(self, prog):
        if prog in self.progs:
            return self.progs[prog]
        
        logDir = self.logConfig["logDir"]
        logLevel = self.logConfig['logLevel']

        logger = logging.getLogger(prog)
        logger.setLevel(logging.DEBUG)
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(logDir, maxBytes=self.max_file_size, backupCount=5)
        file_handler.setLevel(logLevel)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.propagate = False

        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(self.logLevel)
        # console_handler.setFormatter(formatter)
        # logger.addHandler(console_handler)

        self.progs[prog] = logger

        return logger

sys.path.append(os.getcwd())
m_LogManager = LogManager()