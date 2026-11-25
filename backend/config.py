import os
from datetime import timedelta

class Config:
    # Use a project-local sqlite file by default (absolute path) to avoid
    # "unable to open database file" errors on Windows when the CWD differs.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_db_path = os.path.join(project_root, 'instance', 'heatguard.db')
    default_db_path = default_db_path.replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{default_db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    # Use in-memory DB for development to avoid local file permission issues
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
