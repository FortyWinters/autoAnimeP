import sys
import os

sys.path.append(os.getcwd())

from lib.connect import m_DBconnector

sql = 'select * from anime_list'
print(m_DBconnector.execute(sql))