import os


class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  DEBUG = False


class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_DEV_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_DEV_KEY')

class TestingConfig(Config):
  DEBUG = True
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_TEST_URI')
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_TEST_KEY')
  PRESERVE_CONTEXT_ON_EXCEPTION = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

config_by_name = dict(
  dev=DevelopmentConfig,
  test=TestingConfig,
  prod=ProductionConfig
)

key = Config.SECRET_KEY
