import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_TYPE = "filesystem"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///test.db")


config = {
    "dev": DevelopmentConfig,
    "testing": TestingConfig,
}
