from flask import Flask
import config
from exts import db
from models import AnimeModel
from flask_migrate import Migrate
from blueprints.anime import bp as anime_bp

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(anime_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)