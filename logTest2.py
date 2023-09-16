import sys
from lib.logManager import m_LogManager

logger = m_LogManager.getLogObj(sys.argv[0])
logger = m_LogManager.getLogObj(sys.argv[0])


logger.debug('Exec %s', sys.argv[0])
logger.info('Exec %s', sys.argv[0])
logger.warning('Exec %s', sys.argv[0])
logger.error('Exec %s', sys.argv[0])
logger.critical('Exec %s', sys.argv[0])

