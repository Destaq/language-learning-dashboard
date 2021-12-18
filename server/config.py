import os
from datetime import datetime, timedelta, timezone

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    CORS_HEADERS = "Content-Type"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # JWT_COOKIE_CSRF_PROTECT = False


class TestingConfig(Config):
    TESTING = True
