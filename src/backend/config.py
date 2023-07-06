import os


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get("POSTGRES_URL")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
