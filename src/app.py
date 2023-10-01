from flask import Flask
from flask_migrate import Migrate
from exts import db, config
from blueprints.index import bp as index_bp
from blueprints.anime import bp as anime_bp
from blueprints.setting import bp as setting_bp

app = Flask(__name__)

app_config = config.get('FLASK')
app.config.update(app_config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(index_bp)
app.register_blueprint(anime_bp)
app.register_blueprint(setting_bp)

if __name__ == "__main__":
    host = app_config['HOST']
    port = app_config['PORT']
    app.run(host=host, port=port)