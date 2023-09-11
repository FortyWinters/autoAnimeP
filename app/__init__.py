# 该文件主要用于初始化整个个 flask 程序

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    from app.url import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # db.init_app(app)
    return app