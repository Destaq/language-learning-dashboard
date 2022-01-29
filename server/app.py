from flask import Flask
from extensions import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
import os

# BLUEPRINT IMPORTS
from blueprints.chengyu import chengyu_bp
from blueprints.log import log_bp
from blueprints.goals import goal_bp
from blueprints.milestones import milestone_bp
from blueprints.statistics import statistics_bp

# MODEL IMPORTS FOR FLASK-MIGRATE
from models.chengyu import Chengyu
from models.goal_message import GoalMessage
from models.log import Log
from models.note import Note
from models.user import User
from models.action import Action
from models.statistic import StatisticSnapshot

load_dotenv()

migrate = Migrate(compare_type=True)
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get("APP_SETTINGS"))
    db.init_app(app)
    migrate.init_app(app, db)
    # register blueprints
    cors.init_app(
        app,
        resources={r"*": {"origins": ["http://localhost:3000", "http://127.1.0.0.1:3000"]}},
        supports_credentials=True,
    )

    app.register_blueprint(chengyu_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(goal_bp)
    app.register_blueprint(milestone_bp)
    app.register_blueprint(statistics_bp)

    return app
