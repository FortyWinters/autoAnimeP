import sys
from logManager import LogManager

logger = LogManager(sys.argv[0]).getLogObj()

logger.debug('Exec %s', sys.argv[0])
logger.info('Exec %s', sys.argv[0])
logger.warning('Exec %s', sys.argv[0])
logger.error('Exec %s', sys.argv[0])
logger.critical('Exec %s', sys.argv[0])