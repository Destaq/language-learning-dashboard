from flask import Flask
from extensions import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
import os

load_dotenv()

migrate = Migrate(compare_type=True)
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get("APP_SETTINGS"))
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/*": {"origins": r"http://localhost:3000/*"}},
        supports_credentials=False,
    )  # TODO: not localhost but custom domain host

    return app
