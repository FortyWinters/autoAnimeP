import yaml

class LogConfig:
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
        
    def getLogFiles(self):
        return "log/autoAnimeApp.log"