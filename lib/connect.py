#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2018/5/13
# ! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2018/5/13
import pymysql
import config
from dbutils.persistent_db import PersistentDB

POOL = PersistentDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is
    # created, 4 = when a query is executed, 7 = always
    closeable=False,
    # 如果为False时， conn.close() 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close(
    # )则关闭链接，那么再次调用pool.connection时就会报错，因为已经真的关闭了连接（pool.steady_connection()可以获取一个新的链接）
    threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
    host=config.HOSTNAME,
    port=int(config.PORT),
    user=config.USERNAME,
    password=config.PASSWORD,
    database=config.DATABASE,
    charset='utf8',
)


def func(whole_sql):
    # try:
        conn = POOL.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(whole_sql)
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return result
    # except Exception as e:
    #     print('ERROR')
    #     return 'ERROR'


if __name__ == '__main__':
    sql2 = "insert into anime_list (mikan_id,img_url) values (3,'ok')"
    sql = 'select * from anime_list'
    print(func(sql))
