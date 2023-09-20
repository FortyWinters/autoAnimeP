import pymysql
import lib.cfg as cfg
from dbutils.persistent_db import PersistentDB

class DBconnect:
    
    def __init__(self):
        self.POOL = self.initPool()
        self.conn = self.createConnection()
    
    def initPool(self):
        POOL = PersistentDB(
            creator = pymysql,
            maxusage = None, 
            setsession = [], 
            ping = 0,
            closeable = False,
            threadlocal = None,
            host = cfg.HOSTNAME,
            port = int(cfg.PORT),
            user = cfg.USERNAME,
            password = cfg.PASSWORD,
            database = cfg.DATABASE,
            charset = 'utf8',
        )
        return POOL

    def createConnection(self):
        return self.POOL.connection(shareable=False)
    
    def createSession(self):
        return self.conn.cursor()

    def closeSession(self, cursor):
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def execute(self, whole_sql):
        cursor = self.createSession()
        cursor.execute(whole_sql)
        result = self.closeSession(cursor)
        self.commit()
        return result

m_DBconnector = DBconnect()

# if __name__ == '__main__':
#     sql2 = "insert into anime_list (mikan_id,img_url) values (3,'ok')"
#     sql = 'select * from anime_list'
#     print(DBconnect().execute(sql))
