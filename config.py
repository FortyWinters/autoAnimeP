# flask
DEBUG = True
ENV   = 'developmet'

# mysql
HOSTNAME                = '10.112.5.25'
PORT                    = '3306'
DATABASE                = 'auto_anime'
USERNAME                = 'root'
PASSWORD                = 'password'
DB_URI                  = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
