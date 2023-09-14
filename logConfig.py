import yaml
import logging
import sys

logging.basicConfig(filename="log/autoAnimeApp.log", level=logging.DEBUG)
logger = logging.getLogger(sys.argv[0])

class LogConfig:
    def getLogLevel(self):
        try:
            with open('config_file/log_config.yaml', 'r') as config_file:
                logLevel = yaml.safe_load(config_file)['logging']['level']
                logger.debug("Obtain log level successfully.")
        except Exception as e:
                logLevel = "INFO"
                logger.warning("Failed to obtain log level, set log level to INFO.")
            
        if logLevel == "DEBUG":
            return logging.DEBUG
        elif logLevel == "WARNING":
            return logging.WARNING
        elif logLevel == "ERROR":
            return logging.ERROR
        elif logLevel == "CRITICAL":
            return logging.CRITICAL
        else:
            return logging.INFO
        
    def getLogFiles(self):
        return "log/autoAnimeApp.log"