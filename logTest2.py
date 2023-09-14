import logging
import sys
from logConfig import LogConfig
import datetime

LogConfig = LogConfig()
logLevel = LogConfig.getLogLevel()
logFile = LogConfig.getLogFiles()

logging.basicConfig(
    level=logLevel,
    filename=logFile,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(sys.argv[0])

logger.debug('Exec %s', sys.argv[0])
logger.info('Exec %s', sys.argv[0])
logger.warning('Exec %s', sys.argv[0])
logger.error('Exec %s', sys.argv[0])
logger.critical('Exec %s', sys.argv[0])