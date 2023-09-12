# flask
DEBUG = True
HOST  = '0.0.0.0'

# mysql
HOSTNAME                = '127.0.0.1'
PORT                    = '3306'
DATABASE                = 'auto_anime'
USERNAME                = 'root'
PASSWORD                = ''
DB_URI                  = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

