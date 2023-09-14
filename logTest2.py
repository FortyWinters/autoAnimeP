import logging
import sys
from logConfig import LogConfig

LogConfig = LogConfig()
logLevel = LogConfig.getLogLevel()
logFile = LogConfig.getLogFiles()

logging.basicConfig(filename=logFile, level=logLevel)

logger = logging.getLogger(sys.argv[0])

logger.debug('Exec %s', sys.argv[0])
logger.info('Exec %s', sys.argv[0])
logger.warning('Exec %s', sys.argv[0])
logger.error('Exec %s', sys.argv[0])
logger.critical('Exec %s', sys.argv[0])