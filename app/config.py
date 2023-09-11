# config 全局配置文件

######################################### flask设置 ##################################
DEBUG = True

#################################### MYSQL数据库设置 ##################################
DB_MYSQL_USER = 'root'                                                  # mysql数据库账号
DB_MYSQL_PASSWORD = 'root'                                              # mysql数据库密码
DB_MYSQL_HOST = 'localhost'                                             # mysql数据库ip
DB_MYSQL_PORT = 3306  # mysql数据库端口
DB_MYSQL_NAME = 'test'  # mysql数据库名称

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_MYSQL_USER + ":" + DB_MYSQL_PASSWORD + "@" + DB_MYSQL_HOST + "/" + DB_MYSQL_NAME
################################## 其他设置 #######################################
LOG_PATH = './log/flask-stdout-log.log'