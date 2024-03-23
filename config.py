# config.py

class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///facturation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False